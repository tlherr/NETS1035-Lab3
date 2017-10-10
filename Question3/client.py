"""
 Thomas Herr
 200325519

 Code modified from original author: Ian McWilliam
 Create a client that connects to server and sends/receives messages
"""

import socket
import select
import sys
import logging

from libcrypto import aesdecrypt
from libcrypto import aesencrypt

AES_KEY = '00112233445566778899aabbccddeeff'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('127.0.0.1', 8886)
print(f"Connecting to server at ${server_address[0]}:${server_address[1]}")
sock.connect(server_address)
sock.setblocking(0)


def send(message):
    print("Sending: ", message, "Encrypted: ", aesencrypt(AES_KEY, message))
    sock.send(aesencrypt(AES_KEY, message))

def decrypt(message):
    return aesdecrypt(AES_KEY, message)

output_queue = []

try:
    send('Connecting')
    while True:
        readable, writable, exceptional = select.select([sock, sys.stdin], [], [])
        if readable:
            for s in readable:
                if s is sock:
                    data = sock.recv(4096)
                    # Handle the incoming data
                    print(f"Received Message: ${data}")
                    print("Decrypting...")
                    print(decrypt(data))
                if s is sys.stdin:
                    input = sys.stdin.readline()
                    send(input)

except KeyboardInterrupt:
    # User is wanting to exit, clean up
    sock.close()
    exit(0)

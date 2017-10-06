"""
 Thomas Herr
 200325519

 Code modified from original author: Ian McWilliam
 Create a client that connects to server and sends/receives messages
"""

from aescrypt2017 import aesencrypt
from aescrypt2017 import aesdecrypt

import socket
import time

AES_KEY = '00112233445566778899aabbccddeeff'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('127.0.0.1', 8886)
sock.connect(server_address)


def send(message):
    print("Sending: ", message, "Encrypted: ", aesencrypt(AES_KEY, message))
    sock.sendall(aesencrypt(AES_KEY, message))

def decrypt(message):
    return aesdecrypt(AES_KEY, message)

# Send the initial hello
send('Connecting')

# Receive data (Server Response) from the socket
message = sock.recv(1000)
print("Received: ", decrypt(message))

send('Ready')
response = sock.recv(128)
print("Received: ", decrypt(response))

try:
    while True:
        myinput = input("Enter Message: ")
        send(myinput)
        response = sock.recv(32)
except KeyboardInterrupt:
    # User is wanting to exit, clean up
    sock.close()
    exit(0)

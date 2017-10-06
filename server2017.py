from aescrypt2017 import aesencrypt
from aescrypt2017 import aesdecrypt

import socket
import time

AES_KEY = '00112233445566778899aabbccddeeff'

secure_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_socket.bind(('0.0.0.0', 8886))
secure_socket.listen(1)

def send(message):
    print("Sending: ", message, "Encrypted: ", aesencrypt(AES_KEY, message))
    clientsocket.sendall(aesencrypt(AES_KEY, message))

def decrypt(message):
    return aesdecrypt(AES_KEY, message)

print("Waiting for a client...")
(clientsocket, address) = secure_socket.accept()
# Client is connecting
received = clientsocket.recv(400)
print("Client Sent: ", decrypt(received))

send('Connected')

time.sleep(2)

while True:
    data = clientsocket.recv(400)
    print(decrypt(data))
    send('Received')
    time.sleep(2)

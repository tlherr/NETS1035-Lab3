from Crypto.Cipher import AES
from Crypto.Hash import MD5
from base64 import b64decode
from base64 import b64encode
import os

BLOCK_SIZE = 16

# How many bytes do we need to reach the BLOCK_SIZE boundry
# Add that number of bytes to the string and return it
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

# Remove from the back as many bytes as indicated in the padding
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def aesencrypt(key, plaintext):
    # Hash the key
    key = MD5.new(key.encode('utf8')).hexdigest()
    # Pad the input to reach block size
    plaintext = pad(plaintext)
    # Generate a random IV
    iv = os.urandom(16)
    # Generate ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encryptedText = b64encode(iv + cipher.encrypt(plaintext))
    return encryptedText


def aesdecrypt(key, enc):
    # Hash the key
    key = MD5.new(key.encode('utf8')).hexdigest()
    # Decode from base64
    enc = b64decode(enc)
    # IV is in the first 16 bytes
    iv = enc[:16]
    # Generate cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Decrypt everything after the first 16 bytes (which is the IV)
    return unpad(cipher.decrypt(enc[16:]).decode('utf-8'))

# encrypted_val = aesencrypt('1234','summer')
# print encrypted_val
# print aesdecrypt('1234', encrypted_val)

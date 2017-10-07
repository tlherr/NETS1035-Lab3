from Crypto.Cipher import AES
from Crypto.Hash import MD5
from base64 import b64decode
from base64 import b64encode
import os
import hmac
import hashlib

# AES CBC expects messages to be sent in 16 byte lengths
BLOCK_SIZE = 16
# Define the size of the HMAC signature in bytes
HMAC_SIZE = 20
# Key used to verify authenticity of messages
HMAC_KEY = "fiuwh38yr89hafwrgiwfgsaulh"

# How many bytes do we need to reach the BLOCK_SIZE boundry
# Add that number of bytes to the string and return it
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

# Remove from the back as many bytes as indicated in the padding
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def aesencrypt(key, plaintext):
    print("===== Beginning Encryption =====")

    if (len(plaintext) == 0):
        raise Warning("Attempting to encrypt an empty string")

    # Hash the key
    key = MD5.new(key.encode('utf8')).hexdigest()
    print("Hashing Key: ", key)
    # Pad the input to reach block size
    plaintext = pad(plaintext)
    print("Padding Plaintext: ", plaintext)
    # Generate a random IV
    iv = os.urandom(16)
    print("Generating random IV: ", iv)
    # Generate ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)
    print("Generating Cipher Text: ", cipher)
    # Encrypt the message
    encryptedText = iv + cipher.encrypt(plaintext)
    print("Encrypting Message: ", encryptedText)
    # Generate a HMAC signature of the encrypted message
    signature = hmac.new(HMAC_KEY.encode('utf-8'), encryptedText, hashlib.sha1).digest()
    print("Generating Signature for encrypted message: ", signature, len(signature))
    assert len(signature) == HMAC_SIZE

    return b64encode(signature + encryptedText)


def aesdecrypt(key, enc):
    print("===== Beginning Decryption =====")

    if(len(enc)==0):
        raise Warning("Attempting to decrypt an empty string")

    # Hash the key
    key = MD5.new(key.encode('utf8')).hexdigest()
    print("Hashing Key: ", key)
    # Decode from base64
    enc = b64decode(enc)
    print("Decoding Base64: ", enc)
    # Get HMAC signature from the start of the message
    signature = enc[:HMAC_SIZE]
    print("Signature", signature)
    # IV is in the next 16 bytes
    iv = enc[HMAC_SIZE:HMAC_SIZE+16]
    print("IV: ", iv)
    # Generate cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)
    print("Cipher: ", cipher)
    paddedMessage = enc[HMAC_SIZE+16:]
    print("Padded Encrypted Message: ", paddedMessage)


    # Decrypt everything after the first 16 bytes (which is the IV)
    message = unpad(cipher.decrypt(enc[HMAC_SIZE+16:]).decode('utf-8'))
    print("Message: ", message)
    # Generate a signature for the message and check it with what we got
    good_signature= hmac.new(HMAC_KEY.encode('utf-8'), enc[HMAC_SIZE:],  hashlib.sha1).digest()
    print("Our Signature:", good_signature)

    if(signature!=good_signature):
        raise Exception("Bad signature on sent data, implying different keys on sender and receiver")
    else:
        print("HMAC Signature is Valid")

    return message

import os
from Crypto.Cipher import AES
import sys

BLOCK_SIZE = 16

flag = b'UCTF{'+open("flag.txt","rb").read()[:58]+b'}'

def pad(message):
    if len(message) % BLOCK_SIZE != 0:
        message = message + b'0'*(BLOCK_SIZE - len(message)%BLOCK_SIZE)
    return message

def encrypt(key, plain):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(plain)

key = os.urandom(16)

def main():
    while True:
        ot = bytes(input("your open text: "),"UTF-8")
        print(ot, file=sys.stderr)
        print(encrypt(key, pad(ot+flag)).hex())

if __name__ == "__main__":
    main()
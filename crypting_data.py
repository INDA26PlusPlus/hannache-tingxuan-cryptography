import hashlib
import hmac #for signering?
import cryptography
import socket
from random import randint
# vill ha ID: index
# krypterad meddelande
# Signatur -> secret code.

one_time_number = randint(0, 63) #nonce. Used for signature?


def start_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #AF_INET -> IPv4. SOCK_STREAM -> TCP
    client_socket.connect(("127.0.0.1", 1010))

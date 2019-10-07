from Cryptodome.PublicKey import RSA
import os
import socket
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_cert_chain('ground_controller_private_key.pem')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(('127.0.0.1', 8443))
    sock.listen(5)

    with context.wrap_socket(sock, server_side=True) as ssock:
        conn, addr = ssock.accept()
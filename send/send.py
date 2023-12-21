import os
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

SERVER_IP = "127.0.0.1"
SERVER_PORT = 4004

def start_sending(file_path: str):
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)

    while True:
        print(f"Waiting on a connection on {SERVER_IP}:{SERVER_PORT}")
        client_socket, client_address = server_socket.accept()
        
        file_size = os.path.getsize(file_path)
        client_socket.send(f"{file_size}".encode('utf-8'))

        with open(file_path, "rb") as file_to_send:
            chunk = file_to_send.read(1024)
            while chunk:
                client_socket.send(chunk)
                chunk = file_to_send.read(1024)
        
        client_socket.close()

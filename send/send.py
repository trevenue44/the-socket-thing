import os
import socket


SERVER_IP = "127.0.0.1"
SERVER_PORT = 4004

def configure_server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
    return server_socket, f"{SERVER_IP}:{SERVER_PORT}"

def start_sending(server_socket, file_path):
    client_socket, _ = server_socket.accept()
    
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    client_socket.send(f"{file_name}<X>{file_size}".encode('utf-8'))

    with open(file_path, "rb") as file_to_send:
        chunk = file_to_send.read(1024)
        while chunk:
            client_socket.send(chunk)
            chunk = file_to_send.read(1024)
    
    client_socket.close()

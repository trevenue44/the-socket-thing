"""A module with functions connect to sending socket for file receive"""
import socket
import os


def start_receiving(server_ip: str, server_port: int, dir_to_save_in: str):
    """Function connect to sender socket for file receive"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_ip, server_port))
    except ConnectionRefusedError:
        print(f"Connection refused on ({server_ip}, {server_port})")
        client_socket.close()
        return

    file_name, _ = client_socket.recv(1024).decode("utf-8").split("<X>")

    with open(os.path.join(dir_to_save_in, file_name), "wb") as file:
        chunk = client_socket.recv(1024)
        while chunk:
            file.write(chunk)
            chunk = client_socket.recv(1024)

    client_socket.close()

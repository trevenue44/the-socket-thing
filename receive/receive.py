import socket

def start_receiving():
    # server_ip = input("Enter the server IP Address: ").strip()
    # server_port = input("Enter the server port: ").strip()

    server_ip = "127.0.0.1"
    server_port = "4004"

    if server_port.isnumeric():
        server_port = int(server_port)
    else:
        print('Invalid server port')
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((server_ip, server_port))

    file_size = int(client_socket.recv(1024).decode('utf-8'))
    
    with open("received_file.txt", "wb") as file:
        chunk = client_socket.recv(1 024)
        while chunk:
            file.write(chunk)
            chunk = client_socket.recv(1024)
        
    


import socket
import threading

# Server configuration
HOST = '127.0.0.1'   # localhost
PORT = 55555

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

clients = []

def broadcast(message, sender_socket):
    """Send message to all clients except sender"""
    for client in clients:
        if client != sender_socket:
            client.send(message)

def handle_client(client_socket):
    """Handle messages from a single client"""
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, client_socket)
        except:
            break

    clients.remove(client_socket)
    client_socket.close()

print("Chat server started...")

while True:
    client_socket, address = server_socket.accept()
    print(f"New connection from {address}")

    clients.append(client_socket)

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket,)
    )
    thread.start()

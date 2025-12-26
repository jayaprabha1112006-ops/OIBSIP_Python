import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 55555

# Create socket and connect
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

username = input("Enter your name: ")

def receive_messages():
    """Receive messages from server"""
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print(message)
        except:
            print("Connection closed")
            break

def send_messages():
    """Send messages to server"""
    while True:
        message = input()
        full_message = f"{username}: {message}"
        client_socket.send(full_message.encode("utf-8"))

# Start threads
threading.Thread(target=receive_messages).start()
threading.Thread(target=send_messages).start()

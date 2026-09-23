import socket
import threading

HOST = "127.0.0.1"
PORT = 12345

client_socket = socket.socket(
    socket.AF_INET, 
    socket.SOCK_STREAM
)

client_socket.connect((HOST, PORT))

username = input("Enter your username: ")

hello_message = "HELLO|" + username

client_socket.send(
    hello_message.encode()
)

response = client_socket.recv(1024)

print("Server:", response.decode())

# Running on a separate thread
def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode()
            
            if message.startswith("MSG|"):
                print(f"{message.split('|', 1)[1]}")
            else:
                print(f"Server: {message}")
        except:
            break

threading.Thread(target=receive_messages, daemon=True).start()

# Main loop for multi threads.
print("Enter message or type EXIT to leave: ")
while True:

    message = input("")

    if message.upper() == "EXIT":

        client_socket.send(
            "EXIT|".encode()
        )
        
        break

    if message.strip() == "":
        continue

    protocol_message = "MSG|" + message

    client_socket.send(
        protocol_message.encode()
    )

client_socket.close()

print("\n\nDisconnected")
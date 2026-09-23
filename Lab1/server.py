import socket

# Server configuration
HOST = "127.0.0.1"
PORT = 12345

# Create TCP socket
server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

# Bind and listen for connections
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("Server is waiting for a connection...")

# Accept client connection
client_socket, client_address = server_socket.accept()
print("Connected by:", client_address)

username = None
connected = True


# Main loop for receiving and processing messages
while connected:

    try:
        # Receive data from client
        data = client_socket.recv(1024)

        if not data:
            print("Client disconnected unexpectedly")
            break

        # Decode binary data to string
        message = data.decode()
        print("Received:", message)

        # Validate message format
        if "|" not in message:
            client_socket.send(
                "ERROR|Invalid command format".encode()
            )
            continue

        # Split into command and content
        command, content = message.split("|", 1)

        # Handle HELLO command (login)
        if command == "HELLO":
            if content == "":
                client_socket.send(
                    "ERROR|Username required".encode()
                )
            else:
                username = content
                print("Username:", username)

                client_socket.send(
                    "OK|Hello ".encode() + username.encode()
                )


        # Handle MSG command (chat)
        elif command == "MSG":

            if username is None:
                client_socket.send(
                    "ERROR|HELLO required first".encode()
                )

            elif content == "":
                client_socket.send(
                    "ERROR|Message cannot be empty".encode()
                )

            elif len(content) > 200:
                client_socket.send(
                    "ERROR|Message too long".encode()
                )

            else:
                print(username + " says:", content)

                client_socket.send(
                    ("OK|Message received from " + username).encode()
                )
                
        # Handle EXIT command (disconnect)
        elif command == "EXIT":

            client_socket.send(
                "OK|Goodbye".encode()
            )

            connected = False
            
        # Handle unknown commands
        else:
            client_socket.send(
                "ERROR|Unknown command".encode()
            )

    except (ConnectionResetError, KeyboardInterrupt):
        print("Connection reset by client")
        break


# Close sockets
client_socket.close()
server_socket.close()
print("Server closed")

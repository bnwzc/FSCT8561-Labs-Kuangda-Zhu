import socket

# Server configuration (must match the server)
HOST = "127.0.0.1"
PORT = 12345

# Create TCP socket
client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

# Connect to the server
client_socket.connect((HOST, PORT))

# Prompt user for username(have to be something not none)
username = ""
while not username:
    username = input("Enter your username: ")
    if not username:
        print("Username can not be null.")

# Create a command to test Robustness(Skip the loggin)
if username.upper() == "SKIP":
    print("Skipping HELLO command...")
else:
    # Send HELLO command with the valid username
    hello_message = "HELLO|" + username

    client_socket.send(
        hello_message.encode()
    )
    # Receive and print server's response
    response = client_socket.recv(1024)
    print("Server:", response.decode())

# Main loop for sending messages
while True:
    message = input(
        "Enter message or type EXIT to leave: "
    )
    
    # Create a command to test Robustness
    if message.upper() == "TEST":
        client_socket.send(
                           "BADCOMMAND|test".encode()
        )
        
    
    
    # Handle EXIT command to disconnect
    elif message.upper() == "EXIT":

        client_socket.send(
            "EXIT|".encode()
        )

        response = client_socket.recv(1024)

        print("Server:", response.decode())

        break

    # Format message with MSG command and send
    else:
        protocol_message = "MSG|" + message

        client_socket.send(
            protocol_message.encode()
        )

    # Receive and print server's response
    response = client_socket.recv(1024)
    print("Server:", response.decode())

# Close socket connection
client_socket.close()
print("Disconnected")

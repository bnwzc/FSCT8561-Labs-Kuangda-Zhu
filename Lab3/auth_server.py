import hashlib
import pyotp
import socket

# Hash function
def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()

# Verify hash function
def verify_password(password, stored_hash):
    return hash_password(password) == stored_hash

def verify_otp(secret, otp):
    totp = pyotp.TOTP(secret)

    return totp.verify(otp)

users = {
    "Alice": {
        "password_hash":"34bf5eb46102238cd554f7a41353c5278073442ea98f7c30db33aaa4621f99e2", #Cyber123!
        "totp_secret": "INASTOQRQTKUK7T54WAZDVYP7ZKGSMRN"
    },
    "Bob": {
        "password_hash":"54db93dd40ba79498f507d2b293cc6db462de02b0c3262328daeee50fd5e3418", #Cyber321!
        "totp_secret": "QK63QJTSNON32Q7QQEBTYMHYOMANLDG3"
    }
}



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

password_verified = False
OTP_verified = False


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
        
        # Handle EXIT command (disconnect)
        if command == "EXIT":

            client_socket.send(
                "OK|Goodbye".encode()
            )

            connected = False
        
        
        
        elif (command not in ("AUTH", "OTP") and not (password_verified and OTP_verified)):
            client_socket.send(
                "ERROR|Please login first".encode()
            )
            continue
        
        elif command == "AUTH":
            if "|" not in content:
                client_socket.send(
                    "ERROR|Invalid username and password format".encode()
                )
                password_verified = False
                OTP_verified = False
                continue
            else:
                username, password = content.split("|", 1)
            
            if username not in users:
                client_socket.send(
                    "ERROR|User not exisits".encode()
                )
                password_verified = False
                OTP_verified = False
                continue
            else:
                if verify_password(password, users[username]["password_hash"]):
                    client_socket.send(
                        "OTP_REQUIRED".encode()
                    )
                    password_verified = True
                    OTP_verified = False
                else:
                    client_socket.send(
                        "ERROR|Incorrect password".encode()
                    )
                    password_verified = False
                    OTP_verified = False
                    continue
        
    
        elif command == "OTP":
            if not password_verified:
                client_socket.send(
                    "ERROR|Please input the correct username and password first before OTP".encode()
                )
                continue
            
            else:
                if verify_otp(users[username]["totp_secret"], content):
                    client_socket.send(
                        "ACCESS_GRANTED".encode()
                    )
                    OTP_verified = True
                else:
                    client_socket.send(
                        "ACCESS_DENIED".encode()
                    )
                    OTP_verified = False
                    continue
        
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

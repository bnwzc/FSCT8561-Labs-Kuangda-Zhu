import socket
from getpass import getpass

test_mode = 0


def robust_test_6():
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
    password = ""
    password_verified = False
    otp_verified = False
    count = 1
    username = input("Enter your username: ")
    
    if not username:
        print("Username can not be null.")

    password = getpass("Enter your Password: ")
    if not password:
        print("Password can not be null.")

    # Send HELLO command with the valid username
    hello_message = "AUTH|" + username + "|" + password

    client_socket.send(
        hello_message.encode()
    )
    # Receive and print server's response
    response = client_socket.recv(1024)
    print("Server:", response.decode())
    
    if response.decode() == "OTP_REQUIRED":
        password_verified = True

    count = count + 1
    if count > 3:
        print("Too many times! Disconnected.")
    
    
    while not otp_verified:
        otp = input("Enter your code: ")
        otp_message = "OTP|" + otp
        
        client_socket.send(
            otp_message.encode()
        )
        
        response = client_socket.recv(1024)
        print("Server:", response.decode())
        
        if response.decode() == "ACCESS_GRANTED":
            otp_verified = True
        count = count + 1
        if count > 3:
            print("Too many times! Disconnected.")


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

def robust_test_7():
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
    password = ""
    password_verified = False
    otp_verified = False
    count = 1
    while not password_verified:

        username = input("Enter your username: ")
        
        if not username:
            print("Username can not be null.")

        password = getpass("Enter your Password: ")
        if not password:
            print("Password can not be null.")

        # Send HELLO command with the valid username
        hello_message = "AUTH|" + username

        client_socket.send(
            hello_message.encode()
        )
        # Receive and print server's response
        response = client_socket.recv(1024)
        print("Server:", response.decode())
        
        if response.decode() == "OTP_REQUIRED":
            password_verified = True

        count = count + 1
        if count > 3:
            print("Too many times! Disconnected.")
        
    count = 0
    while not otp_verified:
        otp = input("Enter your code (EXIT to dc): ")
        otp_message = "OTP|" + otp
        
        client_socket.send(
            otp_message.encode()
        )
        
        response = client_socket.recv(1024)
        print("Server:", response.decode())
        
        if response.decode() == "ACCESS_GRANTED":
            otp_verified = True
        count = count + 1
        if count > 3:
            print("Too many times! Disconnected.")


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


def main():
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
    password = ""
    password_verified = False
    otp_verified = False
    count = 1
    print("Maximum failed attempts: 3\n\n")
    
    while not (password_verified and otp_verified):
        if count > 3:
            print("\nToo many failed attempts.")
            print("Authentication blocked.")
            break
    
        while not password_verified and count <= 3:

            username = input("Enter your username: ")
            
            if not username:
                print("Username can not be null.")

            password = getpass("Enter your Password: ")
            if not password:
                print("Password can not be null.")

            # Send HELLO command with the valid username
            hello_message = "AUTH|" + username + "|" + password

            client_socket.send(
                hello_message.encode()
            )
            # Receive and print server's response
            response = client_socket.recv(1024)
            
            if response.decode() == "OTP_REQUIRED":
                print(f"Attempt {count} → {response.decode()}")
                password_verified = True
            else:
                print(f"Attempt {count} → {response.decode()}")
                count = count + 1

        
        while not otp_verified and count <= 3:
            otp = input("Enter your code: ")
            otp_message = "OTP|" + otp
            
            client_socket.send(
                otp_message.encode()
            )
            
            response = client_socket.recv(1024)
            
            if response.decode() == "ACCESS_GRANTED":
                print(f"Attempt {count} → {response.decode()}")
                otp_verified = True
            else:
                print(f"Attempt {count} → {response.decode()}")
                count = count + 1


    # Main loop for sending messages
    while True and otp_verified and password_verified:
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

if __name__ == "__main__":
    if test_mode == 7:
        robust_test_7()
    if test_mode == 6:
        robust_test_6()
    else:
        main()
import socket
import threading

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
server_socket.listen(5)
print("Server is waiting for a connections...")

clients = []
clients_lock = threading.Lock()

# Basically same as the previsou part, but just handle single client.
def handle_client(client_socket, client_address):
    print("Connected by:", client_address)

    username = None
    connected = True
    
    with clients_lock:
        clients.append((client_socket, username))

    while connected:

        try:
            data = client_socket.recv(1024)

            if not data:
                print("Client disconnected unexpectedly")
                break

            message = data.decode()

            print("Received:", message)

            if "|" not in message:
                client_socket.send(
                    "ERROR|Invalid command format".encode()
                )
                continue

            command, content = message.split("|", 1)

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
                    with clients_lock:
                        for i, (sock, _) in enumerate(clients):
                            if sock == client_socket:
                                clients[i] = (client_socket, username)
                                break

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


                    # client_socket.send(
                    #     ("OK|Message received from " + username).encode()
                    # )
                    
                    with clients_lock:
                        for client_sock, _ in clients:
                            if client_sock != client_socket:
                                client_sock.send(f"MSG|{username}: {content}".encode())

            elif command == "EXIT":

                client_socket.send(
                    "OK|Goodbye".encode()
                )

                connected = False

            else:
                client_socket.send(
                    "ERROR|Unknown command".encode()
                )

        except ConnectionResetError:
            print("Connection reset by client")
            break
    with clients_lock:
        clients[:] = [(sock, name) for sock, name in clients if sock != client_socket]

    client_socket.close()
    print(f"Connection closed for {client_address}")
    
server_socket.settimeout(1.0)

# Main loop for multiple clients at the same time.
try:
  while True:
    try:
      client_socket, client_address = server_socket.accept()

      t = threading.Thread(
          target=handle_client, args=(client_socket, client_address)
      )
      t.start()

    except socket.timeout:
      continue

except KeyboardInterrupt:
  print("\nServer shutting down...")
finally:
  server_socket.close()
  print("Server closed")

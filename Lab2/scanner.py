import socket 
            
def port_range():
    while True:
        start_port = input("Enter start port: ")
        try:
            if int(start_port) > 0 and int(start_port) < 66535:
                start_port = int(start_port)
                break
            else:
                print("Start port must be 0-65535.")
        except ValueError:
            print("Invalid input")
    
    while True:
        end_port = input("Enter end port: ")
        try:
            if int(end_port) < start_port:
                print("The end port should be bigger or equal than the start port.")
            elif int(end_port) > 0 and int(end_port) < 66535:
                end_port = int(end_port)
                break
            else:
                print("End port must be 0-65535. ")
        except ValueError:
            print("Invalid input")
    
    return (start_port, end_port)

def scan_port(target, port):

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.settimeout(0.5)

    result = sock.connect_ex(
        (target, port)
    )

    sock.close()

    if result == 0:
        return True
    else:
        return False
    
def main():
    while True:
        target_host = input("Enter target host: ")
        try:
            target_ip = socket.gethostbyname(target_host)
            break
        except socket.gaierror:
            print("Unable to resolve target, please input a valid host.")
    start_port, end_port = port_range()
    print("\nTarget: ", target_ip)
    print(f"Scanning TCP ports {start_port}-{end_port}...")
    
    print("")
    print(f"{'PORT':<10}{'STATE':<12}{'SERVICE'}")
    
    open_ports = dict()
    for port in range(start_port, end_port + 1):
        if scan_port(target_ip, port):
            try:
                open_ports[port] = socket.getservbyport(port, "tcp")
            except OSError:
                open_ports[port] = "unknown"
            print(f"{port:<10}{'open':<12}{open_ports[port]}")
    
    print("\n" + "Scan complete.")
    if open_ports:
        print(f"{len(open_ports)} open port(s) found.")
    else:
        print("No open port found.")

if __name__ == "__main__":
    main()
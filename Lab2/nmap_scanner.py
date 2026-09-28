import socket
import nmap

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








def main():
    while True:
        target_host = input("Enter target host: ")
        try:
            target_ip = socket.gethostbyname(target_host)
            break
        except socket.gaierror:
            print("Unable to resolve target, please input a valid host.")
    start_port, end_port = port_range()
    scanner = nmap.PortScanner()
    scanner.scan(target_ip, f"{start_port}-{end_port}", arguments="-Pn")
    print("\nTarget: ", target_ip)
    print("")
    
    print(f"{'PORT':<10}{'STATE':<12}{'SERVICE'}")
    for port in range(start_port, end_port + 1):
        item = scanner[target_ip]["tcp"][port]
        print(f"{port:<10}{item["state"]:<12}{item["name"]}")
    
    print("\n" + "Scan complete.")

if __name__ == "__main__":
    main()
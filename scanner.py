import socket

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_NET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0 # port is open
    except:
        return False
    
def port_scan(ip, ports=range(1, 1025)):
    print(f"\nScanning ports on {ip}...\n")
    open_ports = []

    for port in ports:
        if scan_port(ip, port):
            print(f" [+] Port {port} is OPEN")
            open_ports.append(port)

    return open_ports

port_scan("192.168.1.1")
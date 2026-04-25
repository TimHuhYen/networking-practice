import subprocess, platform, socket
from concurrent.futures import ThreadPoolExecutor

def ping(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    cmd = ["ping", param, "1", "-W", "1", host]
    return subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

def ping_sweep(base_ip):
    live = []
    def check(i):
        ip = f"{base_ip}.{i}"
        if ping(ip):
            print(f"  [+] {ip} is alive")
            live.append(ip)
    with ThreadPoolExecutor(max_workers=50) as ex:
        ex.map(check, range(1, 255))
    return live

def scan_port(ip, port):
    try:
        s = socket.socket()
        s.settimeout(0.5)
        result = s.connect_ex((ip, port))
        s.close()
        return result == 0
    except:
        return False

def port_scan(ip, start=1, end=1024):
    open_ports = []
    for port in range(start, end + 1):
        if scan_port(ip, port):
            print(f"    [+] Port {port} OPEN")
            open_ports.append(port)
    return open_ports

base = input("Enter base IP (e.g. 192.168.1): ")
print(f"\n Sweeping network...")
live_hosts = ping_sweep(base)

if live_hosts:
    target = input("\nEnter IP to port scan: ")
    print(f"\n Scanning ports on {target}...")
    open_ports = port_scan(target)
    print(f"\nDone. Found {len(open_ports)} open ports.")

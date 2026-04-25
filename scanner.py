import subprocess, platform, socket
import sys
from concurrent.futures import ThreadPoolExecutor



def ping(host):
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ping", "-n", "1", "-w", "500", host]  # -w in milliseconds on Windows
    else:
        cmd = ["ping", "-c", "1", "-W", "1", host]
    return subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

def ping_sweep(base_ip):
    live = []
    lock = __import__('threading').Lock() # fixing append race condition

    def check(i):
        ip = f"{base_ip}.{i}"
        if ping(ip):
            with lock:
                print(f"  [+] {ip} is alive")
                live.append(ip)
    
    with ThreadPoolExecutor(max_workers=50) as ex:
        ex.map(check, range(1, 255))
    return live



def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((ip, port))
        s.close()
        return result == 0
    
    except:
        return False



def port_scan(ip, start=1, end=1024):
    open_ports = []
    lock = __import__('threading').Lock()

    def check(port):
        if scan_port(ip, port):
            with lock:
                print(f"   [+] Port {port} OPEN")
                open_ports.append(port)

    print(f"\nScanning ports on {ip}...\n")

    with ThreadPoolExecutor(max_workers=100) as ex:
        ex.map(check, range(start, end + 1))
    
    return open_ports




base = input("Enter base IP (e.g. 192.168.1): ").strip()
print(f"\n Sweeping network {base}.1-254...\n...")
live_hosts = ping_sweep(base)

print(f"\n Found {len(live_hosts)} live hosts: {live_hosts}")

if live_hosts:
    target = input("\nEnter IP to port scan: ")
        
    open_ports = port_scan(target)
    print(f"\nDone. Found {len(open_ports)} open ports.")

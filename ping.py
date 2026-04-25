import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor

def ping(host):
    # Windows -n | Linux/Max -c
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0 # success

def ping_sweep(base_ip, start=1, end=254):
    live_hosts = []

    def check(i):
        ip = f"{base_ip}.{i}"
        if ping(ip):
            print(f" [+] {ip} is alive!")
            live_hosts.append(ip)

    print(f"Scanning {base_ip}.{start} - {base_ip}.{end}...\n")
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(check, range(start, end + 1))

    return live_hosts

live = ping_sweep("192.168.1")
print(f"\nFound {len(live)} live hosts")
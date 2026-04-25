import subprocess
import platform

def ping(host):
    # Windows -n | Linux/Max -c
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0 # success

print(ping("8.8.8.8")) # Google DNS return true
import socket
import termcolor
from tqdm import tqdm
import concurrent.futures

def scan(target, ports):
    print(termcolor.colored(f"\nStarting Scan for {target}", 'blue'))
    with tqdm(total=ports, desc="Scanning Ports", unit="port") as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = {executor.submit(scan_port, target, port): port for port in range(1, ports + 1)}
            for future in concurrent.futures.as_completed(futures):
                pbar.update(1)

def scan_port(ipaddress, port):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((ipaddress, port))
        try:
            service = socket.getservbyport(port) 
        except OSError:
            service = "unknown"
        print(termcolor.colored(f"[+] Port {port} ({service}) is open", 'green'))
        sock.close()
    except (socket.timeout, ConnectionRefusedError, OSError):
        pass

targets = input("[*] Enter Targets To Scan (split by ,): ").split(',')
targets = [t.strip() for t in targets]

try:
    ports = int(input("[*] Enter Max Port Number: "))
except ValueError:
    print(termcolor.colored("[!] Invalid port number", 'red'))
    exit()

for target in targets:
    scan(target, ports)

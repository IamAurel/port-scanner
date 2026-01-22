import argparse

from concurrent.futures import ThreadPoolExecutor, as_completed
from scanner.tcp_scanner import scan_port

def parse_ports(ports_input):
    if "-" in ports_input:
        start, end = ports_input.split("-")
        return range(int(start), int(end) + 1)
    else:
        return [int(ports_input)]

def main():
    parser = argparse.ArgumentParser("Simple TCP Port Scanner")
    parser.add_argument("-t", "--target", required = True, help = "IP ou hostname")
    parser.add_argument("-p", "--ports", required = True, help = "Port ou range (ex: 22 ou 1-1024)")
    parser.add_argument("-w", "--workers", type = int, default = 50, help = "Nombre de threads")

    args = parser.parse_args()

    target = args.target
    ports = parse_ports(args.ports)

    print(f"[+] Scan de {target}")

    open_ports = []

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_to_port = {executor.submit(scan_port, target, port): port for port in ports}

        for future in as_completed(future_to_port):
            port = future_to_port[future]
            if future.result():
                open_ports.append(port)
                print(f"[OPEN] Port {port}")
    
    if not open_ports:
        print("[-] Aucun port ouvert détecté")            

if __name__ == "__main__":
    main()



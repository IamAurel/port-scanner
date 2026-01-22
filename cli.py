import argparse
from scanner.tcp_scanner import scan_port

def main():
    parser = argparse.ArgumentParser(description="Simple TCP Port Scanner")
    parser.add_argument("-t", "--target", required=True, help="IP ou hostname")
    parser.add_argument("-p", "--ports", required=True, help="Port ou range (ex: 22 ou 1-1024)")

    args = parser.parse_args()

    target = args.target
    ports_input = args.ports

    if "-" in ports_input:
        start, end = ports_input.split("-")
        ports = range(int(start), int(end) + 1)
    else:
        ports = [int(ports_input)]

    print(f"[+] Scan de {target}")

    for port in ports:
        if scan_port(target, port):
            print(f"[OPEN] Port {port}")

if __name__ == "__main__":
    main()
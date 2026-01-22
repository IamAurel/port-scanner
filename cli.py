import argparse
import json

from concurrent.futures import ThreadPoolExecutor, as_completed
from scanner.tcp_scanner import scan_port
from scanner.grabber_banner import grab_banner

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
    parser.add_argument("--banner", action = "store_true", help = "Activer le banner grabbing (plus lent)")
    parser.add_argument("--json", help = "Chemin du fichier JSON de sortie")

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

                banner = None  # <-- important

                if args.banner:
                    banner = grab_banner(target, port, 1.0)
                    if banner:
                        print(f"[OPEN] Port {port} - {banner}")
                    else:
                        print(f"[OPEN] Port {port}")
                else:
                    print(f"[OPEN] Port {port}")

                open_ports.append({"port": port, "banner": banner})
            
    if not open_ports:
        print("[-] Aucun port ouvert détecté")  

    if args.json:
        result = {"target": target, "ports": open_ports}
        with open(args.json, "w", encoding = "utf-8") as f:
            json.dump(result, f, indent = 2, ensure_ascii = False)         

if __name__ == "__main__":
    main()



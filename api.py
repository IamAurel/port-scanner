from fastapi import FastAPI, HTTPException
from concurrent.futures import ThreadPoolExecutor, as_completed
from scanner.tcp_scanner import scan_port
from scanner.grabber_banner import grab_banner

app = FastAPI()

def parse_ports(ports_input: str):
    if "-" in ports_input:
        start, end = ports_input.split("-")
        return range(int(start), int(end) + 1)
    else:
        return [int(ports_input)]
    
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/status")
def status(target: str, port: int):
    is_open = scan_port(target, port)
    return {"target": target, "port": port, "open": is_open}

@app.get("/scan")
def scan(target: str, ports: str, workers: int = 50, banner: bool = False):
    ports_range = parse_ports(ports)

    open_ports = []

    with ThreadPoolExecutor(max_workers = workers) as executor:
        future_to_port = {executor.submit(scan_port, target, port): port for port in ports_range}

        for future in as_completed(future_to_port):
            port = future_to_port[future]
            if future.result():
                banner_text = None  # <- toujours défini

                if banner:
                    banner_text = grab_banner(target, port, timeout=1.0)

                open_ports.append({"port": port, "banner": banner_text})

    return{"target": target, "open_ports": open_ports}
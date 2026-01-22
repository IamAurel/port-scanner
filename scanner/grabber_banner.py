import socket

def grab_banner(target: str, port: int, timeout: 1.0):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((target, port))

            # HTTP
            if port == 80:
                http_request = ("GET / HTTTP/1.1\r\n"
                                f"Host: {target}\r\n"
                                "Connection: close\r\n\r\n")
                sock.sendall(http_request.encode())
                response = sock.recv(1024).decode(errors = "ignore")
                return parse_http_banner(response)
            
            # HTTPS
            if port == 443:
                https_request = ("GET / HTTP/1.1\r\n"
                                 f"Host:{target}\r\n"
                                 "Connection: close\r\n\r\n")
                sock.sendall(https_request.encode())
                sock.recv(1024).decode(errors = "ignore")
                return parse_http_banner(response)
            
            # Autres services (SSH, FTP,etc...)
            response = sock.recv(1024).decode(errors = "ignore")
            return response.strip()
        
    except socket.error:
        return None
    
def parse_http_banner(response: str):
    if not response:
        return None
    
    lines = response.split("\r\n")
    status = lines[0] if lines else ""
    server = None
    
    for line in lines:
        if line.lower().startswith("server:"):
            server = line.split(":", 1)[1].strip()
            break

    if server:
        return f"{status} - Server: {server}"
    return status
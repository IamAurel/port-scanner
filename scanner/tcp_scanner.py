import socket

def scan_port(target: str, port: int, timeout: float = 1.0):
    """
    Scan un port TCP sur une cible
    Retourne True si le port est ouvert, false sinon
    """

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            return result == 0
    except socket.error:
        return False
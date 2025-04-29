import socket
import time

def scanner(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        sock.connect((ip, port))
        print(f"[!] Port {port} is open")
    except:
        None


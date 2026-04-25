import socket
import threading
from http_client import send_get, send_post

TCP_PORT = 8888

def handle_browser(conn):
    raw     = conn.recv(65535).decode()
    parts   = raw.split("\r\n")[0].split(" ")
    method  = parts[0]
    path    = parts[1]

    print(f"Browser requested: {method} {path}")

    if method == "GET":
        response = send_get(path)
    elif method == "POST":
        body     = raw.split("\r\n\r\n", 1)[1]
        response = send_post(path, body)

    conn.sendall(response.encode())
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", TCP_PORT))
server.listen(5)
print(f"Open your browser and go to: http://127.0.0.1:{TCP_PORT}/index.html")

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_browser, args=(conn,)).start()
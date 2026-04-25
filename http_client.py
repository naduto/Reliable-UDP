from RelUDP import ReliableUDP

HOST = "127.0.0.1"
PORT = 8081

def send_get(path):
    request = f"GET {path} HTTP/1.0\r\nHost: {HOST}\r\n\r\n"
    return _send(request.encode())

def send_post(path, body):
    request = (
        f"POST {path} HTTP/1.0\r\n"
        f"Host: {HOST}\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"\r\n"
        f"{body}"
    )
    return _send(request.encode())

def _send(raw_request):
    client = ReliableUDP()
    client.connect(HOST, PORT)
    client.send_data(raw_request)
    raw_response = client.recv_data()
    print("\n" + "="*50)
    print("RESPONSE:")
    print("="*50)
    print(raw_response.decode())
    print("="*50 + "\n")
    client.close()
    return raw_response.decode()     

if __name__ == "__main__":
    send_get("/index.html")

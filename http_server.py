import os
from RelUDP import ReliableUDP
from http_utils import parse_request, build_response

PORT     = 8081
WWW_DIR  = "./www"          

def run():
    os.makedirs(WWW_DIR, exist_ok=True)

    while True:
        # --- step 1: create fresh socket and wait ---
        server = ReliableUDP()
        server.bind(PORT)
        print("\nWaiting for connection...")
        # handshake
        server.accept()                           

        # --- step 2: receive the HTTP request ---
        raw = server.recv_data()
        method, path, body = parse_request(raw)
        print("\n" + "="*50)
        print(f"REQUEST: {method} {path}")
        print(f"BODY: {body}" if body else "")
        print("="*50 + "\n")

        # --- step 3: handle it ---
        if method == "GET":
            filename = path.lstrip("/") or "index.html"
            filepath = os.path.join(WWW_DIR, filename)

            if os.path.isfile(filepath):
                content = open(filepath).read()
                response = build_response(200, content)
            else:
                response = build_response(404, f"<h1>404 - {filename} not found</h1>")

        elif method == "POST":
            print("\n" + "="*50)
            print(f"REQUEST: {method} {path}")
            print(f"BODY: {body}" if body else "")
            print("="*50 + "\n")
            response = build_response(200, f"<h1>Received: {body}</h1>")

        else:
            response = build_response(404, "<h1>Method not supported</h1>")

        # --- step 4: send response and close ---
        server.send_data(response)
        server.close()
        print("--- Connection closed ---")

if __name__ == "__main__":
    run()
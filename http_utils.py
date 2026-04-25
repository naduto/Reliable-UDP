from datetime import datetime

def parse_request(raw_bytes):
    text = raw_bytes.decode()
    
    # Split headers from body
    if "\r\n\r\n" in text:
        head, body = text.split("\r\n\r\n", 1)
    else:
        head, body = text, ""

    lines = head.split("\r\n")
    # "GET /index.html HTTP/1.0"
    parts = lines[0].split(" ")      
    method = parts[0]
    # /index.html                
    path   = parts[1]               
    
    return method, path, body        


def build_response(status_code, body_text):
    if status_code == 200:
        status = "200 OK"
    else:
        status = "404 Not Found"

    body_bytes = body_text.encode()

    response = (
        f"HTTP/1.0 {status}\r\n"
        f"Content-Type: text/html\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
        f"\r\n"
        f"{body_text}"
    )
    return response.encode()
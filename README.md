# Reliable-UDP

A Python-based project that simulates TCP reliability over UDP, with a fully functional HTTP/1.0 server and client built on top.

## Project Structure

```
Reliable-UDP/
├── packet.py          # packet structure, checksum, flags
├── RelUDP.py          # reliable UDP transport layer
├── http_utils.py      # HTTP request parser and response builder
├── http_server.py     # HTTP server
├── http_client.py     # HTTP client
├── proxy.py           # TCP proxy for browser communication
├── test_transport.py  # transport layer test cases
├── test_http.py       # HTTP layer test cases
└── www/
└── index.html     # served files
```
## How to Run

### HTTP Server and Client
```bash
# terminal 1
python3 http_server.py

# terminal 2
python3 http_client.py
```

### Browser Communication
```bash
# terminal 1
python3 http_server.py

# terminal 2
python3 proxy.py

# open your browser and go to
http://127.0.0.1:8888/index.html
```

### Run Tests
```bash
# terminal 1
python3 http_server.py

# terminal 2 - transport layer tests
python3 test_transport.py

# terminal 2 - HTTP layer tests
python3 test_http.py
```

## Features

- UDP socket using Python's socket library
- 3-way handshake (SYN, SYN-ACK, ACK)
- Stop-and-Wait reliable data transfer
- Checksum calculation and verification
- Packet corruption detection and simulation
- Packet loss simulation
- Sequence numbers and duplicate detection
- Retransmission and timeouts
- FIN connection teardown
- HTTP 1.0 server and client
- GET and POST methods
- 200 OK and 404 Not Found responses
- HTTP headers (Content-Type, Content-Length, Date)

## Limitations

- Only supports HTTP 1.0
- Only GET and POST methods
- No congestion control or sliding window
- Single connection at a time
- No HTTPS support

## Wireshark Traffic
![Wireshark](wireshark.png)
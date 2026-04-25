from http_client import send_get, send_post

passed = 0
failed = 0

def check(name, condition):
    global passed, failed
    if condition:
        print(f"  PASS - {name}")
        passed += 1
    else:
        print(f"  FAIL - {name}")
        failed += 1

print("\n--- running HTTP tests ---\n")

# test 1 - GET existing file
print("Test 1: GET existing file")
r = send_get("/index.html")
check("status is 200 OK", "200 OK" in r)
check("body contains html", "<html>" in r.lower())

# test 2 - GET missing file
print("\nTest 2: GET missing file")
r = send_get("/missing.html")
check("status is 404", "404" in r)

# test 3 - POST with data
print("\nTest 3: POST with data")
r = send_post("/submit", "name=Nada&message=hello")
check("status is 200 OK", "200 OK" in r)
check("data echoed back", "Nada" in r)

# test 4 - POST with empty body
print("\nTest 4: POST with empty body")
r = send_post("/submit", "")
check("server returns 200", "200 OK" in r)

# test 5 - GET root path
print("\nTest 5: GET root /")
r = send_get("/")
check("returns 200 OK", "200 OK" in r)

# test 6 - response headers
print("\nTest 6: response headers")
r = send_get("/index.html")
check("has Content-Type",   "Content-Type" in r)
check("has Content-Length", "Content-Length" in r)
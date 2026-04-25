from RelUDP import ReliableUDP
from packet import Packet, SYN, ACK, FIN, SYNACK
import socket

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

print("\n transport tests are running\n")

# test 1 - pack and unpack
print("Test 1: pack and unpack")
p = Packet(seq=1, ack=0, flags=SYN, data=b'hello')
p2 = Packet.unpack(p.pack())
check("seq is correct", p2.seq == 1)
check("data is correct", p2.data == b'hello')
check("flag is SYN", p2.is_syn())

# test 2 - checksum
print("\nTest 2: checksum")
p = Packet(seq=0, data=b'hello')
p.pack()
check("clean packet is valid", p.is_valid())
p.corrupt()
check("corrupted packet is invalid", not p.is_valid())

# test 3 - flags
print("\nTest 3: flags")
check("SYN works", Packet(flags=SYN).is_syn())
check("ACK works", Packet(flags=ACK).is_ack())
check("FIN works", Packet(flags=FIN).is_fin())
check("SYNACK works", Packet(flags=SYNACK).is_synack())

# test 4 - sequence numbers
print("\nTest 4: sequence numbers")
p1 = Packet(seq=0, data=b'first')
p2 = Packet(seq=1, data=b'second')
check("seq numbers are different", p1.seq != p2.seq)
check("seq increments correctly", p2.seq == p1.seq + 1)

# summary
print(f"\n--- results: {passed} passed, {failed} failed ---\n")
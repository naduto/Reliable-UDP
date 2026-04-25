import socket
import random
from packet import Packet, SYN, ACK, FIN, SYNACK
BUFFER_SIZE = 65535
TIMEOUT = 2      
MAX_RETRIES = 5 
LOSS_PROBABILITY = 0.3
class ReliableUDP:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dest = None
        self.seq = 0
        self.expected_seq = 0
                    
    def bind(self, port):
        self.sock.bind(('', port))

    def send_packet(self, packet, raw=None,simulate_loss=False):
        if simulate_loss and random.random() < LOSS_PROBABILITY:
            print("packet lost! (simulated)")
            return
        if raw is not None:
            self.sock.sendto(raw, self.dest)
            print(f"sent raw bytes")
        else:
            self.sock.sendto(packet.pack(), self.dest)
            print(f"sent: {packet}")

    def recv_packet(self):
        raw, addr = self.sock.recvfrom(BUFFER_SIZE)
        packet = Packet.unpack(raw)
        print(f"received: {packet} from {addr}")
        return packet, addr
    
    def send_data(self, data,simulate_loss=False):
        packet = Packet(seq=self.seq, data=data)
        retries_count = 0
        while retries_count < MAX_RETRIES:
            self.send_packet(packet,simulate_loss=simulate_loss)
            try:
                self.sock.settimeout(TIMEOUT)
                ack_packet, _ = self.recv_packet()
                if ack_packet.is_ack() and ack_packet.ack == self.seq:
                    self.seq += 1
                    print(f"ack received for seq {self.seq - 1}, sending next packet")
                    return True
                else:
                    print(f"wrong ack, retrying... ")
            except socket.timeout:
                retries_count += 1
                print(f"timeout, retrying... ({retries_count}/{MAX_RETRIES})")
        print(f"max retries reached, failed to send packet with seq {self.seq}")
        return False
            
    def recv_data(self):
        while True:
            packet, addr = self.recv_packet()
            if not packet.is_valid():
                print(f"corrupted packet, retrying...")
                continue
            if packet.seq == self.expected_seq:
                self.expected_seq += 1
                print(f"ack received for seq {self.expected_seq - 1}, sending next packet")
                ack_packet = Packet(seq=0, ack=packet.seq,flags=ACK)
                self.dest=addr
                self.send_packet(ack_packet)
                return packet.data
            elif packet.seq<self.expected_seq :
                print(f"duplicate packet, resending ack")
                ack_packet = Packet(seq=0, ack=packet.seq,flags=ACK)
                self.dest=addr
                self.send_packet(ack_packet)
            else:
                print(f"out of order packet seq={packet.seq}, expected={self.expected_seq}, dropping it...")    
    def connect(self, dest , port):
        self.dest = (dest , port)
        retries_count = 0
        while retries_count < MAX_RETRIES:
            syn = Packet(seq=0,ack=0,flags=SYN)
            self.send_packet(syn)
            try:
                self.sock.settimeout(TIMEOUT)
                response, _ = self.recv_packet()
                if response.is_synack():
                    print("syn+ack received , ack is being sent")
                    ack = Packet(seq=0,ack=response.seq,flags=ACK)
                    self.send_packet(ack)
                    self.seq =0
                    self.sock.settimeout(None)
                    print("connection successful")
                    return True
                else:
                    print("wrong ack, retrying... ")
            except socket.timeout:
                retries_count += 1
                print(f"timeout, retrying... ({retries_count}/{MAX_RETRIES})")
        print(f"3 way handshake failed")
        return False
    def accept(self):
          while True:
            packet, addr = self.recv_packet()            
            if not packet.is_syn():
                print("expected SYN, got something else, ignoring...")
                continue
            print(f"got SYN from {addr}, sending SYN+ACK...")
            self.dest = addr
            # step 2 - send SYN+ACK back to client
            synack = Packet(seq=0, ack=packet.seq, flags=SYNACK)
            self.send_packet(synack)
            try:
                self.sock.settimeout(TIMEOUT)
                # step 3 - wait for ACK from client
                ack, _ = self.recv_packet()
                
                if ack.is_ack():
                    print("got ACK, connection established!")
                    self.seq =0
                    self.expected_seq = 0
                    self.sock.settimeout(None)
                    return True
                else:
                    print("expected ACK, got something else, retrying...")
                    
            except socket.timeout:
                print("timeout waiting for ACK, retrying...")
    def close(self):
        if self.dest is not None:
            fin = Packet(seq=self.seq, ack=0, flags=FIN)
            self.send_packet(fin)
        self.sock.close()
        print("Connection closed !!")
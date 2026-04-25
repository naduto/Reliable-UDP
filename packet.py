import struct

# these are just bit flags we'll use to mark what kind of packet we're sending
SYN = 0b00000001
ACK = 0b00000010
FIN = 0b00000100
SYNACK = SYN | ACK


class Packet:
    FORMAT = '!IIBHI'
    HEADER_SIZE = struct.calcsize(FORMAT)

    def __init__(self, seq=0, ack=0, flags=0, data=b''):
        self.seq = seq
        self.ack = ack
        self.flags = flags
        self.data = data
        self.checksum = 0

    def pack(self):
        # first pack with checksum = 0 to calculate it
        header = struct.pack(self.FORMAT, self.seq, self.ack, self.flags, 0, len(self.data))
        
        # calculate checksum over header + data
        self.checksum = self.calc_checksum(header + self.data)
        
        # now repack with the real checksum
        header = struct.pack(self.FORMAT, self.seq, self.ack, self.flags, self.checksum, len(self.data))
        
        return header + self.data

    @classmethod
    def unpack(cls, raw):
        # split header and data
        header = raw[:cls.HEADER_SIZE]
        data = raw[cls.HEADER_SIZE:]
        
        seq, ack, flags, checksum, data_len = struct.unpack(cls.FORMAT, header)
        
        p = cls(seq, ack, flags, data)
        p.checksum = checksum
        return p

    def calc_checksum(self, data):
        # pad to even length if needed
        if len(data) % 2 != 0:
            data += b'\x00'
        
        total = 0
        # sum every 2 bytes together
        for i in range(0, len(data), 2):
            word = (data[i] << 8) + data[i + 1]
            total += word
            # wrap around if overflow
            total = (total & 0xFFFF) + (total >> 16)
        
        # return one's complement
        return ~total & 0xFFFF
    def corrupt(self):
        self.checksum = (~self.checksum) & 0xFFFF   
        
    def is_valid(self):
        received = self.checksum
        header = struct.pack(self.FORMAT, self.seq, self.ack, self.flags, 0, len(self.data))
        expected = self.calc_checksum(header + self.data)
        return received == expected

    def is_syn(self):
        return bool(self.flags & SYN)

    def is_ack(self):
        return bool(self.flags & ACK)

    def is_fin(self):
        return bool(self.flags & FIN)

    def is_synack(self):
        return self.is_syn() and self.is_ack()

    def __str__(self):
        flags = []
        if self.is_syn(): flags.append('SYN')
        if self.is_ack(): flags.append('ACK')
        if self.is_fin(): flags.append('FIN')
        flags_str = '+'.join(flags) if flags else 'NONE'
        return f"[seq={self.seq} ack={self.ack} flags={flags_str} checksum={self.checksum} data={self.data}]"


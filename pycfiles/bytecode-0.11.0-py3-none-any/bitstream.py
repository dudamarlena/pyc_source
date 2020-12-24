# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/bitstream.py
# Compiled at: 2011-06-27 17:46:54


class BitStream(object):

    @property
    def from_bytes(cls, bytes):
        bs = cls()
        bs.bytes = bytes
        return bs

    def __init__(self, bits=''):
        self.bits = bits

    @property
    def bytes(self):
        bytes = ''
        pos = 0
        while True:
            chunk = self.bits[pos:pos + 8]
            if not chunk:
                break
            pos += 8
            chunk = chunk.ljust(8, '0')
            c = chr(int(chunk, 2))
            bytes += c

        return bytes

    @bytes.setter
    def bytes(self, bytes):
        self.bits = ('').join([ bin(ord(byte))[2:].zfill(8) for byte in bytes ])

    @property
    def int_be(self):
        n = 0
        for byte in self.bytes:
            n = (n << 8) + ord(byte)

        return n

    @property
    def int_le(self):
        n = 0
        for byte in reversed(self.bytes):
            n = (n << 8) + ord(byte)

        return n

    def __add__(self, other):
        if isinstance(other, str):
            return BitStream(self.bits + other)
        if isinstance(other, BitStream):
            return BitStream(self.bits + other.bits)

    def __len__(self):
        return len(self.bits)

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.bits[index] == '1'
        if isinstance(index, slice):
            return BitStream(self.bits[index])

    def __setitem__(self, index, value):
        if isinstance(index, int):
            self.bits = self.bits[:index] + (value and '1' or '0') + self.bits[index + 1:]
        elif isinstance(index, slice):
            if isinstance(value, BitStream):
                value = value.bits
            if index.start is None:
                index.start = 0
            if index.stop is None:
                index.stop = len(self)
            if index.stop < 0:
                index.stop += len(self)
            vlen = len(value)
            gaplen = index.stop - index.start
            if vlen < gaplen:
                times = gaplen / vlen + 1
                value = (value * times)[:gaplen]
            self.bits = self.bits[:index.start] + value + self.bits[index.stop:]
        return


class BitMask(object):

    def __init__(self, s):
        self.length = len(s)
        self.fields = []
        self.fieldnames = {}
        lastc = None
        for thisc in s:
            if not thisc.strip():
                continue
            if lastc == thisc:
                (c, l) = self.fields[(-1)]
                self.fields[-1] = (c, l + 1)
            else:
                self.fieldnames[thisc] = len(self.fields)
                self.fields.append((thisc, 1))
            lastc = thisc

        return

    def get_field_length(self, name):
        if name in self.fieldnames:
            (c, l) = self.fields[self.fieldnames[name]]
            return l
        return 0

    def get_field_offset(self, name):
        if name in self.fieldnames:
            offset = 0
            for (c, l) in self.fields:
                if c == name:
                    return offset
                offset += l

        return 0

    def fill(self, **values):
        bits = BitStream()
        for (name, length) in self.fields:
            v = int(values.get(name, 0))
            bits += bin(v)[2:].zfill(length)[-length:]

        return bits

    def parse(self, bits):
        values = {}
        offset = 0
        for (name, length) in self.fields:
            values[name] = bits[offset:offset + length].int_be
            offset += length

        return values

    def __len__(self):
        n = 0
        for (c, l) in self.fields:
            n += l

        return n
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/bytebuilder.py
# Compiled at: 2011-06-28 13:26:57


class Pointer(object):

    def __init__(self, bb, size=1):
        self.bb = bb
        self.pos = bb.get_pos() - size
        self.size = size

    def now(self):
        self.fill(self.bb.get_pos())

    def fill(self, v):
        if isinstance(v, int):
            v = self.bb.format_num(v, self.size)
        self.bb.replace(self.pos, self.size, v)


class Flags(object):

    def __init__(self, *args, **kwds):
        self.flags = {}
        v = 1
        for name in args:
            self.flags[name] = v
            v += 1

        self.flags.update(kwds)

    def parse(self, n):
        res = {}
        for (name, bitpos) in self.flags.iteritems():
            res[name] = bool(n & 1 << bitpos)

        return res

    def create(self, *present, **kwds):
        values = dict.fromkeys(present, True)
        values.update(kwds)
        n = 0
        for (name, bitpos) in self.flags.iteritems():
            if values.get(name):
                n |= 1 << bitpos

        return n


class ByteBuilder(object):

    def __init__(self, little_endian=False):
        self.little_endian = little_endian
        self.reset()

    @property
    def start_marker(self):
        if self.start_markers:
            return self.start_markers[(-1)]
        else:
            return 0

    def reset(self):
        self.data = ''
        self.measure_start = 0
        self.binfrag = ''
        self.start_markers = []

    def push_start_marker(self):
        p = self.get_pos()
        self.start_markers.append(p)
        return p

    def pop_start_marker(self):
        return self.start_markers.pop(-1)

    def write(self, s):
        self.data += s

    def start_measure(self):
        self.measure_start = self.get_pos()

    def end_measure(self):
        return self.get_pos() - self.measure_start

    def get_pos(self):
        return len(self.data) - self.start_marker

    def pointer(self, size):
        self.pad(size)
        return Pointer(self, size)

    def pad(self, n=1):
        self.write('\x00' * n)

    def pad_to(self, p):
        self.pad(p - self.get_pos())

    def char(self, c):
        if len(c) != 1:
            raise ValueError('Argument must be a string of length 1')
        self.write(c)

    def string(self, s, l=None, padding='\x00'):
        if l is not None:
            s = s[:l].ljust(l, padding)
        self.write(s)
        return

    def lstring(self, s, size):
        l = len(s)
        if l >= 1 << size * 8:
            raise ValueError('String is too long')
        self.write(self.format_num(l, size))
        self.write(s)

    def nulterm(self, s):
        self.write(s)
        self.write('\x00')

    def nulpad(self, s, size, dir='right'):
        if dir == 'right':
            s = s.ljust(size, '\x00')
        elif dir == 'left':
            s = s.rjust(size, '\x00')
        self.write(s)

    def binary(self, s, l=8):
        if isinstance(s, bool):
            s = int(s)
            l = 1
        if isinstance(s, int):
            s = bin(s)[2:].zfill(l)[-l:]
        self.binfrag += s
        while len(self.binfrag) >= 8:
            s = self.binfrag[:8]
            self.binfrag = self.binfrag[8:]
            self.byte(int(s, 2))

    def byte(self, n):
        self.write(chr(n))

    def short(self, n):
        self.write(self.format_num(n, 2))

    def int(self, n):
        self.write(self.format_num(n, 4))

    def long(self, n):
        self.write(self.format_num(n, 8))

    ubyte = byte
    ushort = short
    uint = int
    ulong = long

    def sbyte(self, n):
        self.byte(self.s2u(n))

    def sshort(self, n):
        self.short(self.s2u(n))

    def sint(self, n):
        self.int(self.s2u(n))

    def slong(self, n):
        self.long(self.s2u(n))

    def s2u(self, n, size=1):
        if n < 0:
            n += 1 << (size << 3)
        return n

    def format_num(self, n, size=1):
        s = ''
        for i in range(size):
            s = chr(n & 255) + s
            n = n >> 8

        if self.little_endian:
            s = s[::-1]
        return s

    def write_num(self, n, size=1):
        self.write(self.format_num(n, size))

    def get_data(self):
        return self.data

    def replace(self, start, length, s):
        end = start + length
        self.data = self.data[:start] + s + self.data[end:]


class ByteScanner(object):

    def __init__(self, source, little_endian=False):
        self.source = source
        self.little_endian = little_endian
        self.reset()

    @property
    def start_marker(self):
        if self.start_markers:
            return self.start_markers[(-1)]
        else:
            return 0

    def reset(self):
        self.start_markers = [self.source.tell()]

    def push_start_marker(self):
        p = self.get_pos()
        self.start_markers.append(p)
        return p

    def pop_start_marker(self):
        return self.start_markers.pop(-1)

    def read(self, n):
        return self.source.read(n)

    def get_pos(self):
        return self.source.tell() - self.start_marker

    def pad(self, n=1):
        self.read(n)

    def pad_to(self, p):
        self.pad(p - self.get_pos())

    def char(self):
        return self.read(1)

    def string(self, l, padding=None):
        s = self.read(l)
        if padding is not None:
            s = s.rstrip(padding)
        return s

    def lstring(self, size):
        l = self.parse_num(self.read(size))
        return self.read(l)

    def nulterm(self):
        s = ''
        while True:
            c = self.read(1)
            if c == '\x00':
                break
            else:
                s += c

        return s

    def nulpad(self, s, size, dir='right'):
        s = self.read(size)
        if dir == 'right':
            s = s.rstrip('\x00')
        elif dir == 'left':
            s = s.lstrip('\x00')
        return s

    def byte(self, n):
        return ord(self.read(1))

    def short(self, n):
        return self.parse_num(self.read(2))

    def int(self, n):
        return self.parse_num(self.read(4))

    def long(self, n):
        return self.parse_num(self.read(8))

    ubyte = byte
    ushort = short
    uint = int
    ulong = long

    def sbyte(self, n):
        return self.byte(self.s2u(n))

    def sshort(self, n):
        return self.short(self.s2u(n))

    def sint(self, n):
        return self.int(self.s2u(n))

    def slong(self, n):
        return self.long(self.s2u(n))

    def s2u(self, n, size=1):
        if n < 0:
            n += 1 << (size << 3)
        return n

    def parse_num(self, s):
        if self.little_endian:
            s = s[::-1]
        n = 0
        for c in s:
            n = n << 8
            n += ord(c)

        return n

    def read_num(self, num_bytes):
        return self.parse_num(self.read(num_bytes))
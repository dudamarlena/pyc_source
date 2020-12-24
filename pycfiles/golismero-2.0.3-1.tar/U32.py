# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/requests_ntlm/ntlm/U32.py
# Compiled at: 2013-08-26 10:52:44
C = 68719476736

def norm(n):
    return n & 4294967295


class U32:
    v = 0

    def __init__(self, value=0):
        self.v = C + norm(abs(long(value)))

    def set(self, value=0):
        self.v = C + norm(abs(long(value)))

    def __repr__(self):
        return hex(norm(self.v))

    def __long__(self):
        return long(norm(self.v))

    def __int__(self):
        return int(norm(self.v))

    def __chr__(self):
        return chr(norm(self.v))

    def __add__(self, b):
        r = U32()
        r.v = C + norm(self.v + b.v)
        return r

    def __sub__(self, b):
        r = U32()
        if self.v < b.v:
            r.v = C + norm(4294967296 - (b.v - self.v))
        else:
            r.v = C + norm(self.v - b.v)
        return r

    def __mul__(self, b):
        r = U32()
        r.v = C + norm(self.v * b.v)
        return r

    def __div__(self, b):
        r = U32()
        r.v = C + norm(self.v) / norm(b.v)
        return r

    def __mod__(self, b):
        r = U32()
        r.v = C + norm(self.v) % norm(b.v)
        return r

    def __neg__(self):
        return U32(self.v)

    def __pos__(self):
        return U32(self.v)

    def __abs__(self):
        return U32(self.v)

    def __invert__(self):
        r = U32()
        r.v = C + norm(~self.v)
        return r

    def __lshift__(self, b):
        r = U32()
        r.v = C + norm(self.v << b)
        return r

    def __rshift__(self, b):
        r = U32()
        r.v = C + (norm(self.v) >> b)
        return r

    def __and__(self, b):
        r = U32()
        r.v = C + norm(self.v & b.v)
        return r

    def __or__(self, b):
        r = U32()
        r.v = C + norm(self.v | b.v)
        return r

    def __xor__(self, b):
        r = U32()
        r.v = C + norm(self.v ^ b.v)
        return r

    def __not__(self):
        return U32(not norm(self.v))

    def truth(self):
        return norm(self.v)

    def __cmp__(self, b):
        if norm(self.v) > norm(b.v):
            return 1
        else:
            if norm(self.v) < norm(b.v):
                return -1
            return 0

    def __nonzero__(self):
        return norm(self.v)
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kaa/metadata/audio/eyeD3/binfuncs.py
# Compiled at: 2006-03-11 16:05:34


def bytes2bin(bytes, sz=8):
    if sz < 1 or sz > 8:
        raise ValueError('Invalid sz value: ' + str(sz))
    retVal = []
    for b in bytes:
        bits = []
        b = ord(b)
        while b > 0:
            bits.append(b & 1)
            b >>= 1

        if len(bits) < sz:
            bits.extend([0] * (sz - len(bits)))
        elif len(bits) > sz:
            bits = bits[:sz]
        bits.reverse()
        retVal.extend(bits)

    if len(retVal) == 0:
        retVal = [
         0]
    return retVal


def bin2bytes(x):
    bits = []
    bits.extend(x)
    bits.reverse()
    i = 0
    out = ''
    multi = 1
    ttl = 0
    for b in bits:
        i += 1
        ttl += b * multi
        multi *= 2
        if i == 8:
            i = 0
            out += chr(ttl)
            multi = 1
            ttl = 0

    if multi > 1:
        out += chr(ttl)
    out = list(out)
    out.reverse()
    out = ('').join(out)
    return out


def bin2dec(x):
    bits = []
    bits.extend(x)
    bits.reverse()
    multi = 1
    value = long(0)
    for b in bits:
        value += b * multi
        multi *= 2

    return value


def bytes2dec(bytes, sz=8):
    return bin2dec(bytes2bin(bytes, sz))


def dec2bin(n, p=0):
    assert n >= 0
    retVal = []
    while n > 0:
        retVal.append(n & 1)
        n >>= 1

    if p > 0:
        retVal.extend([0] * (p - len(retVal)))
    retVal.reverse()
    return retVal


def dec2bytes(n, p=0):
    return bin2bytes(dec2bin(n, p))


def bin2synchsafe(x):
    if len(x) > 32 or bin2dec(x) > 268435456:
        raise ValueError('Invalid value')
    elif len(x) < 8:
        return x
    n = bin2dec(x)
    bites = ''
    bites += chr(n >> 21 & 127)
    bites += chr(n >> 14 & 127)
    bites += chr(n >> 7 & 127)
    bites += chr(n >> 0 & 127)
    bits = bytes2bin(bites)
    if len(bits) < 32:
        bits = [
         0] * (32 - len(x)) + bits
    return bits


def bytes2str(bytes):
    s = ''
    for b in bytes:
        s += '\\x%02x' % ord(b)

    return s
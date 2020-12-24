# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/pymorton/__init__.py
# Compiled at: 2018-02-14 20:26:33
_DIVISORS = [ 180.0 / 2 ** n for n in range(32) ]

def __part1by1(n):
    n &= 65535
    n = (n | n << 8) & 16711935
    n = (n | n << 4) & 252645135
    n = (n | n << 2) & 858993459
    n = (n | n << 1) & 1431655765
    return n


def __part1by2(n):
    n &= 1023
    n = (n ^ n << 16) & 4278190335
    n = (n ^ n << 8) & 50393103
    n = (n ^ n << 4) & 51130563
    n = (n ^ n << 2) & 153391689
    return n


def __unpart1by1(n):
    n &= 1431655765
    n = (n ^ n >> 1) & 858993459
    n = (n ^ n >> 2) & 252645135
    n = (n ^ n >> 4) & 16711935
    n = (n ^ n >> 8) & 65535
    return n


def __unpart1by2(n):
    n &= 153391689
    n = (n ^ n >> 2) & 51130563
    n = (n ^ n >> 4) & 50393103
    n = (n ^ n >> 8) & 4278190335
    n = (n ^ n >> 16) & 1023
    return n


def interleave2(*args):
    if len(args) != 2:
        raise ValueError('Usage: interleave2(x, y)')
    for arg in args:
        if not isinstance(arg, int):
            print 'Usage: interleave2(x, y)'
            raise ValueError('Supplied arguments contain a non-integer!')

    return __part1by1(args[0]) | __part1by1(args[1]) << 1


def interleave3(*args):
    if len(args) != 3:
        raise ValueError('Usage: interleave3(x, y, z)')
    for arg in args:
        if not isinstance(arg, int):
            print 'Usage: interleave3(x, y, z)'
            raise ValueError('Supplied arguments contain a non-integer!')

    return __part1by2(args[0]) | __part1by2(args[1]) << 1 | __part1by2(args[2]) << 2


def interleave(*args):
    if len(args) < 2 or len(args) > 3:
        print 'Usage: interleave(x, y, (optional) z)'
        raise ValueError('You must supply two or three integers to interleave!')
    method = globals()[('interleave' + str(len(args)))]
    return method(*args)


def deinterleave2(n):
    if not isinstance(n, int):
        print 'Usage: deinterleave2(n)'
        raise ValueError('Supplied arguments contain a non-integer!')
    return (
     __unpart1by1(n), __unpart1by1(n >> 1))


def deinterleave3(n):
    if not isinstance(n, int):
        print 'Usage: deinterleave2(n)'
        raise ValueError('Supplied arguments contain a non-integer!')
    return (
     __unpart1by2(n), __unpart1by2(n >> 1), __unpart1by2(n >> 2))


def interleave_latlng(lat, lng):
    if not isinstance(lat, float) or not isinstance(lng, float):
        print 'Usage: interleave_latlng(float, float)'
        raise ValueError('Supplied arguments must be of type float!')
    if lng > 180:
        x = lng % 180 + 180.0
    else:
        if lng < -180:
            x = -(-lng % 180) + 180.0
        else:
            x = lng + 180.0
        if lat > 90:
            y = lat % 90 + 90.0
        elif lat < -90:
            y = -(-lat % 90) + 90.0
        else:
            y = lat + 90.0
        morton_code = ''
        for dx in _DIVISORS:
            digit = 0
            if y >= dx:
                digit |= 2
                y -= dx
            if x >= dx:
                digit |= 1
                x -= dx
            morton_code += str(digit)

    return morton_code


def deinterleave_latlng(n):
    x = y = 0
    for digit, multiplier in zip([ int(d) for d in n ], _DIVISORS):
        if digit & 2:
            y += multiplier
        if digit & 1:
            x += multiplier

    return (round(y - 90.0, 6), round(x - 180.0, 6))
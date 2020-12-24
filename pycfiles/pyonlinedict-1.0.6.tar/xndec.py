# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/xndec/xndec.py
# Compiled at: 2015-12-22 13:15:03
import ctypes, os
types = [
 '', '.so', '.dylib', '.pyd']
x = None
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
for a in types:
    try:
        x = ctypes.CDLL(os.path.join(dir_path, 'libxndec' + a))
        break
    except:
        pass

f = x.XnStreamUncompressDepth16ZWithEmbTable
et = ctypes.POINTER(ctypes.c_uint8)
f.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(ctypes.c_int)]
f.restype = ctypes.c_int
XnStreamUncompressDepth16ZWithEmbTable = f
f = x.XnStreamUncompressDepth16Z
et = ctypes.POINTER(ctypes.c_uint8)
f.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(ctypes.c_int)]
f.restype = ctypes.c_int
XnStreamUncompressDepth16Z = f
f = x.XnStreamUncompressImage8Z
et = ctypes.POINTER(ctypes.c_uint8)
f.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_int)]
f.restype = ctypes.c_int
XnStreamUncompressImage8Z = f
f = x.XnStreamUncompressConf4
et = ctypes.POINTER(ctypes.c_uint8)
f.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_int)]
f.restype = ctypes.c_int
XnStreamUncompressConf4 = f
f = x.XnStreamCompressDepth16ZWithEmbTable
et = ctypes.POINTER(ctypes.c_uint8)
f.argtypes = [ctypes.POINTER(ctypes.c_uint16), ctypes.c_int, ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_int), ctypes.c_int]
f.restype = ctypes.c_int
XnStreamCompressDepth16ZWithEmbTable = f

def allocoutput16(n):
    return ctypes.create_string_buffer(n * 2)


def allocoutput8(n):
    return ctypes.create_string_buffer(n)


def doXnStreamUncompressConf4(input, outputbuffer):
    r = ctypes.c_int(len(outputbuffer))
    rr = XnStreamUncompressConf4(ctypes.c_char_p(input), len(input), ctypes.cast(outputbuffer, ctypes.POINTER(ctypes.c_uint8)), ctypes.byref(r))
    return (
     rr, r.value)


def doXnStreamUncompressImage8Z(input, outputbuffer):
    r = ctypes.c_int(len(outputbuffer))
    rr = XnStreamUncompressImage8Z(ctypes.c_char_p(input), len(input), ctypes.cast(outputbuffer, ctypes.POINTER(ctypes.c_uint8)), ctypes.byref(r))
    return (
     rr, r.value)


def doXnStreamUncompressDepth16ZWithEmbTable(input, outputbuffer):
    r = ctypes.c_int(len(outputbuffer))
    rr = XnStreamUncompressDepth16ZWithEmbTable(ctypes.c_char_p(input), len(input), ctypes.cast(outputbuffer, ctypes.POINTER(ctypes.c_uint16)), ctypes.byref(r))
    return (
     rr, r.value)


def doXnStreamCompressDepth16ZWithEmbTable(input, outputbuffer, maxvalue):
    r = ctypes.c_int(len(outputbuffer))
    rr = XnStreamCompressDepth16ZWithEmbTable(ctypes.cast(input, ctypes.POINTER(ctypes.c_uint16)), len(input), ctypes.cast(outputbuffer, ctypes.POINTER(ctypes.c_uint8)), ctypes.byref(r), maxvalue)
    return (
     rr, r.value)


def doXnStreamUncompressDepth16Z(input, outputbuffer):
    r = ctypes.c_int(len(outputbuffer))
    rr = XnStreamUncompressDepth16Z(ctypes.c_char_p(input), len(input), ctypes.cast(outputbuffer, ctypes.POINTER(ctypes.c_uint16)), ctypes.byref(r))
    return (
     rr, r.value)


if __name__ == '__main__':
    a = '1234'
    b = allocoutput16(123)
    print doXnStreamUncompressDepth16ZWithEmbTable(a, b)
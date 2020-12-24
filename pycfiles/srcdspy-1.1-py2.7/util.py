# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/srcdspy/util.py
# Compiled at: 2012-12-27 21:51:43
import struct

def unpack_byte(data):
    return (struct.unpack('<B', data[:1])[0], data[1:])


def unpack_short(data):
    return (
     struct.unpack('<h', data[:2])[0], data[2:])


def unpack_long(data):
    return (
     struct.unpack('<l', data[:4])[0], data[4:])


def unpack_longlong(data):
    return (
     struct.unpack('<Q', data[:8])[0], data[8:])


def unpack_float(data):
    return (
     struct.unpack('<f', data[:4])[0], data[4:])


def unpack_string(data):
    return data.split('\x00', 1)


def pack_byte(val):
    return struct.pack('<B', val)


def pack_short(val):
    return struct.pack('<h', val)


def pack_long(val):
    return struct.pack('<l', val)


def pack_float(val):
    return struct.pack('<f', val)


def pack_string(val):
    return val + '\x00'
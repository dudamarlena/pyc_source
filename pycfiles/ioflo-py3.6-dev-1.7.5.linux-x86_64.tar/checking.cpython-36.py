# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/aid/checking.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 2341 bytes
"""
checking.py utility functions for crc or chechsum type checking
"""
from __future__ import absolute_import, division, print_function
import sys, os, struct
from .sixing import *
from .consoling import getConsole
console = getConsole()

def crc16(inpkt):
    """ Returns 16 bit crc or inpkt packed binary string
        compatible with ANSI 709.1 and 852
        inpkt is bytes in python3 or str in python2
        needs struct module
    """
    inpkt = bytearray(inpkt)
    poly = 4129
    crc = 65535
    for element in inpkt:
        i = 0
        byte = element
        while i < 8:
            crcbit = 0
            if crc & 32768:
                crcbit = 1
            databit = 0
            if byte & 128:
                databit = 1
            crc = crc << 1
            crc = crc & 65535
            if crcbit != databit:
                crc = crc ^ poly
            byte = byte << 1
            byte = byte & 255
            i += 1

    crc = crc ^ 65535
    return struct.pack('!H', crc)


def crc64(inpkt):
    """ Returns 64 bit crc of inpkt binary packed string inpkt
        inpkt is bytes in python3 or str in python2
        returns tuple of two 32 bit numbers for top and bottom of 64 bit crc
    """
    inpkt = bytearray(inpkt)
    polytop = 1123082731
    polybot = 2850698899
    crctop = 4294967295
    crcbot = 4294967295
    for element in inpkt:
        i = 0
        byte = element
        while i < 8:
            topbit = 0
            if crctop & 2147483648:
                topbit = 1
            databit = 0
            if byte & 128:
                databit = 1
            crctop = crctop << 1
            crctop = crctop & 4294967295
            botbit = 0
            if crcbot & 2147483648:
                botbit = 1
            crctop = crctop | botbit
            crcbot = crcbot << 1
            crcbot = crcbot & 4294967295
            if topbit != databit:
                crctop = crctop ^ polytop
                crcbot = crcbot ^ polybot
            byte = byte << 1
            byte = byte & 255
            i += 1

    crctop = crctop ^ 4294967295
    crcbot = crcbot ^ 4294967295
    return (crctop, crcbot)
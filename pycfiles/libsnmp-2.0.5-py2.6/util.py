# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/libsnmp/util.py
# Compiled at: 2008-10-18 18:59:45


def octetsToHex(octets):
    """ convert a string of octets to a string of hex digits
    """
    result = ''
    while octets:
        byte = octets[0]
        octets = octets[1:]
        result += '%.2x' % ord(byte)

    return result


def octetsToOct(octets):
    """ convert a string of octets to a string of octal digits
    """
    result = ''
    while octets:
        byte = octets[0]
        octets = octets[1:]
        result += '%.4s,' % oct(ord(byte))

    return result
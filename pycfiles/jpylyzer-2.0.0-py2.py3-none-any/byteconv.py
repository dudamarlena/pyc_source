# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johan/jpylyzer/jpylyzer/byteconv.py
# Compiled at: 2019-10-08 11:09:01
"""Various functions for converting and manipulating bytes objects."""
import struct, binascii, unicodedata

def _doConv(bytestr, bOrder, formatCharacter):
    """Convert bytestr object of bOrder byteorder.

    Formatted using formatCharacter.
    Returns -9999 if struct.unpack raises an error
    """
    formatStr = bOrder + formatCharacter
    try:
        result = struct.unpack(formatStr, bytestr)[0]
    except:
        result = -9999

    return result


def bytesToULongLong(bytestring):
    """Unpack 8 byte string to unsigned long long integer.

    Assuming big-endian byte order.
    """
    return _doConv(bytestring, '>', 'Q')


def bytesToUInt(bytestring):
    """Unpack 4 byte string to unsigned integer.

    Assuming big-endian byte order.
    """
    return _doConv(bytestring, '>', 'I')


def bytesToUShortInt(bytestring):
    """Unpack 2 byte string to unsigned short integer.

    Assuming big-endian byte order.
    """
    return _doConv(bytestring, '>', 'H')


def bytesToUnsignedChar(bytestring):
    """Unpack 1 byte string to unsigned character/integer.

    Assuming big-endian byte order.
    """
    return _doConv(bytestring, '>', 'B')


def bytesToSignedChar(bytestring):
    """Unpack 1 byte string to signed character/integer.

    Assuming big-endian byte order.
    """
    return _doConv(bytestring, '>', 'b')


def bytesToInteger(bytestring):
    """Unpack byte string of any length to integer.

    Taken from:
    http://stackoverflow.com/questions/4358285/

    JvdK: what endianness is assumed here? Could go wrong on some systems?

    binascii.hexlify will be obsolete in python3 soon
    They will add a .tohex() method to bytes class
    Issue 3532 bugs.python.org
    """
    try:
        result = int(binascii.hexlify(bytestring), 16)
    except:
        result = -9999

    return result


def isctrl(c):
    """Return True if byte corresponds to device control character.

    (See also: http://www.w3schools.com/tags/ref_ascii.asp)
    """
    return ord(c) < 32 or ord(c) == 127


def bytesToHex(bytestring):
    """Return hexadecimal ascii representation of bytestring."""
    return binascii.hexlify(bytestring)


def containsControlCharacters(bytestring):
    """Return True if bytestring object contains control characters."""
    for i in range(len(bytestring)):
        if isctrl(bytestring[i:i + 1]):
            return True

    return False


def removeControlCharacters(string):
    """Remove control characters from string.

    Adapted from: http://stackoverflow.com/a/19016117/1209004
    """
    allowedChars = [
     '\t', '\n', '\r']
    return ('').join(ch for ch in string if unicodedata.category(ch)[0] != 'C' or ch in allowedChars)


def removeNullTerminator(bytestring):
    """Remove null terminator from bytestring."""
    bytesOut = bytestring.rstrip('\x00')
    return bytesOut


def bytesToText(bytestring):
    """Unpack byte object to text string, assuming big-endian byte order."""
    enc = 'utf-8'
    errorMode = 'strict'
    try:
        string = bytestring.decode(encoding=enc, errors=errorMode)
        result = removeControlCharacters(string)
    except:
        result = ''

    return result
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johan/isolyzer/isolyzer/byteconv.py
# Compiled at: 2018-01-25 10:48:37
"""Various conversion functions from bytes to other data types"""
import struct, binascii, unicodedata

def _doConv(bytestr, bOrder, formatCharacter):
    """Convert byte object of bOrder byteorder to format using formatCharacter
    Return -9999 if unpack raised an error
    """
    formatStr = bOrder + formatCharacter
    try:
        result = struct.unpack(formatStr, bytestr)[0]
    except:
        result = -9999

    return result


def swap32(i):
    """ Byte-swap 4 byte integer (Credit: http://stackoverflow.com/a/27506692)"""
    return struct.unpack('<I', struct.pack('>I', i))[0]


def bytesToULongLong(bytestring):
    """Unpack 8 byte string to unsigned long long integer, assuming big-endian
    byte order
    """
    return _doConv(bytestring, '>', 'Q')


def bytesToUInt(bytestring):
    """Unpack 4 byte string to unsigned integer, assuming big-endian byte order"""
    return _doConv(bytestring, '>', 'I')


def bytesToUShortInt(bytestring):
    """Unpack 2 byte string to unsigned short integer, assuming big-endian
    byte order
    """
    return _doConv(bytestring, '>', 'H')


def bytesToUnsignedChar(bytestring):
    """Unpack 1 byte string to unsigned character/integer, assuming big-endian
    byte order
    """
    return _doConv(bytestring, '>', 'B')


def bytesToSignedChar(bytestring):
    """Unpack 1 byte string to signed character/integer, assuming big-endian
    byte order
    """
    return _doConv(bytestring, '>', 'b')


def bytesToULongLongL(bytestring):
    """Unpack 8 byte string to unsigned long long integer, assuming little-endian
    byte order
    """
    return _doConv(bytestring, '<', 'Q')


def bytesToUIntL(bytestring):
    """Unpack 4 byte string to unsigned integer, assuming little-endian byte order"""
    return _doConv(bytestring, '<', 'I')


def bytesToUShortIntL(bytestring):
    """Unpack 2 byte string to unsigned short integer, assuming little-endian
    byte order
    """
    return _doConv(bytestring, '<', 'H')


def bytesToUnsignedCharL(bytestring):
    """Unpack 1 byte string to unsigned character/integer, assuming little-endian
    byte order
    """
    return _doConv(bytestring, '<', 'B')


def bytesToInteger(bytestring):
    """Unpack byte string of any length to integer"""
    try:
        result = int(binascii.hexlify(bytestring), 16)
    except:
        result = -9999

    return result


def isctrl(c):
    """Returns True if byte corresponds to device control character"""
    return ord(c) < 32 or ord(c) == 127


def bytesToHex(bytestring):
    """Return hexadecimal ascii representation of bytestring"""
    return binascii.hexlify(bytestring)


def containsControlCharacters(bytestring):
    """Returns True if bytestring object contains control characters"""
    for i in range(len(bytestring)):
        if isctrl(bytestring[i:i + 1]):
            return True

    return False


def removeControlCharacters(string):
    """Remove control characters from string"""
    allowedChars = [
     '\t', '\n', '\r']
    return ('').join(ch for ch in string if unicodedata.category(ch)[0] != 'C' or ch in allowedChars)


def removeNullTerminator(bytestring):
    """Remove null terminator from bytestring"""
    bytesOut = bytestring.rstrip('\x00')
    return bytesOut


def bytesToText(bytestring):
    """Unpack byte object to text string, assuming big-endian
    byte order
    """
    enc = 'utf-8'
    errorMode = 'ignore'
    try:
        string = bytestring.decode(encoding=enc, errors=errorMode)
        result = removeControlCharacters(string)
    except:
        result = ''

    return result
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\util\hexutil.py
# Compiled at: 2017-01-26 21:08:30
# Size of source mod 2**32: 1594 bytes
"""Miscellaneous utility routines relating to hex and byte strings"""
from binascii import a2b_hex, b2a_hex
from dicom import in_py3
from dicom.charset import default_encoding

def hex2bytes(hexstring):
    """Return bytestring for a string of hex bytes separated by whitespace

    This is useful for creating specific byte sequences for testing, using
    python's implied concatenation for strings with comments allowed.
    Example:
        hex_string = (
         "08 00 32 10"     # (0008, 1032) SQ "Procedure Code Sequence"
         " 08 00 00 00"    # length 8
         " fe ff 00 e0"    # (fffe, e000) Item Tag
        )
        byte_string = hex2bytes(hex_string)
    Note in the example that all lines except the first must start with a space,
    alternatively the space could end the previous line.
    """
    if isinstance(hexstring, bytes):
        return a2b_hex(hexstring.replace(b' ', b''))
    else:
        return a2b_hex(bytes(hexstring.replace(' ', ''), default_encoding))


def bytes2hex(byte_string):
    s = b2a_hex(byte_string)
    if in_py3:
        s = s.decode()
    return ' '.join(s[i:i + 2] for i in range(0, len(s), 2))
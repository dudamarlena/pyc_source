# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/Projects/chris/various/pdfminer/venv/lib/python2.7/site-packages/pdfminer/ascii85.py
# Compiled at: 2015-10-31 16:12:15
""" Python implementation of ASCII85/ASCIIHex decoder (Adobe version).

This code is in the public domain.

"""
import re, struct, six

def ascii85decode(data):
    """
    In ASCII85 encoding, every four bytes are encoded with five ASCII
    letters, using 85 different types of characters (as 256**4 < 85**5).
    When the length of the original bytes is not a multiple of 4, a special
    rule is used for round up.

    The Adobe's ASCII85 implementation is slightly different from
    its original in handling the last characters.

    """
    n = b = 0
    out = ''
    for i in six.iterbytes(data):
        c = six.int2byte(i)
        if '!' <= c and c <= 'u':
            n += 1
            b = b * 85 + (ord(c) - 33)
            if n == 5:
                out += struct.pack('>L', b)
                n = b = 0
        elif c == 'z':
            assert n == 0
            out += '\x00\x00\x00\x00'
        elif c == '~':
            if n:
                for _ in range(5 - n):
                    b = b * 85 + 84

                out += struct.pack('>L', b)[:n - 1]
            break

    return out


hex_re = re.compile('([a-f\\d]{2})', re.IGNORECASE)
trail_re = re.compile('^(?:[a-f\\d]{2}|\\s)*([a-f\\d])[\\s>]*$', re.IGNORECASE)

def asciihexdecode(data):
    """
    ASCIIHexDecode filter: PDFReference v1.4 section 3.3.1
    For each pair of ASCII hexadecimal digits (0-9 and A-F or a-f), the
    ASCIIHexDecode filter produces one byte of binary data. All white-space
    characters are ignored. A right angle bracket character (>) indicates
    EOD. Any other characters will cause an error. If the filter encounters
    the EOD marker after reading an odd number of hexadecimal digits, it
    will behave as if a 0 followed the last digit.
    """

    def decode(x):
        i = int(x, 16)
        return six.int2byte(i)

    out = ''
    for x in hex_re.findall(data):
        out += decode(x)

    m = trail_re.search(data)
    if m:
        out += decode(m.group(1) + '0')
    return out
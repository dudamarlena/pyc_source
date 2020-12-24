# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Haibin\AppData\Local\Temp\pip-build-8dr99z6a\segpy\segpy\encoding.py
# Compiled at: 2017-02-16 13:30:25
# Size of source mod 2**32: 1970 bytes
ASCII = 'ascii'
EBCDIC = 'cp037'
SUPPORTED_ENCODINGS = (
 ASCII, EBCDIC)

class UnsupportedEncodingError(Exception):

    def __init__(self, text, encoding):
        self._encoding = encoding
        super(UnsupportedEncodingError, self).__init__(text)

    @property
    def encoding(self):
        return self._encoding

    def __str__(self):
        return '{} not supported for encoding {}'.format(self.args[0], self._encoding)

    def __repr__(self):
        return '{}({!r}, {!r}'.format(self.__class__.__name__, self.args[0], self._encoding)


def is_supported_encoding(encoding):
    return encoding in SUPPORTED_ENCODINGS


COMMON_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789:_- '
COMMON_EBCDIC_CHARS = set(COMMON_CHARS.encode(EBCDIC))
COMMON_ASCII_CHARS = set(COMMON_CHARS.encode(ASCII))

def guess_encoding(bs, threshold=0.5):
    """Try to determine whether the encoding of byte stream b is an ASCII string or an EBCDIC string.

    Args:
        bs: A byte string (Python 2 - str; Python 3 - bytes)

    Returns:
        A string which can be used with the Python encoding functions: 'cp037' for EBCDIC, 'ascii' for ASCII or None
        if neither.
    """
    ebcdic_count = 0
    ascii_count = 0
    null_count = 0
    count = 0
    for b in bs:
        if b in COMMON_EBCDIC_CHARS:
            ebcdic_count += 1
        if b in COMMON_ASCII_CHARS:
            ascii_count += 1
        if b == 0:
            null_count += 1
        count += 1

    if count == 0:
        return
    ebcdic_freq = ebcdic_count / count
    ascii_freq = ascii_count / count
    null_freq = null_count / count
    if null_freq == 1.0:
        return ASCII
    if ebcdic_freq < threshold and ascii_freq >= threshold:
        return ASCII
    if ebcdic_freq >= threshold and ascii_freq < threshold:
        return EBCDIC
    if ebcdic_freq < threshold and ascii_freq < threshold:
        return
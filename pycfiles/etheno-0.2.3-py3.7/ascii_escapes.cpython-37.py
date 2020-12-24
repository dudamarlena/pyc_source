# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/etheno/ascii_escapes.py
# Compiled at: 2019-06-27 23:49:12
# Size of source mod 2**32: 3024 bytes
CONTROL_CODES = {b'0':b'\x00',  b'a':b'\x07', 
 b'b':b'\x08', 
 b'f':b'\x0c', 
 b'n':b'\n', 
 b'r':b'\r', 
 b't':b'\t', 
 b'v':b'\x0b', 
 b'"':b'"', 
 b'&':b'', 
 b"'":b"'", 
 b'\\':b'\\', 
 b'NUL':b'\x00', 
 b'SOH':b'\x01', 
 b'STX':b'\x02', 
 b'ETX':b'\x03', 
 b'EOT':b'\x04', 
 b'ENQ':b'\x05', 
 b'ACK':b'\x06', 
 b'BEL':b'\x07', 
 b'BS':b'\x08', 
 b'HT':b'\t', 
 b'LF':b'\n', 
 b'VT':b'\x0b', 
 b'FF':b'\x0c', 
 b'CR':b'\r', 
 b'SO':b'\x0e', 
 b'SI':b'\x0f', 
 b'DLE':b'\x10', 
 b'DC1':b'\x11', 
 b'DC2':b'\x12', 
 b'DC3':b'\x13', 
 b'DC4':b'\x14', 
 b'NAK':b'\x15', 
 b'SYN':b'\x16', 
 b'ETB':b'\x17', 
 b'CAN':b'\x18', 
 b'EM':b'\x19', 
 b'SUB':b'\x1a', 
 b'ESC':b'\x1b', 
 b'FS':b'\x1c', 
 b'GS':b'\x1d', 
 b'RS':b'\x1e', 
 b'US':b'\x1f', 
 b'SP':b' ', 
 b'DEL':b'\x7f', 
 b'^@':b'\x00', 
 b'^[':b'\x1b', 
 b'^\\':b'\x1c', 
 b'^]':b'\x1d', 
 b'^^':b'\x1e', 
 b'^_':b'\x1f'}
for i in range(26):
    CONTROL_CODES[bytes([ord('^'), ord('A') + i])] = bytes([i + 1])

def decode(text):
    escaped = None
    ret = b''
    for c in text:
        if isinstance(c, str):
            c = ord(c)
        c = bytes([c])
        if escaped is not None:
            escaped += c
            if escaped in CONTROL_CODES:
                ret += CONTROL_CODES[escaped]
                escaped = None
            elif len(escaped) >= 3:
                if len(escaped) == 3:
                    try:
                        value = int(escaped)
                        if value >= 0:
                            if value <= 255:
                                ret += bytes([value])
                                escaped = None
                                continue
                    except Exception:
                        pass

                raise ValueError("Unknown escape sequence '\\%s'" % escaped)
            else:
                if c == b'\\':
                    escaped = b''
        else:
            ret += c

    return ret
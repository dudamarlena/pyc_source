# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Mydemos_pkg\unicodeconvert.py
# Compiled at: 2020-05-04 09:17:41
# Size of source mod 2**32: 1175 bytes
r"""
A unicodeconvert for demo.
USAGE:
'''do you want to print idle a smily face(emoji)?maybe u tried this:
print('\U0001F600')
but you got this:
Traceback (most recent call last):
  File "<pyshell#29>", line 1, in <module>
    print('\U0001F600')
UnicodeEncodeError: 'UCS-2' codec can't encode character '\U0001f600' in position 0: Non-BMP character not supported in Tk
>>>
'''
#try this:
nonBMPtoBMP('😀')
ok,have fun!
"""

class UnicodeConvertError(BaseException):
    pass


def nonBMPtoBMP_e(up):
    u = ord(up)
    vc = u - 65536
    vh = (vc & 1047552) >> 10
    vl = vc & 1023
    w1 = 55296
    w2 = 56320
    w1 = w1 | vh
    w2 = w2 | vl
    return chr(w1) + chr(w2)


import unicodedata

def UnicodetoASCII(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')


def ASCIItoUnicode(s):
    return chr(ord(s))


def nonBMPtoBMP(up):
    u = ord(up)
    if u <= 65535:
        raise UnicodeConvertError("The arg shouldn't be lesser than 0x10000.")
    else:
        return nonBMPtoBMP_e(up)


def toUTF16(u):
    if u <= 65535:
        return u
    return nonBMPtoBMP_e(u)
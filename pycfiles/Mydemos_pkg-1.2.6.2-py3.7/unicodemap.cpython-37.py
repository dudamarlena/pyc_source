# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Mydemos_pkg\unicodemap.py
# Compiled at: 2020-05-04 09:20:44
# Size of source mod 2**32: 658 bytes
"""
do you want ａ to a or a to ａ?try:
HalfToFullWidth('a')
!!!!!!!!!!!!!

"""
HTFW = 65248

def HalfToFullWidth(s):
    """
    This is for like 'ａ'to'a'.
    """
    try:
        try:
            sn = ord(s) + HTFW
            temptp_1_1 = chr(sn)
        except:
            raise UnicodeEncodeError('this is not a fullwidth alpha.')

    finally:
        pass

    return chr(sn)


def FullToHalfWidth(s):
    """
    This is for like 'a'to'ａ'.
    """
    try:
        try:
            sn = ord(s) - HTFW
            temptp_1_1 = chr(sn)
        except:
            raise UnicodeEncodeError('this is not a fullwidth alpha.')

    finally:
        pass

    return chr(sn)
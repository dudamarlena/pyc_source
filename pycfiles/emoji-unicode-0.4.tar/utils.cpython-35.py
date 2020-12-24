# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/esteban/PycharmProjects/emoji-unicode/emoji_unicode/utils.py
# Compiled at: 2015-11-18 15:40:45
# Size of source mod 2**32: 305 bytes
from __future__ import unicode_literals

def code_point_to_unicode(code_point):
    try:
        return unichr(int(code_point, 16))
    except NameError:
        return chr(int(code_point, 16))


def unicode_to_code_point(uni_char):
    return format(ord(uni_char), 'x').lower()
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/idohyeon/Projects/motty/app/utils.py
# Compiled at: 2017-11-13 00:12:09
# Size of source mod 2**32: 91 bytes


def remove_last_slash(txt):
    if txt[(len(txt) - 1)] == '/':
        return txt[0:len(txt) - 1]
    else:
        return txt
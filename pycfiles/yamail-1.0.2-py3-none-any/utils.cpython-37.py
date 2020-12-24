# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/didi/PycharmProjects/nnmail/yamail/utils.py
# Compiled at: 2018-06-18 13:03:30
# Size of source mod 2**32: 344 bytes
import os

class raw(str):
    __doc__ = " Ensure that a string is treated as text and will not receive 'magic'. "


class inline(str):
    __doc__ = ' Only needed when wanting to inline an image rather than attach it '


def find_user_home_path():
    with open(os.path.expanduser('~/.yagmail')) as (f):
        return f.read().strip()
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tamell/code/pyteslaapi/pyteslaapi/exceptions.py
# Compiled at: 2018-11-02 14:47:36
# Size of source mod 2**32: 812 bytes


class TeslaException(Exception):

    def __init__(self, code, *args, **kwargs):
        self.message = ''
        (super().__init__)(*args, **kwargs)
        self.code = code
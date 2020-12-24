# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: puke/Std.py
# Compiled at: 2012-01-03 06:28:43


class Std:

    def __init__(self, out='', err='', code=0):
        self.out = out
        self.err = err
        self.code = code

    def set(self, out, err, code=0):
        self.out = out
        self.err = err
        self.code = code

    def __repr__(self):
        return 'Stdout : %s\n\nStdErr : %s\n' % (self.out, self.err, self.code)

    def __str__(self):
        return self.__repr__()
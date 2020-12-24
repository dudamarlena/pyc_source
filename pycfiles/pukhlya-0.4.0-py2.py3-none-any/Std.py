# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
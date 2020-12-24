# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/scox/dev/grayson/venv/lib/python2.7/site-packages/grayson/compiler/exception.py
# Compiled at: 2012-03-02 14:59:52


class GraysonCompilerException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class CycleException(GraysonCompilerException):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class SyntaxError(GraysonCompilerException):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class CompositeError(GraysonCompilerException):

    def __init__(self, values):
        self.values = values

    def __str__(self):
        buffer = []
        for val in self.values:
            buffer.append(val.__str__())

        return ('\n').join(buffer)
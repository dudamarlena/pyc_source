# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/psqlparse/exceptions.py
# Compiled at: 2016-11-16 22:08:56
# Size of source mod 2**32: 279 bytes
import six

@six.python_2_unicode_compatible
class PSqlParseError(Exception):

    def __init__(self, message, lineno, cursorpos):
        self.message = message
        self.lineno = lineno
        self.cursorpos = cursorpos

    def __str__(self):
        return self.message
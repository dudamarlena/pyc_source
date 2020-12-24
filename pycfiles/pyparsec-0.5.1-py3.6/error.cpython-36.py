# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/parsec/error.py
# Compiled at: 2015-07-18 05:50:49
# Size of source mod 2**32: 441 bytes


class ParsecError(Exception):

    def __init__(self, state, message):
        self.index = state.index
        self.message = message

    def __str__(self):
        return 'Error at {0}: {1}'.format(self.index, self.message)


class ParsecEof(ParsecError):

    def __init__(self, state):
        ParsecError.__init__(self, state, 'eof')
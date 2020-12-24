# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/rply/rply/errors.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 1035 bytes


class ParserGeneratorError(Exception):
    pass


class LexingError(Exception):
    __doc__ = '\n    Raised by a Lexer, if no rule matches.\n    '

    def __init__(self, message, source_pos):
        self.message = message
        self.source_pos = source_pos

    def getsourcepos(self):
        """
        Returns the position in the source, at which this error occurred.
        """
        return self.source_pos

    def __repr__(self):
        return 'LexingError(%r, %r)' % (self.message, self.source_pos)


class ParsingError(Exception):
    __doc__ = '\n    Raised by a Parser, if no production rule can be applied.\n    '

    def __init__(self, message, source_pos):
        self.message = message
        self.source_pos = source_pos

    def getsourcepos(self):
        """
        Returns the position in the source, at which this error occurred.
        """
        return self.source_pos

    def __repr__(self):
        return 'ParsingError(%r, %r)' % (self.message, self.source_pos)


class ParserGeneratorWarning(Warning):
    pass
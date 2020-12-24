# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\geoffrey\workspace\python-plex\build\lib\plex\errors.py
# Compiled at: 2018-02-04 13:37:17
# Size of source mod 2**32: 1048 bytes
"""
Python Lexical Analyser

Exception classes
"""

class PlexError(Exception):
    message = ''


class PlexTypeError(PlexError, TypeError):
    pass


class PlexValueError(PlexError, ValueError):
    pass


class InvalidRegex(PlexError):
    pass


class InvalidToken(PlexError):

    def __init__(self, token_number, message):
        PlexError.__init__(self, 'Token number %d: %s' % (
         token_number, message))


class InvalidScanner(PlexError):
    pass


class AmbiguousAction(PlexError):
    message = 'Two tokens with different actions can match the same string'

    def __init__(self):
        pass


class UnrecognizedInput(PlexError):
    scanner = None
    position = None
    state_name = None

    def __init__(self, scanner, state_name):
        self.scanner = scanner
        self.position = scanner.position()
        self.state_name = state_name

    def __str__(self):
        return "'%s', line %d, char %d: Token not recognised in state %s" % (self.position + (repr(self.state_name),))
# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: c:\users\geoffrey\workspace\python-plex\build\lib\plex\errors.py
# Compiled at: 2018-02-04 13:37:17
# Size of source mod 2**32: 1048 bytes
__doc__ = '\nPython Lexical Analyser\n\nException classes\n'

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
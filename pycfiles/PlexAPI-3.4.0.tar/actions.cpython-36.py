# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: c:\users\geoffrey\workspace\python-plex\build\lib\plex\actions.py
# Compiled at: 2018-02-04 13:21:25
# Size of source mod 2**32: 2347 bytes
__doc__ = '\nPython Lexical Analyser\n\nActions for use in token specifications\n'

class Action:

    def same_as(self, other):
        return self is other


class Return(Action):
    """Return"""
    value = None

    def __init__(self, value):
        self.value = value

    def perform(self, token_stream, text):
        return self.value

    def same_as(self, other):
        return isinstance(other, Return) and self.value == other.value

    def __repr__(self):
        return 'Return(%s)' % repr(self.value)


class Call(Action):
    """Call"""
    function = None

    def __init__(self, function):
        self.function = function

    def perform(self, token_stream, text):
        return self.function(token_stream, text)

    def __repr__(self):
        return 'Call(%s)' % self.function.__name__

    def same_as(self, other):
        return isinstance(other, Call) and self.function is other.function


class Begin(Action):
    """Begin"""
    state_name = None

    def __init__(self, state_name):
        self.state_name = state_name

    def perform(self, token_stream, text):
        token_stream.begin(self.state_name)

    def __repr__(self):
        return 'Begin(%s)' % self.state_name

    def same_as(self, other):
        return isinstance(other, Begin) and self.state_name == other.state_name


class Ignore(Action):
    """Ignore"""

    def perform(self, token_stream, text):
        pass

    def __repr__(self):
        return 'IGNORE'


IGNORE = Ignore()
IGNORE.__doc__ = Ignore.__doc__

class Text(Action):
    """Text"""

    def perform(self, token_stream, text):
        return text

    def __repr__(self):
        return 'TEXT'


TEXT = Text()
TEXT.__doc__ = Text.__doc__
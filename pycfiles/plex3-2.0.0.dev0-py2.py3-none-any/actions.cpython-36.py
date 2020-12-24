# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\geoffrey\workspace\python-plex\build\lib\plex\actions.py
# Compiled at: 2018-02-04 13:21:25
# Size of source mod 2**32: 2347 bytes
"""
Python Lexical Analyser

Actions for use in token specifications
"""

class Action:

    def same_as(self, other):
        return self is other


class Return(Action):
    __doc__ = '\n    Internal Plex action which causes |value| to\n    be returned as the value of the associated token\n    '
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
    __doc__ = '\n    Internal Plex action which causes a function to be called.\n    '
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
    __doc__ = '\n    Begin(state_name) is a Plex action which causes the Scanner to\n    enter the state |state_name|. See the docstring of Plex.Lexicon\n    for more information.\n    '
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
    __doc__ = '\n    IGNORE is a Plex action which causes its associated token\n    to be ignored. See the docstring of Plex.Lexicon  for more\n    information.\n    '

    def perform(self, token_stream, text):
        pass

    def __repr__(self):
        return 'IGNORE'


IGNORE = Ignore()
IGNORE.__doc__ = Ignore.__doc__

class Text(Action):
    __doc__ = '\n    TEXT is a Plex action which causes the text of a token to\n    be returned as the value of the token. See the docstring of\n    Plex.Lexicon  for more information.\n    '

    def perform(self, token_stream, text):
        return text

    def __repr__(self):
        return 'TEXT'


TEXT = Text()
TEXT.__doc__ = Text.__doc__
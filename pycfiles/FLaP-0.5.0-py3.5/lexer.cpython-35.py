# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\flap\latex\lexer.py
# Compiled at: 2016-12-16 08:56:53
# Size of source mod 2**32: 5526 bytes
from flap.latex.commons import Stream, Position
from flap.latex.tokens import TokenFactory

class Lexer:
    __doc__ = '\n    Scan a stream of character and yields a stream of token. The lexer shall define handler for each category of symbols.\n    These handlers are automatically selected using reflection: each handler shall be named "_read_category".\n    '

    def __init__(self, symbols, source):
        self._source = source
        self._symbols = symbols
        self._tokens = TokenFactory(self._symbols)
        self._reset()

    def _reset(self):
        self._position = Position(1, 0, self._source.name)
        self._input = Stream(iter(self._source.content), self._on_take)

    def _on_take(self, character):
        if character in self._symbols.NEW_LINE:
            self._position = self._position.next_line()
        else:
            self._position = self._position.next_character()

    @property
    def position(self):
        return self._position

    def _take(self):
        return self._input.take()

    @property
    def _next(self):
        return self._input.look_ahead()

    def __iter__(self):
        return self

    def __next__(self):
        if self._next is None:
            raise StopIteration()
        return self._one_token()

    def _one_token(self):
        handler = self._handler_for(self._symbols.category_of(self._next))
        return handler()

    def _handler_for(self, category):
        handler_name = '_read_' + category.name.lower()
        handler = getattr(self, handler_name)
        assert handler, "Lexer has no handler for '%s' symbols" % category.name
        return handler

    def _read_character(self):
        character = self._take()
        return self._tokens.character(self._position, character)

    def _read_control(self):
        marker = self._take()
        location = self._position
        assert marker in self._symbols.CONTROL
        if self._next not in self._symbols.CHARACTER:
            name = self._take()
        else:
            name = self._take_while(lambda c: c in self._symbols.CHARACTER)
        return self._tokens.command(location, marker + name)

    def _take_while(self, predicate):
        return ''.join(self._input.take_while(predicate))

    def _read_comment(self):
        marker = self._input.take()
        location = self._position
        assert marker in self._symbols.COMMENT
        text = self._take_while(lambda c: c not in self._symbols.NEW_LINE)
        return self._tokens.comment(location, marker + text)

    def _read_white_spaces(self):
        marker = self._input.take()
        location = self._position
        spaces = self._take_while(lambda c: c in self._symbols.WHITE_SPACES)
        return self._tokens.white_space(location, marker + spaces)

    def _read_new_line(self):
        marker = self._input.take()
        location = self._position
        assert marker in self._symbols.NEW_LINE
        return self._tokens.new_line(location, marker)

    def _read_begin_group(self):
        marker = self._input.take()
        location = self._position
        assert marker in self._symbols.BEGIN_GROUP
        return self._tokens.begin_group(location, marker)

    def _read_end_group(self):
        marker = self._take()
        location = self._position
        assert marker in self._symbols.END_GROUP
        return self._tokens.end_group(location, marker)

    def _read_parameter(self):
        marker = self._input.take()
        location = self._position
        assert marker in self._symbols.PARAMETER
        text = marker + self._take_while(lambda c: c.isdigit())
        return self._tokens.parameter(location, text)

    def _read_math(self):
        marker = self._input.take()
        location = self._position
        assert marker in self._symbols.MATH
        return self._tokens.math(location)

    def _read_superscript(self):
        marker = self._input.take()
        location = self._position
        assert marker in self._symbols.SUPERSCRIPT
        return self._tokens.superscript(location, marker)

    def _read_subscript(self):
        marker = self._input.take()
        location = self._position
        assert marker in self._symbols.SUBSCRIPT
        return self._tokens.subscript(location, marker)

    def _read_non_breaking_space(self):
        marker = self._input.take()
        location = self._position
        assert marker in self._symbols.NON_BREAKING_SPACE
        return self._tokens.non_breaking_space(location, marker)

    def _read_others(self):
        marker = self._input.take()
        location = self._position
        return self._tokens.others(location, marker)
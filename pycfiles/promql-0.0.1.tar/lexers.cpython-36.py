# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/layout/lexers.py
# Compiled at: 2019-08-15 23:53:39
# Size of source mod 2**32: 11338 bytes
__doc__ = '\nLexer interface and implementation.\nUsed for syntax highlighting.\n'
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from six import with_metaclass
from six.moves import range
from prompt_tool_kit.token import Token
from prompt_tool_kit.filters import to_cli_filter
from .utils import split_lines
import re, six
__all__ = ('Lexer', 'SimpleLexer', 'PygmentsLexer', 'SyntaxSync', 'SyncFromStart',
           'RegexSync')

class Lexer(with_metaclass(ABCMeta, object)):
    """Lexer"""

    @abstractmethod
    def lex_document(self, cli, document):
        """
        Takes a :class:`~prompt_tool_kit.document.Document` and returns a
        callable that takes a line number and returns the tokens for that line.
        """
        pass


class SimpleLexer(Lexer):
    """SimpleLexer"""

    def __init__(self, token=Token, default_token=None):
        self.token = token
        if default_token is not None:
            self.token = default_token

    def lex_document(self, cli, document):
        lines = document.lines

        def get_line(lineno):
            try:
                return [
                 (
                  self.token, lines[lineno])]
            except IndexError:
                return []

        return get_line


class SyntaxSync(with_metaclass(ABCMeta, object)):
    """SyntaxSync"""

    @abstractmethod
    def get_sync_start_position(self, document, lineno):
        """
        Return the position from where we can start lexing as a (row, column)
        tuple.

        :param document: `Document` instance that contains all the lines.
        :param lineno: The line that we want to highlight. (We need to return
            this line, or an earlier position.)
        """
        pass


class SyncFromStart(SyntaxSync):
    """SyncFromStart"""

    def get_sync_start_position(self, document, lineno):
        return (0, 0)


class RegexSync(SyntaxSync):
    """RegexSync"""
    MAX_BACKWARDS = 500
    FROM_START_IF_NO_SYNC_POS_FOUND = 100

    def __init__(self, pattern):
        assert isinstance(pattern, six.text_type)
        self._compiled_pattern = re.compile(pattern)

    def get_sync_start_position(self, document, lineno):
        """ Scan backwards, and find a possible position to start. """
        pattern = self._compiled_pattern
        lines = document.lines
        for i in range(lineno, max(-1, lineno - self.MAX_BACKWARDS), -1):
            match = pattern.match(lines[i])
            if match:
                return (i, match.start())

        if lineno < self.FROM_START_IF_NO_SYNC_POS_FOUND:
            return (0, 0)
        else:
            return (
             lineno, 0)

    @classmethod
    def from_pygments_lexer_cls(cls, lexer_cls):
        """
        Create a :class:`.RegexSync` instance for this Pygments lexer class.
        """
        patterns = {'Python':'^\\s*(class|def)\\s+', 
         'Python 3':'^\\s*(class|def)\\s+', 
         'HTML':'<[/a-zA-Z]', 
         'JavaScript':'\\bfunction\\b'}
        p = patterns.get(lexer_cls.name, '^')
        return cls(p)


class PygmentsLexer(Lexer):
    """PygmentsLexer"""
    MIN_LINES_BACKWARDS = 50
    REUSE_GENERATOR_MAX_DISTANCE = 100

    def __init__(self, pygments_lexer_cls, sync_from_start=True, syntax_sync=None):
        if not syntax_sync is None:
            if not isinstance(syntax_sync, SyntaxSync):
                raise AssertionError
        self.pygments_lexer_cls = pygments_lexer_cls
        self.sync_from_start = to_cli_filter(sync_from_start)
        self.pygments_lexer = pygments_lexer_cls(stripnl=False,
          stripall=False,
          ensurenl=False)
        self.syntax_sync = syntax_sync or RegexSync.from_pygments_lexer_cls(pygments_lexer_cls)

    @classmethod
    def from_filename(cls, filename, sync_from_start=True):
        """
        Create a `Lexer` from a filename.
        """
        from pygments.util import ClassNotFound
        from pygments.lexers import get_lexer_for_filename
        try:
            pygments_lexer = get_lexer_for_filename(filename)
        except ClassNotFound:
            return SimpleLexer()
        else:
            return cls((pygments_lexer.__class__), sync_from_start=sync_from_start)

    def lex_document(self, cli, document):
        """
        Create a lexer function that takes a line number and returns the list
        of (Token, text) tuples as the Pygments lexer returns for that line.
        """
        cache = {}
        line_generators = {}

        def get_syntax_sync():
            if self.sync_from_start(cli):
                return SyncFromStart()
            else:
                return self.syntax_sync

        def find_closest_generator(i):
            for generator, lineno in line_generators.items():
                if lineno < i:
                    if i - lineno < self.REUSE_GENERATOR_MAX_DISTANCE:
                        return generator

        def create_line_generator(start_lineno, column=0):
            """
            Create a generator that yields the lexed lines.
            Each iteration it yields a (line_number, [(token, text), ...]) tuple.
            """

            def get_tokens():
                text = '\n'.join(document.lines[start_lineno:])[column:]
                for _, t, v in self.pygments_lexer.get_tokens_unprocessed(text):
                    yield (
                     t, v)

            return enumerate(split_lines(get_tokens()), start_lineno)

        def get_generator(i):
            generator = find_closest_generator(i)
            if generator:
                return generator
            else:
                i = max(0, i - self.MIN_LINES_BACKWARDS)
                if i == 0:
                    row = 0
                    column = 0
                else:
                    row, column = get_syntax_sync().get_sync_start_position(document, i)
            generator = find_closest_generator(i)
            if generator:
                return generator
            else:
                generator = create_line_generator(row, column)
                if column:
                    next(generator)
                    row += 1
                line_generators[generator] = row
                return generator

        def get_line(i):
            try:
                return cache[i]
            except KeyError:
                generator = get_generator(i)
                for num, line in generator:
                    cache[num] = line
                    if num == i:
                        line_generators[generator] = i
                        if num + 1 in cache:
                            del cache[num + 1]
                        return cache[num]

            return []

        return get_line
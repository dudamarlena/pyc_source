# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/rply/rply/lexergenerator.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 3208 bytes
import re
try:
    import rpython
    from rpython.rlib.objectmodel import we_are_translated
    from rpython.rlib.rsre import rsre_core
    from rpython.rlib.rsre.rpy import get_code
except ImportError:
    rpython = None

    def we_are_translated():
        return False


from rply.lexer import Lexer

class Rule(object):
    _attrs_ = [
     'name', 'flags', '_pattern']

    def __init__(self, name, pattern, flags=0):
        self.name = name
        self.re = re.compile(pattern, flags=flags)
        if rpython:
            self.flags = flags
            self._pattern = get_code(pattern, flags)

    def _freeze_(self):
        return True

    def matches(self, s, pos):
        if not we_are_translated():
            m = self.re.match(s, pos)
            if m is not None:
                return Match(*m.span(0))
            return
        else:
            assert pos >= 0
            ctx = rsre_core.StrMatchContext(s, pos, len(s), self.flags)
            matched = rsre_core.match_context(ctx, self._pattern)
            if matched:
                return Match(ctx.match_start, ctx.match_end)
            return


class Match(object):
    _attrs_ = [
     'start', 'end']

    def __init__(self, start, end):
        self.start = start
        self.end = end


class LexerGenerator(object):
    __doc__ = "\n    A LexerGenerator represents a set of rules that match pieces of text that\n    should either be turned into tokens or ignored by the lexer.\n\n    Rules are added using the :meth:`add` and :meth:`ignore` methods:\n\n    >>> from rply import LexerGenerator\n    >>> lg = LexerGenerator()\n    >>> lg.add('NUMBER', r'\\d+')\n    >>> lg.add('ADD', r'\\+')\n    >>> lg.ignore(r'\\s+')\n\n    The rules are passed to :func:`re.compile`. If you need additional flags,\n    e.g. :const:`re.DOTALL`, you can pass them to :meth:`add` and\n    :meth:`ignore` as an additional optional parameter:\n\n    >>> import re\n    >>> lg.add('ALL', r'.*', flags=re.DOTALL)\n\n    You can then build a lexer with which you can lex a string to produce an\n    iterator yielding tokens:\n\n    >>> lexer = lg.build()\n    >>> iterator = lexer.lex('1 + 1')\n    >>> iterator.next()\n    Token('NUMBER', '1')\n    >>> iterator.next()\n    Token('ADD', '+')\n    >>> iterator.next()\n    Token('NUMBER', '1')\n    >>> iterator.next()\n    Traceback (most recent call last):\n    ...\n    StopIteration\n    "

    def __init__(self):
        self.rules = []
        self.ignore_rules = []

    def add(self, name, pattern, flags=0):
        """
        Adds a rule with the given `name` and `pattern`. In case of ambiguity,
        the first rule added wins.
        """
        self.rules.append(Rule(name, pattern, flags=flags))

    def ignore(self, pattern, flags=0):
        """
        Adds a rule whose matched value will be ignored. Ignored rules will be
        matched before regular ones.
        """
        self.ignore_rules.append(Rule('', pattern, flags=flags))

    def build(self):
        """
        Returns a lexer instance, which provides a `lex` method that must be
        called with a string and returns an iterator yielding
        :class:`~rply.Token` instances.
        """
        return Lexer(self.rules, self.ignore_rules)
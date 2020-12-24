# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/modgrammar/extras.py
# Compiled at: 2012-11-11 04:35:00
import re
from modgrammar import Terminal, GrammarClass, OPTIONAL, WORD
from modgrammar import util
__all__ = [
 'QuotedString', 'Integer', 'PositiveInteger', 'RE']

def RE(regexp, **kwargs):
    cdict = util.make_classdict(REGrammar, (), kwargs, regexp=regexp)
    return GrammarClass('<RE>', (REGrammar,), cdict)


_recaret_re = re.compile('(^|[^[])\\^')

class REGrammar(Terminal):
    regexp = None

    @classmethod
    def __class_init__(cls, attrs):
        if isinstance(cls.regexp, str):
            cls.regexp = re.compile(cls.regexp, re.MULTILINE)
        if cls.regexp and _recaret_re.search(cls.regexp.pattern):
            cls.boltest = True
        else:
            cls.boltest = False
        if 'grammar_name' not in attrs:
            if cls.regexp is not None:
                cls.grammar_name = ('RE({0!r})').format(cls.regexp.pattern)
            else:
                cls.grammar_name = None
        return

    @classmethod
    def grammar_parse(cls, text, index, sessiondata):
        while True:
            string = text.string
            if index == 0 and cls.boltest and not text.bol:
                string = ' ' + string
                index = 1
            m = cls.regexp.match(string, index)
            if not m:
                break
            end = m.end()
            if end < len(string) or text.eof:
                yield (
                 end - index, cls(string[index:end]))
                break
            else:
                text = yield (None, None)

        yield util.error_result(index, cls)
        return

    @classmethod
    def grammar_ebnf_lhs(cls, opts):
        return (util.ebnf_specialseq(cls, opts), ())

    @classmethod
    def grammar_ebnf_rhs(cls, opts):
        return


class QuotedString(Terminal):
    grammar_desc = 'quoted string'
    quote_char = "'"
    newline_ok = False

    @classmethod
    def __class_init__(cls, attrs):
        if cls.newline_ok:
            regexp = '([^' + cls.quote_char + '\\\\]+|\\\\.)*'
        else:
            regexp = '([^' + cls.quote_char + '\\n\\\\]+|\\\\.)*'
        cls.grammar = util.regularize((cls.quote_char, RE(regexp), cls.quote_char))
        cls.grammar_min = len(cls.grammar)
        cls.grammar_max = len(cls.grammar)

    def elem_init(self, sessiondata):
        contents = self.elements[1].string
        self.value = re.sub('\\\\(.)', '\\1', contents)

    def __repr__(self):
        return ('{0.__class__.__name__}<{0.string}>').format(self)


class Integer(Terminal):
    grammar = (
     OPTIONAL('-'), WORD('0-9'))

    def elem_init(self, sessiondata):
        self.value = int(self.string)


class PositiveInteger(Integer):
    grammar = WORD('0-9')
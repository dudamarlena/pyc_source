# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/couchfti/query.py
# Compiled at: 2010-01-19 08:32:18
"""
FTI query string tokenizer/untokenizer.
"""
from pyparsing import CharsNotIn, Group, oneOf, Optional, QuotedString, Suppress, White, Word, ZeroOrMore, FollowedBy
_control_chars = ' !"$%^&*()-=+[]{};\'#:@~,./<>?'
_operators = '= < > <= >= != ~ =* *='
_safe_word = CharsNotIn(_control_chars) + ~FollowedBy(oneOf(_operators))
_field_name = Word('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_')
_field_value = _safe_word | QuotedString('"')
_field = Group(_field_name + oneOf(_operators) + _field_value).setResultsName('field')
_term = Group(_safe_word | QuotedString('"')).setResultsName('term')
_order = Group('{' + Optional('-') + _field_name + '}').setResultsName('order')
_query = Optional(_term | _field | _order) + ZeroOrMore(Suppress(White()) + (_term | _field | _order))
_parser = _query.parseString

def tokenize(q):
    """
    Tokenize a query string into a sequence of (type, data) tuples where type
    and data are one of the following:

        'term', <term text>
        'field', (<name>, <operator>, <value>)
        'order', <name>, <ascending>
    """

    def gen():
        if not isinstance(q, unicode):
            raise TypeError("'q' must be unicode")
        for i in _parser(q):
            if i.getName() == 'term':
                yield (
                 'term', i[0])
            elif i.getName() == 'field':
                yield (
                 'field', tuple(i))
            elif i.getName() == 'order':
                if i[1] == '-':
                    yield (
                     'order', (i[2], False))
                else:
                    yield (
                     'order', (i[1], True))

    if not q:
        return []
    return list(gen())


def untokenize(q):
    """
    Serialize a sequence of tokens into a string.
    """
    return unicode((' ').join(_untokenize(q)))


def _untokenize(q):
    for (name, data) in q:
        if name == 'term':
            if _needs_quoting(data):
                yield '"%s"' % data
            else:
                yield data
        elif name == 'field':
            (name, operator, value) = data
            if _needs_quoting(value):
                yield '%s%s"%s"' % tuple(data)
            else:
                yield '%s%s%s' % tuple(data)
        elif name == 'order':
            if data[1]:
                yield '{%s}' % data[0]
            else:
                yield '{-%s}' % data[0]


def _needs_quoting(s):
    return not ('').join(_safe_word.parseString(s)[0]) == s


if __name__ == '__main__':
    import unittest
    GBP = ('£').decode('utf-8')

    class TestCase(unittest.TestCase):

        def test_tokenize(self):
            tests = [
             (
              '', []),
             (
              'wibble', [('term', 'wibble')]),
             (
              'wibble wobble', [('term', 'wibble'), ('term', 'wobble')]),
             (
              'wibble age=42', [('term', 'wibble'), ('field', ('age', '=', '42'))]),
             (
              'wibble age=42 foo=bar', [('term', 'wibble'), ('field', ('age', '=', '42')), ('field', ('foo', '=', 'bar'))]),
             (
              'age=42', [('field', ('age', '=', '42'))]),
             (
              'age=42 foo=bar', [('field', ('age', '=', '42')), ('field', ('foo', '=', 'bar'))]),
             (
              'wibble wobble foo=bar', [('term', 'wibble'), ('term', 'wobble'), ('field', ('foo', '=', 'bar'))]),
             (
              'wibble wobble age>10 age<20', [('term', 'wibble'), ('term', 'wobble'), ('field', ('age', '>', '10')), ('field', ('age', '<', '20'))]),
             (
              '"wibble" foo=1', [('term', 'wibble'), ('field', ('foo', '=', '1'))]),
             (
              '"wibble wobble" foo=1', [('term', 'wibble wobble'), ('field', ('foo', '=', '1'))]),
             (
              '"wibble" foo=1 wobble', [('term', 'wibble'), ('field', ('foo', '=', '1')), ('term', 'wobble')]),
             (
              '"1 & 2"', [('term', '1 & 2')]),
             (
              '"foo=bar" foo=bar', [('term', 'foo=bar'), ('field', ('foo', '=', 'bar'))]),
             (
              'foo_bar=true', [('field', ('foo_bar', '=', 'true'))]),
             (
              'foo_bar', [('term', 'foo_bar')]),
             (
              'foo="one two"', [('field', ('foo', '=', 'one two'))]),
             (
              GBP, [('term', GBP)]),
             (
              'foo=%s' % GBP, [('field', ('foo', '=', GBP))]),
             (
              'foo="%s"' % GBP, [('field', ('foo', '=', GBP))]),
             (
              'abc foo=%s' % (GBP,), [('term', 'abc'), ('field', ('foo', '=', GBP))]),
             (
              '"%s" foo=abc' % (GBP,), [('term', GBP), ('field', ('foo', '=', 'abc'))]),
             (
              '%s foo=abc' % (GBP,), [('term', GBP), ('field', ('foo', '=', 'abc'))]),
             (
              '%s foo=%s' % (GBP, GBP), [('term', GBP), ('field', ('foo', '=', GBP))]),
             (
              '%s foo="%s"' % (GBP, GBP), [('term', GBP), ('field', ('foo', '=', GBP))]),
             (
              '"%s %s" foo="%s"' % (GBP, GBP, GBP), [('term', '%s %s' % (GBP, GBP)), ('field', ('foo', '=', GBP))]),
             (
              '{foo}', [('order', ('foo', True))]),
             (
              'wibble {foo}', [('term', 'wibble'), ('order', ('foo', True))]),
             (
              'wibble {-foo}', [('term', 'wibble'), ('order', ('foo', False))]),
             (
              'wibble foo=bar {foo}', [('term', 'wibble'), ('field', ('foo', '=', 'bar')), ('order', ('foo', True))]),
             (
              'wibble foo=bar {-foo}', [('term', 'wibble'), ('field', ('foo', '=', 'bar')), ('order', ('foo', False))])]
            for (test, result) in tests:
                print '=>', test
                tokenized = list(tokenize(test))
                print '  ', tokenized
                assert tokenized == result

        def test_untokenize(self):
            tests = [
             'wibble',
             'wibble wobble',
             '"wibble wobble"',
             '"wibble wobble" foo=bar',
             '"wibble wobble" foo=bar one two a=b "R&D"',
             'foo="one two"',
             GBP,
             '%s foo=%s' % (GBP, GBP),
             'wibble {foo}',
             'wibble {-foo}']
            for test in tests:
                print '=>', test
                untokenized = untokenize(tokenize(test))
                print '  ', untokenized
                assert untokenized == test


    unittest.main()
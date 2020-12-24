# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jinja\lexer.py
# Compiled at: 2007-11-17 17:38:42
"""
    jinja.lexer
    ~~~~~~~~~~~

    This module implements a Jinja / Python combination lexer. The
    `Lexer` class provided by this module is used to do some preprocessing
    for Jinja.

    On the one hand it filters out invalid operators like the bitshift
    operators we don't allow in templates. On the other hand it separates
    template code and python code in expressions.

    Because of some limitations in the compiler package which are just
    natural but annoying for Jinja, the lexer also "escapes" non names that
    are not keywords. The Jinja parser then removes those escaping marks
    again.

    This is required in order to make "class" and some other python keywords
    we don't use valid identifiers.

    :copyright: 2007 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import re, unicodedata
from jinja.datastructure import TokenStream, Token
from jinja.exceptions import TemplateSyntaxError
from jinja.utils import set, sorted
from weakref import WeakValueDictionary
__all__ = [
 'Lexer', 'Failure', 'keywords']
_lexer_cache = WeakValueDictionary()
whitespace_re = re.compile('\\s+(?um)')
name_re = re.compile('[a-zA-Z_][a-zA-Z0-9_]*')
string_re = re.compile('(\'([^\'\\\\]*(?:\\\\.[^\'\\\\]*)*)\'|"([^"\\\\]*(?:\\\\.[^"\\\\]*)*)")(?ms)')
integer_re = re.compile('\\d+')
float_re = re.compile('\\d+\\.\\d+')
regex_re = re.compile('@/([^/\\\\]*(?:\\\\.[^/\\\\]*)*)*/[a-z]*(?ms)')
keywords = set(['and', 'block', 'cycle', 'elif', 'else', 'endblock',
 'endfilter', 'endfor', 'endif', 'endmacro', 'endraw',
 'endtrans', 'extends', 'filter', 'for', 'if', 'in',
 'include', 'is', 'macro', 'not', 'or', 'pluralize', 'raw',
 'recursive', 'set', 'trans', 'print', 'call', 'endcall'])
operators = {'+': 'add', 
   '-': 'sub', 
   '/': 'div', 
   '//': 'floordiv', 
   '*': 'mul', 
   '%': 'mod', 
   '**': 'pow', 
   '~': 'tilde', 
   '!': 'bang', 
   '@': 'at', 
   '[': 'lbracket', 
   ']': 'rbracket', 
   '(': 'lparen', 
   ')': 'rparen', 
   '{': 'lbrace', 
   '}': 'rbrace', 
   '==': 'eq', 
   '!=': 'ne', 
   '>': 'gt', 
   '>=': 'gteq', 
   '<': 'lt', 
   '<=': 'lteq', 
   '=': 'assign', 
   '.': 'dot', 
   ':': 'colon', 
   '|': 'pipe', 
   ',': 'comma'}
reverse_operators = dict([ (v, k) for (k, v) in operators.iteritems() ])
assert len(operators) == len(reverse_operators), 'operators dropped'
operator_re = re.compile('(%s)' % ('|').join([ re.escape(x) for x in sorted(operators, key=lambda x: -len(x))
                                             ]))

def unescape_string(lineno, filename, s):
    r"""
    Unescape a string. Supported escapes:
        \a, \n, \r\, \f, \v, \\, \", \', \0

        \x00, \u0000, \U00000000, \N{...}

    Not supported are \101 because imho redundant.
    """
    result = []
    write = result.append
    simple_escapes = {'a': '\x07', 
       'n': '\n', 
       'r': '\r', 
       'f': '\x0c', 
       't': '\t', 
       'v': '\x0b', 
       '\\': '\\', 
       '"': '"', 
       "'": "'", 
       '0': '\x00'}
    unicode_escapes = {'x': 2, 
       'u': 4, 
       'U': 8}
    chariter = iter(s)
    next_char = chariter.next
    try:
        for char in chariter:
            if char == '\\':
                char = next_char()
                if char in simple_escapes:
                    write(simple_escapes[char])
                elif char in unicode_escapes:
                    seq = [ next_char() for x in xrange(unicode_escapes[char]) ]
                    try:
                        write(unichr(int(('').join(seq), 16)))
                    except ValueError:
                        raise TemplateSyntaxError('invalid unicode codepoint', lineno, filename)

                elif char == 'N':
                    if next_char() != '{':
                        raise TemplateSyntaxError('no name for codepoint', lineno, filename)
                    seq = []
                    while True:
                        char = next_char()
                        if char == '}':
                            break
                        seq.append(char)

                    try:
                        write(unicodedata.lookup(('').join(seq)))
                    except KeyError:
                        raise TemplateSyntaxError('unknown character name', lineno, filename)

                else:
                    write('\\' + char)
            else:
                write(char)

    except StopIteration:
        raise TemplateSyntaxError('invalid string escape', lineno, filename)

    return ('').join(result)


def unescape_regex(s):
    """
    Unescape rules for regular expressions.
    """
    buffer = []
    write = buffer.append
    in_escape = False
    for char in s:
        if in_escape:
            in_escape = False
            if char not in safe_chars:
                write('\\' + char)
                continue
        write(char)

    return ('').join(buffer)


class Failure(object):
    """
    Class that raises a `TemplateSyntaxError` if called.
    Used by the `Lexer` to specify known errors.
    """

    def __init__(self, message, cls=TemplateSyntaxError):
        self.message = message
        self.error_class = cls

    def __call__(self, lineno, filename):
        raise self.error_class(self.message, lineno, filename)


class LexerMeta(type):
    """
    Metaclass for the lexer that caches instances for
    the same configuration in a weak value dictionary.
    """

    def __call__(cls, environment):
        key = hash((environment.block_start_string,
         environment.block_end_string,
         environment.variable_start_string,
         environment.variable_end_string,
         environment.comment_start_string,
         environment.comment_end_string,
         environment.trim_blocks))
        if key in _lexer_cache:
            return _lexer_cache[key]
        lexer = type.__call__(cls, environment)
        _lexer_cache[key] = lexer
        return lexer


class Lexer(object):
    """
    Class that implements a lexer for a given environment. Automatically
    created by the environment class, usually you don't have to do that.

    Note that the lexer is not automatically bound to an environment.
    Multiple environments can share the same lexer.
    """
    __metaclass__ = LexerMeta

    def __init__(self, environment):
        c = lambda x: re.compile(x, re.M | re.S)
        e = re.escape
        tag_rules = [
         (
          whitespace_re, None, None),
         (
          float_re, 'float', None),
         (
          integer_re, 'integer', None),
         (
          name_re, 'name', None),
         (
          string_re, 'string', None),
         (
          regex_re, 'regex', None),
         (
          operator_re, 'operator', None)]
        self.no_variable_block = environment.variable_start_string is environment.variable_end_string is None or environment.variable_start_string == environment.block_start_string and environment.variable_end_string == environment.block_end_string
        root_tag_rules = [
         (
          'comment', environment.comment_start_string),
         (
          'block', environment.block_start_string)]
        if not self.no_variable_block:
            root_tag_rules.append(('variable',
             environment.variable_start_string))
        root_tag_rules.sort(lambda a, b: cmp(len(b[1]), len(a[1])))
        block_suffix_re = environment.trim_blocks and '\\n?' or ''
        self.rules = {'root': [
                  (
                   c('(.*?)(?:%s)' % ('|').join([
                    '(?P<raw_begin>(?:\\s*%s\\-|%s)\\s*raw\\s*%s)' % (
                     e(environment.block_start_string),
                     e(environment.block_start_string),
                     e(environment.block_end_string))] + [ '(?P<%s_begin>\\s*%s\\-|%s)' % (n, e(r), e(r)) for (n, r) in root_tag_rules
                                                         ])),
                   ('data', '#bygroup'), '#bygroup'),
                  (
                   c('.+'), 'data', None)], 
           'comment_begin': [
                           (
                            c('(.*?)((?:\\-%s\\s*|%s)%s)' % (
                             e(environment.comment_end_string),
                             e(environment.comment_end_string),
                             block_suffix_re)),
                            ('comment', 'comment_end'), '#pop'),
                           (
                            c('(.)'), (Failure('Missing end of comment tag'),), None)], 
           'block_begin': [
                         (
                          c('(?:\\-%s\\s*|%s)%s' % (
                           e(environment.block_end_string),
                           e(environment.block_end_string),
                           block_suffix_re)),
                          'block_end', '#pop')] + tag_rules, 
           'raw_begin': [
                       (
                        c('(.*?)((?:\\s*%s\\-|%s)\\s*endraw\\s*(?:\\-%s\\s*|%s%s))' % (
                         e(environment.block_start_string),
                         e(environment.block_start_string),
                         e(environment.block_end_string),
                         e(environment.block_end_string),
                         block_suffix_re)),
                        ('data', 'raw_end'), '#pop'),
                       (
                        c('(.)'), (Failure('Missing end of raw directive'),), None)]}
        if not self.no_variable_block:
            self.rules['variable_begin'] = [
             (
              c('\\-%s\\s*|%s' % (
               e(environment.variable_end_string),
               e(environment.variable_end_string))),
              'variable_end', '#pop')] + tag_rules
        return

    def tokenize(self, source, filename=None):
        """
        Works like `tokeniter` but returns a tokenstream of tokens and not a
        generator or token tuples. Additionally all token values are already
        converted into types and postprocessed. For example keywords are
        already keyword tokens, not named tokens, comments are removed,
        integers and floats converted, strings unescaped etc.
        """

        def generate():
            for (lineno, token, value) in self.tokeniter(source, filename):
                if token in ('comment_begin', 'comment', 'comment_end'):
                    continue
                elif token == 'data':
                    try:
                        value = str(value)
                    except UnicodeError:
                        pass

                elif token == 'name':
                    value = str(value)
                    if value in keywords:
                        token = value
                        value = ''
                elif token == 'string':
                    value = unescape_string(lineno, filename, value[1:-1])
                    try:
                        value = str(value)
                    except UnicodeError:
                        pass

                elif token == 'regex':
                    args = value[value.rfind('/') + 1:]
                    value = unescape_regex(value[2:-(len(args) + 1)])
                    if args:
                        value = '(?%s)%s' % (args, value)
                elif token == 'integer':
                    value = int(value)
                elif token == 'float':
                    value = float(value)
                elif token == 'operator':
                    token = operators[value]
                    value = ''
                yield Token(lineno, token, value)

        return TokenStream(generate(), filename)

    def tokeniter(self, source, filename=None):
        """
        This method tokenizes the text and returns the tokens in a generator.
        Use this method if you just want to tokenize a template. The output
        you get is not compatible with the input the jinja parser wants. The
        parser uses the `tokenize` function with returns a `TokenStream` and
        keywords instead of just names.
        """
        source = ('\n').join(source.splitlines())
        pos = 0
        lineno = 1
        stack = ['root']
        statetokens = self.rules['root']
        source_length = len(source)
        balancing_stack = []
        while True:
            for (regex, tokens, new_state) in statetokens:
                m = regex.match(source, pos)
                if not m:
                    continue
                if balancing_stack and tokens in ('variable_end', 'block_end'):
                    continue
                if isinstance(tokens, tuple):
                    for (idx, token) in enumerate(tokens):
                        if token is None:
                            g = m.group(idx)
                            if g:
                                lineno += g.count('\n')
                            continue
                        elif token.__class__ is Failure:
                            raise token(lineno, filename)
                        elif token == '#bygroup':
                            for (key, value) in m.groupdict().iteritems():
                                if value is not None:
                                    yield (
                                     lineno, key, value)
                                    lineno += value.count('\n')
                                    break
                            else:
                                raise RuntimeError('%r wanted to resolve the token dynamically but no group matched' % regex)
                        else:
                            data = m.group(idx + 1)
                            if data:
                                yield (
                                 lineno, token, data)
                            lineno += data.count('\n')

                else:
                    data = m.group()
                    if tokens == 'operator':
                        if data == '{':
                            balancing_stack.append('}')
                        elif data == '(':
                            balancing_stack.append(')')
                        elif data == '[':
                            balancing_stack.append(']')
                        elif data in ('}', ')', ']'):
                            if not balancing_stack:
                                raise TemplateSyntaxError('unexpected "%s"' % data, lineno, filename)
                            expected_op = balancing_stack.pop()
                            if expected_op != data:
                                raise TemplateSyntaxError('unexpected "%s", expected "%s"' % (
                                 data, expected_op), lineno, filename)
                    if tokens is not None:
                        if data:
                            yield (
                             lineno, tokens, data)
                    lineno += data.count('\n')
                pos2 = m.end()
                if new_state is not None:
                    if new_state == '#pop':
                        stack.pop()
                    elif new_state == '#bygroup':
                        for (key, value) in m.groupdict().iteritems():
                            if value is not None:
                                stack.append(key)
                                break
                        else:
                            raise RuntimeError('%r wanted to resolve the new state dynamically but no group matched' % regex)
                    else:
                        stack.append(new_state)
                    statetokens = self.rules[stack[(-1)]]
                elif pos2 == pos:
                    raise RuntimeError('%r yielded empty string without stack change' % regex)
                pos = pos2
                break
            else:
                if pos >= source_length:
                    return
                raise TemplateSyntaxError('unexpected char %r at %d' % (
                 source[pos], pos), lineno, filename)

        return
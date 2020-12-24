# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apacheconfig/lexer.py
# Compiled at: 2020-01-09 16:01:59
from __future__ import unicode_literals
import logging, re, ply.lex as lex, six
from apacheconfig.error import ApacheConfigError
log = logging.getLogger(__name__)

class SingleQuotedString(six.text_type):
    is_single_quoted = True


class DoubleQuotedString(six.text_type):
    is_double_quoted = True


class HashCommentsLexer(object):
    tokens = ('HASHCOMMENT', )
    states = ()

    def t_HASHCOMMENT(self, t):
        r"""(?<!\\)\#(?:(?:\\\n)|[^\n\r])*"""
        if not self.options.get(b'multilinehashcomments'):
            if b'\n' in t.value:
                (first, second) = t.value.split(b'\n', 1)
                t.lexer.lexpos = t.lexer.lexpos - len(second) - 1
                t.value = first
        return t


class CStyleCommentsLexer(object):
    tokens = ('CCOMMENT', )
    states = (('ccomment', 'exclusive'), )

    def t_CCOMMENT(self, t):
        r"""\/\*"""
        t.lexer.code_start = t.lexer.lexpos
        t.lexer.ccomment_level = 1
        t.lexer.begin(b'ccomment')

    def t_ccomment_open(self, t):
        r"""\/\*"""
        t.lexer.ccomment_level += 1

    def t_ccomment_close(self, t):
        r"""\*\/"""
        t.lexer.ccomment_level -= 1
        if t.lexer.ccomment_level == 0:
            t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos + 1 - 3]
            t.type = b'CCOMMENT'
            t.lexer.lineno += t.value.count(b'\n')
            t.lexer.begin(b'INITIAL')
            return t

    def t_ccomment_body(self, t):
        """.+?"""
        pass

    def t_ccomment_error(self, t):
        raise ApacheConfigError(b"Illegal character '%s' in C-style comment" % t.value[0])


class ApacheIncludesLexer(object):
    tokens = ('APACHEINCLUDE', 'APACHEINCLUDEOPTIONAL')
    states = ()

    def t_APACHEINCLUDE(self, t):
        r"""include[\t ]+[^\n\r]+"""
        (include, whitespace, value) = re.split(b'([ \\t]+)', t.value, maxsplit=1)
        t.value = (include, whitespace, value)
        return t

    def t_APACHEINCLUDEOPTIONAL(self, t):
        r"""includeoptional[\t ]+[^\n\r]+"""
        (include, whitespace, value) = re.split(b'([ \\t]+)', t.value, maxsplit=1)
        t.value = (include, whitespace, value)
        return t


class BaseApacheConfigLexer(object):
    tokens = ('INCLUDE', 'OPEN_TAG', 'CLOSE_TAG', 'OPEN_CLOSE_TAG', 'OPTION_AND_VALUE',
              'OPTION_AND_VALUE_NOSTRIP', 'WHITESPACE', 'NEWLINE')
    states = (
     ('multiline', 'exclusive'),
     ('heredoc', 'exclusive'))

    def __init__(self, tempdir=None, debug=False):
        self._tempdir = tempdir
        self._debug = debug
        self.engine = None
        self.reset()
        return

    def reset(self):
        self.engine = lex.lex(module=self, reflags=re.DOTALL | re.IGNORECASE, outputdir=self._tempdir, debuglog=log if self._debug else None, errorlog=log if self._debug else None)
        return

    def tokenize(self, text):
        self.engine.input(text)
        tokens = []
        while True:
            token = self.engine.token()
            if not token:
                break
            tokens.append(token.value)

        return tokens

    def t_INCLUDE(self, t):
        r"""<<include[\t ]+[^\n\r\t]+>>"""
        (include, whitespace, value) = re.split(b'([ \\t]+)', t.value[2:-2], maxsplit=1)
        t.value = (b'<<', include, whitespace, value, b'>>')
        return t

    def t_CLOSE_TAG(self, t):
        r"""</[^\n\r]+>"""
        t.value = t.value[2:-1]
        return t

    def t_OPEN_CLOSE_TAG(self, t):
        r"""<[^\n\r/]*?[^\n\r/ ]/>"""
        if self.options.get(b'disableemptyelementtags', False):
            t.type = b'OPEN_TAG'
            return self.t_OPEN_TAG(t)
        t.value = t.value[1:-2]
        return self._lex_option(t)

    def t_OPEN_TAG(self, t):
        r"""<[^\n\r]+>|<[^\n\r]+\\\n"""
        t.value = t.value[1:-1]
        return self._lex_option(t)

    @staticmethod
    def _parse_option_value(token, lineno):
        match = re.search(b'[^=\\s"\\\']+|"([^"]*)"|\\\'([^\\\']*)\\\'', token)
        if not match:
            raise ApacheConfigError(b'Syntax error in option-value pair %s on line %d' % (
             token, lineno))
        option = match.group(0)
        if len(token.strip()) == len(option):
            return (token, None, None)
        else:
            (_, middle, value) = re.split(b'((?:\\s|=|\\\\\\s)+)', token[len(option):], maxsplit=1)
            if not option:
                raise ApacheConfigError(b'Syntax error in option-value pair %s on line %d' % (
                 token, lineno))
            if value:
                stripped = value.strip()
                if stripped[0] == b'"' and stripped[(-1)] == b'"':
                    value = DoubleQuotedString(stripped[1:-1])
                if stripped[0] == b"'" and stripped[(-1)] == b"'":
                    value = SingleQuotedString(stripped[1:-1])
            return (
             option, middle, value)

    def _pre_parse_value(self, option, value):
        try:
            pre_parse_value = self.options[b'plug'][b'pre_parse_value']
            return pre_parse_value(option, value)
        except KeyError:
            return (
             True, option, value)

    def _lex_option(self, t):
        if t.value.endswith(b'\\'):
            t.lexer.multiline_newline_seen = False
            t.lexer.code_start = t.lexer.lexpos - len(t.value)
            if b'TAG' in t.type:
                t.lexer.code_start -= 1
            t.lexer.begin(b'multiline')
            self._current_type = t.type
            return
        lineno = len(re.findall(b'\\r\\n|\\n|\\r', t.value))
        (option, whitespace, value) = self._parse_option_value(t.value, t.lineno)
        if not value:
            t.value = (
             option,)
            return t
        (process, option, value) = self._pre_parse_value(option, value)
        if not process:
            return
        if value.startswith(b'<<'):
            t.lexer.heredoc_anchor = value[2:].strip()
            t.lexer.heredoc_option = option
            t.lexer.heredoc_whitespace = whitespace
            t.lexer.code_start = t.lexer.lexpos + 1
            t.lexer.begin(b'heredoc')
            return
        t.value = (
         option, whitespace, value)
        t.lexer.lineno += lineno
        return t

    def t_multiline_OPTION_AND_VALUE(self, t):
        r"""[^\r\n]+"""
        t.lexer.multiline_newline_seen = False
        if t.value.endswith(b'\\'):
            return
        t.type = self._current_type
        t.lexer.begin(b'INITIAL')
        value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos + 1]
        value = self._remove_trailing_whitespace(value)
        t.lexer.lexpos = t.lexer.code_start + len(value)
        t.lexer.lineno += len(re.findall(b'\\r\\n|\\n|\\r', value))
        (option, whitespace, value) = self._parse_option_value(value, t.lineno)
        (process, option, value) = self._pre_parse_value(option, value)
        if not process:
            return
        if t.type == b'OPEN_TAG':
            if value.endswith(b'/>'):
                t.type = b'OPEN_CLOSE_TAG'
                value = value[:-1]
            value = value[:-1]
        if b'\\\n' in value and not self.options.get(b'preservewhitespace', False):
            value = (b' ').join(re.split(b'(?:\\s|\\\\\\s)+', value))
        t.value = (
         option, whitespace, value)
        return t

    def t_multiline_NEWLINE(self, t):
        r"""\r\n|\n|\r"""
        if t.lexer.multiline_newline_seen:
            return self.t_multiline_OPTION_AND_VALUE(t)
        t.lexer.multiline_newline_seen = True

    def t_multiline_error(self, t):
        raise ApacheConfigError(b"Illegal character '%s' in multi-line text on line %d" % (
         t.value[0], t.lineno))

    def _remove_trailing_whitespace(self, value):

        def trailing_escape(s):
            return (len(s) - len(s.rstrip(b'\\'))) % 2 == 1

        value = value.rstrip()
        while trailing_escape(value):
            value = value[:-1].rstrip()

        return value

    def t_heredoc_OPTION_AND_VALUE(self, t):
        r"""[^\r\n]+"""
        if t.value.lstrip() != t.lexer.heredoc_anchor:
            return
        t.type = b'OPTION_AND_VALUE'
        t.lexer.begin(b'INITIAL')
        value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos - len(t.lexer.heredoc_anchor)]
        value = self._remove_trailing_whitespace(value)
        t.lexer.lineno += len(re.findall(b'\\r\\n|\\n|\\r', t.value))
        t.value = (
         t.lexer.heredoc_option, t.lexer.heredoc_whitespace, value)
        return t

    def t_heredoc_NEWLINE(self, t):
        r"""\r\n|\n|\r"""
        t.lexer.lineno += 1

    def t_heredoc_error(self, t):
        raise ApacheConfigError(b"Illegal character '%s' in here-document text on line %d" % (
         t.value[0], t.lineno))

    def t_NEWLINE(self, t):
        r"""[ \t]*((\r\n|\n|\r|\\)[\t ]*)+"""
        if t.value != b'\\':
            t.lexer.lineno += 1
        return t

    def t_WHITESPACE(self, t):
        r"""[ \t]+"""
        return t

    def t_error(self, t):
        raise ApacheConfigError(b"Illegal character '%s' on line %d" % (t.value[0], t.lineno))


class OptionLexer(BaseApacheConfigLexer):

    def t_OPTION_AND_VALUE(self, t):
        r"""[^ \n\r\t=\#]+([ \t=]+(?:\\\#|[^ \t\r\n\#])+)*"""
        return self._lex_option(t)


class NoStripLexer(BaseApacheConfigLexer):

    def t_OPTION_AND_VALUE_NOSTRIP(self, t):
        r"""[^ \n\r\t=\#]+[ \t=]+(?:\\\#|[^\r\n\#])+"""
        return self._lex_option(t)


def make_lexer(**options):
    lexer_class = OptionLexer
    if options.get(b'nostripvalues'):
        lexer_class = NoStripLexer
    lexer_class = type(str(b'ApacheConfigLexer'), (
     lexer_class, HashCommentsLexer), {b'tokens': lexer_class.tokens + HashCommentsLexer.tokens, 
       b'states': lexer_class.states + HashCommentsLexer.states, 
       b'options': options})
    if options.get(b'ccomments', True):
        lexer_class = type(str(b'ApacheConfigLexer'), (
         lexer_class, CStyleCommentsLexer), {b'tokens': lexer_class.tokens + CStyleCommentsLexer.tokens, 
           b'states': lexer_class.states + CStyleCommentsLexer.states, 
           b'options': options})
    if options.get(b'useapacheinclude', True):
        lexer_class = type(str(b'ApacheConfigLexer'), (
         lexer_class, ApacheIncludesLexer), {b'tokens': lexer_class.tokens + ApacheIncludesLexer.tokens, 
           b'states': lexer_class.states + ApacheIncludesLexer.states, 
           b'options': options})
    return lexer_class
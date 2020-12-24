# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apacheconfig/parser.py
# Compiled at: 2020-01-09 16:01:59
from __future__ import unicode_literals
import logging, ply.yacc as yacc, six
from apacheconfig.error import ApacheConfigError
log = logging.getLogger(__name__)

class HashCommentsParser(object):

    def p_hashcomment(self, p):
        """comment : HASHCOMMENT
        """
        p[0] = [
         b'comment', p[1]]


class CStyleCommentsParser(object):

    def p_comment(self, p):
        """comment : HASHCOMMENT
                   | CCOMMENT
        """
        p[0] = [
         b'comment', p[1]]


class IncludesParser(object):

    def p_include(self, p):
        """include : INCLUDE
           includeoptional : INCLUDE
        """
        if self._preserve_whitespace:
            p[0] = [
             b'include'] + p[1]
        else:
            p[0] = [
             b'include', p[1][3]]


class ApacheIncludesParser(object):

    def p_apacheinclude(self, p):
        """include : INCLUDE
                   | APACHEINCLUDE
        """
        if self._preserve_whitespace:
            p[0] = [
             b'include'] + list(p[1])
            return
        filename_index = 2
        if p[1][0] == b'<<':
            filename_index = 3
        p[0] = [
         b'include', p[1][filename_index]]

    def p_includeoptional(self, p):
        """includeoptional : APACHEINCLUDEOPTIONAL
        """
        if self._preserve_whitespace:
            p[0] = [
             b'includeoptional'] + list(p[1])
        else:
            p[0] = [
             b'includeoptional', p[1][2]]


class BaseApacheConfigParser(object):

    def __init__(self, lexer, start=b'config', tempdir=None, debug=False):
        self._lexer = lexer
        self.tokens = lexer.tokens
        self._tempdir = tempdir
        self._debug = debug
        self._start = start
        self._preserve_whitespace = self.options.get(b'preservewhitespace', False)
        self.engine = None
        self.reset()
        return

    def reset(self):
        self.engine = yacc.yacc(module=self, start=self._start, outputdir=self._tempdir, write_tables=bool(self._tempdir), debug=self._debug, debuglog=log if self._debug else yacc.NullLogger(), errorlog=log if self._debug else yacc.NullLogger())

    def parse(self, text):
        self.reset()
        return self.engine.parse(text)

    def p_requirednewline(self, p):
        """requirednewline : NEWLINE
        """
        p[0] = p[1]

    def p_whitespace(self, p):
        """whitespace : requirednewline
                      | WHITESPACE
        """
        p[0] = p[1]

    def p_statement(self, p):
        """statement : OPTION_AND_VALUE
                     | OPTION_AND_VALUE_NOSTRIP
        """
        p[0] = [
         b'statement']
        if self._preserve_whitespace:
            p[0] += p[1]
        elif len(p[1]) > 1:
            p[0] += [p[1][0], p[1][2]]
        else:
            p[0] += p[1]
        if self.options.get(b'lowercasenames'):
            p[0][1] = p[0][1].lower()

    def p_item(self, p):
        """item : statement
                | include
                | includeoptional
                | block
        """
        p[0] = p[1]

    def p_startitem(self, p):
        """startitem : whitespace item
                     | whitespace comment
                     | item
                     | comment
        """
        if len(p) == 3:
            if self._preserve_whitespace:
                item = p[2]
                p[0] = [item[0]] + [p[1]] + item[1:]
            else:
                p[0] = p[2]
        else:
            p[0] = p[1]

    def p_miditem(self, p):
        """miditem : requirednewline item
                   | whitespace comment
                   | comment
        """
        if len(p) == 3:
            if self._preserve_whitespace:
                item = p[2]
                p[0] = [item[0]] + [p[1]] + item[1:]
            else:
                p[0] = p[2]
        else:
            p[0] = p[1]

    def p_contents(self, p):
        """contents : contents whitespace
                    | contents miditem
                    | whitespace
                    | startitem
        """
        n = len(p)
        if n == 3:
            if isinstance(p[2], six.text_type) and p[2].isspace():
                if self._preserve_whitespace:
                    p[0] = p[1] + [p[2]]
                else:
                    p[0] = p[1]
            else:
                p[0] = p[1] + [p[2]]
        elif not self._preserve_whitespace and isinstance(p[1], six.text_type) and p[1].isspace():
            p[0] = []
        else:
            p[0] = [b'contents', p[1]]

    def p_block(self, p):
        """block : OPEN_TAG contents CLOSE_TAG
                 | OPEN_CLOSE_TAG
        """
        n = len(p)
        if n == 4:
            if isinstance(p[2], six.text_type) and p[2].isspace():
                p[2] = []
            p[0] = [
             b'block', p[1], p[2], p[3]]
        else:
            p[0] = [
             b'block', p[1], [], (b'').join(p[1])]
        if self.options.get(b'lowercasenames'):
            p[0][1] = tuple(x.lower() for x in p[0][1])
            p[0][3] = p[0][3].lower()

    def p_config(self, p):
        """config : config contents
                  | contents
        """
        n = len(p)
        if n == 3:
            p[0] = p[1] + [p[2]]
        elif n == 2:
            p[0] = [
             b'config', p[1]]

    def p_error(self, p):
        raise ApacheConfigError(b"Parser error at '%s'" % p.value if p else b'Unexpected EOF')


def make_parser(**options):
    parser_class = BaseApacheConfigParser
    if options.get(b'ccomments', True):
        parser_class = type(str(b'ApacheConfigParser'), (
         parser_class, CStyleCommentsParser), {b'options': options})
    else:
        parser_class = type(str(b'ApacheConfigParser'), (
         parser_class, HashCommentsParser), {b'options': options})
    if options.get(b'useapacheinclude', True):
        parser_class = type(str(b'ApacheConfigParser'), (
         parser_class, ApacheIncludesParser), {b'options': options})
    else:
        parser_class = type(str(b'ApacheConfigParser'), (
         parser_class, IncludesParser), {b'options': options})
    return parser_class
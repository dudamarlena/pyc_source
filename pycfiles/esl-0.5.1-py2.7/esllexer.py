# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/esl/esllexer.py
# Compiled at: 2016-04-10 04:53:29
from ply.lex import TOKEN
import re, ply.lex as lex
digit = '([0-9])'
nondigit = '([_A-Za-z])'
variable = '[a-zA-Z0-9\\[\\]\\-_.]+'
header = '--h' + variable
querystring = '--q' + variable
body = '--b' + variable
value = '=[a-zA-Z0-9\\[\\]\\-_.]+'
shell = '=\\$\\(.*?\\)'

class ESLLexer(object):
    tokens = ('URL', 'METHOD', 'HEADER', 'QUERYSTRING', 'BODY', 'VALUE', 'SHELL')

    def t_URL(self, t):
        """^[^ ]+"""
        return t

    def t_METHOD(self, t):
        """(GET|get|POST|post|DELETE|delete|OPTIONS|options|CONNECT|connect)"""
        t.value = t.value
        return t

    @TOKEN(value)
    def t_VALUE(self, t):
        return t

    @TOKEN(shell)
    def t_SHELL(self, t):
        t.value = t.value
        return t

    @TOKEN(header)
    def t_HEADER(self, t):
        return t

    @TOKEN(querystring)
    def t_QUERYSTRING(self, t):
        return t

    @TOKEN(body)
    def t_BODY(self, t):
        return t

    def t_newline(self, t):
        r"""\n+"""
        t.lexer.lineno += len(t.value)

    t_ignore = ' \t'

    def t_error(self, t):
        print "unkonw character '%s'" % t.value[0]
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print tok


if __name__ == '__main__':
    m = ESLLexer()
    m.build()
    m.test('/api/cmdb/peoples/ get --qhost_ip=$(ifconfig eth0) --qhost_name=bj-sdf --hContent-Type=abcd --bslkjsdf=123')
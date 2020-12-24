# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/parser/preprocessor.py
# Compiled at: 2019-12-10 16:20:40
# Size of source mod 2**32: 6927 bytes
"""Preprocess a C source file using gcc and convert the result into
   a token stream

Reference is C99:
  * http://www.open-std.org/JTC1/SC22/WG14/www/docs/n1124.pdf

"""
__docformat__ = 'restructuredtext'
import os, re, shlex, sys, tokenize, traceback, subprocess, ctypes
from . import lex, yacc
from .lex import TOKEN, LexError
from . import pplexer

class PreprocessorLexer(lex.Lexer):

    def __init__(self):
        lex.Lexer.__init__(self)
        self.filename = '<input>'
        self.in_define = False

    def input(self, data, filename=None):
        if filename:
            self.filename = filename
        self.lasttoken = None
        self.input_stack = []
        lex.Lexer.input(self, data)

    def push_input(self, data, filename):
        self.input_stack.append((self.lexdata, self.lexpos, self.filename, self.lineno))
        self.lexdata = data
        self.lexpos = 0
        self.lineno = 1
        self.filename = filename
        self.lexlen = len(self.lexdata)

    def pop_input(self):
        self.lexdata, self.lexpos, self.filename, self.lineno = self.input_stack.pop()
        self.lexlen = len(self.lexdata)

    def token(self):
        result = lex.Lexer.token(self)
        while result is None and self.input_stack:
            self.pop_input()
            result = lex.Lexer.token(self)

        if result:
            self.lasttoken = result.type
            result.filename = self.filename
        else:
            self.lasttoken = None
        return result


class TokenListLexer(object):

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def token(self):
        if self.pos < len(self.tokens):
            t = self.tokens[self.pos]
            self.pos += 1
            return t
        else:
            return


def symbol_to_token(sym):
    if isinstance(sym, yacc.YaccSymbol):
        return sym.value
    else:
        if isinstance(sym, lex.LexToken):
            return sym
        assert False, 'Not a symbol: %r' % sym


def create_token(type, value, production=None):
    """Create a token of type and value, at the position where 'production'
    was reduced.  Don't specify production if the token is built-in"""
    t = lex.LexToken()
    t.type = type
    t.value = value
    t.lexpos = -1
    if production:
        t.lineno = production.slice[1].lineno
        t.filename = production.slice[1].filename
    else:
        t.lineno = -1
        t.filename = '<builtin>'
    return t


class PreprocessorParser(object):

    def __init__(self, options, cparser):
        self.defines = [
         'inline=',
         '__inline__=',
         '__extension__=',
         '__const=const',
         '__asm__(x)=',
         '__asm(x)=',
         'CTYPESGEN=1']
        if sys.platform == 'darwin':
            self.defines += ['__uint16_t=uint16_t', '__uint32_t=uint32_t', '__uint64_t=uint64_t']
        self.matches = []
        self.output = []
        optimize = options.optimize_lexer if hasattr(options, 'optimize_lexer') else False
        self.lexer = lex.lex(cls=PreprocessorLexer,
          optimize=optimize,
          lextab='lextab',
          outputdir=(os.path.dirname(__file__)),
          module=pplexer)
        self.options = options
        self.cparser = cparser

    def parse(self, filename):
        """Parse a file and save its output"""
        cmd = self.options.cpp
        cmd += ' -U __GNUC__ -dD'
        for undefine in self.options.cpp_undefines:
            cmd += ' -U%s' % undefine

        if sys.platform == 'darwin':
            cmd += ' -U __BLOCKS__'
        for path in self.options.include_search_paths:
            cmd += ' -I"%s"' % path

        for define in self.defines + self.options.cpp_defines:
            cmd += ' "-D%s"' % define

        cmd += ' "' + filename + '"'
        self.cparser.handle_status(cmd)
        pp = subprocess.Popen(cmd,
          shell=True, universal_newlines=True, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
        ppout, pperr = pp.communicate()
        for line in pperr.split('\n'):
            if line:
                self.cparser.handle_pp_error(line)

        source_lines = []
        define_lines = []
        first_token_reg = re.compile('^#\\s*([^ ]+)($|\\s)')
        for line in ppout.split('\n'):
            line += '\n'
            search = first_token_reg.match(line)
            hash_token = search.group(1) if search else None
            if not hash_token or hash_token == 'pragma':
                source_lines.append(line)
                define_lines.append('\n')
            else:
                if hash_token.isdigit():
                    source_lines.append(line)
                    define_lines.append(line)
                else:
                    source_lines.append('\n')
                    define_lines.append(line)

        text = ''.join(source_lines + define_lines)
        if self.options.save_preprocessed_headers:
            self.cparser.handle_status('Saving preprocessed headers to %s.' % self.options.save_preprocessed_headers)
            try:
                with open(self.options.save_preprocessed_headers, 'w') as (f):
                    f.write(text)
            except IOError:
                self.cparser.handle_error("Couldn't save headers.")

        self.lexer.input(text)
        self.output = []
        try:
            while 1:
                token = self.lexer.token()
                if token is not None:
                    self.output.append(token)
                else:
                    break

        except LexError as e:
            self.cparser.handle_error('{}; {}'.format(e, e.text.partition('\n')[0]), filename, 0)
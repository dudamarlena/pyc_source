# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/slimit/slimit/lexer.py
# Compiled at: 2018-07-11 18:15:31
__author__ = 'Ruslan Spivak <ruslan.spivak@gmail.com>'
import ply.lex
from slimit.unicode_chars import LETTER, DIGIT, COMBINING_MARK, CONNECTOR_PUNCTUATION
TOKENS_THAT_IMPLY_DIVISON = frozenset([
 'ID',
 'NUMBER',
 'STRING',
 'REGEX',
 'TRUE',
 'FALSE',
 'NULL',
 'THIS',
 'PLUSPLUS',
 'MINUSMINUS',
 'RPAREN',
 'RBRACE',
 'RBRACKET'])

class Lexer(object):
    """A JavaScript lexer.

    >>> from slimit.lexer import Lexer
    >>> lexer = Lexer()

    Lexer supports iteration:

    >>> lexer.input('a = 1;')
    >>> for token in lexer:
    ...     print token
    ...
    LexToken(ID,'a',1,0)
    LexToken(EQ,'=',1,2)
    LexToken(NUMBER,'1',1,4)
    LexToken(SEMI,';',1,5)

    Or call one token at a time with 'token' method:

    >>> lexer.input('a = 1;')
    >>> while True:
    ...     token = lexer.token()
    ...     if not token:
    ...         break
    ...     print token
    ...
    LexToken(ID,'a',1,0)
    LexToken(EQ,'=',1,2)
    LexToken(NUMBER,'1',1,4)
    LexToken(SEMI,';',1,5)

    >>> lexer.input('a = 1;')
    >>> token = lexer.token()
    >>> token.type, token.value, token.lineno, token.lexpos
    ('ID', 'a', 1, 0)

    For more information see:
    http://www.ecma-international.org/publications/files/ECMA-ST/ECMA-262.pdf
    """

    def __init__(self):
        self.prev_token = None
        self.cur_token = None
        self.next_tokens = []
        self.build()
        return

    def build(self, **kwargs):
        """Build the lexer."""
        self.lexer = ply.lex.lex(object=self, **kwargs)

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        if self.next_tokens:
            return self.next_tokens.pop()
        else:
            lexer = self.lexer
            while True:
                pos = lexer.lexpos
                try:
                    char = lexer.lexdata[pos]
                    while char in ' \t':
                        pos += 1
                        char = lexer.lexdata[pos]

                    next_char = lexer.lexdata[(pos + 1)]
                except IndexError:
                    tok = self._get_update_token()
                    if tok is not None and tok.type == 'LINE_TERMINATOR':
                        continue
                    else:
                        return tok

                if char != '/' or char == '/' and next_char in ('/', '*'):
                    tok = self._get_update_token()
                    if tok.type in ('LINE_TERMINATOR', 'LINE_COMMENT', 'BLOCK_COMMENT'):
                        continue
                    else:
                        return tok
                cur_token = self.cur_token
                is_division_allowed = cur_token is not None and cur_token.type in TOKENS_THAT_IMPLY_DIVISON
                if is_division_allowed:
                    return self._get_update_token()
                self.prev_token = self.cur_token
                self.cur_token = self._read_regex()
                return self.cur_token

            return

    def auto_semi(self, token):
        if token is None or token.type == 'RBRACE' or self._is_prev_token_lt():
            if token:
                self.next_tokens.append(token)
            return self._create_semi_token(token)
        else:
            return

    def _is_prev_token_lt(self):
        return self.prev_token and self.prev_token.type == 'LINE_TERMINATOR'

    def _read_regex(self):
        self.lexer.begin('regex')
        token = self.lexer.token()
        self.lexer.begin('INITIAL')
        return token

    def _get_update_token(self):
        self.prev_token = self.cur_token
        self.cur_token = self.lexer.token()
        if self.cur_token is not None and self.cur_token.type == 'LINE_TERMINATOR' and self.prev_token is not None and self.prev_token.type in ('BREAK',
                                                                                                                                                'CONTINUE',
                                                                                                                                                'RETURN',
                                                                                                                                                'THROW'):
            return self._create_semi_token(self.cur_token)
        else:
            return self.cur_token

    def _create_semi_token(self, orig_token):
        token = ply.lex.LexToken()
        token.type = 'SEMI'
        token.value = ';'
        if orig_token is not None:
            token.lineno = orig_token.lineno
            token.lexpos = orig_token.lexpos
        else:
            token.lineno = 0
            token.lexpos = 0
        return token

    def __iter__(self):
        return self

    def next(self):
        token = self.token()
        if not token:
            raise StopIteration
        return token

    states = (('regex', 'exclusive'), )
    keywords = ('BREAK', 'CASE', 'CATCH', 'CONTINUE', 'DEBUGGER', 'DEFAULT', 'DELETE',
                'DO', 'ELSE', 'FINALLY', 'FOR', 'FUNCTION', 'IF', 'IN', 'INSTANCEOF',
                'NEW', 'RETURN', 'SWITCH', 'THIS', 'THROW', 'TRY', 'TYPEOF', 'VAR',
                'VOID', 'WHILE', 'WITH', 'NULL', 'TRUE', 'FALSE', 'CLASS', 'CONST',
                'ENUM', 'EXPORT', 'EXTENDS', 'IMPORT', 'SUPER')
    keywords_dict = dict((key.lower(), key) for key in keywords)
    tokens = ('PERIOD', 'COMMA', 'SEMI', 'COLON', 'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD',
              'BAND', 'BOR', 'BXOR', 'BNOT', 'CONDOP', 'NOT', 'LPAREN', 'RPAREN',
              'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 'EQ', 'EQEQ', 'NE', 'STREQ',
              'STRNEQ', 'LT', 'GT', 'LE', 'GE', 'OR', 'AND', 'PLUSPLUS', 'MINUSMINUS',
              'LSHIFT', 'RSHIFT', 'URSHIFT', 'PLUSEQUAL', 'MINUSEQUAL', 'MULTEQUAL',
              'DIVEQUAL', 'LSHIFTEQUAL', 'RSHIFTEQUAL', 'URSHIFTEQUAL', 'ANDEQUAL',
              'MODEQUAL', 'XOREQUAL', 'OREQUAL', 'NUMBER', 'STRING', 'ID', 'REGEX',
              'GETPROP', 'SETPROP', 'LINE_COMMENT', 'BLOCK_COMMENT', 'LINE_TERMINATOR') + keywords
    t_regex_REGEX = '(?:\n        /                       # opening slash\n        # First character is..\n        (?: [^*\\\\/[]            # anything but * \\ / or [\n        |   \\\\.                 # or an escape sequence\n        |   \\[                  # or a class, which has\n                (?: [^\\]\\\\]     # anything but \\ or ]\n                |   \\\\.         # or an escape sequence\n                )*              # many times\n            \\]\n        )\n        # Following characters are same, except for excluding a star\n        (?: [^\\\\/[]             # anything but \\ / or [\n        |   \\\\.                 # or an escape sequence\n        |   \\[                  # or a class, which has\n                (?: [^\\]\\\\]     # anything but \\ or ]\n                |   \\\\.         # or an escape sequence\n                )*              # many times\n            \\]\n        )*                      # many times\n        /                       # closing slash\n        [a-zA-Z0-9]*            # trailing flags\n        )\n        '
    t_regex_ignore = ' \t'

    def t_regex_error(self, token):
        raise TypeError("Error parsing regular expression '%s' at %s" % (
         token.value, token.lineno))

    t_PERIOD = '\\.'
    t_COMMA = ','
    t_SEMI = ';'
    t_COLON = ':'
    t_PLUS = '\\+'
    t_MINUS = '-'
    t_MULT = '\\*'
    t_DIV = '/'
    t_MOD = '%'
    t_BAND = '&'
    t_BOR = '\\|'
    t_BXOR = '\\^'
    t_BNOT = '~'
    t_CONDOP = '\\?'
    t_NOT = '!'
    t_LPAREN = '\\('
    t_RPAREN = '\\)'
    t_LBRACE = '{'
    t_RBRACE = '}'
    t_LBRACKET = '\\['
    t_RBRACKET = '\\]'
    t_EQ = '='
    t_EQEQ = '=='
    t_NE = '!='
    t_STREQ = '==='
    t_STRNEQ = '!=='
    t_LT = '<'
    t_GT = '>'
    t_LE = '<='
    t_GE = '>='
    t_OR = '\\|\\|'
    t_AND = '&&'
    t_PLUSPLUS = '\\+\\+'
    t_MINUSMINUS = '--'
    t_LSHIFT = '<<'
    t_RSHIFT = '>>'
    t_URSHIFT = '>>>'
    t_PLUSEQUAL = '\\+='
    t_MINUSEQUAL = '-='
    t_MULTEQUAL = '\\*='
    t_DIVEQUAL = '/='
    t_LSHIFTEQUAL = '<<='
    t_RSHIFTEQUAL = '>>='
    t_URSHIFTEQUAL = '>>>='
    t_ANDEQUAL = '&='
    t_MODEQUAL = '%='
    t_XOREQUAL = '\\^='
    t_OREQUAL = '\\|='
    t_LINE_COMMENT = '//[^\\r\\n]*'
    t_BLOCK_COMMENT = '/\\*[^*]*\\*+([^/*][^*]*\\*+)*/'
    t_LINE_TERMINATOR = '[\\n\\r]+'
    t_ignore = ' \t'
    t_NUMBER = '\n    (?:\n        0[xX][0-9a-fA-F]+              # hex_integer_literal\n     |  0[0-7]+                        # or octal_integer_literal (spec B.1.1)\n     |  (?:                            # or decimal_literal\n            (?:0|[1-9][0-9]*)          # decimal_integer_literal\n            \\.                         # dot\n            [0-9]*                     # decimal_digits_opt\n            (?:[eE][+-]?[0-9]+)?       # exponent_part_opt\n         |\n            \\.                         # dot\n            [0-9]+                     # decimal_digits\n            (?:[eE][+-]?[0-9]+)?       # exponent_part_opt\n         |\n            (?:0|[1-9][0-9]*)          # decimal_integer_literal\n            (?:[eE][+-]?[0-9]+)?       # exponent_part_opt\n         )\n    )\n    '
    string = '\n    (?:\n        # double quoted string\n        (?:"                               # opening double quote\n            (?: [^"\\\\\\n\\r]                 # no \\, line terminators or "\n                | \\\\[a-zA-Z!-\\/:-@\\[-`{-~] # or escaped characters\n                | \\\\x[0-9a-fA-F]{2}        # or hex_escape_sequence\n                | \\\\u[0-9a-fA-F]{4}        # or unicode_escape_sequence\n            )*?                            # zero or many times\n            (?: \\\\\\n                       # multiline ?\n              (?:\n                [^"\\\\\\n\\r]                 # no \\, line terminators or "\n                | \\\\[a-zA-Z!-\\/:-@\\[-`{-~] # or escaped characters\n                | \\\\x[0-9a-fA-F]{2}        # or hex_escape_sequence\n                | \\\\u[0-9a-fA-F]{4}        # or unicode_escape_sequence\n              )*?                          # zero or many times\n            )*\n        ")                                 # closing double quote\n        |\n        # single quoted string\n        (?:\'                               # opening single quote\n            (?: [^\'\\\\\\n\\r]                 # no \\, line terminators or \'\n                | \\\\[a-zA-Z!-\\/:-@\\[-`{-~] # or escaped characters\n                | \\\\x[0-9a-fA-F]{2}        # or hex_escape_sequence\n                | \\\\u[0-9a-fA-F]{4}        # or unicode_escape_sequence\n            )*?                            # zero or many times\n            (?: \\\\\\n                       # multiline ?\n              (?:\n                [^\'\\\\\\n\\r]                 # no \\, line terminators or \'\n                | \\\\[a-zA-Z!-\\/:-@\\[-`{-~] # or escaped characters\n                | \\\\x[0-9a-fA-F]{2}        # or hex_escape_sequence\n                | \\\\u[0-9a-fA-F]{4}        # or unicode_escape_sequence\n              )*?                          # zero or many times\n            )*\n        \')                                 # closing single quote\n    )\n    '

    @ply.lex.TOKEN(string)
    def t_STRING(self, token):
        token.value = token.value.replace('\\\n', '')
        return token

    identifier_start = '(?:[a-zA-Z_$]|' + LETTER + ')+'
    identifier_part = '(?:' + COMBINING_MARK + '|' + '[0-9a-zA-Z_$]' + '|' + DIGIT + '|' + CONNECTOR_PUNCTUATION + ')*'
    identifier = identifier_start + identifier_part
    getprop = 'get(?=\\s' + identifier + ')'

    @ply.lex.TOKEN(getprop)
    def t_GETPROP(self, token):
        return token

    setprop = 'set(?=\\s' + identifier + ')'

    @ply.lex.TOKEN(setprop)
    def t_SETPROP(self, token):
        return token

    @ply.lex.TOKEN(identifier)
    def t_ID(self, token):
        token.type = self.keywords_dict.get(token.value, 'ID')
        return token

    def t_error(self, token):
        print 'Illegal character %r at %s:%s after %s' % (
         token.value[0], token.lineno, token.lexpos, self.prev_token)
        token.lexer.skip(1)
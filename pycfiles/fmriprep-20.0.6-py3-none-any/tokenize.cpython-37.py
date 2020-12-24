# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/src/fmriprep/build/lib/python3.7/tokenize.py
# Compiled at: 2019-09-12 11:41:56
# Size of source mod 2**32: 27031 bytes
"""Tokenization help for Python programs.

tokenize(readline) is a generator that breaks a stream of bytes into
Python tokens.  It decodes the bytes according to PEP-0263 for
determining source file encoding.

It accepts a readline-like method which is called repeatedly to get the
next line of input (or b"" for EOF).  It generates 5-tuples with these
members:

    the token type (see token.py)
    the token (a string)
    the starting (row, column) indices of the token (a 2-tuple of ints)
    the ending (row, column) indices of the token (a 2-tuple of ints)
    the original line (string)

It is designed to match the working of the Python tokenizer exactly, except
that it produces COMMENT tokens for comments and gives type OP for all
operators.  Additionally, all token lists start with an ENCODING token
which tells you which encoding was used to decode the bytes stream.
"""
__author__ = 'Ka-Ping Yee <ping@lfw.org>'
__credits__ = 'GvR, ESR, Tim Peters, Thomas Wouters, Fred Drake, Skip Montanaro, Raymond Hettinger, Trent Nelson, Michael Foord'
from builtins import open as _builtin_open
from codecs import lookup, BOM_UTF8
import collections
from io import TextIOWrapper
from itertools import chain
import itertools as _itertools, re, sys
from token import *
cookie_re = re.compile('^[ \\t\\f]*#.*?coding[:=][ \\t]*([-\\w.]+)', re.ASCII)
blank_re = re.compile(b'^[ \\t\\f]*(?:[#\\r\\n]|$)', re.ASCII)
import token
__all__ = token.__all__ + ['tokenize', 'detect_encoding',
 'untokenize', 'TokenInfo']
del token
EXACT_TOKEN_TYPES = {'(':LPAR, 
 ')':RPAR, 
 '[':LSQB, 
 ']':RSQB, 
 ':':COLON, 
 ',':COMMA, 
 ';':SEMI, 
 '+':PLUS, 
 '-':MINUS, 
 '*':STAR, 
 '/':SLASH, 
 '|':VBAR, 
 '&':AMPER, 
 '<':LESS, 
 '>':GREATER, 
 '=':EQUAL, 
 '.':DOT, 
 '%':PERCENT, 
 '{':LBRACE, 
 '}':RBRACE, 
 '==':EQEQUAL, 
 '!=':NOTEQUAL, 
 '<=':LESSEQUAL, 
 '>=':GREATEREQUAL, 
 '~':TILDE, 
 '^':CIRCUMFLEX, 
 '<<':LEFTSHIFT, 
 '>>':RIGHTSHIFT, 
 '**':DOUBLESTAR, 
 '+=':PLUSEQUAL, 
 '-=':MINEQUAL, 
 '*=':STAREQUAL, 
 '/=':SLASHEQUAL, 
 '%=':PERCENTEQUAL, 
 '&=':AMPEREQUAL, 
 '|=':VBAREQUAL, 
 '^=':CIRCUMFLEXEQUAL, 
 '<<=':LEFTSHIFTEQUAL, 
 '>>=':RIGHTSHIFTEQUAL, 
 '**=':DOUBLESTAREQUAL, 
 '//':DOUBLESLASH, 
 '//=':DOUBLESLASHEQUAL, 
 '...':ELLIPSIS, 
 '->':RARROW, 
 '@':AT, 
 '@=':ATEQUAL}

class TokenInfo(collections.namedtuple('TokenInfo', 'type string start end line')):

    def __repr__(self):
        annotated_type = '%d (%s)' % (self.type, tok_name[self.type])
        return 'TokenInfo(type=%s, string=%r, start=%r, end=%r, line=%r)' % self._replace(type=annotated_type)

    @property
    def exact_type(self):
        if self.type == OP:
            if self.string in EXACT_TOKEN_TYPES:
                return EXACT_TOKEN_TYPES[self.string]
        return self.type


def group(*choices):
    return '(' + '|'.join(choices) + ')'


def any(*choices):
    return group(*choices) + '*'


def maybe(*choices):
    return group(*choices) + '?'


Whitespace = '[ \\f\\t]*'
Comment = '#[^\\r\\n]*'
Ignore = Whitespace + any('\\\\\\r?\\n' + Whitespace) + maybe(Comment)
Name = '\\w+'
Hexnumber = '0[xX](?:_?[0-9a-fA-F])+'
Binnumber = '0[bB](?:_?[01])+'
Octnumber = '0[oO](?:_?[0-7])+'
Decnumber = '(?:0(?:_?0)*|[1-9](?:_?[0-9])*)'
Intnumber = group(Hexnumber, Binnumber, Octnumber, Decnumber)
Exponent = '[eE][-+]?[0-9](?:_?[0-9])*'
Pointfloat = group('[0-9](?:_?[0-9])*\\.(?:[0-9](?:_?[0-9])*)?', '\\.[0-9](?:_?[0-9])*') + maybe(Exponent)
Expfloat = '[0-9](?:_?[0-9])*' + Exponent
Floatnumber = group(Pointfloat, Expfloat)
Imagnumber = group('[0-9](?:_?[0-9])*[jJ]', Floatnumber + '[jJ]')
Number = group(Imagnumber, Floatnumber, Intnumber)

def _all_string_prefixes():
    _valid_string_prefixes = [
     'b', 'r', 'u', 'f', 'br', 'fr']
    result = {
     ''}
    for prefix in _valid_string_prefixes:
        for t in _itertools.permutations(prefix):
            for u in (_itertools.product)(*[(c, c.upper()) for c in t]):
                result.add(''.join(u))

    return result


def _compile(expr):
    return re.compile(expr, re.UNICODE)


StringPrefix = group(*_all_string_prefixes())
Single = "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'"
Double = '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"'
Single3 = "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''"
Double3 = '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""'
Triple = group(StringPrefix + "'''", StringPrefix + '"""')
String = group(StringPrefix + "'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*'", StringPrefix + '"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*"')
Operator = group('\\*\\*=?', '>>=?', '<<=?', '!=', '//=?', '->', '[+\\-*/%&@|^=<>]=?', '~')
Bracket = '[][(){}]'
Special = group('\\r?\\n', '\\.\\.\\.', '[:;.,@]')
Funny = group(Operator, Bracket, Special)
PlainToken = group(Number, Funny, String, Name)
Token = Ignore + PlainToken
ContStr = group(StringPrefix + "'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*" + group("'", '\\\\\\r?\\n'), StringPrefix + '"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*' + group('"', '\\\\\\r?\\n'))
PseudoExtras = group('\\\\\\r?\\n|\\Z', Comment, Triple)
PseudoToken = Whitespace + group(PseudoExtras, Number, Funny, ContStr, Name)
endpats = {}
for _prefix in _all_string_prefixes():
    endpats[_prefix + "'"] = Single
    endpats[_prefix + '"'] = Double
    endpats[_prefix + "'''"] = Single3
    endpats[_prefix + '"""'] = Double3

single_quoted = set()
triple_quoted = set()
for t in _all_string_prefixes():
    for u in (t + '"', t + "'"):
        single_quoted.add(u)

    for u in (t + '"""', t + "'''"):
        triple_quoted.add(u)

tabsize = 8

class TokenError(Exception):
    pass


class StopTokenizing(Exception):
    pass


class Untokenizer:

    def __init__(self):
        self.tokens = []
        self.prev_row = 1
        self.prev_col = 0
        self.encoding = None

    def add_whitespace(self, start):
        row, col = start
        if (row < self.prev_row or row) == self.prev_row:
            if col < self.prev_col:
                raise ValueError('start ({},{}) precedes previous end ({},{})'.format(row, col, self.prev_row, self.prev_col))
        row_offset = row - self.prev_row
        if row_offset:
            self.tokens.append('\\\n' * row_offset)
            self.prev_col = 0
        col_offset = col - self.prev_col
        if col_offset:
            self.tokens.append(' ' * col_offset)

    def untokenize(self, iterable):
        it = iter(iterable)
        indents = []
        startline = False
        for t in it:
            if len(t) == 2:
                self.compat(t, it)
                break
            else:
                tok_type, token, start, end, line = t
                if tok_type == ENCODING:
                    self.encoding = token
                    continue
                if tok_type == ENDMARKER:
                    break
                if tok_type == INDENT:
                    indents.append(token)
                    continue
                else:
                    if tok_type == DEDENT:
                        indents.pop()
                        self.prev_row, self.prev_col = end
                        continue
                    else:
                        if tok_type in (NEWLINE, NL):
                            startline = True
                        else:
                            if startline:
                                if indents:
                                    indent = indents[(-1)]
                                    if start[1] >= len(indent):
                                        self.tokens.append(indent)
                                        self.prev_col = len(indent)
                                    startline = False
            self.add_whitespace(start)
            self.tokens.append(token)
            self.prev_row, self.prev_col = end
            if tok_type in (NEWLINE, NL):
                self.prev_row += 1
                self.prev_col = 0

        return ''.join(self.tokens)

    def compat(self, token, iterable):
        indents = []
        toks_append = self.tokens.append
        startline = token[0] in (NEWLINE, NL)
        prevstring = False
        for tok in chain([token], iterable):
            toknum, tokval = tok[:2]
            if toknum == ENCODING:
                self.encoding = tokval
                continue
            else:
                if toknum in (NAME, NUMBER):
                    tokval += ' '
                if toknum == STRING:
                    if prevstring:
                        tokval = ' ' + tokval
                    prevstring = True
                else:
                    prevstring = False
            if toknum == INDENT:
                indents.append(tokval)
                continue
            else:
                if toknum == DEDENT:
                    indents.pop()
                    continue
                else:
                    if toknum in (NEWLINE, NL):
                        startline = True
                    else:
                        if startline:
                            if indents:
                                toks_append(indents[(-1)])
                                startline = False
            toks_append(tokval)


def untokenize(iterable):
    """Transform tokens back into Python source code.
    It returns a bytes object, encoded using the ENCODING
    token, which is the first token sequence output by tokenize.

    Each element returned by the iterable must be a token sequence
    with at least two elements, a token number and token value.  If
    only two tokens are passed, the resulting output is poor.

    Round-trip invariant for full input:
        Untokenized source will match input source exactly

    Round-trip invariant for limited input:
        # Output bytes will tokenize back to the input
        t1 = [tok[:2] for tok in tokenize(f.readline)]
        newcode = untokenize(t1)
        readline = BytesIO(newcode).readline
        t2 = [tok[:2] for tok in tokenize(readline)]
        assert t1 == t2
    """
    ut = Untokenizer()
    out = ut.untokenize(iterable)
    if ut.encoding is not None:
        out = out.encode(ut.encoding)
    return out


def _get_normal_name(orig_enc):
    """Imitates get_normal_name in tokenizer.c."""
    enc = orig_enc[:12].lower().replace('_', '-')
    if enc == 'utf-8' or enc.startswith('utf-8-'):
        return 'utf-8'
    if enc in ('latin-1', 'iso-8859-1', 'iso-latin-1') or enc.startswith(('latin-1-',
                                                                          'iso-8859-1-',
                                                                          'iso-latin-1-')):
        return 'iso-8859-1'
    return orig_enc


def detect_encoding(readline):
    """
    The detect_encoding() function is used to detect the encoding that should
    be used to decode a Python source file.  It requires one argument, readline,
    in the same way as the tokenize() generator.

    It will call readline a maximum of twice, and return the encoding used
    (as a string) and a list of any lines (left as bytes) it has read in.

    It detects the encoding from the presence of a utf-8 bom or an encoding
    cookie as specified in pep-0263.  If both a bom and a cookie are present,
    but disagree, a SyntaxError will be raised.  If the encoding cookie is an
    invalid charset, raise a SyntaxError.  Note that if a utf-8 bom is found,
    'utf-8-sig' is returned.

    If no encoding is specified, then the default of 'utf-8' will be returned.
    """
    try:
        filename = readline.__self__.name
    except AttributeError:
        filename = None

    bom_found = False
    encoding = None
    default = 'utf-8'

    def read_or_stop():
        try:
            return readline()
        except StopIteration:
            return ''

    def find_cookie(line):
        try:
            line_string = line.decode('utf-8')
        except UnicodeDecodeError:
            msg = 'invalid or missing encoding declaration'
            if filename is not None:
                msg = '{} for {!r}'.format(msg, filename)
            raise SyntaxError(msg)

        match = cookie_re.match(line_string)
        if not match:
            return
        encoding = _get_normal_name(match.group(1))
        try:
            codec = lookup(encoding)
        except LookupError:
            if filename is None:
                msg = 'unknown encoding: ' + encoding
            else:
                msg = 'unknown encoding for {!r}: {}'.format(filename, encoding)
            raise SyntaxError(msg)

        if bom_found:
            if encoding != 'utf-8':
                if filename is None:
                    msg = 'encoding problem: utf-8'
                else:
                    msg = 'encoding problem for {!r}: utf-8'.format(filename)
                raise SyntaxError(msg)
            encoding += '-sig'
        return encoding

    first = read_or_stop()
    if first.startswith(BOM_UTF8):
        bom_found = True
        first = first[3:]
        default = 'utf-8-sig'
    else:
        if not first:
            return (
             default, [])
        else:
            encoding = find_cookie(first)
            if encoding:
                return (
                 encoding, [first])
            return blank_re.match(first) or (
             default, [first])
        second = read_or_stop()
        return second or (
         default, [first])
    encoding = find_cookie(second)
    if encoding:
        return (
         encoding, [first, second])
    return (default, [first, second])


def open(filename):
    """Open a file in read only mode using the encoding detected by
    detect_encoding().
    """
    buffer = _builtin_open(filename, 'rb')
    try:
        encoding, lines = detect_encoding(buffer.readline)
        buffer.seek(0)
        text = TextIOWrapper(buffer, encoding, line_buffering=True)
        text.mode = 'r'
        return text
    except:
        buffer.close()
        raise


def tokenize(readline):
    """
    The tokenize() generator requires one argument, readline, which
    must be a callable object which provides the same interface as the
    readline() method of built-in file objects.  Each call to the function
    should return one line of input as bytes.  Alternatively, readline
    can be a callable function terminating with StopIteration:
        readline = open(myfile, 'rb').__next__  # Example of alternate readline

    The generator produces 5-tuples with these members: the token type; the
    token string; a 2-tuple (srow, scol) of ints specifying the row and
    column where the token begins in the source; a 2-tuple (erow, ecol) of
    ints specifying the row and column where the token ends in the source;
    and the line on which the token was found.  The line passed is the
    logical line; continuation lines are included.

    The first token sequence will always be an ENCODING token
    which tells you which encoding was used to decode the bytes stream.
    """
    from itertools import chain, repeat
    encoding, consumed = detect_encoding(readline)
    rl_gen = iter(readline, '')
    empty = repeat('')
    return _tokenize(chain(consumed, rl_gen, empty).__next__, encoding)


def _tokenize--- This code section failed: ---

 L. 488         0  LOAD_CONST               0
                2  DUP_TOP          
                4  STORE_FAST               'lnum'
                6  DUP_TOP          
                8  STORE_FAST               'parenlev'
               10  STORE_FAST               'continued'

 L. 489        12  LOAD_STR                 '0123456789'
               14  STORE_FAST               'numchars'

 L. 490        16  LOAD_CONST               ('', 0)
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'contstr'
               22  STORE_FAST               'needcont'

 L. 491        24  LOAD_CONST               None
               26  STORE_FAST               'contline'

 L. 492        28  LOAD_CONST               0
               30  BUILD_LIST_1          1 
               32  STORE_FAST               'indents'

 L. 494        34  LOAD_FAST                'encoding'
               36  LOAD_CONST               None
               38  COMPARE_OP               is-not
               40  POP_JUMP_IF_FALSE    72  'to 72'

 L. 495        42  LOAD_FAST                'encoding'
               44  LOAD_STR                 'utf-8-sig'
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    54  'to 54'

 L. 497        50  LOAD_STR                 'utf-8'
               52  STORE_FAST               'encoding'
             54_0  COME_FROM            48  '48'

 L. 498        54  LOAD_GLOBAL              TokenInfo
               56  LOAD_GLOBAL              ENCODING
               58  LOAD_FAST                'encoding'
               60  LOAD_CONST               (0, 0)
               62  LOAD_CONST               (0, 0)
               64  LOAD_STR                 ''
               66  CALL_FUNCTION_5       5  '5 positional arguments'
               68  YIELD_VALUE      
               70  POP_TOP          
             72_0  COME_FROM            40  '40'

 L. 499        72  LOAD_STR                 ''
               74  STORE_FAST               'last_line'

 L. 500        76  LOAD_STR                 ''
               78  STORE_FAST               'line'

 L. 501     80_82  SETUP_LOOP         1534  'to 1534'

 L. 502        84  SETUP_EXCEPT        100  'to 100'

 L. 507        86  LOAD_FAST                'line'
               88  STORE_FAST               'last_line'

 L. 508        90  LOAD_FAST                'readline'
               92  CALL_FUNCTION_0       0  '0 positional arguments'
               94  STORE_FAST               'line'
               96  POP_BLOCK        
               98  JUMP_FORWARD        124  'to 124'
            100_0  COME_FROM_EXCEPT     84  '84'

 L. 509       100  DUP_TOP          
              102  LOAD_GLOBAL              StopIteration
              104  COMPARE_OP               exception-match
              106  POP_JUMP_IF_FALSE   122  'to 122'
              108  POP_TOP          
              110  POP_TOP          
              112  POP_TOP          

 L. 510       114  LOAD_STR                 ''
              116  STORE_FAST               'line'
              118  POP_EXCEPT       
              120  JUMP_FORWARD        124  'to 124'
            122_0  COME_FROM           106  '106'
              122  END_FINALLY      
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM            98  '98'

 L. 512       124  LOAD_FAST                'encoding'
              126  LOAD_CONST               None
              128  COMPARE_OP               is-not
              130  POP_JUMP_IF_FALSE   142  'to 142'

 L. 513       132  LOAD_FAST                'line'
              134  LOAD_METHOD              decode
              136  LOAD_FAST                'encoding'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  STORE_FAST               'line'
            142_0  COME_FROM           130  '130'

 L. 514       142  LOAD_FAST                'lnum'
              144  LOAD_CONST               1
              146  INPLACE_ADD      
              148  STORE_FAST               'lnum'

 L. 515       150  LOAD_CONST               0
              152  LOAD_GLOBAL              len
              154  LOAD_FAST                'line'
              156  CALL_FUNCTION_1       1  '1 positional argument'
              158  ROT_TWO          
              160  STORE_FAST               'pos'
              162  STORE_FAST               'max'

 L. 517       164  LOAD_FAST                'contstr'
          166_168  POP_JUMP_IF_FALSE   372  'to 372'

 L. 518       170  LOAD_FAST                'line'
              172  POP_JUMP_IF_TRUE    184  'to 184'

 L. 519       174  LOAD_GLOBAL              TokenError
              176  LOAD_STR                 'EOF in multi-line string'
              178  LOAD_FAST                'strstart'
              180  CALL_FUNCTION_2       2  '2 positional arguments'
              182  RAISE_VARARGS_1       1  'exception instance'
            184_0  COME_FROM           172  '172'

 L. 520       184  LOAD_FAST                'endprog'
              186  LOAD_METHOD              match
              188  LOAD_FAST                'line'
              190  CALL_METHOD_1         1  '1 positional argument'
              192  STORE_FAST               'endmatch'

 L. 521       194  LOAD_FAST                'endmatch'
          196_198  POP_JUMP_IF_FALSE   266  'to 266'

 L. 522       200  LOAD_FAST                'endmatch'
              202  LOAD_METHOD              end
              204  LOAD_CONST               0
              206  CALL_METHOD_1         1  '1 positional argument'
              208  DUP_TOP          
              210  STORE_FAST               'pos'
              212  STORE_FAST               'end'

 L. 523       214  LOAD_GLOBAL              TokenInfo
              216  LOAD_GLOBAL              STRING
              218  LOAD_FAST                'contstr'
              220  LOAD_FAST                'line'
              222  LOAD_CONST               None
              224  LOAD_FAST                'end'
              226  BUILD_SLICE_2         2 
              228  BINARY_SUBSCR    
              230  BINARY_ADD       

 L. 524       232  LOAD_FAST                'strstart'
              234  LOAD_FAST                'lnum'
              236  LOAD_FAST                'end'
              238  BUILD_TUPLE_2         2 
              240  LOAD_FAST                'contline'
              242  LOAD_FAST                'line'
              244  BINARY_ADD       
              246  CALL_FUNCTION_5       5  '5 positional arguments'
              248  YIELD_VALUE      
              250  POP_TOP          

 L. 525       252  LOAD_CONST               ('', 0)
              254  UNPACK_SEQUENCE_2     2 
              256  STORE_FAST               'contstr'
              258  STORE_FAST               'needcont'

 L. 526       260  LOAD_CONST               None
              262  STORE_FAST               'contline'
              264  JUMP_FORWARD        820  'to 820'
            266_0  COME_FROM           196  '196'

 L. 527       266  LOAD_FAST                'needcont'
          268_270  POP_JUMP_IF_FALSE   350  'to 350'
              272  LOAD_FAST                'line'
              274  LOAD_CONST               -2
              276  LOAD_CONST               None
              278  BUILD_SLICE_2         2 
              280  BINARY_SUBSCR    
              282  LOAD_STR                 '\\\n'
              284  COMPARE_OP               !=
          286_288  POP_JUMP_IF_FALSE   350  'to 350'
              290  LOAD_FAST                'line'
              292  LOAD_CONST               -3
              294  LOAD_CONST               None
              296  BUILD_SLICE_2         2 
              298  BINARY_SUBSCR    
              300  LOAD_STR                 '\\\r\n'
              302  COMPARE_OP               !=
          304_306  POP_JUMP_IF_FALSE   350  'to 350'

 L. 528       308  LOAD_GLOBAL              TokenInfo
              310  LOAD_GLOBAL              ERRORTOKEN
              312  LOAD_FAST                'contstr'
              314  LOAD_FAST                'line'
              316  BINARY_ADD       

 L. 529       318  LOAD_FAST                'strstart'
              320  LOAD_FAST                'lnum'
              322  LOAD_GLOBAL              len
              324  LOAD_FAST                'line'
              326  CALL_FUNCTION_1       1  '1 positional argument'
              328  BUILD_TUPLE_2         2 
              330  LOAD_FAST                'contline'
              332  CALL_FUNCTION_5       5  '5 positional arguments'
              334  YIELD_VALUE      
              336  POP_TOP          

 L. 530       338  LOAD_STR                 ''
              340  STORE_FAST               'contstr'

 L. 531       342  LOAD_CONST               None
              344  STORE_FAST               'contline'

 L. 532       346  CONTINUE             84  'to 84'
              348  JUMP_FORWARD        820  'to 820'
            350_0  COME_FROM           304  '304'
            350_1  COME_FROM           286  '286'
            350_2  COME_FROM           268  '268'

 L. 534       350  LOAD_FAST                'contstr'
              352  LOAD_FAST                'line'
              354  BINARY_ADD       
              356  STORE_FAST               'contstr'

 L. 535       358  LOAD_FAST                'contline'
              360  LOAD_FAST                'line'
              362  BINARY_ADD       
              364  STORE_FAST               'contline'

 L. 536       366  CONTINUE             84  'to 84'
          368_370  JUMP_FORWARD        820  'to 820'
            372_0  COME_FROM           166  '166'

 L. 538       372  LOAD_FAST                'parenlev'
              374  LOAD_CONST               0
              376  COMPARE_OP               ==
          378_380  POP_JUMP_IF_FALSE   796  'to 796'
              382  LOAD_FAST                'continued'
          384_386  POP_JUMP_IF_TRUE    796  'to 796'

 L. 539       388  LOAD_FAST                'line'
          390_392  POP_JUMP_IF_TRUE    396  'to 396'

 L. 539       394  BREAK_LOOP       
            396_0  COME_FROM           390  '390'

 L. 540       396  LOAD_CONST               0
              398  STORE_FAST               'column'

 L. 541       400  SETUP_LOOP          504  'to 504'
              402  LOAD_FAST                'pos'
              404  LOAD_FAST                'max'
              406  COMPARE_OP               <
          408_410  POP_JUMP_IF_FALSE   502  'to 502'

 L. 542       412  LOAD_FAST                'line'
              414  LOAD_FAST                'pos'
              416  BINARY_SUBSCR    
              418  LOAD_STR                 ' '
              420  COMPARE_OP               ==
          422_424  POP_JUMP_IF_FALSE   436  'to 436'

 L. 543       426  LOAD_FAST                'column'
              428  LOAD_CONST               1
              430  INPLACE_ADD      
              432  STORE_FAST               'column'
              434  JUMP_FORWARD        490  'to 490'
            436_0  COME_FROM           422  '422'

 L. 544       436  LOAD_FAST                'line'
              438  LOAD_FAST                'pos'
              440  BINARY_SUBSCR    
              442  LOAD_STR                 '\t'
              444  COMPARE_OP               ==
          446_448  POP_JUMP_IF_FALSE   468  'to 468'

 L. 545       450  LOAD_FAST                'column'
              452  LOAD_GLOBAL              tabsize
              454  BINARY_FLOOR_DIVIDE
              456  LOAD_CONST               1
              458  BINARY_ADD       
              460  LOAD_GLOBAL              tabsize
              462  BINARY_MULTIPLY  
              464  STORE_FAST               'column'
              466  JUMP_FORWARD        490  'to 490'
            468_0  COME_FROM           446  '446'

 L. 546       468  LOAD_FAST                'line'
              470  LOAD_FAST                'pos'
              472  BINARY_SUBSCR    
              474  LOAD_STR                 '\x0c'
              476  COMPARE_OP               ==
          478_480  POP_JUMP_IF_FALSE   488  'to 488'

 L. 547       482  LOAD_CONST               0
              484  STORE_FAST               'column'
              486  JUMP_FORWARD        490  'to 490'
            488_0  COME_FROM           478  '478'

 L. 549       488  BREAK_LOOP       
            490_0  COME_FROM           486  '486'
            490_1  COME_FROM           466  '466'
            490_2  COME_FROM           434  '434'

 L. 550       490  LOAD_FAST                'pos'
              492  LOAD_CONST               1
              494  INPLACE_ADD      
              496  STORE_FAST               'pos'
          498_500  JUMP_BACK           402  'to 402'
            502_0  COME_FROM           408  '408'
              502  POP_BLOCK        
            504_0  COME_FROM_LOOP      400  '400'

 L. 551       504  LOAD_FAST                'pos'
              506  LOAD_FAST                'max'
              508  COMPARE_OP               ==
          510_512  POP_JUMP_IF_FALSE   516  'to 516'

 L. 552       514  BREAK_LOOP       
            516_0  COME_FROM           510  '510'

 L. 554       516  LOAD_FAST                'line'
              518  LOAD_FAST                'pos'
              520  BINARY_SUBSCR    
              522  LOAD_STR                 '#\r\n'
              524  COMPARE_OP               in
          526_528  POP_JUMP_IF_FALSE   648  'to 648'

 L. 555       530  LOAD_FAST                'line'
              532  LOAD_FAST                'pos'
              534  BINARY_SUBSCR    
              536  LOAD_STR                 '#'
              538  COMPARE_OP               ==
          540_542  POP_JUMP_IF_FALSE   608  'to 608'

 L. 556       544  LOAD_FAST                'line'
              546  LOAD_FAST                'pos'
              548  LOAD_CONST               None
              550  BUILD_SLICE_2         2 
              552  BINARY_SUBSCR    
              554  LOAD_METHOD              rstrip
              556  LOAD_STR                 '\r\n'
              558  CALL_METHOD_1         1  '1 positional argument'
              560  STORE_FAST               'comment_token'

 L. 557       562  LOAD_GLOBAL              TokenInfo
              564  LOAD_GLOBAL              COMMENT
              566  LOAD_FAST                'comment_token'

 L. 558       568  LOAD_FAST                'lnum'
              570  LOAD_FAST                'pos'
              572  BUILD_TUPLE_2         2 
              574  LOAD_FAST                'lnum'
              576  LOAD_FAST                'pos'
              578  LOAD_GLOBAL              len
              580  LOAD_FAST                'comment_token'
              582  CALL_FUNCTION_1       1  '1 positional argument'
              584  BINARY_ADD       
              586  BUILD_TUPLE_2         2 
              588  LOAD_FAST                'line'
              590  CALL_FUNCTION_5       5  '5 positional arguments'
              592  YIELD_VALUE      
              594  POP_TOP          

 L. 559       596  LOAD_FAST                'pos'
              598  LOAD_GLOBAL              len
              600  LOAD_FAST                'comment_token'
              602  CALL_FUNCTION_1       1  '1 positional argument'
              604  INPLACE_ADD      
              606  STORE_FAST               'pos'
            608_0  COME_FROM           540  '540'

 L. 561       608  LOAD_GLOBAL              TokenInfo
              610  LOAD_GLOBAL              NL
              612  LOAD_FAST                'line'
              614  LOAD_FAST                'pos'
              616  LOAD_CONST               None
              618  BUILD_SLICE_2         2 
              620  BINARY_SUBSCR    

 L. 562       622  LOAD_FAST                'lnum'
              624  LOAD_FAST                'pos'
              626  BUILD_TUPLE_2         2 
              628  LOAD_FAST                'lnum'
              630  LOAD_GLOBAL              len
              632  LOAD_FAST                'line'
              634  CALL_FUNCTION_1       1  '1 positional argument'
              636  BUILD_TUPLE_2         2 
              638  LOAD_FAST                'line'
              640  CALL_FUNCTION_5       5  '5 positional arguments'
              642  YIELD_VALUE      
              644  POP_TOP          

 L. 563       646  CONTINUE             84  'to 84'
            648_0  COME_FROM           526  '526'

 L. 565       648  LOAD_FAST                'column'
              650  LOAD_FAST                'indents'
              652  LOAD_CONST               -1
              654  BINARY_SUBSCR    
              656  COMPARE_OP               >
          658_660  POP_JUMP_IF_FALSE   706  'to 706'

 L. 566       662  LOAD_FAST                'indents'
              664  LOAD_METHOD              append
              666  LOAD_FAST                'column'
              668  CALL_METHOD_1         1  '1 positional argument'
              670  POP_TOP          

 L. 567       672  LOAD_GLOBAL              TokenInfo
              674  LOAD_GLOBAL              INDENT
              676  LOAD_FAST                'line'
              678  LOAD_CONST               None
              680  LOAD_FAST                'pos'
              682  BUILD_SLICE_2         2 
              684  BINARY_SUBSCR    
              686  LOAD_FAST                'lnum'
              688  LOAD_CONST               0
              690  BUILD_TUPLE_2         2 
              692  LOAD_FAST                'lnum'
              694  LOAD_FAST                'pos'
              696  BUILD_TUPLE_2         2 
              698  LOAD_FAST                'line'
              700  CALL_FUNCTION_5       5  '5 positional arguments'
              702  YIELD_VALUE      
              704  POP_TOP          
            706_0  COME_FROM           658  '658'

 L. 568       706  SETUP_LOOP          820  'to 820'
              708  LOAD_FAST                'column'
              710  LOAD_FAST                'indents'
              712  LOAD_CONST               -1
            714_0  COME_FROM           264  '264'
              714  BINARY_SUBSCR    
              716  COMPARE_OP               <
          718_720  POP_JUMP_IF_FALSE   792  'to 792'

 L. 569       722  LOAD_FAST                'column'
              724  LOAD_FAST                'indents'
              726  COMPARE_OP               not-in
          728_730  POP_JUMP_IF_FALSE   750  'to 750'

 L. 570       732  LOAD_GLOBAL              IndentationError

 L. 571       734  LOAD_STR                 'unindent does not match any outer indentation level'

 L. 572       736  LOAD_STR                 '<tokenize>'
              738  LOAD_FAST                'lnum'
              740  LOAD_FAST                'pos'
              742  LOAD_FAST                'line'
              744  BUILD_TUPLE_4         4 
              746  CALL_FUNCTION_2       2  '2 positional arguments'
              748  RAISE_VARARGS_1       1  'exception instance'
            750_0  COME_FROM           728  '728'

 L. 573       750  LOAD_FAST                'indents'
              752  LOAD_CONST               None
              754  LOAD_CONST               -1
              756  BUILD_SLICE_2         2 
              758  BINARY_SUBSCR    
              760  STORE_FAST               'indents'

 L. 575       762  LOAD_GLOBAL              TokenInfo
              764  LOAD_GLOBAL              DEDENT
              766  LOAD_STR                 ''
              768  LOAD_FAST                'lnum'
              770  LOAD_FAST                'pos'
              772  BUILD_TUPLE_2         2 
              774  LOAD_FAST                'lnum'
              776  LOAD_FAST                'pos'
              778  BUILD_TUPLE_2         2 
              780  LOAD_FAST                'line'
              782  CALL_FUNCTION_5       5  '5 positional arguments'
              784  YIELD_VALUE      
              786  POP_TOP          
          788_790  JUMP_BACK           708  'to 708'
            792_0  COME_FROM           718  '718'
              792  POP_BLOCK        
              794  JUMP_FORWARD        820  'to 820'
            796_0  COME_FROM           384  '384'
            796_1  COME_FROM           378  '378'

 L. 578       796  LOAD_FAST                'line'
            798_0  COME_FROM           348  '348'
          798_800  POP_JUMP_IF_TRUE    816  'to 816'

 L. 579       802  LOAD_GLOBAL              TokenError
              804  LOAD_STR                 'EOF in multi-line statement'
              806  LOAD_FAST                'lnum'
              808  LOAD_CONST               0
              810  BUILD_TUPLE_2         2 
              812  CALL_FUNCTION_2       2  '2 positional arguments'
              814  RAISE_VARARGS_1       1  'exception instance'
            816_0  COME_FROM           798  '798'

 L. 580       816  LOAD_CONST               0
              818  STORE_FAST               'continued'
            820_0  COME_FROM           794  '794'
            820_1  COME_FROM_LOOP      706  '706'
            820_2  COME_FROM           368  '368'

 L. 582   820_822  SETUP_LOOP         1530  'to 1530'
              824  LOAD_FAST                'pos'
              826  LOAD_FAST                'max'
              828  COMPARE_OP               <
          830_832  POP_JUMP_IF_FALSE  1528  'to 1528'

 L. 583       834  LOAD_GLOBAL              _compile
              836  LOAD_GLOBAL              PseudoToken
              838  CALL_FUNCTION_1       1  '1 positional argument'
              840  LOAD_METHOD              match
              842  LOAD_FAST                'line'
              844  LOAD_FAST                'pos'
              846  CALL_METHOD_2         2  '2 positional arguments'
              848  STORE_FAST               'pseudomatch'

 L. 584       850  LOAD_FAST                'pseudomatch'
          852_854  POP_JUMP_IF_FALSE  1482  'to 1482'

 L. 585       856  LOAD_FAST                'pseudomatch'
              858  LOAD_METHOD              span
              860  LOAD_CONST               1
              862  CALL_METHOD_1         1  '1 positional argument'
              864  UNPACK_SEQUENCE_2     2 
              866  STORE_FAST               'start'
              868  STORE_FAST               'end'

 L. 586       870  LOAD_FAST                'lnum'
              872  LOAD_FAST                'start'
              874  BUILD_TUPLE_2         2 
              876  LOAD_FAST                'lnum'
              878  LOAD_FAST                'end'
              880  BUILD_TUPLE_2         2 
              882  LOAD_FAST                'end'
              884  ROT_THREE        
              886  ROT_TWO          
              888  STORE_FAST               'spos'
              890  STORE_FAST               'epos'
              892  STORE_FAST               'pos'

 L. 587       894  LOAD_FAST                'start'
              896  LOAD_FAST                'end'
              898  COMPARE_OP               ==
          900_902  POP_JUMP_IF_FALSE   908  'to 908'

 L. 588   904_906  CONTINUE            824  'to 824'
            908_0  COME_FROM           900  '900'

 L. 589       908  LOAD_FAST                'line'
              910  LOAD_FAST                'start'
              912  LOAD_FAST                'end'
              914  BUILD_SLICE_2         2 
              916  BINARY_SUBSCR    
              918  LOAD_FAST                'line'
              920  LOAD_FAST                'start'
              922  BINARY_SUBSCR    
              924  ROT_TWO          
              926  STORE_FAST               'token'
              928  STORE_FAST               'initial'

 L. 591       930  LOAD_FAST                'initial'
              932  LOAD_FAST                'numchars'
              934  COMPARE_OP               in
          936_938  POP_JUMP_IF_TRUE    970  'to 970'

 L. 592       940  LOAD_FAST                'initial'
              942  LOAD_STR                 '.'
              944  COMPARE_OP               ==
          946_948  POP_JUMP_IF_FALSE   992  'to 992'
              950  LOAD_FAST                'token'
              952  LOAD_STR                 '.'
              954  COMPARE_OP               !=
          956_958  POP_JUMP_IF_FALSE   992  'to 992'
              960  LOAD_FAST                'token'
              962  LOAD_STR                 '...'
              964  COMPARE_OP               !=
          966_968  POP_JUMP_IF_FALSE   992  'to 992'
            970_0  COME_FROM           936  '936'

 L. 593       970  LOAD_GLOBAL              TokenInfo
              972  LOAD_GLOBAL              NUMBER
              974  LOAD_FAST                'token'
              976  LOAD_FAST                'spos'
              978  LOAD_FAST                'epos'
              980  LOAD_FAST                'line'
              982  CALL_FUNCTION_5       5  '5 positional arguments'
              984  YIELD_VALUE      
              986  POP_TOP          
          988_990  JUMP_ABSOLUTE      1524  'to 1524'
            992_0  COME_FROM           966  '966'
            992_1  COME_FROM           956  '956'
            992_2  COME_FROM           946  '946'

 L. 594       992  LOAD_FAST                'initial'
              994  LOAD_STR                 '\r\n'
              996  COMPARE_OP               in
         998_1000  POP_JUMP_IF_FALSE  1054  'to 1054'

 L. 595      1002  LOAD_FAST                'parenlev'
             1004  LOAD_CONST               0
             1006  COMPARE_OP               >
         1008_1010  POP_JUMP_IF_FALSE  1032  'to 1032'

 L. 596      1012  LOAD_GLOBAL              TokenInfo
             1014  LOAD_GLOBAL              NL
             1016  LOAD_FAST                'token'
             1018  LOAD_FAST                'spos'
             1020  LOAD_FAST                'epos'
             1022  LOAD_FAST                'line'
             1024  CALL_FUNCTION_5       5  '5 positional arguments'
             1026  YIELD_VALUE      
             1028  POP_TOP          
             1030  JUMP_ABSOLUTE      1524  'to 1524'
           1032_0  COME_FROM          1008  '1008'

 L. 598      1032  LOAD_GLOBAL              TokenInfo
             1034  LOAD_GLOBAL              NEWLINE
             1036  LOAD_FAST                'token'
             1038  LOAD_FAST                'spos'
             1040  LOAD_FAST                'epos'
             1042  LOAD_FAST                'line'
             1044  CALL_FUNCTION_5       5  '5 positional arguments'
             1046  YIELD_VALUE      
             1048  POP_TOP          
         1050_1052  JUMP_ABSOLUTE      1524  'to 1524'
           1054_0  COME_FROM           998  '998'

 L. 600      1054  LOAD_FAST                'initial'
             1056  LOAD_STR                 '#'
             1058  COMPARE_OP               ==
         1060_1062  POP_JUMP_IF_FALSE  1102  'to 1102'

 L. 601      1064  LOAD_FAST                'token'
             1066  LOAD_METHOD              endswith
             1068  LOAD_STR                 '\n'
             1070  CALL_METHOD_1         1  '1 positional argument'
         1072_1074  POP_JUMP_IF_FALSE  1080  'to 1080'
             1076  LOAD_GLOBAL              AssertionError
             1078  RAISE_VARARGS_1       1  'exception instance'
           1080_0  COME_FROM          1072  '1072'

 L. 602      1080  LOAD_GLOBAL              TokenInfo
             1082  LOAD_GLOBAL              COMMENT
             1084  LOAD_FAST                'token'
             1086  LOAD_FAST                'spos'
             1088  LOAD_FAST                'epos'
             1090  LOAD_FAST                'line'
             1092  CALL_FUNCTION_5       5  '5 positional arguments'
             1094  YIELD_VALUE      
             1096  POP_TOP          
         1098_1100  JUMP_ABSOLUTE      1524  'to 1524'
           1102_0  COME_FROM          1060  '1060'

 L. 604      1102  LOAD_FAST                'token'
             1104  LOAD_GLOBAL              triple_quoted
             1106  COMPARE_OP               in
         1108_1110  POP_JUMP_IF_FALSE  1218  'to 1218'

 L. 605      1112  LOAD_GLOBAL              _compile
             1114  LOAD_GLOBAL              endpats
             1116  LOAD_FAST                'token'
             1118  BINARY_SUBSCR    
             1120  CALL_FUNCTION_1       1  '1 positional argument'
             1122  STORE_FAST               'endprog'

 L. 606      1124  LOAD_FAST                'endprog'
             1126  LOAD_METHOD              match
             1128  LOAD_FAST                'line'
             1130  LOAD_FAST                'pos'
             1132  CALL_METHOD_2         2  '2 positional arguments'
             1134  STORE_FAST               'endmatch'

 L. 607      1136  LOAD_FAST                'endmatch'
         1138_1140  POP_JUMP_IF_FALSE  1188  'to 1188'

 L. 608      1142  LOAD_FAST                'endmatch'
             1144  LOAD_METHOD              end
             1146  LOAD_CONST               0
             1148  CALL_METHOD_1         1  '1 positional argument'
             1150  STORE_FAST               'pos'

 L. 609      1152  LOAD_FAST                'line'
             1154  LOAD_FAST                'start'
             1156  LOAD_FAST                'pos'
             1158  BUILD_SLICE_2         2 
             1160  BINARY_SUBSCR    
             1162  STORE_FAST               'token'

 L. 610      1164  LOAD_GLOBAL              TokenInfo
             1166  LOAD_GLOBAL              STRING
             1168  LOAD_FAST                'token'
             1170  LOAD_FAST                'spos'
             1172  LOAD_FAST                'lnum'
             1174  LOAD_FAST                'pos'
             1176  BUILD_TUPLE_2         2 
             1178  LOAD_FAST                'line'
             1180  CALL_FUNCTION_5       5  '5 positional arguments'
             1182  YIELD_VALUE      
             1184  POP_TOP          
             1186  JUMP_ABSOLUTE      1524  'to 1524'
           1188_0  COME_FROM          1138  '1138'

 L. 612      1188  LOAD_FAST                'lnum'
             1190  LOAD_FAST                'start'
             1192  BUILD_TUPLE_2         2 
             1194  STORE_FAST               'strstart'

 L. 613      1196  LOAD_FAST                'line'
             1198  LOAD_FAST                'start'
             1200  LOAD_CONST               None
             1202  BUILD_SLICE_2         2 
             1204  BINARY_SUBSCR    
             1206  STORE_FAST               'contstr'

 L. 614      1208  LOAD_FAST                'line'
             1210  STORE_FAST               'contline'

 L. 615      1212  BREAK_LOOP       
         1214_1216  JUMP_ABSOLUTE      1524  'to 1524'
           1218_0  COME_FROM          1108  '1108'

 L. 627      1218  LOAD_FAST                'initial'
             1220  LOAD_GLOBAL              single_quoted
             1222  COMPARE_OP               in
         1224_1226  POP_JUMP_IF_TRUE   1264  'to 1264'

 L. 628      1228  LOAD_FAST                'token'
             1230  LOAD_CONST               None
             1232  LOAD_CONST               2
             1234  BUILD_SLICE_2         2 
             1236  BINARY_SUBSCR    
             1238  LOAD_GLOBAL              single_quoted
             1240  COMPARE_OP               in
         1242_1244  POP_JUMP_IF_TRUE   1264  'to 1264'

 L. 629      1246  LOAD_FAST                'token'
             1248  LOAD_CONST               None
             1250  LOAD_CONST               3
             1252  BUILD_SLICE_2         2 
             1254  BINARY_SUBSCR    
             1256  LOAD_GLOBAL              single_quoted
             1258  COMPARE_OP               in
         1260_1262  POP_JUMP_IF_FALSE  1378  'to 1378'
           1264_0  COME_FROM          1242  '1242'
           1264_1  COME_FROM          1224  '1224'

 L. 630      1264  LOAD_FAST                'token'
             1266  LOAD_CONST               -1
             1268  BINARY_SUBSCR    
             1270  LOAD_STR                 '\n'
             1272  COMPARE_OP               ==
         1274_1276  POP_JUMP_IF_FALSE  1358  'to 1358'

 L. 631      1278  LOAD_FAST                'lnum'
             1280  LOAD_FAST                'start'
             1282  BUILD_TUPLE_2         2 
             1284  STORE_FAST               'strstart'

 L. 638      1286  LOAD_GLOBAL              _compile
             1288  LOAD_GLOBAL              endpats
             1290  LOAD_METHOD              get
             1292  LOAD_FAST                'initial'
             1294  CALL_METHOD_1         1  '1 positional argument'
         1296_1298  JUMP_IF_TRUE_OR_POP  1328  'to 1328'

 L. 639      1300  LOAD_GLOBAL              endpats
             1302  LOAD_METHOD              get
             1304  LOAD_FAST                'token'
             1306  LOAD_CONST               1
             1308  BINARY_SUBSCR    
             1310  CALL_METHOD_1         1  '1 positional argument'
         1312_1314  JUMP_IF_TRUE_OR_POP  1328  'to 1328'

 L. 640      1316  LOAD_GLOBAL              endpats
             1318  LOAD_METHOD              get
             1320  LOAD_FAST                'token'
             1322  LOAD_CONST               2
             1324  BINARY_SUBSCR    
             1326  CALL_METHOD_1         1  '1 positional argument'
           1328_0  COME_FROM          1312  '1312'
           1328_1  COME_FROM          1296  '1296'
             1328  CALL_FUNCTION_1       1  '1 positional argument'
             1330  STORE_FAST               'endprog'

 L. 641      1332  LOAD_FAST                'line'
             1334  LOAD_FAST                'start'
             1336  LOAD_CONST               None
             1338  BUILD_SLICE_2         2 
             1340  BINARY_SUBSCR    
             1342  LOAD_CONST               1
             1344  ROT_TWO          
             1346  STORE_FAST               'contstr'
             1348  STORE_FAST               'needcont'

 L. 642      1350  LOAD_FAST                'line'
             1352  STORE_FAST               'contline'

 L. 643      1354  BREAK_LOOP       
             1356  JUMP_FORWARD       1376  'to 1376'
           1358_0  COME_FROM          1274  '1274'

 L. 645      1358  LOAD_GLOBAL              TokenInfo
             1360  LOAD_GLOBAL              STRING
             1362  LOAD_FAST                'token'
             1364  LOAD_FAST                'spos'
             1366  LOAD_FAST                'epos'
             1368  LOAD_FAST                'line'
             1370  CALL_FUNCTION_5       5  '5 positional arguments'
             1372  YIELD_VALUE      
             1374  POP_TOP          
           1376_0  COME_FROM          1356  '1356'
             1376  JUMP_FORWARD       1480  'to 1480'
           1378_0  COME_FROM          1260  '1260'

 L. 647      1378  LOAD_FAST                'initial'
             1380  LOAD_METHOD              isidentifier
             1382  CALL_METHOD_0         0  '0 positional arguments'
         1384_1386  POP_JUMP_IF_FALSE  1408  'to 1408'

 L. 648      1388  LOAD_GLOBAL              TokenInfo
             1390  LOAD_GLOBAL              NAME
             1392  LOAD_FAST                'token'
             1394  LOAD_FAST                'spos'
             1396  LOAD_FAST                'epos'
             1398  LOAD_FAST                'line'
             1400  CALL_FUNCTION_5       5  '5 positional arguments'
             1402  YIELD_VALUE      
             1404  POP_TOP          
             1406  JUMP_FORWARD       1480  'to 1480'
           1408_0  COME_FROM          1384  '1384'

 L. 649      1408  LOAD_FAST                'initial'
             1410  LOAD_STR                 '\\'
             1412  COMPARE_OP               ==
         1414_1416  POP_JUMP_IF_FALSE  1424  'to 1424'

 L. 650      1418  LOAD_CONST               1
             1420  STORE_FAST               'continued'
             1422  JUMP_FORWARD       1480  'to 1480'
           1424_0  COME_FROM          1414  '1414'

 L. 652      1424  LOAD_FAST                'initial'
             1426  LOAD_STR                 '([{'
             1428  COMPARE_OP               in
         1430_1432  POP_JUMP_IF_FALSE  1444  'to 1444'

 L. 653      1434  LOAD_FAST                'parenlev'
             1436  LOAD_CONST               1
             1438  INPLACE_ADD      
             1440  STORE_FAST               'parenlev'
             1442  JUMP_FORWARD       1462  'to 1462'
           1444_0  COME_FROM          1430  '1430'

 L. 654      1444  LOAD_FAST                'initial'
             1446  LOAD_STR                 ')]}'
             1448  COMPARE_OP               in
         1450_1452  POP_JUMP_IF_FALSE  1462  'to 1462'

 L. 655      1454  LOAD_FAST                'parenlev'
             1456  LOAD_CONST               1
             1458  INPLACE_SUBTRACT 
             1460  STORE_FAST               'parenlev'
           1462_0  COME_FROM          1450  '1450'
           1462_1  COME_FROM          1442  '1442'

 L. 656      1462  LOAD_GLOBAL              TokenInfo
             1464  LOAD_GLOBAL              OP
             1466  LOAD_FAST                'token'
             1468  LOAD_FAST                'spos'
             1470  LOAD_FAST                'epos'
             1472  LOAD_FAST                'line'
             1474  CALL_FUNCTION_5       5  '5 positional arguments'
             1476  YIELD_VALUE      
             1478  POP_TOP          
           1480_0  COME_FROM          1422  '1422'
           1480_1  COME_FROM          1406  '1406'
           1480_2  COME_FROM          1376  '1376'
             1480  JUMP_BACK           824  'to 824'
           1482_0  COME_FROM           852  '852'

 L. 658      1482  LOAD_GLOBAL              TokenInfo
             1484  LOAD_GLOBAL              ERRORTOKEN
             1486  LOAD_FAST                'line'
             1488  LOAD_FAST                'pos'
             1490  BINARY_SUBSCR    

 L. 659      1492  LOAD_FAST                'lnum'
             1494  LOAD_FAST                'pos'
             1496  BUILD_TUPLE_2         2 
             1498  LOAD_FAST                'lnum'
             1500  LOAD_FAST                'pos'
             1502  LOAD_CONST               1
             1504  BINARY_ADD       
             1506  BUILD_TUPLE_2         2 
             1508  LOAD_FAST                'line'
             1510  CALL_FUNCTION_5       5  '5 positional arguments'
             1512  YIELD_VALUE      
             1514  POP_TOP          

 L. 660      1516  LOAD_FAST                'pos'
             1518  LOAD_CONST               1
             1520  INPLACE_ADD      
             1522  STORE_FAST               'pos'
         1524_1526  JUMP_BACK           824  'to 824'
           1528_0  COME_FROM           830  '830'
             1528  POP_BLOCK        
           1530_0  COME_FROM_LOOP      820  '820'
             1530  JUMP_BACK            84  'to 84'
             1532  POP_BLOCK        
           1534_0  COME_FROM_LOOP       80  '80'

 L. 663      1534  LOAD_FAST                'last_line'
         1536_1538  POP_JUMP_IF_FALSE  1600  'to 1600'
             1540  LOAD_FAST                'last_line'
             1542  LOAD_CONST               -1
             1544  BINARY_SUBSCR    
             1546  LOAD_STR                 '\r\n'
             1548  COMPARE_OP               not-in
         1550_1552  POP_JUMP_IF_FALSE  1600  'to 1600'

 L. 664      1554  LOAD_GLOBAL              TokenInfo
             1556  LOAD_GLOBAL              NEWLINE
             1558  LOAD_STR                 ''
             1560  LOAD_FAST                'lnum'
             1562  LOAD_CONST               1
             1564  BINARY_SUBTRACT  
             1566  LOAD_GLOBAL              len
             1568  LOAD_FAST                'last_line'
             1570  CALL_FUNCTION_1       1  '1 positional argument'
             1572  BUILD_TUPLE_2         2 
             1574  LOAD_FAST                'lnum'
             1576  LOAD_CONST               1
             1578  BINARY_SUBTRACT  
             1580  LOAD_GLOBAL              len
             1582  LOAD_FAST                'last_line'
             1584  CALL_FUNCTION_1       1  '1 positional argument'
             1586  LOAD_CONST               1
             1588  BINARY_ADD       
             1590  BUILD_TUPLE_2         2 
             1592  LOAD_STR                 ''
             1594  CALL_FUNCTION_5       5  '5 positional arguments'
             1596  YIELD_VALUE      
             1598  POP_TOP          
           1600_0  COME_FROM          1550  '1550'
           1600_1  COME_FROM          1536  '1536'

 L. 665      1600  SETUP_LOOP         1650  'to 1650'
             1602  LOAD_FAST                'indents'
             1604  LOAD_CONST               1
             1606  LOAD_CONST               None
             1608  BUILD_SLICE_2         2 
             1610  BINARY_SUBSCR    
             1612  GET_ITER         
             1614  FOR_ITER           1648  'to 1648'
             1616  STORE_FAST               'indent'

 L. 666      1618  LOAD_GLOBAL              TokenInfo
             1620  LOAD_GLOBAL              DEDENT
             1622  LOAD_STR                 ''
             1624  LOAD_FAST                'lnum'
             1626  LOAD_CONST               0
             1628  BUILD_TUPLE_2         2 
             1630  LOAD_FAST                'lnum'
             1632  LOAD_CONST               0
             1634  BUILD_TUPLE_2         2 
             1636  LOAD_STR                 ''
             1638  CALL_FUNCTION_5       5  '5 positional arguments'
             1640  YIELD_VALUE      
             1642  POP_TOP          
         1644_1646  JUMP_BACK          1614  'to 1614'
             1648  POP_BLOCK        
           1650_0  COME_FROM_LOOP     1600  '1600'

 L. 667      1650  LOAD_GLOBAL              TokenInfo
             1652  LOAD_GLOBAL              ENDMARKER
             1654  LOAD_STR                 ''
             1656  LOAD_FAST                'lnum'
             1658  LOAD_CONST               0
             1660  BUILD_TUPLE_2         2 
             1662  LOAD_FAST                'lnum'
             1664  LOAD_CONST               0
             1666  BUILD_TUPLE_2         2 
             1668  LOAD_STR                 ''
             1670  CALL_FUNCTION_5       5  '5 positional arguments'
             1672  YIELD_VALUE      
             1674  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 714_0


def generate_tokens(readline):
    return _tokenize(readline, None)


def main():
    import argparse

    def perror(message):
        print(message, file=(sys.stderr))

    def error(message, filename=None, location=None):
        if location:
            args = (
             filename,) + location + (message,)
            perror('%s:%d:%d: error: %s' % args)
        else:
            if filename:
                perror('%s: error: %s' % (filename, message))
            else:
                perror('error: %s' % message)
        sys.exit(1)

    parser = argparse.ArgumentParser(prog='python -m tokenize')
    parser.add_argument(dest='filename', nargs='?', metavar='filename.py',
      help='the file to tokenize; defaults to stdin')
    parser.add_argument('-e', '--exact', dest='exact', action='store_true', help='display token names using the exact type')
    args = parser.parse_args()
    try:
        if args.filename:
            filename = args.filename
            with _builtin_open(filename, 'rb') as (f):
                tokens = list(tokenize(f.readline))
        else:
            filename = '<stdin>'
            tokens = _tokenize(sys.stdin.readline, None)
        for token in tokens:
            token_type = token.type
            if args.exact:
                token_type = token.exact_type
            token_range = '%d,%d-%d,%d:' % (token.start + token.end)
            print('%-20s%-15s%-15r' % (
             token_range, tok_name[token_type], token.string))

    except IndentationError as err:
        try:
            line, column = err.args[1][1:3]
            error(err.args[0], filename, (line, column))
        finally:
            err = None
            del err

    except TokenError as err:
        try:
            line, column = err.args[1]
            error(err.args[0], filename, (line, column))
        finally:
            err = None
            del err

    except SyntaxError as err:
        try:
            error(err, filename)
        finally:
            err = None
            del err

    except OSError as err:
        try:
            error(err)
        finally:
            err = None
            del err

    except KeyboardInterrupt:
        print('interrupted\n')
    except Exception as err:
        try:
            perror('unexpected error: %s' % err)
            raise
        finally:
            err = None
            del err


if __name__ == '__main__':
    main()
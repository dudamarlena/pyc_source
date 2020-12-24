# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/Projects/chris/various/pdfminer/venv/lib/python2.7/site-packages/pdfminer/psparser.py
# Compiled at: 2015-11-01 11:43:45
import re, logging, six
from .settings import STRICT

def bytesindex(s, i, j=None):
    """implements s[i], s[i:], s[i:j] for Python2 and Python3"""
    if i < 0:
        i = len(s) + i
    if j is None:
        j = i + 1
    if j < 0:
        j = len(s)
    return s[i:j]


from .utils import choplist

class PSException(Exception):
    pass


class PSEOF(PSException):
    pass


class PSSyntaxError(PSException):
    pass


class PSTypeError(PSException):
    pass


class PSValueError(PSException):
    pass


class PSObject(object):
    """Base class for all PS or PDF-related data types."""
    pass


class PSLiteral(PSObject):
    """A class that represents a PostScript literal.

    Postscript literals are used as identifiers, such as
    variable names, property names and dictionary keys.
    Literals are case sensitive and denoted by a preceding
    slash sign (e.g. "/Name")

    Note: Do not create an instance of PSLiteral directly.
    Always use PSLiteralTable.intern().
    """

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        name = self.name
        return '/%r' % name


class PSKeyword(PSObject):
    """A class that represents a PostScript keyword.

    PostScript keywords are a dozen of predefined words.
    Commands and directives in PostScript are expressed by keywords.
    They are also used to denote the content boundaries.

    Note: Do not create an instance of PSKeyword directly.
    Always use PSKeywordTable.intern().
    """

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        name = self.name
        return '/%r' % name


class PSSymbolTable(object):
    """A utility class for storing PSLiteral/PSKeyword objects.

    Interned objects can be checked its identity with "is" operator.
    """

    def __init__(self, klass):
        self.dict = {}
        self.klass = klass

    def intern(self, name):
        if name in self.dict:
            lit = self.dict[name]
        else:
            lit = self.klass(name)
            self.dict[name] = lit
        return lit


PSLiteralTable = PSSymbolTable(PSLiteral)
PSKeywordTable = PSSymbolTable(PSKeyword)
LIT = PSLiteralTable.intern
KWD = PSKeywordTable.intern
KEYWORD_PROC_BEGIN = KWD('{')
KEYWORD_PROC_END = KWD('}')
KEYWORD_ARRAY_BEGIN = KWD('[')
KEYWORD_ARRAY_END = KWD(']')
KEYWORD_DICT_BEGIN = KWD('<<')
KEYWORD_DICT_END = KWD('>>')

def literal_name(x):
    if not isinstance(x, PSLiteral):
        if STRICT:
            raise PSTypeError('Literal required: %r' % x)
        else:
            name = x
    else:
        name = x.name
        if six.PY3:
            try:
                name = str(name, 'utf-8')
            except:
                pass

    return name


def keyword_name(x):
    if not isinstance(x, PSKeyword):
        if STRICT:
            raise PSTypeError('Keyword required: %r' % x)
        else:
            name = x
    else:
        name = x.name
        if six.PY3:
            try:
                name = str(name, 'utf-8')
            except:
                pass

    return name


EOL = re.compile('[\\r\\n]')
SPC = re.compile('\\s')
NONSPC = re.compile('\\S')
HEX = re.compile('[0-9a-fA-F]')
END_LITERAL = re.compile('[#/%\\[\\]()<>{}\\s]')
END_HEX_STRING = re.compile('[^\\s0-9a-fA-F]')
HEX_PAIR = re.compile('[0-9a-fA-F]{2}|.')
END_NUMBER = re.compile('[^0-9]')
END_KEYWORD = re.compile('[#/%\\[\\]()<>{}\\s]')
END_STRING = re.compile('[()\\134]')
OCT_STRING = re.compile('[0-7]')
ESC_STRING = {'b': 8, 't': 9, 'n': 10, 'f': 12, 'r': 13, '(': 40, ')': 41, '\\': 92}

class PSBaseParser(object):
    """Most basic PostScript parser that performs only tokenization.
    """
    BUFSIZ = 4096

    def __init__(self, fp):
        self.fp = fp
        self.seek(0)

    def __repr__(self):
        return '<%s: %r, bufpos=%d>' % (self.__class__.__name__, self.fp, self.bufpos)

    def flush(self):
        pass

    def close(self):
        self.flush()

    def tell(self):
        return self.bufpos + self.charpos

    def poll(self, pos=None, n=80):
        pos0 = self.fp.tell()
        if not pos:
            pos = self.bufpos + self.charpos
        self.fp.seek(pos)
        logging.info('poll(%d): %r', pos, self.fp.read(n))
        self.fp.seek(pos0)

    def seek(self, pos):
        """Seeks the parser to the given position.
        """
        logging.debug('seek: %r', pos)
        self.fp.seek(pos)
        self.bufpos = pos
        self.buf = ''
        self.charpos = 0
        self._parse1 = self._parse_main
        self._curtoken = ''
        self._curtokenpos = 0
        self._tokens = []

    def fillbuf(self):
        if self.charpos < len(self.buf):
            return
        self.bufpos = self.fp.tell()
        self.buf = self.fp.read(self.BUFSIZ)
        if not self.buf:
            raise PSEOF('Unexpected EOF')
        self.charpos = 0

    def nextline(self):
        r"""Fetches a next line that ends either with \r or \n.
        """
        linebuf = ''
        linepos = self.bufpos + self.charpos
        eol = False
        while 1:
            self.fillbuf()
            if eol:
                c = bytesindex(self.buf, self.charpos)
                if c == '\n':
                    linebuf += c
                    self.charpos += 1
                break
            m = EOL.search(self.buf, self.charpos)
            if m:
                linebuf += bytesindex(self.buf, self.charpos, m.end(0))
                self.charpos = m.end(0)
                if bytesindex(linebuf, -1) == '\r':
                    eol = True
                else:
                    break
            else:
                linebuf += bytesindex(self.buf, self.charpos, -1)
                self.charpos = len(self.buf)

        logging.debug('nextline: %r, %r', linepos, linebuf)
        return (
         linepos, linebuf)

    def revreadlines(self):
        """Fetches a next line backword.

        This is used to locate the trailers at the end of a file.
        """
        self.fp.seek(0, 2)
        pos = self.fp.tell()
        buf = ''
        while 0 < pos:
            prevpos = pos
            pos = max(0, pos - self.BUFSIZ)
            self.fp.seek(pos)
            s = self.fp.read(prevpos - pos)
            if not s:
                break
            while 1:
                n = max(s.rfind('\r'), s.rfind('\n'))
                if n == -1:
                    buf = s + buf
                    break
                yield bytesindex(s, n, -1) + buf
                s = bytesindex(s, 0, n)
                buf = ''

    def _parse_main(self, s, i):
        m = NONSPC.search(s, i)
        if not m:
            return len(s)
        else:
            j = m.start(0)
            c = bytesindex(s, j)
            self._curtokenpos = self.bufpos + j
            if c == '%':
                self._curtoken = '%'
                self._parse1 = self._parse_comment
                return j + 1
            if c == '/':
                self._curtoken = ''
                self._parse1 = self._parse_literal
                return j + 1
            if c in '-+' or c.isdigit():
                self._curtoken = c
                self._parse1 = self._parse_number
                return j + 1
            if c == '.':
                self._curtoken = c
                self._parse1 = self._parse_float
                return j + 1
            if c.isalpha():
                self._curtoken = c
                self._parse1 = self._parse_keyword
                return j + 1
            if c == '(':
                self._curtoken = ''
                self.paren = 1
                self._parse1 = self._parse_string
                return j + 1
            if c == '<':
                self._curtoken = ''
                self._parse1 = self._parse_wopen
                return j + 1
            if c == '>':
                self._curtoken = ''
                self._parse1 = self._parse_wclose
                return j + 1
            self._add_token(KWD(c))
            return j + 1

    def _add_token(self, obj):
        self._tokens.append((self._curtokenpos, obj))

    def _parse_comment(self, s, i):
        m = EOL.search(s, i)
        if not m:
            self._curtoken += bytesindex(s, i, -1)
            return (
             self._parse_comment, len(s))
        j = m.start(0)
        self._curtoken += bytesindex(s, i, j)
        self._parse1 = self._parse_main
        return j

    def _parse_literal(self, s, i):
        m = END_LITERAL.search(s, i)
        if not m:
            self._curtoken += bytesindex(s, i, -1)
            return len(s)
        j = m.start(0)
        self._curtoken += bytesindex(s, i, j)
        c = bytesindex(s, j)
        if c == '#':
            self.hex = ''
            self._parse1 = self._parse_literal_hex
            return j + 1
        try:
            self._curtoken = str(self._curtoken, 'utf-8')
        except:
            pass

        self._add_token(LIT(self._curtoken))
        self._parse1 = self._parse_main
        return j

    def _parse_literal_hex(self, s, i):
        c = bytesindex(s, i)
        if HEX.match(c) and len(self.hex) < 2:
            self.hex += c
            return i + 1
        if self.hex:
            self._curtoken += six.int2byte(int(self.hex, 16))
        self._parse1 = self._parse_literal
        return i

    def _parse_number(self, s, i):
        m = END_NUMBER.search(s, i)
        if not m:
            self._curtoken += bytesindex(s, i, -1)
            return len(s)
        j = m.start(0)
        self._curtoken += bytesindex(s, i, j)
        c = bytesindex(s, j)
        if c == '.':
            self._curtoken += c
            self._parse1 = self._parse_float
            return j + 1
        try:
            self._add_token(int(self._curtoken))
        except ValueError:
            pass

        self._parse1 = self._parse_main
        return j

    def _parse_float(self, s, i):
        m = END_NUMBER.search(s, i)
        if not m:
            self._curtoken += bytesindex(s, i, -1)
            return len(s)
        j = m.start(0)
        self._curtoken += bytesindex(s, i, j)
        try:
            self._add_token(float(self._curtoken))
        except ValueError:
            pass

        self._parse1 = self._parse_main
        return j

    def _parse_keyword(self, s, i):
        m = END_KEYWORD.search(s, i)
        if not m:
            self._curtoken += bytesindex(s, i, -1)
            return len(s)
        j = m.start(0)
        self._curtoken += bytesindex(s, i, j)
        if self._curtoken == 'true':
            token = True
        elif self._curtoken == 'false':
            token = False
        else:
            token = KWD(self._curtoken)
        self._add_token(token)
        self._parse1 = self._parse_main
        return j

    def _parse_string(self, s, i):
        m = END_STRING.search(s, i)
        if not m:
            self._curtoken += bytesindex(s, i, -1)
            return len(s)
        j = m.start(0)
        self._curtoken += bytesindex(s, i, j)
        c = bytesindex(s, j)
        if c == '\\':
            self.oct = ''
            self._parse1 = self._parse_string_1
            return j + 1
        if c == '(':
            self.paren += 1
            self._curtoken += c
            return j + 1
        if c == ')':
            self.paren -= 1
            if self.paren:
                self._curtoken += c
                return j + 1
        self._add_token(self._curtoken)
        self._parse1 = self._parse_main
        return j + 1

    def _parse_string_1(self, s, i):
        c = bytesindex(s, i)
        if OCT_STRING.match(c) and len(self.oct) < 3:
            self.oct += c
            return i + 1
        if self.oct:
            self._curtoken += six.int2byte(int(self.oct, 8))
            self._parse1 = self._parse_string
            return i
        if c in ESC_STRING:
            self._curtoken += six.int2byte(ESC_STRING[c])
        self._parse1 = self._parse_string
        return i + 1

    def _parse_wopen(self, s, i):
        c = bytesindex(s, i)
        if c == '<':
            self._add_token(KEYWORD_DICT_BEGIN)
            self._parse1 = self._parse_main
            i += 1
        else:
            self._parse1 = self._parse_hexstring
        return i

    def _parse_wclose(self, s, i):
        c = bytesindex(s, i)
        if c == '>':
            self._add_token(KEYWORD_DICT_END)
            i += 1
        self._parse1 = self._parse_main
        return i

    def _parse_hexstring(self, s, i):
        m = END_HEX_STRING.search(s, i)
        if not m:
            self._curtoken += bytesindex(s, i, -1)
            return len(s)
        j = m.start(0)
        self._curtoken += bytesindex(s, i, j)
        token = HEX_PAIR.sub(lambda m: six.int2byte(int(m.group(0), 16)), SPC.sub('', self._curtoken))
        self._add_token(token)
        self._parse1 = self._parse_main
        return j

    def nexttoken(self):
        while not self._tokens:
            self.fillbuf()
            self.charpos = self._parse1(self.buf, self.charpos)

        token = self._tokens.pop(0)
        logging.debug('nexttoken: %r', token)
        return token


class PSStackParser(PSBaseParser):

    def __init__(self, fp):
        PSBaseParser.__init__(self, fp)
        self.reset()

    def reset(self):
        self.context = []
        self.curtype = None
        self.curstack = []
        self.results = []
        return

    def seek(self, pos):
        PSBaseParser.seek(self, pos)
        self.reset()

    def push(self, *objs):
        self.curstack.extend(objs)

    def pop(self, n):
        objs = self.curstack[-n:]
        self.curstack[(-n):] = []
        return objs

    def popall(self):
        objs = self.curstack
        self.curstack = []
        return objs

    def add_results(self, *objs):
        try:
            logging.debug('add_results: %r', objs)
        except:
            logging.debug('add_results: (unprintable object)')

        self.results.extend(objs)

    def start_type(self, pos, type):
        self.context.append((pos, self.curtype, self.curstack))
        self.curtype, self.curstack = type, []
        logging.debug('start_type: pos=%r, type=%r', pos, type)

    def end_type(self, type):
        if self.curtype != type:
            raise PSTypeError('Type mismatch: %r != %r' % (self.curtype, type))
        objs = [ obj for _, obj in self.curstack ]
        pos, self.curtype, self.curstack = self.context.pop()
        logging.debug('end_type: pos=%r, type=%r, objs=%r', pos, type, objs)
        return (pos, objs)

    def do_keyword(self, pos, token):
        pass

    def nextobject(self):
        """Yields a list of objects.

        Returns keywords, literals, strings, numbers, arrays and dictionaries.
        Arrays and dictionaries are represented as Python lists and dictionaries.
        """
        while not self.results:
            pos, token = self.nexttoken()
            if isinstance(token, (six.integer_types, float, bool, six.string_types, six.binary_type, PSLiteral)):
                self.push((pos, token))
            elif token == KEYWORD_ARRAY_BEGIN:
                self.start_type(pos, 'a')
            elif token == KEYWORD_ARRAY_END:
                try:
                    self.push(self.end_type('a'))
                except PSTypeError:
                    if STRICT:
                        raise

            elif token == KEYWORD_DICT_BEGIN:
                self.start_type(pos, 'd')
            elif token == KEYWORD_DICT_END:
                try:
                    pos, objs = self.end_type('d')
                    if len(objs) % 2 != 0:
                        raise PSSyntaxError('Invalid dictionary construct: %r' % objs)
                    d = dict((literal_name(k), v) for k, v in choplist(2, objs) if v is not None)
                    self.push((pos, d))
                except PSTypeError:
                    if STRICT:
                        raise

            elif token == KEYWORD_PROC_BEGIN:
                self.start_type(pos, 'p')
            elif token == KEYWORD_PROC_END:
                try:
                    self.push(self.end_type('p'))
                except PSTypeError:
                    if STRICT:
                        raise

            elif isinstance(token, PSKeyword):
                logging.debug('do_keyword: pos=%r, token=%r, stack=%r', pos, token, self.curstack)
                self.do_keyword(pos, token)
            else:
                logging.error('unknown token: pos=%r, token=%r, stack=%r', pos, token, self.curstack)
                self.do_keyword(pos, token)
                raise
            if self.context:
                continue
            else:
                self.flush()

        obj = self.results.pop(0)
        try:
            logging.debug('nextobject: %r', obj)
        except:
            logging.debug('nextobject: (unprintable object)')

        return obj
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zif/jsonserver/minjson.py
# Compiled at: 2007-05-25 16:54:18
from re import compile, sub, search, DOTALL
from token import ENDMARKER, NAME, NUMBER, STRING, OP, ERRORTOKEN
from tokenize import tokenize, TokenError, NL
emergencyEncoding = 'utf-8'

class ReadException(Exception):
    __module__ = __name__


class WriteException(Exception):
    __module__ = __name__


slashstarcomment = compile('/\\*.*?\\*/', DOTALL)
doubleslashcomment = compile('//.*\\n')
unichrRE = compile('\\\\u[0-9a-fA-F]{4,4}')

def unichrReplace(match):
    return unichr(int(match.group()[2:], 16))


escapeStrs = (
 ('\n', '\\n'), ('\x08', '\\b'), ('\x0c', '\\f'), ('\t', '\\t'), ('\r', '\\r'), ('"', '\\"'))

class DictToken:
    __module__ = __name__
    __slots__ = []


class ListToken:
    __module__ = __name__
    __slots__ = []


class ColonToken:
    __module__ = __name__
    __slots__ = []


class CommaToken:
    __module__ = __name__
    __slots__ = []


class JSONReader(object):
    """raise SyntaxError if it is not JSON, and make the object available"""
    __module__ = __name__

    def __init__(self, data):
        self.stop = False
        self._data = iter([data])
        self.lastOp = None
        self.objects = []
        self.tokenize()
        return

    def tokenize(self):
        try:
            tokenize(self._data.next, self.readTokens)
        except TokenError:
            raise SyntaxError

    def resolveList(self):
        if isinstance(self.objects[(-1)], ListToken):
            self.objects[-1] = []
            return
        theList = []
        commaCount = 0
        try:
            item = self.objects.pop()
        except IndexError:
            raise SyntaxError

        while not isinstance(item, ListToken):
            if isinstance(item, CommaToken):
                commaCount += 1
            else:
                theList.append(item)
            try:
                item = self.objects.pop()
            except IndexError:
                raise SyntaxError

        if not commaCount == len(theList) - 1:
            raise SyntaxError
        theList.reverse()
        item = theList
        self.objects.append(item)

    def resolveDict(self):
        theList = []
        if isinstance(self.objects[(-1)], DictToken):
            self.objects[-1] = {}
            return
        try:
            value = self.objects.pop()
        except IndexError:
            raise SyntaxError

        try:
            colon = self.objects.pop()
            if not isinstance(colon, ColonToken):
                raise SyntaxError
        except IndexError:
            raise SyntaxError

        try:
            key = self.objects.pop()
            if not isinstance(key, basestring):
                raise SyntaxError
        except IndexError:
            raise SyntaxError

        comma = value
        while not isinstance(comma, DictToken):
            theList.append((key, value))
            try:
                comma = self.objects.pop()
            except IndexError:
                raise SyntaxError

            if isinstance(comma, CommaToken):
                try:
                    value = self.objects.pop()
                except IndexError:
                    raise SyntaxError
                else:
                    try:
                        colon = self.objects.pop()
                        if not isinstance(colon, ColonToken):
                            raise SyntaxError
                    except IndexError:
                        raise SyntaxError
                    else:
                        try:
                            key = self.objects.pop()
                            if not isinstance(key, basestring):
                                raise SyntaxError
                        except IndexError:
                            raise SyntaxError

        theDict = {}
        for k in theList:
            theDict[k[0]] = k[1]

        self.objects.append(theDict)

    def readTokens(self, type, token, (srow, scol), (erow, ecol), line):
        if type == OP:
            if token not in '[{}],:-':
                raise SyntaxError
            else:
                self.lastOp = token
            if token == '[':
                self.objects.append(ListToken())
            elif token == '{':
                self.objects.append(DictToken())
            elif token == ']':
                self.resolveList()
            elif token == '}':
                self.resolveDict()
            elif token == ':':
                self.objects.append(ColonToken())
            elif token == ',':
                self.objects.append(CommaToken())
        elif type == STRING:
            tok = token[1:-1]
            parts = tok.split('\\\\')
            for k in escapeStrs:
                if k[1] in tok:
                    parts = [ part.replace(k[1], k[0]) for part in parts ]

            self.objects.append(('\\').join(parts))
        elif type == NUMBER:
            if self.lastOp == '-':
                factor = -1
            else:
                factor = 1
            try:
                self.objects.append(factor * int(token))
            except ValueError:
                self.objects.append(factor * float(token))

        elif type == NAME:
            try:
                self.objects.append({'true': True, 'false': False, 'null': None}[token])
            except KeyError:
                raise SyntaxError

        elif type == ENDMARKER:
            pass
        elif type == NL:
            pass
        elif type == ERRORTOKEN:
            if ecol == len(line):
                pass
            else:
                raise SyntaxError
        else:
            raise SyntaxError
        return

    def output(self):
        try:
            assert len(self.objects) == 1
        except AssertionError:
            raise SyntaxError

        return self.objects[0]


def safeRead(aString, encoding=None):
    """read the js, first sanitizing a bit and removing any c-style comments
    If the input is a unicode string, great.  That's preferred.  If the input 
    is a byte string, strings in the object will be produced as unicode anyway.
    """
    CHR0 = chr(0)
    while aString.endswith(CHR0):
        aString = aString[:-1]

    aString = aString.strip()
    aString = slashstarcomment.sub('', aString)
    aString = doubleslashcomment.sub('', aString)
    unicodechars = unichrRE.search(aString)
    if unicodechars:
        aString = unichrRE.sub(unichrReplace, aString)
    if isinstance(aString, unicode):
        s = aString
    else:
        if encoding:
            s = unicode(aString, encoding)
        else:
            try:
                s = unicode(aString)
            except UnicodeDecodeError:
                enc = emergencyEncoding
                s = unicode(aString, enc)

        try:
            data = JSONReader(s).output()
        except SyntaxError:
            raise ReadException, 'Unacceptable JSON expression: %s' % aString

    return data


read = safeRead
import re, codecs
from cStringIO import StringIO

def jsonreplace_handler(exc):
    r"""Error handler for json

    If encoding fails, \uxxxx must be emitted. This
    is similar to the "backshashreplace" handler, only
    that we never emit \xnn since this is not legal
    according to the JSON syntax specs.
    """
    if isinstance(exc, UnicodeEncodeError):
        part = exc.object[exc.start]
        return (
         '\\u%04x' % ord(part), exc.start + 1)
    else:
        raise exc


codecs.register_error('jsonreplace', jsonreplace_handler)

def write(input, encoding='utf-8', outputEncoding=None):
    writer = JsonWriter(input_encoding=encoding, output_encoding=outputEncoding)
    writer.write(input)
    return writer.getvalue()


re_strmangle = re.compile('"|\x08|\x0c|\n|\r|\t|\\\\')

def func_strmangle(match):
    return {'"': '\\"', '\x08': '\\b', '\x0c': '\\f', '\n': '\\n', '\r': '\\r', '\t': '\\t', '\\': '\\\\'}[match.group(0)]


def strmangle(text):
    return re_strmangle.sub(func_strmangle, text)


class JsonStream(object):
    __module__ = __name__

    def __init__(self):
        self.buf = []

    def write(self, text):
        self.buf.append(text)

    def getvalue(self):
        return ('').join(self.buf)


class JsonWriter(object):
    __module__ = __name__

    def __init__(self, stream=None, input_encoding='utf-8', output_encoding=None):
        """
        - stream is optional, if specified must also give output_encoding
        - The input strings can be unicode or in input_encoding
        - output_encoding is optional, if omitted, result will be unicode
        """
        if stream is not None:
            if output_encoding is None:
                raise WriteException, 'If a stream is given, output encoding must also be provided'
        else:
            stream = JsonStream()
        self.stream = stream
        self.input_encoding = input_encoding
        self.output_encoding = output_encoding
        return

    def write(self, obj):
        if isinstance(obj, (list, tuple)):
            self.stream.write('[')
            first = True
            for elem in obj:
                if first:
                    first = False
                else:
                    self.stream.write(',')
                self.write(elem)

            (
             self.stream.write(']'),)
        elif isinstance(obj, dict):
            self.stream.write('{')
            first = True
            for (key, value) in obj.iteritems():
                if first:
                    first = False
                else:
                    self.stream.write(',')
                self.write(key)
                self.stream.write(':')
                self.write(value)

            self.stream.write('}')
        elif obj is True:
            self.stream.write('true')
        elif obj is False:
            self.stream.write('false')
        elif obj is None:
            self.stream.write('null')
        elif not isinstance(obj, basestring):
            try:
                obj = str(obj)
            except Exception, exc:
                raise WriteException, 'Cannot write object (%s: %s)' % (exc.__class__, exc)
            else:
                self.stream.write(obj)
        else:
            if not isinstance(obj, unicode):
                try:
                    obj = unicode(obj, self.input_encoding)
                except (UnicodeDecodeError, UnicodeTranslateError):
                    obj = unicode(obj, 'utf-8', 'replace')

            obj = strmangle(obj)
            if self.output_encoding is not None:
                obj = obj.encode(self.output_encoding, 'jsonreplace')
            self.stream.write('"')
            self.stream.write(obj)
            self.stream.write('"')
        return

    def getvalue(self):
        return self.stream.getvalue()
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sparrow/ntriples.py
# Compiled at: 2009-07-20 09:57:48
"""
N-Triples Parser
Copyright 2004, Sean B. Palmer, inamidst.com
Licensed under GPL 2, W3C, BSD, MIT, or EFL 2
Documentation: 
   http://inamidst.com/proj/rdf/ntriples-doc

Command line usage: 
   ./ntriples.py <URI>    - parses URI as N-Triples
   ./ntriples.py --help   - prints out this help message
# @@ fully empty document?
"""
import re
uriref = '<([^:]+:[^\\s"<>]+)>'
literal = '"([^"\\\\]*(?:\\\\.[^"\\\\]*)*)"'
litinfo = '(?:@([a-z]+(?:-[a-z0-9]+)*)|\\^\\^' + uriref + ')?'
r_line = re.compile('([^\\r\\n]*)(?:\\r\\n|\\r|\\n)')
r_wspace = re.compile('[ \\t]*')
r_wspaces = re.compile('[ \\t]+')
r_tail = re.compile('[ \\t]*\\.[ \\t]*')
r_uriref = re.compile(uriref)
r_nodeid = re.compile('_:([A-Za-z][A-Za-z0-9]*)')
r_literal = re.compile(literal + litinfo)
bufsiz = 2048
validate = False

class Node(unicode):
    pass


class URI(Node):
    pass


class bNode(Node):
    pass


class Literal(Node):

    def __new__(cls, lit, lang=None, dtype=None):
        n = str(lang) + ' ' + str(dtype) + ' ' + lit
        return unicode.__new__(cls, n)


class Sink(object):

    def __init__(self):
        self.length = 0

    def triple(self, s, p, o):
        self.length += 1
        print (s, p, o)


class ParseError(Exception):
    pass


quot = {'t': '\t', 'n': '\n', 'r': '\r', '"': '"', '\\': '\\'}
r_safe = re.compile('([\\x20\\x21\\x23-\\x5B\\x5D-\\x7E]+)')
r_quot = re.compile('\\\\(t|n|r|"|\\\\)')
r_uniquot = re.compile('\\\\u([0-9A-F]{4})|\\\\U([0-9A-F]{8})')

def unquote(s):
    """Unquote an N-Triples string."""
    result = []
    while s:
        m = r_safe.match(s)
        if m:
            s = s[m.end():]
            result.append(m.group(1))
            continue
        m = r_quot.match(s)
        if m:
            s = s[2:]
            result.append(quot[m.group(1)])
            continue
        m = r_uniquot.match(s)
        if m:
            s = s[m.end():]
            (u, U) = m.groups()
            codepoint = int(u or U, 16)
            if codepoint > 1114111:
                raise ParseError('Disallowed codepoint: %08X' % codepoint)
            result.append(unichr(codepoint))
        elif s.startswith('\\'):
            raise ParseError('Illegal escape at: %s...' % s[:10])
        else:
            raise ParseError('Illegal literal character: %r' % s[0])

    return unicode(('').join(result))


if not validate:

    def unquote(s):
        return s.decode('unicode-escape')


r_hibyte = re.compile('([\\x80-\\xFF])')

def uriquote(uri):
    return r_hibyte.sub(lambda m: '%%%02X' % ord(m.group(1)), uri)


if not validate:

    def uriquote(uri):
        return uri


class NTriplesParser(object):
    """An N-Triples Parser.
      Usage: 
         p = NTriplesParser(sink=MySink())
         sink = p.parse(f) # file; use parsestring for a string
   """

    def __init__(self, sink=None):
        if sink is not None:
            self.sink = sink
        else:
            self.sink = Sink()
        return

    def parse(self, f):
        """Parse f as an N-Triples file."""
        if not hasattr(f, 'read'):
            raise ParseError('Item to parse must be a file-like object.')
        self.file = f
        self.buffer = ''
        while True:
            self.line = self.readline()
            if self.line is None:
                break
            try:
                self.parseline()
            except ParseError:
                raise ParseError('Invalid line: %r' % self.line)

        return self.sink

    def parsestring(self, s):
        """Parse s as an N-Triples string."""
        if not isinstance(s, basestring):
            raise ParseError('Item to parse must be a string instance.')
        from cStringIO import StringIO
        f = StringIO()
        f.write(s)
        f.seek(0)
        self.parse(f)

    def readline(self):
        """Read an N-Triples line from buffered input."""
        if not self.buffer:
            buffer = self.file.read(bufsiz)
            if not buffer:
                return
            self.buffer = buffer
        while True:
            m = r_line.match(self.buffer)
            if m:
                self.buffer = self.buffer[m.end():]
                return m.group(1)
            else:
                buffer = self.file.read(bufsiz)
                if not buffer:
                    raise ParseError('EOF in line')
                self.buffer += buffer

        return

    def parseline(self):
        self.eat(r_wspace)
        if not self.line or self.line.startswith('#'):
            return
        subject = self.subject()
        self.eat(r_wspaces)
        predicate = self.predicate()
        self.eat(r_wspaces)
        object = self.object()
        self.eat(r_tail)
        if self.line:
            raise ParseError('Trailing garbage')
        self.sink.triple(subject, predicate, object)

    def peek(self, token):
        return self.line.startswith(token)

    def eat(self, pattern):
        m = pattern.match(self.line)
        if not m:
            raise ParseError('Failed to eat %s' % pattern)
        self.line = self.line[m.end():]
        return m

    def subject(self):
        subj = self.uriref() or self.nodeid()
        if not subj:
            raise ParseError('Subject must be uriref or nodeID')
        return subj

    def predicate(self):
        pred = self.uriref()
        if not pred:
            raise ParseError('Predicate must be uriref')
        return pred

    def object(self):
        objt = self.uriref() or self.nodeid() or self.literal()
        if not objt:
            raise ParseError('Unrecognised object type')
        return objt

    def uriref(self):
        if self.peek('<'):
            uri = self.eat(r_uriref).group(1)
            uri = unquote(uri)
            uri = uriquote(uri)
            return URI(uri)
        return False

    def nodeid(self):
        if self.peek('_'):
            return bNode(self.eat(r_nodeid).group(1))
        return False

    def literal(self):
        if self.peek('"'):
            (lit, lang, dtype) = self.eat(r_literal).groups()
            if lang and dtype:
                raise ParseError("Can't have both a language and a datatype")
            lit = unquote(lit)
            return Literal(lit, lang, dtype)
        return False


def parseURI(uri):
    import urllib
    parser = NTriplesParser()
    u = urllib.urlopen(uri)
    sink = parser.parse(u)
    u.close()
    print 'Length of input:', sink.length


def main():
    import sys
    if len(sys.argv) == 2:
        parseURI(sys.argv[1])
    else:
        print __doc__


if __name__ == '__main__':
    main()
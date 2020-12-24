# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/compatibility/SimpleXMLWriter.py
# Compiled at: 2009-10-07 18:08:46
import re, sys, string
try:
    unicode('')
except NameError:

    def encode(s, encoding):
        return s


    _escape = re.compile('[&<>\\"\\x80-\\xff]+')
else:

    def encode(s, encoding):
        return s.encode(encoding)


    _escape = re.compile(eval('u"[&<>\\"\\u0080-\\uffff]+"'))

def encode_entity(text, pattern=_escape):

    def escape_entities(m):
        out = []
        for char in m.group():
            out.append('&#%d;' % ord(char))

        return string.join(out, '')

    return encode(pattern.sub(escape_entities, text), 'ascii')


del _escape

def escape_cdata(s, encoding=None, replace=string.replace):
    s = replace(s, '&', '&amp;')
    s = replace(s, '<', '&lt;')
    s = replace(s, '>', '&gt;')
    if encoding:
        try:
            return encode(s, encoding)
        except UnicodeError:
            return encode_entity(s)

    return s


def escape_attrib(s, encoding=None, replace=string.replace):
    s = replace(s, '&', '&amp;')
    s = replace(s, "'", '&apos;')
    s = replace(s, '"', '&quot;')
    s = replace(s, '<', '&lt;')
    s = replace(s, '>', '&gt;')
    if encoding:
        try:
            return encode(s, encoding)
        except UnicodeError:
            return encode_entity(s)

    return s


class XMLWriter:
    __module__ = __name__

    def __init__(self, file, encoding='us-ascii'):
        self.__write = file.write
        self.__open = 0
        self.__tags = []
        self.__data = []
        self.__encoding = encoding

    def __flush(self):
        if self.__open:
            self.__write('>')
            self.__open = 0
        if self.__data:
            data = string.join(self.__data, '')
            self.__write(escape_cdata(data, self.__encoding))
            self.__data = []

    def start(self, tag, attrib={}, **extra):
        self.__flush()
        tag = escape_cdata(tag, self.__encoding)
        self.__data = []
        self.__tags.append(tag)
        self.__write('<%s' % tag)
        if attrib or extra:
            attrib = attrib.copy()
            attrib.update(extra)
            attrib = attrib.items()
            attrib.sort()
            for (k, v) in attrib:
                k = escape_cdata(k, self.__encoding)
                v = escape_attrib(v, self.__encoding)
                self.__write(' %s="%s"' % (k, v))

        self.__open = 1
        return len(self.__tags) - 1

    def comment(self, comment):
        self.__flush()
        self.__write('<!-- %s -->\n' % escape_cdata(comment, self.__encoding))

    def data(self, text):
        self.__data.append(text)

    def end(self, tag=None):
        if tag:
            assert self.__tags, 'unbalanced end(%s)' % tag
            assert escape_cdata(tag, self.__encoding) == self.__tags[(-1)], 'expected end(%s), got %s' % (self.__tags[(-1)], tag)
        else:
            assert self.__tags, 'unbalanced end()'
        tag = self.__tags.pop()
        if self.__data:
            self.__flush()
        elif self.__open:
            self.__open = 0
            self.__write(' />')
            return
        self.__write('</%s>' % tag)

    def close(self, id):
        while len(self.__tags) > id:
            self.end()

    def element(self, tag, text=None, attrib={}, **extra):
        apply(self.start, (tag, attrib), extra)
        if text:
            self.data(text)
        self.end()
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/dblatex/rawparse.py
# Compiled at: 2017-04-03 18:58:57
import re
from texcodec import LatexCodec, TexCodec
from texhyphen import BasicHyphenator, UrlHyphenator

def utf8(u):
    return u.encode('utf8')


class RawKey:

    def __init__(self, key, incr):
        self.key = key
        self.depth = incr
        self.pos = -1
        self.len = len(key)


class RawLatexParser:

    def __init__(self, key_in=utf8('Ͱt'), key_out=utf8('ͱt'), codec=None, output_encoding='latin-1'):
        self.key_in = RawKey(key_in, 1)
        self.key_out = RawKey(key_out, -1)
        self.depth = 0
        self.hyphenate = 0
        self.codec = codec or LatexCodec(output_encoding=output_encoding)
        self.hyphenator = UrlHyphenator(codec=self.codec)
        self.hypon = re.compile(utf8('Ͱh'))
        self.hypof = re.compile(utf8('ͱh'))

    def parse(self, line):
        lout = ''
        while line:
            self.key_in.pos = line.find(self.key_in.key)
            self.key_out.pos = line.find(self.key_out.key)
            if self.key_out.pos == -1 or self.key_in.pos >= 0 and self.key_in.pos < self.key_out.pos:
                key = self.key_in
            else:
                key = self.key_out
            if key.pos != -1:
                text = line[:key.pos]
                line = line[key.pos + key.len:]
            else:
                text = line
                line = ''
            if text:
                if self.depth > 0:
                    lout += self.translate(text)
                else:
                    text, hon = self.hypon.subn('', text)
                    text, hof = self.hypof.subn('', text)
                    self.hyphenate += hon - hof
                    lout += text
            if key.pos != -1:
                self.depth += key.depth

        return lout

    def translate(self, text):
        if self.hyphenate:
            text = self.hyphenator.hyphenate(text)
        else:
            text = self.codec.decode(text)
            text = self.codec.encode(text)
        return text


class RawUtfParser(RawLatexParser):
    """Just encode from UTF-8 without latex escaping"""

    def __init__(self, codec=None, output_encoding='latin-1'):
        texcodec = codec or TexCodec(output_encoding=output_encoding)
        RawLatexParser.__init__(self, utf8('Ͱu'), utf8('ͱu'), texcodec)

    def translate(self, text):
        text = self.codec.decode(text)
        return self.codec.encode(text)
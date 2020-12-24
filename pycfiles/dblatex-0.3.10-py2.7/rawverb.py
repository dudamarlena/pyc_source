# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/dblatex/rawverb.py
# Compiled at: 2017-04-03 18:58:57
import re
from texcodec import TexCodec
from texcodec import tex_handler_counter
from rawparse import RawUtfParser

class VerbCodec(TexCodec):

    def __init__(self, pre, post, errors='verbtex', input_encoding='utf8', output_encoding='latin-1'):
        self.pre = pre
        self.post = post
        self.output_encoding = output_encoding
        TexCodec.__init__(self, input_encoding, output_encoding, errors=errors, pre=pre, post=post)

    def decode(self, text):
        global tex_handler_counter
        ntext = TexCodec.decode(self, text)
        if self.output_encoding != 'utf8':
            return ntext
        text = ''
        n = tex_handler_counter[self._errors]
        for c in ntext:
            if ord(c) > 255:
                c = self.pre + c + self.post
                n += 1
            text += c

        tex_handler_counter[self._errors] = n
        return text


class VerbParser:

    def __init__(self, output_encoding='latin-1'):
        self.start_re = re.compile('\\\\begin{lst[^}]*}')
        self.stop_re = re.compile('\\\\end{lst[^}]*}')
        self.esc_re = re.compile('escapeinside={([^}]*)}{([^}]*)}')
        self.block = ''
        self.encoding = output_encoding
        self.default_esc_start = '<:'
        self.default_esc_stop = ':>'
        self.default_codec = VerbCodec(self.default_esc_start, self.default_esc_stop, output_encoding=output_encoding)

    def parse(self, line):
        if not self.block:
            m = self.start_re.search(line)
            if not m:
                return line
            return self.parse_begin(line, m)
        else:
            m = self.stop_re.search(line)
            if not m:
                return self.block_grow(line)
            return self.parse_end(line, m)

    def parse_begin(self, line, m):
        preblock = line[:m.start()]
        self.command = line[m.start():m.end()]
        line = line[m.end():]
        self.esc_start = ''
        self.esc_stop = ''
        self.options = ''
        if line[0] == '[':
            e = line.find(']') + 1
            self.options = line[:e]
            line = line[e:]
            m = self.esc_re.search(self.options)
            if m:
                self.esc_start = m.group(1)
                self.esc_stop = m.group(2)
        self.block_grow(line)
        return preblock

    def parse_end(self, line, m):
        self.block_grow(line[:m.start()])
        c = self.get_codec()
        c.clear_errors()
        p = RawUtfParser(codec=c)
        text = p.parse(self.block)
        if not self.esc_start and c.get_errors() != 0:
            escopt = 'escapeinside={%s}{%s}' % (c.pre, c.post)
            if self.options:
                if self.options[(-2)] != ',':
                    escopt = ',' + escopt
                self.options = self.options[:-1] + escopt + ']'
            else:
                self.options = '[' + escopt + ']'
        block = self.command + self.options + text + line[m.start():]
        self.block = ''
        return block

    def block_grow(self, line):
        self.block += line
        return ''

    def get_codec(self):
        if self.esc_start:
            if self.esc_start != self.default_esc_start:
                return VerbCodec(self.esc_start, self.esc_stop, 'verbtex' + self.esc_start, output_encoding=self.encoding)
            else:
                return self.default_codec

        s = self.default_esc_start
        iter = 0
        i = self.block.find(s)
        while i != -1:
            s = '<' + str(iter) + ':'
            i = self.block.find(s)
            iter += 1

        if s == self.default_esc_start:
            return self.default_codec
        return VerbCodec(s, self.default_esc_stop, 'verbtex' + s, output_encoding=self.encoding)


if __name__ == '__main__':
    import sys
    v = VerbParser()
    f = open(sys.argv[1])
    for line in f:
        text = v.parse(line)
        if text:
            sys.stdout.write(text)
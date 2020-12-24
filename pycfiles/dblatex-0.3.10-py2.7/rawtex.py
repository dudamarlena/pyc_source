# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/dblatex/rawtex.py
# Compiled at: 2017-04-03 18:58:57
import sys, os, re
from rawparse import RawLatexParser, RawUtfParser
from rawverb import VerbParser
from xetex.codec import XetexCodec
from dbtexmf.core.imagedata import *

class RawLatex:
    """Main latex file parser"""

    def __init__(self):
        self.figre = re.compile('(\\\\includegraphics[\\[]?|\\\\begin{overpic}|\\\\imgexits)[^{]*{([^}]*)}')
        self.image = Imagedata()
        self.parsers = []
        self.format = None
        self.backend = None
        return

    def set_fig_paths(self, paths):
        self.image.paths = paths

    def set_parsers(self, input, output_encoding=''):
        codec = None
        if self.backend == 'xetex':
            output_encoding = 'utf8'
            codec = XetexCodec()
        elif not output_encoding:
            f = file(input)
            params = {}
            started = 0
            for line in f:
                if not started:
                    if line.startswith('%%<params>'):
                        started = 1
                    continue
                if line.startswith('%%</params>'):
                    break
                p = line.split()
                params[p[1]] = p[2]

            output_encoding = params.get('latex.encoding', 'latin-1')
        self.parsers = [VerbParser(output_encoding=output_encoding),
         RawLatexParser(codec=codec, output_encoding=output_encoding),
         RawUtfParser(output_encoding=output_encoding)]
        self.image.set_encoding(output_encoding or 'latin-1')
        return

    def set_format(self, format, backend=None):
        if format == 'pdf' and backend == 'dvips':
            format = 'ps'
        self.format = format
        self.backend = backend
        self.image.set_format(format, backend)

    def fig_format(self, format):
        self.image.input_format = format

    def parse(self, input, output):
        self.set_parsers(input)
        f = file(input)
        o = file(output, 'w')
        for line in f:
            if self.format:
                line = self.figconvert(line)
            for p in self.parsers:
                line = p.parse(line)
                if not line:
                    break

            if line:
                o.write(line)

        o.close()
        f.close()

    def figconvert(self, line):
        mlist = self.figre.findall(line)
        if not mlist:
            return line
        for m in mlist:
            fig = m[1]
            newfig = self.image.convert(fig)
            if newfig != fig:
                line = re.sub('{%s}' % fig, '{%s}' % newfig, line)

        return line


def main():
    c = RawLatex()
    c.set_fig_paths([os.getcwd()])
    c.parse(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
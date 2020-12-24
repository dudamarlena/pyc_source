# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pdfcat/pdfcat.py
# Compiled at: 2008-04-03 09:32:15
"""
$Id$
"""
__author__ = 'Jean-Nicolas Bès <contact@atreal.net>'
__docformat__ = 'plaintext'
__licence__ = 'GPL'
import os, sys, shutil, tempfile, StringIO
from os.path import isfile, abspath, join

class PdfJoiner:
    __module__ = __name__
    pdflatex = '/usr/bin/pdflatex'
    paper = 'a4paper'
    orient = 'portrait'
    fitpaper = 'true'
    turn = 'true'
    noautoscale = 'false'
    offset = '0 0'
    trim = '0 0 0 0'
    tidy = 'true'
    prologfmt = '\\documentclass[%s,%s]{article}\n\\usepackage{pdfpages}\n\\begin{document}\n'
    pdfitemfmt = '\\includepdf[pages=-,fitpaper=%s,trim=%s,offset=%s,turn=%s,noautoscale=%s]{%s}\n'
    epilog = '\\end{document}\n'

    def __init__(self, **kwargs):
        for (key, val) in kwargs.items():
            if key not in ('paper', 'orient', 'fitpaper', 'turn', 'noautoscale', 'offset',
                           'trim', 'tidy'):
                continue
            setattr(self, key, val)

    def makeInputAvail(self, tmpdirpath, inputs):
        tmpinputs = []
        toclean = []
        for inp in inputs:
            if isinstance(inp, (str, unicode)):
                if len(inp) < 2000 and isfile(inp):
                    filename = tempfile.mktemp(dir=tmpdirpath, suffix='.pdf')
                    os.symlink(abspath(inp), filename)
                else:
                    (tmpfile, filename) = tempfile.mkstemp(text=False, dir=tmpdirpath, suffix='.pdf')
                    os.write(tmpfile, inp)
                    os.close(tmpfile)
            elif isinstance(inp, file) and isfile(abspath(inp.name)):
                filename = tempfile.mktemp(dir=tmpdirpath, suffix='.pdf')
                os.symlink(abspath(inp.name), filename)
            elif hasattr(inp, '__iter__'):
                (tmpfile, filename) = tempfile.mkstemp(text=False, dir=tmpdirpath, suffix='.pdf')
                for line in inp:
                    os.write(tmpfile, line)

                os.close(tmpfile)
                filename = abspath(filename)
            else:
                print 'WTF?', repr(inp)
                continue
            tmpinputs.append(filename)

        return tmpinputs

    def processOutput(self, outfilepath, want):
        tmpoutput = file(outfilepath)
        if want is str:
            output = tmpoutput.read()
        elif want is StringIO.StringIO:
            output = StringIO.StringIO(tmpoutput.read())
        elif isinstance(want, str):
            want = file(want, 'w')
        if isinstance(want, (file, StringIO.StringIO)):
            want.write(tmpoutput.read())
            output = want
        return output

    def joinpdfs(self, inputs, want=str, **kwargs):
        print 'INPUT', inputs
        print 'WANTR', repr(want)
        self.__init__(**kwargs)
        tmpdirpath = tempfile.mkdtemp()
        (tmptexfile, tmptexname) = tempfile.mkstemp(text=False, dir=tmpdirpath)
        tmpinputs = self.makeInputAvail(tmpdirpath, inputs)
        os.write(tmptexfile, self.prologfmt % (self.paper, self.orient))
        for inp in tmpinputs:
            pdfitem = self.pdfitemfmt % (self.fitpaper, self.trim, self.offset, self.turn, self.noautoscale, inp)
            os.write(tmptexfile, pdfitem)

        os.write(tmptexfile, self.epilog)
        os.system('cd %s && pdflatex -halt-on-error %s >/dev/null' % (tmpdirpath, tmptexname))
        print os.getcwd()
        outfilepath = join(tmpdirpath, tmptexname + '.pdf')
        if not isfile(outfilepath):
            print "Une erreur s'est produite"
            return
        output = self.processOutput(outfilepath, want)
        shutil.rmtree(tmpdirpath)
        return output


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise SystemExit, 'Au moins 2 arguments!!!'
    pj = PdfJoiner()
    print 'INPUT', sys.argv[1:-1], 'OUTPUT', sys.argv[(-1)]
    pj.joinpdfs(sys.argv[1:-1], want=sys.argv[(-1)])
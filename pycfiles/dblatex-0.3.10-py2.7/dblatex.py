# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/dblatex/dblatex.py
# Compiled at: 2017-04-03 18:58:57
import os
from dbtexmf.core.sgmlxml import Osx
from dbtexmf.core.dbtex import DbTex, DbTexCommand
from rawtex import RawLatex
from runtex import RunLatex

class DbLatex(DbTex):

    def __init__(self, base=''):
        DbTex.__init__(self, base=base)
        self.name = 'dblatex'
        self.runtex = RunLatex()
        self.runtex.index_style = os.path.join(self.topdir, 'latex', 'scripts', 'doc.ist')
        self.rawtex = RawLatex()
        self.sgmlxml = Osx()

    def set_base(self, topdir):
        DbTex.set_base(self, topdir)
        self.xslmain = os.path.join(self.topdir, 'xsl', 'latex_book_fast.xsl')
        self.xsllist = os.path.join(self.topdir, 'xsl', 'common', 'mklistings.xsl')
        self.texdir = os.path.join(self.topdir, 'latex')
        self.texlocal = os.path.join(self.topdir, 'latex', 'style')
        self.confdir = os.path.join(self.topdir, 'latex', 'specs')


def main(base=''):
    command = DbTexCommand(base)
    command.run = DbLatex(base=base)
    command.main()


if __name__ == '__main__':
    main()
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/dblatex/grubber/pdftex.py
# Compiled at: 2017-04-03 18:58:57
"""
pdfLaTeX support for Rubber.

When this module loaded with the otion 'dvi', the document is compiled to DVI
using pdfTeX.

The module optimizes the pdflatex calls by setting -draftmode and apply a last
call to build the final PDF output.
"""
import os, re, subprocess
from subprocess import Popen, PIPE
from msg import _, msg
from plugins import TexModule

class Module(TexModule):

    def __init__(self, doc, dict):
        self.doc = doc
        doc.program = 'pdflatex'
        doc.engine = 'pdfTeX'
        doc.set_format('pdf')
        if self._draft_is_supported():
            self.doc.draft_support = True
        else:
            self.doc.draft_support = False

    def _draft_is_supported(self):
        opts = os.getenv('DBLATEX_PDFTEX_OPTIONS', '')
        if '-draftmode' not in opts:
            return False
        return self._get_version() == '1.40'

    def pre_compile(self):
        if not self.doc.draft_support:
            return
        self.doc.opts.append('-draftmode')

    def last_compile(self):
        if not self.doc.draft_support or self.doc.draft_only:
            return
        self.doc.opts.remove('-draftmode')
        rc = self.doc.compile()
        return rc

    def _get_version(self):
        """
        Parse something like:

          pdfTeX using libpoppler 3.141592-1.40.3-2.2 (Web2C 7.5.6)
          kpathsea version 3.5.6
          Copyright 2007 Peter Breitenlohner (eTeX)/Han The Thanh (pdfTeX).
          Kpathsea is copyright 2007 Karl Berry and Olaf Weber.
          ...
        and return '1.40'
        """
        p = Popen('pdflatex -version', shell=True, stdout=PIPE)
        data = p.communicate()[0]
        m = re.search('pdfTeX.*3.14[^-]*-(\\d*.\\d*)', data, re.M)
        if not m:
            return ''
        else:
            return m.group(1)
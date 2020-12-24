# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/dblatex/grubber/texbuilder.py
# Compiled at: 2017-04-03 18:58:57
"""
LaTeX document building system for Grubber.

This module is specific to Grubber and provides a class that encapsulates some
of the rubber internals.
"""
import subprocess, os, shlex
from msg import _, msg
from maker import Maker
from latex import Latex

class IndexBuilder:
    """
    Index configuration data to set the index tool maker to use
    """

    def __init__(self):
        self.style = ''
        self.tool = ''
        self.lang = ''


class LatexBuilder:
    """
    Main (g)rubber wrapper hiding all the internals and compiling the
    required tex file.
    """

    def __init__(self):
        self.maker = Maker()
        self.tex = Latex(self.maker)
        self.maker.dep_append(self.tex)
        self.backend = 'pdftex'
        self.format = 'pdf'
        self.index_style = ''
        self.batch = 1
        self.encoding = 'latin-1'
        self.texpost = ''
        self.options = ''
        self.lang = ''
        self.index = IndexBuilder()

    def set_format(self, format):
        self.format = format

    def set_backend(self, backend):
        self.backend = backend

    def _texpost_call(self, source, msg):
        if isinstance(self.texpost, str):
            cmd = [self.texpost, source]
            msg.log((' ').join(cmd))
            rc = subprocess.call(cmd, stdout=msg.stdout)
        else:
            rc = self.texpost.main(source, msg.stdout)
        return rc

    def compile(self, source):
        self.tex.batch = self.batch
        self.tex.encoding = self.encoding
        self.tex.lang = self.lang
        self.tex.set_source(source)
        if self.options:
            self.tex.opts += shlex.split(self.options)
        if self.format == 'pdf':
            if self.backend == 'pdftex':
                self.tex.modules.register('pdftex')
            elif self.backend == 'xetex':
                self.tex.modules.register('xetex')
            else:
                self.tex.modules.register('dvips')
                self.tex.modules.register('ps2pdf')
        else:
            if self.format == 'ps':
                self.tex.modules.register('dvips')
            self.tex.prepare()
            if self.tex.modules.has_key('makeidx'):
                idx = self.tex.modules['makeidx']
                if self.index.style:
                    idx.do_style(self.index.style)
                if self.index.tool:
                    idx.do_tool(self.index.tool)
                if self.index.lang:
                    idx.do_language(self.index.lang)
            rc = self.maker.make()
            if rc != 0:
                raise OSError('%s compilation failed' % self.tex.program)
            if not self.texpost:
                return
            os.environ['LATEX'] = self.tex.program
            rc = self._texpost_call(source, msg)
            if rc == 1:
                return
        if rc != 0:
            raise OSError('%s texpost failed' % self.texpost)
        rc = self.maker.make(force=1)
        if rc != 0:
            raise OSError('%s post compilation failed' % self.tex.program)

    def clean(self):
        self.tex.clean()
        self.reinit()

    def reinit(self):
        self.tex.reinit()
        self.maker.reinit()
        self.maker.dep_append(self.tex)

    def print_errors(self):
        msg.display_all(self.tex.get_errors(), writer=msg.write_stderr)

    def print_misschars(self):
        self.tex.print_misschars()
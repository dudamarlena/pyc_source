# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/dblatex/runtex.py
# Compiled at: 2017-04-03 18:58:57
import os, re, shutil
from grubber.texbuilder import LatexBuilder

class RunLatex:

    def __init__(self):
        self.fig_paths = []
        self.index_style = ''
        self.backend = 'pdftex'
        self.texpost = ''
        self.texer = LatexBuilder()

    def set_fig_paths(self, paths):
        if not paths:
            return
        paths_blank = []
        paths_input = []
        for p in paths:
            if p.find(' ') != -1:
                paths_blank.append(p + '//')
            else:
                paths_input.append(p)

        if paths_blank:
            texinputs = os.pathsep.join(paths_blank)
            os.environ['TEXINPUTS'] = os.getenv('TEXINPUTS') + os.pathsep + texinputs
        paths = paths_input
        if os.sep != '/':
            paths = [ p.replace(os.sep, '/') for p in paths ]
        self.fig_paths = [ p.replace('~', '\\string~') for p in paths ]

    def set_bib_paths(self, bibpaths, bstpaths=None):
        if bibpaths:
            os.environ['BIBINPUTS'] = os.pathsep.join(bibpaths + [
             os.getenv('BIBINPUTS', '')])
        if bstpaths:
            os.environ['BSTINPUTS'] = os.pathsep.join(bstpaths + [
             os.getenv('BSTINPUTS', '')])

    def set_backend(self, backend):
        if backend not in ('dvips', 'pdftex', 'xetex'):
            raise ValueError("'%s': invalid backend" % backend)
        self.backend = backend

    def get_backend(self):
        return self.backend

    def _clear_params(self):
        self._param_started = 0
        self._param_ended = 0
        self._params = {}

    def _set_params(self, line):
        if self._param_ended:
            return
        if not self._param_started:
            if line.startswith('%%<params>'):
                self._param_started = 1
            return
        if line.startswith('%%</params>'):
            self._param_ended = 1
            return
        p = line.split(' ', 2)
        self._params[p[1]] = p[2].strip()

    def compile(self, texfile, binfile, format, batch=1):
        root = os.path.splitext(texfile)[0]
        tmptex = root + '_tmp' + '.tex'
        texout = root + '.' + format
        f = file(tmptex, 'w')
        if self.fig_paths:
            paths = '{' + ('//}{').join(self.fig_paths) + '//}'
            f.write('\\makeatletter\n')
            f.write('\\def\\input@path{%s}\n' % paths)
            f.write('\\makeatother\n')
        self._clear_params()
        input = file(texfile)
        for line in input:
            self._set_params(line)
            f.write(line)

        f.close()
        input.close()
        shutil.move(tmptex, texfile)
        try:
            self.texer.batch = batch
            self.texer.texpost = self.texpost
            self.texer.encoding = self._params.get('latex.encoding', 'latin-1')
            self.texer.options = self._params.get('latex.engine.options')
            self.texer.lang = self._params.get('document.language')
            self.texer.set_format(format)
            self.texer.set_backend(self.backend)
            if self.index_style:
                self.texer.index.style = self.index_style
            self.texer.index.tool = self._params.get('latex.index.tool')
            self.texer.index.lang = self._params.get('latex.index.language')
            self.texer.compile(texfile)
            self.texer.print_misschars()
        except:
            self.texer.print_errors()
            raise

        if texout != binfile:
            shutil.move(texout, binfile)

    def clean(self):
        self.texer.clean()

    def reinit(self):
        self.texer.reinit()
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/xslt/xsltproc.py
# Compiled at: 2017-04-03 18:58:57
import os, logging, re
from subprocess import call, Popen, PIPE

class XsltProc:

    def __init__(self):
        self.catalogs = os.getenv('SGML_CATALOG_FILES')
        self.use_catalogs = 1
        self.log = logging.getLogger('dblatex')
        self.run_opts = ['--xinclude']
        if self._has_xincludestyle():
            self.run_opts.append('--xincludestyle')

    def get_deplist(self):
        return ['xsltproc']

    def run(self, xslfile, xmlfile, outfile, opts=None, params=None):
        cmd = ['xsltproc', '-o', os.path.basename(outfile)] + self.run_opts
        if self.use_catalogs and self.catalogs:
            cmd.append('--catalogs')
        if params:
            for param, value in params.items():
                cmd += ['--param', param, "'%s'" % value]

        if opts:
            cmd += opts
        cmd += [xslfile, xmlfile]
        self.system(cmd)

    def system(self, cmd):
        self.log.debug((' ').join(cmd))
        rc = call(cmd)
        if rc != 0:
            raise ValueError('xsltproc failed')

    def _has_xincludestyle(self):
        p = Popen(['xsltproc'], stdout=PIPE)
        data = p.communicate()[0]
        m = re.search('--xincludestyle', data, re.M)
        if not m:
            return False
        else:
            return True


class Xslt(XsltProc):
    """Plugin Class to load"""
    pass
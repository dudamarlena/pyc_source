# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/xslt/saxon.py
# Compiled at: 2017-04-03 18:58:57
import os, logging, re
from subprocess import call, Popen, PIPE

class Saxon:

    def __init__(self):
        self.catalogs = os.getenv('SGML_CATALOG_FILES')
        self.use_catalogs = 1
        self.log = logging.getLogger('dblatex')
        self.run_opts = []

    def get_deplist(self):
        return [
         'saxon']

    def run(self, xslfile, xmlfile, outfile, opts=None, params=None):
        cmd = ['saxon-xslt', '-o', os.path.basename(outfile)] + self.run_opts
        if opts:
            cmd += opts
        cmd += [xmlfile, xslfile]
        if params:
            for param, value in params.items():
                cmd += ['%s=%s' % (param, "'%s'" % value)]

        self.system(cmd)

    def system(self, cmd):
        self.log.debug((' ').join(cmd))
        rc = call(cmd)
        if rc != 0:
            raise ValueError('saxon failed')

    def _has_xincludestyle(self):
        return False


class Xslt(Saxon):
    """Plugin Class to load"""
    pass
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/setuptools_epydoc/__init__.py
# Compiled at: 2014-06-04 07:29:11
import os, sys, re
from setuptools import Command

class EpydocCommand(Command):
    """
    Setuptools command used to build an API documentation with epydoc.

    @author: jwienke
    """
    user_options = [
     ('format=', 'f', 'the output format to use (html and pdf)'),
     ('config=', 'c', 'Epydoc configuration file'),
     ('names=', None, 'Names of packages to document. Defaults to all configured packages in the project. Comma-separated.'),
     ('output-dir=', 'o', 'Folder for generated output. Default: docs'),
     ('verbose', 'v', 'print verbose warnings')]
    description = 'Generates an API documentation using epydoc.'
    FORMAT_HTML = 'html'
    FORMAT_PDF = 'pdf'

    def initialize_options(self):
        self.format = None
        self.verbose = False
        self.config = None
        self.names = ''
        self.output_dir = 'docs'
        return

    def finalize_options(self):
        if self.format is None:
            self.format = self.FORMAT_HTML
        if self.format not in [self.FORMAT_HTML, self.FORMAT_PDF]:
            self.format = self.FORMAT_HTML
        self.names = [ module.strip() for module in re.split('[\\s,]+', self.names) if len(module.strip()) > 0
                     ]
        return

    def run(self):
        self.run_command('build')
        outdir = os.path.join(self.output_dir, self.format)
        try:
            os.makedirs(outdir)
        except OSError:
            pass

        cmdline = []
        cmdline.append('--' + self.format)
        cmdline.append('-o')
        cmdline.append(outdir)
        if self.verbose:
            cmdline.append('-v')
        if self.config is not None:
            cmdline.append('--config')
            cmdline.append(self.config)
        base = self.get_finalized_command('build_py')
        names = []
        if self.names is None or len(self.names) == 0:
            for package, _, _ in base.find_all_modules():
                pdir = base.get_package_dir(package)
                names.append(pdir)

            cmdline = cmdline + list(set(names))
        else:
            cmdline = cmdline + self.names
        import copy, epydoc.cli as ep
        argv = copy.copy(sys.argv)
        try:
            sys.argv = cmdline
            ep.cli()
        finally:
            sys.argv = argv

        return
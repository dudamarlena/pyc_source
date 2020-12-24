# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\DistExt\InstallText.py
# Compiled at: 2006-08-27 18:09:14
import os
from distutils import util
from distutils.core import Command, DEBUG
from Ft.Lib.DistExt import Structures

class InstallText(Command):
    __module__ = __name__
    command_name = 'install_text'
    description = 'install plain text documentation'
    user_options = [
     (
      'install-dir=', 'd', 'directory to install documentation to'), ('force', 'f', 'force installation (overwrite existing files)')]
    boolean_options = [
     'force']

    def initialize_options(self):
        self.install_dir = None
        self.force = None
        return
        return

    def finalize_options(self):
        self.set_undefined_options('install', (
         'install_docs', 'install_dir'), (
         'force', 'force'))
        self.files = [ f for f in self.distribution.doc_files if isinstance(f, Structures.File) ]
        if self.distribution.license_file:
            self.files.append(Structures.File(self.distribution.license_file))
        return

    def run(self):
        for file in self.files:
            source = util.convert_path(file.source)
            destdir = util.convert_path(file.outdir)
            destdir = os.path.join(self.install_dir, destdir)
            self.mkpath(destdir)
            self.copy_file(source, destdir)

        return

    def get_source_files(self):
        sources = []
        for file in self.files:
            sources.append(util.convert_path(file.source))

        return sources

    def get_inputs(self):
        inputs = []
        for file in self.files:
            inputs.append(util.convert_path(file.source))

        return inputs

    def get_outputs(self):
        outputs = []
        for file in self.files:
            source = util.convert_path(file.source)
            source = os.path.basename(source)
            outdir = util.convert_path(file.outdir)
            outputs.append(os.path.join(self.install_dir, outdir, source))

        return outputs
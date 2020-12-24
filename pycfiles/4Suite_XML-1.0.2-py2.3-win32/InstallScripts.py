# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\DistExt\InstallScripts.py
# Compiled at: 2005-10-21 15:40:16
import os
from distutils.core import Command

class InstallScripts(Command):
    __module__ = __name__
    command_name = 'install_scripts'
    description = 'install scripts (Python or otherwise)'
    user_options = [
     (
      'force', 'f', 'force installation (overwrite existing files)')]
    boolean_options = [
     'force']

    def initialize_options(self):
        self.force = None
        self.install_dir = None
        self.skip_build = None
        return
        return

    def finalize_options(self):
        self.set_undefined_options('install', (
         'install_scripts', 'install_dir'), (
         'force', 'force'), (
         'skip_build', 'skip_build'))
        return

    def run(self):
        if not self.skip_build:
            self.run_command('build_scripts')
        self.mkpath(self.install_dir)
        for source in self.get_inputs():
            self.copy_file(source, self.install_dir)

        return

    def get_source_files(self):
        return []

    def get_inputs(self):
        build_scripts = self.get_finalized_command('build_scripts')
        return build_scripts.get_outputs()

    def get_outputs(self):
        outputs = []
        for source in self.get_inputs():
            source = os.path.basename(source)
            outfile = os.path.join(self.install_dir, source)
            outputs.append(outfile)

        return outputs
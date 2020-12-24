# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\DistExt\InstallL10n.py
# Compiled at: 2004-01-26 02:40:16
import os
from distutils.core import Command

class InstallL10n(Command):
    __module__ = __name__
    command_name = 'install_l10n'
    description = 'install binary message catalogs'
    user_options = [
     (
      'force', 'f', 'force installation (overwrite existing files)'), ('skip-build', None, 'skip the build steps')]
    boolean_options = [
     'force', 'skip-build']

    def initialize_options(self):
        self.install_dir = None
        self.force = None
        self.skip_build = None
        return
        return

    def finalize_options(self):
        self.set_undefined_options('install', (
         'install_l10n', 'install_dir'), (
         'force', 'force'), (
         'skip_build', 'skip_build'))
        return

    def run(self):
        if not self.distribution.l10n:
            return
        if not self.skip_build:
            self.run_command('build_l10n')
        for (src, dst) in self.get_inputs_outputs():
            self.mkpath(os.path.dirname(dst))
            self.copy_file(src, dst)

        return

    def get_inputs_outputs(self):
        build_cmd = self.get_finalized_command('build_l10n')
        build_dir = build_cmd.build_dir
        build_files = build_cmd.get_outputs()
        prefix_len = len(build_dir) + len(os.sep)
        paired = []
        for source in build_files:
            outfile = os.path.join(self.install_dir, source[prefix_len:])
            paired.append((source, outfile))

        return paired

    def get_inputs(self):
        return [ src for (src, dst) in self.get_inputs_outputs() ]

    def get_outputs(self):
        return [ dst for (src, dst) in self.get_inputs_outputs() ]
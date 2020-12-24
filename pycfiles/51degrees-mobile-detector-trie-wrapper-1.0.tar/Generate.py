# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\DistExt\Generate.py
# Compiled at: 2003-12-07 17:20:58
from distutils.core import Command

class Generate(Command):
    __module__ = __name__
    command_name = 'generate'
    description = 'generate additional files needed to install'
    user_options = [
     (
      'force', 'f', 'forcibly generate everything (ignore file timestamps)')]
    boolean_options = [
     'force']

    def initialize_options(self):
        self.force = 0

    def finalize_options(self):
        return

    def run(self):
        for cmd_name in self.get_sub_commands():
            self.run_command(cmd_name)

        return

    def get_source_files(self):
        files = []
        for cmd_name in self.get_sub_commands():
            cmd = self.get_finalized_command(cmd_name)
            files.extend(cmd.get_source_files())

        return files

    def get_outputs(self):
        outputs = []
        for cmd_name in self.get_sub_commands():
            cmd = self.get_finalized_command(cmd_name)
            outputs.extend(cmd.get_outputs())

        return outputs

    def has_bgen(self):
        return self.distribution.has_bgen()

    def has_l10n(self):
        return self.distribution.has_l10n()

    sub_commands = [
     (
      'generate_bgen', has_bgen), ('generate_l10n', has_l10n)]
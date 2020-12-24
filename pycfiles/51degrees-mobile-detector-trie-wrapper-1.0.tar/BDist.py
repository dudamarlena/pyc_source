# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\DistExt\BDist.py
# Compiled at: 2006-08-27 14:36:34
import os, sys
from distutils.command import bdist
from Ft.Lib.DistExt import Util

class BDist(bdist.bdist):
    """
    Extended 'bdist' command that adds support for InnoSetup Windows installers
    and Python Egg files.
    """
    __module__ = __name__
    command_name = 'bdist'
    default_format = bdist.bdist.default_format.copy()
    default_format['nt'] = 'inno'
    format_commands = bdist.bdist.format_commands + ['inno', 'egg']
    format_command = bdist.bdist.format_command.copy()
    format_command['inno'] = ('bdist_inno', 'Windows InnoSetup installer')
    format_command['egg'] = ('bdist_egg', 'Python Egg file')
    if sys.version < '2.3':
        user_options = bdist.bdist.user_options + [('skip-build', None, 'skip rebuilding everything (for testing/debugging)')]
        boolean_options = [
         'skip-build']
    else:
        user_options = bdist.bdist.user_options
        boolean_options = bdist.bdist.boolean_options
    user_options = user_options + [('keep-temp', 'k', 'keep the pseudo-installation tree around after ' + 'creating the distribution archive')]
    boolean_options = boolean_options + ['keep-temp']

    def initialize_options(self):
        bdist.bdist.initialize_options(self)
        self.skip_build = False
        self.keep_temp = False
        return

    def finalize_options(self):
        self.set_undefined_options('config', ('plat_name', 'plat_name'))
        if self.bdist_base is None:
            build_base = self.get_finalized_command('build').build_base
            bdist_base = 'bdist.' + self.plat_name + '-' + sys.version[:3]
            self.bdist_base = os.path.join(build_base, bdist_base)
        bdist.bdist.finalize_options(self)
        for format in self.formats:
            if format not in self.format_command:
                raise DistutilsOptionError("invalid format '%s'" % format)

        return
        return

    sub_commands = []
    for format in format_commands:
        (command, description) = format_command[format]
        if command not in dict(sub_commands):
            sub_commands.append((command, lambda self: False))
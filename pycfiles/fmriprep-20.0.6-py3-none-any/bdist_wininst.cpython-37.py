# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-92t6atcz/setuptools/setuptools/command/bdist_wininst.py
# Compiled at: 2020-04-16 14:32:20
# Size of source mod 2**32: 637 bytes
import distutils.command.bdist_wininst as orig

class bdist_wininst(orig.bdist_wininst):

    def reinitialize_command(self, command, reinit_subcommands=0):
        """
        Supplement reinitialize_command to work around
        http://bugs.python.org/issue20819
        """
        cmd = self.distribution.reinitialize_command(command, reinit_subcommands)
        if command in ('install', 'install_lib'):
            cmd.install_lib = None
        return cmd

    def run(self):
        self._is_running = True
        try:
            orig.bdist_wininst.run(self)
        finally:
            self._is_running = False
# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\DistExt\InstallSysconf.py
# Compiled at: 2006-08-11 14:46:52
import os
from distutils.core import Command, DEBUG
from distutils.dep_util import newer
from distutils import util

class InstallSysconf(Command):
    __module__ = __name__
    command_name = 'install_sysconf'
    description = 'install read-only host-specific data (configuration files)'
    user_options = []

    def initialize_options(self):
        self.install_dir = None
        return
        return

    def finalize_options(self):
        self.set_undefined_options('install', (
         'install_sysconf', 'install_dir'))
        self.sysconf_files = self.distribution.sysconf_files
        return

    def run(self):
        self.mkpath(self.install_dir)
        for (dest, src) in self.sysconf_files:
            dest = os.path.join(self.install_dir, util.convert_path(dest))
            src = util.convert_path(src)
            if os.path.exists(dest) and newer(src, dest):
                self.warn('saving %r as %r' % (dest, dest + '.orig'))
                self.copy_file(dest, dest + '.orig')
            self.copy_file(util.convert_path(src), dest)

        return

    def get_source_files(self):
        sources = []
        for (dest, src) in self.sysconf_files:
            sources.append(util.convert_path(src))

        return sources

    def get_inputs(self):
        inputs = []
        for (dest, src) in self.sysconf_files:
            inputs.append(util.convert_path(src))

        return inputs

    def get_outputs(self):
        outputs = []
        for (dest, src) in self.sysconf_files:
            dest = os.path.join(self.install_dir, util.convert_path(dest))
            outputs.append(dest)

        return outputs
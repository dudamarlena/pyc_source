# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\DistExt\InstallConfig.py
# Compiled at: 2006-10-20 14:39:47
"""
distutils command for installing the configuration file.

Copyright 2006 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
import os
from distutils.core import Command
from distutils.util import convert_path, subst_vars
from Ft.Lib.DistExt import Install
METADATA_KEYS = (
 'name', 'version', 'fullname', 'url')
CONFIG_KEYS = (
 'resourcebundle', 'pythonlibdir', 'bindir', 'datadir', 'sysconfdir', 'localstatedir', 'libdir', 'localedir')
CONFIG_MAPPING = {'pythonlibdir': 'lib', 'bindir': 'scripts', 'datadir': 'data', 'sysconfdir': 'sysconf', 'localstatedir': 'localstate', 'libdir': 'devel', 'localedir': 'l10n'}
CONFIG_STUB = '# Configuration variables\n%(metadata)s\n\nimport sys\nif getattr(sys, \'frozen\', False):\n    # "bundled" installation locations (e.g., py2exe, cx_Freeze)\n    %(bundle_config)s\nelse:\n    # standard distutils installation directories\n    %(install_config)s\ndel sys\n'

class InstallConfig(Command):
    __module__ = __name__
    command_name = 'install_config'
    description = 'install configuration file'
    user_options = [
     (
      'install-dir=', 'd', 'directory to install to')]

    def initialize_options(self):
        self.install_dir = None
        return
        return

    def finalize_options(self):
        self.set_undefined_options('install_lib', (
         'install_dir', 'install_dir'))
        if self.distribution.config_module:
            parts = self.distribution.config_module.split('.')
            basename = os.path.join(*parts) + '.py'
            self.config_filename = os.path.join(self.install_dir, basename)
        else:
            self.config_filename = None
        return
        return

    def run(self):
        if not self.config_filename:
            return
        install = self.get_finalized_command('install')
        prefix_len = len(install.root or '')
        install_config = dict(install.config_vars)
        install_config['resourcebundle'] = install.scheme == 'zip'
        config_vars = CONFIG_MAPPING.values()
        for var in config_vars:
            command = 'install_' + var
            install_dir = self.get_finalized_command(command).install_dir
            if install_dir and prefix_len:
                install_dir = install_dir[prefix_len:]
            install_config[var] = install_dir

        self.announce('writing %s' % self.config_filename, 2)
        if not self.dry_run:
            f = open(self.config_filename, 'w')
            try:
                self.write_config_module(f, install_config)
            finally:
                f.close()
        return

    def write_config_module(self, file, install_config):
        """
        Write the configuration variables to a file object.
        """
        maxlen = max(map(len, METADATA_KEYS))
        lines = []
        for name in METADATA_KEYS:
            value = getattr(self.distribution, 'get_' + name)()
            lines.append('%-*s = %r' % (maxlen, name.upper(), value))

        metadata = ('\n').join(lines)
        maxlen = max(map(len, CONFIG_KEYS))
        lines = []
        for name in CONFIG_KEYS:
            value = install_config[CONFIG_MAPPING.get(name, name)]
            lines.append('%-*s = %r' % (maxlen, name.upper(), value))

        install_config = ('\n    ').join(lines)
        lines = []
        bundle_config = Install.GetBundleScheme()
        bundle_config['resourcebundle'] = True
        for name in CONFIG_KEYS:
            value = bundle_config[CONFIG_MAPPING.get(name, name)]
            lines.append('%-*s = %r' % (maxlen, name.upper(), value))

        bundle_config = ('\n    ').join(lines)
        file.write(CONFIG_STUB % {'metadata': metadata, 'bundle_config': bundle_config, 'install_config': install_config})
        return

    def get_source_files(self):
        return []

    def get_outputs(self):
        if self.config_filename:
            outputs = [
             self.config_filename]
        else:
            outputs = []
        return outputs
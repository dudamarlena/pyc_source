# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pti7pv2_/setuptools/setuptools/command/install_egg_info.py
# Compiled at: 2020-02-14 17:24:43
# Size of source mod 2**32: 2203 bytes
from distutils import log, dir_util
import os
from setuptools import Command
from setuptools import namespaces
from setuptools.archive_util import unpack_archive
import pkg_resources

class install_egg_info(namespaces.Installer, Command):
    __doc__ = 'Install an .egg-info directory for the package'
    description = 'Install an .egg-info directory for the package'
    user_options = [
     ('install-dir=', 'd', 'directory to install to')]

    def initialize_options(self):
        self.install_dir = None

    def finalize_options(self):
        self.set_undefined_options('install_lib', ('install_dir', 'install_dir'))
        ei_cmd = self.get_finalized_command('egg_info')
        basename = pkg_resources.Distribution(None, None, ei_cmd.egg_name, ei_cmd.egg_version).egg_name() + '.egg-info'
        self.source = ei_cmd.egg_info
        self.target = os.path.join(self.install_dir, basename)
        self.outputs = []

    def run(self):
        self.run_command('egg_info')
        if os.path.isdir(self.target):
            os.path.islink(self.target) or dir_util.remove_tree((self.target), dry_run=(self.dry_run))
        else:
            if os.path.exists(self.target):
                self.execute(os.unlink, (self.target,), 'Removing ' + self.target)
            else:
                self.dry_run or pkg_resources.ensure_directory(self.target)
            self.execute(self.copytree, (), 'Copying %s to %s' % (self.source, self.target))
            self.install_namespaces()

    def get_outputs(self):
        return self.outputs

    def copytree(self):

        def skimmer(src, dst):
            for skip in ('.svn/', 'CVS/'):
                if src.startswith(skip) or '/' + skip in src:
                    return

            self.outputs.append(dst)
            log.debug('Copying %s to %s', src, dst)
            return dst

        unpack_archive(self.source, self.target, skimmer)
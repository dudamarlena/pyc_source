# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/setuptools/setuptools/command/develop.py
# Compiled at: 2020-01-10 16:25:25
# Size of source mod 2**32: 8184 bytes
from distutils.util import convert_path
from distutils import log
from distutils.errors import DistutilsError, DistutilsOptionError
import os, glob, io
from setuptools.extern import six
import pkg_resources
from setuptools.command.easy_install import easy_install
from setuptools import namespaces
import setuptools
__metaclass__ = type

class develop(namespaces.DevelopInstaller, easy_install):
    __doc__ = 'Set up package for development'
    description = "install package in 'development mode'"
    user_options = easy_install.user_options + [
     ('uninstall', 'u', 'Uninstall this source package'),
     ('egg-path=', None, 'Set the path to be used in the .egg-link file')]
    boolean_options = easy_install.boolean_options + ['uninstall']
    command_consumes_arguments = False

    def run(self):
        if self.uninstall:
            self.multi_version = True
            self.uninstall_link()
            self.uninstall_namespaces()
        else:
            self.install_for_development()
        self.warn_deprecated_options()

    def initialize_options(self):
        self.uninstall = None
        self.egg_path = None
        easy_install.initialize_options(self)
        self.setup_path = None
        self.always_copy_from = '.'

    def finalize_options(self):
        ei = self.get_finalized_command('egg_info')
        if ei.broken_egg_info:
            template = "Please rename %r to %r before using 'develop'"
            args = (ei.egg_info, ei.broken_egg_info)
            raise DistutilsError(template % args)
        self.args = [
         ei.egg_name]
        easy_install.finalize_options(self)
        self.expand_basedirs()
        self.expand_dirs()
        self.package_index.scan(glob.glob('*.egg'))
        egg_link_fn = ei.egg_name + '.egg-link'
        self.egg_link = os.path.join(self.install_dir, egg_link_fn)
        self.egg_base = ei.egg_base
        if self.egg_path is None:
            self.egg_path = os.path.abspath(ei.egg_base)
        target = pkg_resources.normalize_path(self.egg_base)
        egg_path = pkg_resources.normalize_path(os.path.join(self.install_dir, self.egg_path))
        if egg_path != target:
            raise DistutilsOptionError('--egg-path must be a relative path from the install directory to ' + target)
        self.dist = pkg_resources.Distribution(target,
          (pkg_resources.PathMetadata(target, os.path.abspath(ei.egg_info))),
          project_name=(ei.egg_name))
        self.setup_path = self._resolve_setup_path(self.egg_base, self.install_dir, self.egg_path)

    @staticmethod
    def _resolve_setup_path(egg_base, install_dir, egg_path):
        """
        Generate a path from egg_base back to '.' where the
        setup script resides and ensure that path points to the
        setup path from $install_dir/$egg_path.
        """
        path_to_setup = egg_base.replace(os.sep, '/').rstrip('/')
        if path_to_setup != os.curdir:
            path_to_setup = '../' * (path_to_setup.count('/') + 1)
        resolved = pkg_resources.normalize_path(os.path.join(install_dir, egg_path, path_to_setup))
        if resolved != pkg_resources.normalize_path(os.curdir):
            raise DistutilsOptionError("Can't get a consistent path to setup script from installation directory", resolved, pkg_resources.normalize_path(os.curdir))
        return path_to_setup

    def install_for_development(self):
        if six.PY3:
            if getattr(self.distribution, 'use_2to3', False):
                self.reinitialize_command('build_py', inplace=0)
                self.run_command('build_py')
                bpy_cmd = self.get_finalized_command('build_py')
                build_path = pkg_resources.normalize_path(bpy_cmd.build_lib)
                self.reinitialize_command('egg_info', egg_base=build_path)
                self.run_command('egg_info')
                self.reinitialize_command('build_ext', inplace=0)
                self.run_command('build_ext')
                ei_cmd = self.get_finalized_command('egg_info')
                self.egg_path = build_path
                self.dist.location = build_path
                self.dist._provider = pkg_resources.PathMetadata(build_path, ei_cmd.egg_info)
            else:
                self.run_command('egg_info')
                self.reinitialize_command('build_ext', inplace=1)
                self.run_command('build_ext')
        else:
            self.install_site_py()
            if setuptools.bootstrap_install_from:
                self.easy_install(setuptools.bootstrap_install_from)
                setuptools.bootstrap_install_from = None
            self.install_namespaces()
            log.info('Creating %s (link to %s)', self.egg_link, self.egg_base)
            if not self.dry_run:
                with open(self.egg_link, 'w') as (f):
                    f.write(self.egg_path + '\n' + self.setup_path)
        self.process_distribution(None, self.dist, not self.no_deps)

    def uninstall_link(self):
        if os.path.exists(self.egg_link):
            log.info('Removing %s (link to %s)', self.egg_link, self.egg_base)
            egg_link_file = open(self.egg_link)
            contents = [line.rstrip() for line in egg_link_file]
            egg_link_file.close()
            if contents not in ([self.egg_path],
             [
              self.egg_path, self.setup_path]):
                log.warn('Link points to %s: uninstall aborted', contents)
                return
            if not self.dry_run:
                os.unlink(self.egg_link)
        else:
            if not self.dry_run:
                self.update_pth(self.dist)
            if self.distribution.scripts:
                log.warn('Note: you must uninstall or replace scripts manually!')

    def install_egg_scripts(self, dist):
        if dist is not self.dist:
            return easy_install.install_egg_scripts(self, dist)
        self.install_wrapper_scripts(dist)
        for script_name in self.distribution.scripts or []:
            script_path = os.path.abspath(convert_path(script_name))
            script_name = os.path.basename(script_path)
            with io.open(script_path) as (strm):
                script_text = strm.read()
            self.install_script(dist, script_name, script_text, script_path)

    def install_wrapper_scripts(self, dist):
        dist = VersionlessRequirement(dist)
        return easy_install.install_wrapper_scripts(self, dist)


class VersionlessRequirement:
    __doc__ = "\n    Adapt a pkg_resources.Distribution to simply return the project\n    name as the 'requirement' so that scripts will work across\n    multiple versions.\n\n    >>> from pkg_resources import Distribution\n    >>> dist = Distribution(project_name='foo', version='1.0')\n    >>> str(dist.as_requirement())\n    'foo==1.0'\n    >>> adapted_dist = VersionlessRequirement(dist)\n    >>> str(adapted_dist.as_requirement())\n    'foo'\n    "

    def __init__(self, dist):
        self._VersionlessRequirement__dist = dist

    def __getattr__(self, name):
        return getattr(self._VersionlessRequirement__dist, name)

    def as_requirement(self):
        return self.project_name
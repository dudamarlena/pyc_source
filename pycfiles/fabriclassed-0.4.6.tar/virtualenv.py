# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/movister/env/src/fabriclassed/fabriclassed/contrib/virtualenv.py
# Compiled at: 2015-02-27 04:15:18
from fabric.api import lcd, local, run
from fabric.context_managers import prefix, settings
from contextlib import contextmanager
from os.path import join, isdir, relpath
from os import listdir

class VirtualenvFabric(object):
    """
    Fabric command file with base virtualenv commands
    """
    use_virtualenv = True
    virtualenv_dir = 'env'
    packages_path = join(virtualenv_dir, 'lib', 'python2.7', 'site-packages')
    patched_applications = []
    diff_dir = 'diffs'
    applications_dir = 'apps'

    def _site_packages_path(self):
        return self.project_path_join(self.packages_path)

    def _site_package_path(self, app_name):
        return join(self._site_packages_path(), app_name)

    def _source_package_path(self, app_name):
        return self.project_path_join(self.virtualenv_dir, 'src', app_name)

    @contextmanager
    def virtualenv(self, remote=False):
        """
        Context manager for running command in virtualenv environment
        """
        with prefix('. %s/bin/activate' % join(self.remote_project_path if remote else self.project_path, self.virtualenv_dir)):
            yield

    def run_pip(self, command):
        """
        Run pip on production
        """
        if getattr(self, 'use_virtualenv', False):
            with self.virtualenv(remote=True):
                run('pip %s' % command)
        else:
            run('pip %s' % command)

    def fab_patch(self):
        """
        Walk over 'diffs' directory and patch every application
        """
        vcs_commands = {'git': 'git checkout .', 
           'svn': 'svn revert -R .', 
           'hg': 'hg revert .'}
        for patch in listdir(self.project_path_join(self.diff_dir)):
            app_name, vcs = ('.').join(patch.split('.')[:-2]), patch.split('.')[(-2)]
            if vcs == 'lib':
                app_dir = self._site_packages_path()
                if isdir(self._site_package_path(app_name)) and isdir(self._site_package_path('%s.original' % app_name)):
                    with lcd(app_dir):
                        local('rm -R %(app)s && mv %(app)s.original %(app)s' % {'app': app_name}, capture=False)
                with lcd(app_dir):
                    local('cp -R %(app)s %(app)s.original' % {'app': app_name}, capture=False)
            else:
                app_dir = self._source_package_path(app_name)
                with lcd(app_dir):
                    local(vcs_commands[vcs], capture=False)
            with lcd(app_dir):
                patch_command = 'patch -p1' if vcs == 'hg' else 'patch -p0'
                local('%s < %s' % (patch_command, self.project_path_join(self.diff_dir, patch)), capture=False)

    def fab_diff_dump(self):
        """
        Walk over map of patched applications and make diff files in 'diffs' directory
        """
        vcs_commands = {'git': 'git diff --no-prefix', 
           'svn': 'svn diff', 
           'hg': 'hg diff'}
        for app_name, vcs in self.patched_applications:
            patch_path = self.project_path_join(self.diff_dir, '%s.%s.diff' % (app_name, vcs))
            if vcs == 'lib':
                app_dir = self._site_packages_path()
                with lcd(app_dir):
                    with settings(warn_only=True):
                        local('diff -rcx .pyc %s.original %s > %s' % (app_name, app_name, patch_path), capture=False)
            else:
                app_dir = self._source_package_path(app_name)
                with lcd(app_dir):
                    local('%s > %s' % (vcs_commands[vcs], patch_path), capture=False)

    def fab_symlink(self, app_name):
        """
        Create symlink from 'apps' dir to the site-packages or source application dir
        """
        source_dir = None
        if isdir(self._source_package_path(app_name)):
            source_dir = self._source_package_path(app_name)
        elif isdir(self._site_package_path(app_name)):
            source_dir = self._site_package_path(app_name)
        if source_dir:
            source_dir = relpath(source_dir, self.project_path_join(self.applications_dir))
            local('ln -s %s %s' % (source_dir, join(self.applications_dir, app_name)))
        return
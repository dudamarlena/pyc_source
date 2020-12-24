# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/exedre/Dropbox/exedre@gmail.com/Dropbox/Work/GeCo-dev/infomedia-1.0/build/lib/infomedia/dist/legacy.py
# Compiled at: 2012-07-22 06:13:42
from distutils.command.build import build
from distutils.command.build_py import build_py
from distutils.command.build_ext import build_ext
from distutils.command.build_scripts import build_scripts
from distutils.command.install import install
from distutils.command.install_data import install_data
from distutils import log
from distutils.util import convert_path
from distutils.errors import *
from types import IntType, StringType
import os, string
from subprocess import Popen, PIPE

def get_revision():
    """
    Try get_mercurial_revision and get_subversion_revision in that
    order.  Take the first result that isn't UNKNOWN.
    """
    revision = get_mercurial_revision()
    if revision == 'UNKNOWN':
        revision = get_subversion_revision()
    return revision


def get_mercurial_revision():
    """
    If subversion is available and this is a subversion-controlled
    directory, fetch the version number.  Otherwise, use the cached
    version number.  We fetch both a descriptor of the branch/tag, and
    the revision number.
    """
    revision = None
    try:
        p = None
        try:
            p = Popen(['hg', 'identify', '-i'], stdin=None, stdout=PIPE, stderr=open('/dev/null', 'r'))
            for l in p.stdout:
                l = l.strip()
                revision = l

        finally:
            if p:
                p.wait()

    except:
        pass

    if revision is None:
        try:
            f = None
            try:
                f = open('.hg_archival.txt', 'r')
                for l in f:
                    k, v = l.strip().split(': ')
                    if k == 'node':
                        revision

                revision = v[:12]
            finally:
                if f:
                    f.close()

        except:
            pass

    if revision is not None:
        return revision
    else:
        return 'UNKNOWN'
        return


def get_subversion_revision():
    """
    If subversion is available and this is a subversion-controlled
    directory, fetch the version number.  Otherwise, use the cached
    version number.  We fetch both a descriptor of the branch/tag, and
    the revision number.
    """
    revision = None
    branch = ''
    try:
        p = None
        try:
            p = Popen(['svnversion', '-c'], stdin=None, stdout=PIPE)
            for l in p.stdout:
                l = l.strip()
                revision = l.split(':')[(-1)]

            if revision == 'exported':
                revision = None
        finally:
            if p:
                p.wait()

    except:
        pass

    if revision is not None:
        try:
            p = None
            try:
                p = Popen(['svn', 'info'], stdout=PIPE)
                for l in p.stdout:
                    if ':' not in l:
                        continue
                    k, v = l.split(':', 1)
                    k = k.strip()
                    v = v.strip()
                    if k == 'Repository Root':
                        repos_root = v
                    elif k == 'URL':
                        repos_url = v

                if repos_url.startswith(repos_root):
                    branch = repos_url[len(repos_root) + 1:]
                    if branch.startswith('trunk/'):
                        branch = ''
                    elif branch.startswith('branches/'):
                        branch = '-' + branch.split('/')[1]
                    else:
                        if branch.startswith('tags/'):
                            return
                        branch = '-R-' + branch.replace('/', '-')
                else:
                    branch = '-HUH'
            finally:
                if p:
                    p.wait()

        except:
            pass

    if revision is not None:
        try:
            f = None
            try:
                f = open('.svnrevision', 'w')
                print >> f, '%s|%s' % (revision, branch)
            finally:
                if f:
                    f.close()

        except:
            pass

    elif revision is None:
        try:
            f = None
            try:
                f = open('.svnrevision', 'r')
                l = f.readline().strip()
                revision, branch = l.split('|')
            finally:
                if f:
                    f.close()

        except:
            pass

    if revision is not None:
        if branch is None:
            branch = ''
        return revision + branch
    else:
        return 'UNKNOWN'
        return


class infomedia_dist_build(build):
    user_options = build.user_options
    user_options.append(('src-dir=', None, 'directory holding the source [default: .]'))

    def initialize_options(self):
        build.initialize_options(self)
        self.src_dir = None
        return

    def finalize_options(self):
        if self.src_dir is None:
            self.src_dir = '.'
        build.finalize_options(self)
        return


class infomedia_dist_build_py(build_py):
    user_options = build_py.user_options
    user_options.append(('src-dir=', None, 'directory holding the source [default: .]'))

    def initialize_options(self):
        build_py.initialize_options(self)
        self.src_dir = None
        return

    def finalize_options(self):
        self.set_undefined_options('build', ('src_dir', 'src_dir'))
        if self.src_dir is None:
            self.src_dir = '.'
        build_py.finalize_options(self)
        return

    def get_package_dir(self, package):
        """Return the directory, relative to the top of the source
           distribution, where package 'package' should be found
           (at least according to the 'package_dir' option, if any)."""
        path = string.split(package, '.')
        if not self.package_dir:
            if path:
                return os.path.join(self.src_dir, apply(os.path.join, path))
            else:
                return self.src_dir

        else:
            tail = []
            while path:
                try:
                    pdir = self.package_dir[string.join(path, '.')]
                except KeyError:
                    tail.insert(0, path[(-1)])
                    del path[-1]
                else:
                    tail.insert(0, pdir)
                    return os.path.join(self.src_dir, apply(os.path.join, tail))

            else:
                pdir = self.package_dir.get('')
                if pdir is not None:
                    tail.insert(0, pdir)
                if tail:
                    return os.path.join(self.src_dir, apply(os.path.join, tail))
                return self.src_dir

        return

    def check_package(self, package, package_dir):
        if package_dir != '':
            if not os.path.exists(package_dir):
                if self.src_dir != '.':
                    raise DistutilsFileError, "package directory '%s' does not exist" % package_dir
                else:
                    os.makedirs(package_dir)
            if not os.path.isdir(package_dir):
                raise DistutilsFileError, ("supposed package directory '%s' exists, " + 'but is not a directory') % package_dir
        if package:
            init_py = os.path.join(self.src_dir, package_dir, '__init__.py')
            if os.path.isfile(init_py):
                return init_py
            log.warn("package init file '%s' not found " + '(or not a regular file)', init_py)
        return


class infomedia_dist_build_scripts(build_scripts):
    user_options = build_scripts.user_options
    user_options.append(('src-dir=', None, 'directory holding the source [default: .]'))

    def initialize_options(self):
        build_scripts.initialize_options(self)
        self.src_dir = None
        return

    def finalize_options(self):
        build_scripts.finalize_options(self)
        self.set_undefined_options('build', ('src_dir', 'src_dir'))
        if self.src_dir is None:
            self.src_dir = '.'
        return


class infomedia_dist_install(install):
    user_options = install.user_options
    user_options.append(('src-dir=', None, 'directory holding the source [default: .]'))

    def initialize_options(self):
        install.initialize_options(self)
        self.src_dir = None
        return

    def finalize_options(self):
        if self.src_dir is None:
            self.src_dir = '.'
        install.finalize_options(self)
        return


class infomedia_dist_install_data(install_data):
    user_options = install_data.user_options
    user_options.append(('src-dir=', None, 'directory holding the source [default: .]'))

    def initialize_options(self):
        install_data.initialize_options(self)
        self.src_dir = None
        return

    def finalize_options(self):
        self.set_undefined_options('install', ('src_dir', 'src_dir'))
        if self.src_dir is None:
            self.src_dir = '.'
        install_data.finalize_options(self)
        return

    def run(self):
        self.mkpath(self.install_dir)
        for f in self.data_files:
            if type(f) is StringType:
                f = convert_path(f)
                if self.warn_dir:
                    self.warn("setup script did not provide a directory for '%s' -- installing right in '%s'" % (
                     f, self.install_dir))
                out, _ = self.copy_file(os.path.join(self.src_dir, f), self.install_dir)
                self.outfiles.append(out)
            else:
                dir = convert_path(f[0])
                if not os.path.isabs(dir):
                    dir = os.path.join(self.install_dir, dir)
                elif self.root:
                    dir = change_root(self.root, dir)
                self.mkpath(dir)
                if f[1] == []:
                    self.outfiles.append(dir)
                else:
                    for data in f[1]:
                        data = convert_path(data)
                        out, _ = self.copy_file(os.path.join(self.src_dir, data), dir)
                        self.outfiles.append(out)


__all__ = ('\n    get_revision\n    get_mercurial_revision\n    get_subversion_revision\n    infomedia_dist_build\n    infomedia_dist_build_py\n    infomedia_dist_build_scripts\n    infomedia_dist_install\n    infomedia_dist_install_data\n').split()
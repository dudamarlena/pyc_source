# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\DistExt\Uninstall.py
# Compiled at: 2005-06-21 15:32:54
import os, sys, string, shutil, glob, tempfile
from distutils import filelist, util
from distutils.core import Command
from distutils.dep_util import newer
from types import *

class Uninstall(Command):
    __module__ = __name__
    description = 'uninstall the package'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.announce('determining installation files')
        orig_dry_run = self.distribution.dry_run
        orig_verbose = self.distribution.verbose
        self.distribution.dry_run = 0
        self.distribution.verbose = 0
        self.run_command('build')
        self.distribution.dry_run = 1
        self.run_command('install')
        self.distribution.dry_run = orig_dry_run
        self.distribution.verbose = orig_verbose
        build = self.get_finalized_command('build')
        install = self.get_finalized_command('install')
        root_dirs = [
         install.install_purelib, install.install_platlib, install.install_scripts, install.install_data]
        self.announce('removing files')
        dirs = {}
        filenames = install.get_outputs()
        for filename in filenames:
            if not os.path.isabs(filename):
                raise DistutilsError, 'filename "%s" from .get_output() not absolute' % filename
            if os.path.isfile(filename):
                self.announce("removing '%s'" % filename)
                if not self.dry_run:
                    try:
                        os.remove(filename)
                    except OSError, details:
                        self.warn('Could not remove file: %s' % details)
                    else:
                        dir = os.path.split(filename)[0]
                        if not dirs.has_key(dir):
                            dirs[dir] = 1
                        if os.path.splitext(filename)[1] == '.py':
                            if filename + 'c' not in filenames:
                                try:
                                    os.remove(filename + 'c')
                                except OSError:
                                    pass

                            if filename + 'o' not in filenames:
                                try:
                                    os.remove(filename + 'o')
                                except OSError:
                                    pass

            elif os.path.isdir(filename):
                if not dirs.has_key(dir):
                    dirs[filename] = 1
            else:
                self.announce("skipping removal of '%s' (not found)" % filename)

        self.announce('removing directories')
        dirs = dirs.keys()
        dirs.sort()
        dirs.reverse()
        for dir in dirs:
            if dir in root_dirs:
                continue
            self.announce("removing directory '%s'" % dir)
            if not self.dry_run:
                if os.listdir(dir):
                    self.warn("skipping removal of '%s' (not empty)" % dir)
                else:
                    try:
                        os.rmdir(dir)
                    except OSError, details:
                        self.warn('could not remove directory: %s' % details)

        return
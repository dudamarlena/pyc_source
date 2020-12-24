# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-92t6atcz/setuptools/setuptools/command/rotate.py
# Compiled at: 2020-04-16 14:32:20
# Size of source mod 2**32: 2164 bytes
from distutils.util import convert_path
from distutils import log
from distutils.errors import DistutilsOptionError
import os, shutil
from setuptools.extern import six
from setuptools import Command

class rotate(Command):
    __doc__ = 'Delete older distributions'
    description = 'delete older distributions, keeping N newest files'
    user_options = [
     ('match=', 'm', 'patterns to match (required)'),
     ('dist-dir=', 'd', 'directory where the distributions are'),
     ('keep=', 'k', 'number of matching distributions to keep')]
    boolean_options = []

    def initialize_options(self):
        self.match = None
        self.dist_dir = None
        self.keep = None

    def finalize_options(self):
        if self.match is None:
            raise DistutilsOptionError("Must specify one or more (comma-separated) match patterns (e.g. '.zip' or '.egg')")
        else:
            if self.keep is None:
                raise DistutilsOptionError('Must specify number of files to keep')
            try:
                self.keep = int(self.keep)
            except ValueError:
                raise DistutilsOptionError('--keep must be an integer')

        if isinstance(self.match, six.string_types):
            self.match = [convert_path(p.strip()) for p in self.match.split(',')]
        self.set_undefined_options('bdist', ('dist_dir', 'dist_dir'))

    def run(self):
        self.run_command('egg_info')
        from glob import glob
        for pattern in self.match:
            pattern = self.distribution.get_name() + '*' + pattern
            files = glob(os.path.join(self.dist_dir, pattern))
            files = [(os.path.getmtime(f), f) for f in files]
            files.sort()
            files.reverse()
            log.info('%d file(s) matching %s', len(files), pattern)
            files = files[self.keep:]
            for t, f in files:
                log.info('Deleting %s', f)
                if not self.dry_run:
                    if os.path.isdir(f):
                        shutil.rmtree(f)
                    else:
                        os.unlink(f)
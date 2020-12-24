# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/pkginfo/pkginfo/installed.py
# Compiled at: 2020-01-10 16:25:33
# Size of source mod 2**32: 2003 bytes
import glob, io, os, sys, warnings
from .distribution import Distribution
from ._compat import STRING_TYPES

class Installed(Distribution):

    def __init__(self, package, metadata_version=None):
        if isinstance(package, STRING_TYPES):
            self.package_name = package
            try:
                __import__(package)
            except ImportError:
                package = None

            package = sys.modules[package]
        else:
            self.package_name = package.__name__
        self.package = package
        self.metadata_version = metadata_version
        self.extractMetadata()

    def read(self):
        opj = os.path.join
        if self.package is not None:
            package = self.package.__package__
            if package is None:
                package = self.package.__name__
            pattern = '%s*.egg-info' % package
            file = getattr(self.package, '__file__', None)
            if file is not None:
                candidates = []

                def _add_candidate(where):
                    candidates.extend(glob.glob(where))

                for entry in sys.path:
                    if file.startswith(entry):
                        _add_candidate(opj(entry, 'EGG-INFO'))
                        _add_candidate(opj(entry, pattern))

                dir, name = os.path.split(self.package.__file__)
                _add_candidate(opj(dir, pattern))
                _add_candidate(opj(dir, '..', pattern))
                for candidate in candidates:
                    if os.path.isdir(candidate):
                        path = opj(candidate, 'PKG-INFO')
                    else:
                        path = candidate
                    if os.path.exists(path):
                        with io.open(path, errors='ignore') as (f):
                            return f.read()

        warnings.warn('No PKG-INFO found for package: %s' % self.package_name)
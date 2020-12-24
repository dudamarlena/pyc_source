# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/twine/twine/_installed.py
# Compiled at: 2020-01-10 16:25:25
# Size of source mod 2**32: 2311 bytes
import glob, os, sys, warnings, pkginfo

class Installed(pkginfo.Installed):

    def read(self):
        opj = os.path.join
        if self.package is not None:
            package = self.package.__package__
            if package is None:
                package = self.package.__name__
            egg_pattern = '%s*.egg-info' % package
            dist_pattern = '%s*.dist-info' % package
            file = getattr(self.package, '__file__', None)
            if file is not None:
                candidates = []

                def _add_candidate(where):
                    candidates.extend(glob.glob(where))

                for entry in sys.path:
                    if file.startswith(entry):
                        _add_candidate(opj(entry, 'METADATA'))
                        _add_candidate(opj(entry, 'EGG-INFO'))
                        _add_candidate(opj(entry, egg_pattern))
                        _add_candidate(opj(entry, dist_pattern))

                dir, name = os.path.split(self.package.__file__)
                _add_candidate(opj(dir, egg_pattern))
                _add_candidate(opj(dir, dist_pattern))
                _add_candidate(opj(dir, '..', egg_pattern))
                _add_candidate(opj(dir, '..', dist_pattern))
                for candidate in candidates:
                    if os.path.isdir(candidate):
                        path = opj(candidate, 'PKG-INFO')
                        if not os.path.exists(path):
                            path = opj(candidate, 'METADATA')
                        else:
                            path = candidate
                        if os.path.exists(path):
                            with open(path) as (f):
                                return f.read()

        warnings.warn('No PKG-INFO or METADATA found for package: %s' % self.package_name)
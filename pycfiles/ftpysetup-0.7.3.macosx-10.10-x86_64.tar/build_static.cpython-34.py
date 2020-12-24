# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/local/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/ftpysetup/cmdbuild/build_static.py
# Compiled at: 2015-01-04 11:32:21
# Size of source mod 2**32: 2419 bytes
"""Enhance ``build_py`` to allow recursive directory globbing with ``**``."""
__author__ = ('Lance Finn Helsten', )
__version__ = '0.7.3'
__copyright__ = 'Copyright (C) 2014 Lance Helsten'
__docformat__ = 'reStructuredText en'
__license__ = '\n    Licensed under the Apache License, Version 2.0 (the "License");\n    you may not use this file except in compliance with the License.\n    You may obtain a copy of the License at\n\n        http://www.apache.org/licenses/LICENSE-2.0\n\n    Unless required by applicable law or agreed to in writing, software\n    distributed under the License is distributed on an "AS IS" BASIS,\n    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n    See the License for the specific language governing permissions and\n    limitations under the License.\n'
__all__ = [
 'build_rglob']
import os
from glob import glob
from setuptools.command.build_py import build_py
from distutils.util import convert_path

class build_rglob(build_py):
    __doc__ = 'Enhance ``build_py`` to allow recursive directory globbing with\n    ``**``.\n    '

    def find_data_files(self, package, src_dir):
        globs = self.package_data.get('', []) + self.package_data.get(package, [])
        globs = []
        for pattern in self.package_data.get('', []) + self.package_data.get(package, []):
            if '**' in pattern:
                globs.extend(self._build_rglob__expand_doublestar(src_dir, pattern))
            else:
                globs.append(pattern)

        files = self.manifest_files.get(package, [])[:]
        for pattern in globs:
            gpath = os.path.join(src_dir, convert_path(pattern))
            files.extend(glob(gpath))

        return self.exclude_data_files(package, src_dir, files)

    def __expand_doublestar(self, src_dir, pattern):
        ret = []
        prefix, suffix = pattern.split(sep='**', maxsplit=1)
        suffix = suffix.lstrip(os.sep)
        rootdir = os.path.join(src_dir, prefix)
        for dirpath, dirnames, filenames in os.walk(rootdir):
            path = os.path.join(dirpath, suffix)
            ret.append(path)

        ret = [d.replace(src_dir + os.sep, '') for d in ret]
        return ret
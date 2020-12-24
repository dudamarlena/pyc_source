# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/local/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/ftpysetup/upvers/upvers.py
# Compiled at: 2014-12-30 15:39:48
# Size of source mod 2**32: 4802 bytes
"""Update version information in a project."""
__author__ = ('Lance Finn Helsten', )
__version__ = '0.7.3'
__copyright__ = 'Copyright (C) 2014 Lance Helsten'
__docformat__ = 'reStructuredText en'
__license__ = '\n    Licensed under the Apache License, Version 2.0 (the "License");\n    you may not use this file except in compliance with the License.\n    You may obtain a copy of the License at\n\n        http://www.apache.org/licenses/LICENSE-2.0\n\n    Unless required by applicable law or agreed to in writing, software\n    distributed under the License is distributed on an "AS IS" BASIS,\n    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n    See the License for the specific language governing permissions and\n    limitations under the License.\n'
__all__ = [
 'UpdateVersion']
import sys
if sys.version_info < (3, 3):
    raise Exception('upvers requires Python 3.3 or higher.')
import os, shutil, errno, re, setuptools
from distutils.version import StrictVersion
VERS_RE = re.compile('^(?P<major>\\d+)\\.(?P<minor>\\d+)(\\.(?P<patch>\\d+))?$')

class UpdateVersion(setuptools.Command):
    description = 'Modify project version by changing ``__version__`` tags.'
    user_options = [
     ('set=', None, 'Change version to given value.'),
     ('major', None, 'Move major number to next value set minor to 0.'),
     ('minor', None, 'Move minor number to next value remove patch.'),
     ('patch', None, 'Move patch number to next value.'),
     ('alpha', None, 'Make alpha or increment if already alpha.'),
     ('beta', None, 'Make beta or increment if already beta.'),
     ('release', None, 'Remove alpha or beta.')]

    def initialize_options(self):
        self.set = None
        self.major = False
        self.minor = False
        self.patch = False
        self.alpha = False
        self.beta = False
        self.release = False

    def finalize_options(self):
        if self.set:
            try:
                self.set = StrictVersion(self.set)
            except ValueError as err:
                print('Error:', err, file=sys.stderr)
                sys.exit(errno.EINVAL)

            self.major = False
            self.minor = False
            self.patch = False
            self.alpha = False
            self.beta = False
            self.release = False
        else:
            self.major = bool(self.major)
            self.minor = bool(self.minor)
            self.patch = bool(self.patch)
            self.alpha = bool(self.alpha)
            self.beta = bool(self.beta)
            self.release = bool(self.release)

    def run(self):
        if self.set:
            newver = str(self.set)
        else:
            try:
                oldver = self.distribution.metadata.version
                oldver = StrictVersion(oldver)
            except ValueError as err:
                print('Error: setup.py', err, file=sys.stderr)
                sys.exit(errno.EINVAL)

            major, minor, patch = oldver.version
            pre = oldver.prerelease
            if self.alpha:
                if pre is None or pre[0] != 'a':
                    pre = ('a', 0)
                else:
                    pre = (
                     pre[0], pre[1] + 1)
            else:
                if self.beta:
                    if pre is None or pre[0] != 'b':
                        pre = ('b', 0)
                    else:
                        pre = (
                         pre[0], pre[1] + 1)
                else:
                    if self.release:
                        pre = None
                    else:
                        if self.patch:
                            patch = patch + 1
                            pre = None
                        else:
                            if self.minor:
                                minor = minor + 1
                                patch = 0
                                pre = None
                            else:
                                if self.major:
                                    major = major + 1
                                    minor = 0
                                    patch = 0
                                    pre = None
                                else:
                                    return
                newver = StrictVersion()
                newver.version = (major, minor, patch)
                newver.prerelease = pre
                newver = str(newver)
        for dirpath, dirnames, filenames in os.walk(os.curdir):
            for filename in (f for f in filenames if os.path.splitext(f)[1] == '.py'):
                inpath = os.path.join(dirpath, filename)
                outpath = inpath + '.tmp'
                with open(inpath) as (fin):
                    with open(outpath, 'w') as (fout):
                        for line in fin:
                            if line.startswith('__version__'):
                                line = "__version__ = '{0}'\n".format(newver)
                            fout.write(line)

                shutil.copystat(inpath, outpath)
                os.replace(outpath, inpath)
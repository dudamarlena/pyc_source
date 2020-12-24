# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pygit2/_build.py
# Compiled at: 2019-12-04 19:15:05
"""
This is an special module, it provides stuff used by setup.py at build time.
But also used by pygit2 at run time.
"""
import os
from os import getenv
__version__ = '0.28.2'

def _get_libgit2_path():
    libgit2_path = getenv('LIBGIT2')
    if libgit2_path is not None:
        return libgit2_path
    else:
        if os.name == 'nt':
            return '%s\\libgit2' % getenv('ProgramFiles')
        return '/usr/local'


def get_libgit2_paths():
    libgit2_path = _get_libgit2_path()
    return (
     os.path.join(libgit2_path, 'bin'),
     os.path.join(libgit2_path, 'include'),
     getenv('LIBGIT2_LIB', os.path.join(libgit2_path, 'lib')))
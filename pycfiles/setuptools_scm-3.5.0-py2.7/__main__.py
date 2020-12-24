# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/setuptools_scm/__main__.py
# Compiled at: 2020-02-13 15:05:29
from __future__ import print_function
import sys
from setuptools_scm import get_version
from setuptools_scm.integration import find_files
from setuptools_scm.version import _warn_if_setuptools_outdated

def main():
    _warn_if_setuptools_outdated()
    print('Guessed Version', get_version())
    if 'ls' in sys.argv:
        for fname in find_files('.'):
            print(fname)


if __name__ == '__main__':
    main()
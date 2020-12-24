# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plottwist/libs/pyblish/__version__.py
# Compiled at: 2020-04-17 19:10:58
# Size of source mod 2**32: 519 bytes
__doc__ = '\nVersion module for plottwist-libs-pyblish\n'
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
__version__ = None

def get_version():
    global __version__
    if __version__:
        return __version__
    else:
        from ._version import get_versions
        __version__ = get_versions()['version']
        del get_versions
        return __version__
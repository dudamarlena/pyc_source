# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ampoule/_version.py
# Compiled at: 2019-12-22 01:44:27
# Size of source mod 2**32: 261 bytes
__doc__ = '\nProvides ampoule version information.\n'
from incremental import Version
__version__ = Version('ampoule', 19, 12, 0)
__all__ = ['__version__']
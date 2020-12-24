# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ampoule/_version.py
# Compiled at: 2019-12-22 01:44:27
# Size of source mod 2**32: 261 bytes
"""
Provides ampoule version information.
"""
from incremental import Version
__version__ = Version('ampoule', 19, 12, 0)
__all__ = ['__version__']
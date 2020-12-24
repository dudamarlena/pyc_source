# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hannu/soft/anaconda/envs/p36/lib/python3.6/site-packages/ldtk/__init__.py
# Compiled at: 2017-09-18 12:06:01
# Size of source mod 2**32: 291 bytes
from .ldmodel import *
from .ldtk import LDPSetCreator, LDPSet, load_ldpset
from .filters import BoxcarFilter, TabulatedFilter
version_info = (1, 0, 0)
version = '.'.join(str(c) for c in version_info)
__all__ = [
 'LDPSetCreator', 'LDPSet', 'load_ldpset', 'BoxcarFilter', 'TabulatedFilter']
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/Documents/repos/parsely/fluster/fluster/__init__.py
# Compiled at: 2018-06-08 15:10:06
# Size of source mod 2**32: 152 bytes
__version__ = '0.0.5'
from .cluster import FlusterCluster
from .exceptions import ClusterEmptyError
__all__ = [
 'FlusterCluster', 'ClusterEmptyError']
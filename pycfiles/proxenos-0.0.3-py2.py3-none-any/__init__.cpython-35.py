# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dave/Projects/Github/proxenos/src/proxenos/__init__.py
# Compiled at: 2017-01-21 20:16:05
# Size of source mod 2**32: 271 bytes
"""proxenos: A rendezvous hashing and service routing toolkit."""
from __future__ import absolute_import
import pkg_resources
try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'
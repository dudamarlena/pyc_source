# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /mnt/c/Users/dave/Projects/Github/proxenos/src/proxenos/__init__.py
# Compiled at: 2017-01-19 23:36:30
# Size of source mod 2**32: 275 bytes
__doc__ = 'proxenos: Rendezvous hashing based routing for Consul services.'
from __future__ import absolute_import
import pkg_resources
try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.7.5/x64/lib/python3.7/site-packages/nnp/__init__.py
# Compiled at: 2019-11-24 03:15:15
# Size of source mod 2**32: 210 bytes
"""TODO: doc"""
from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    pass
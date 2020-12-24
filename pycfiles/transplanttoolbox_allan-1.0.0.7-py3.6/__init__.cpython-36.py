# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/transplanttoolbox_allan/__init__.py
# Compiled at: 2018-04-04 17:55:52
# Size of source mod 2**32: 307 bytes
from pkg_resources import get_distribution, DistributionNotFound
try:
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'
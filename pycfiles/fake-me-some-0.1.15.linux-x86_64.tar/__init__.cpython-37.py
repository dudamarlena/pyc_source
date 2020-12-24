# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/fake_me_some/__init__.py
# Compiled at: 2019-06-21 12:12:23
# Size of source mod 2**32: 365 bytes
from pkg_resources import get_distribution, DistributionNotFound
try:
    try:
        dist_name = __name__
        __version__ = get_distribution(dist_name).version
    except DistributionNotFound:
        __version__ = 'unknown'

finally:
    del get_distribution
    del DistributionNotFound
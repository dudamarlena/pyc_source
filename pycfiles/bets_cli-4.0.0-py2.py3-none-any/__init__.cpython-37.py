# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\PROJECT_HOME\bets-cli\src\bets\__init__.py
# Compiled at: 2019-02-08 18:44:59
# Size of source mod 2**32: 436 bytes
from pkg_resources import get_distribution, DistributionNotFound
try:
    try:
        dist_name = 'bets-cli'
        __version__ = get_distribution(dist_name).version
    except DistributionNotFound:
        __version__ = 'unknown'

finally:
    del get_distribution
    del DistributionNotFound
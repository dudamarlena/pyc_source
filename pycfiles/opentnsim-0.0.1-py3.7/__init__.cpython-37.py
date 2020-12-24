# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\transport_network_analysis\__init__.py
# Compiled at: 2019-01-03 05:07:50
# Size of source mod 2**32: 394 bytes
from pkg_resources import get_distribution, DistributionNotFound
try:
    try:
        dist_name = 'transport-network-analysis'
        __version__ = get_distribution(dist_name).version
    except DistributionNotFound:
        __version__ = 'unknown'

finally:
    del get_distribution
    del DistributionNotFound
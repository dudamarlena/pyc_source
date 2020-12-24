# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Alister/miniconda3/envs/obsea/lib/python3.7/site-packages/obsea/__init__.py
# Compiled at: 2019-07-10 06:05:58
# Size of source mod 2**32: 560 bytes
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

from .ais import *
from .beamforming import *
from .core import *
from .datasets import *
from .gis import *
from .io import *
from .plot import *
from .processing import *
from .station import *
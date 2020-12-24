# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flowproc/__init__.py
# Compiled at: 2019-08-04 14:02:53
# Size of source mod 2**32: 481 bytes
"""
tbd
"""
import logging
from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution
__author__ = 'Tobias Frei'
__copyright__ = 'Tobias Frei'
__license__ = 'mit'
logger = logging.getLogger(__name__)
try:
    try:
        dist_name = __name__
        __version__ = get_distribution(dist_name).version
    except DistributionNotFound:
        __version__ = 'unknown'

finally:
    del get_distribution
    del DistributionNotFound
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/project/datamaestro/__init__.py
# Compiled at: 2020-02-25 07:34:23
# Size of source mod 2**32: 235 bytes
from .context import Context, Repository, prepare_dataset
from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = None
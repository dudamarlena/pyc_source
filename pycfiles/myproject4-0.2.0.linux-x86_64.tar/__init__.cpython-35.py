# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ranjeet/pythonProjects/evironments2/venv/lib/python3.5/site-packages/myproject4/__init__.py
# Compiled at: 2018-03-26 21:51:30
# Size of source mod 2**32: 307 bytes
from pkg_resources import get_distribution, DistributionNotFound
try:
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'
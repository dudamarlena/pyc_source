# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/py2opencl/__init__.py
# Compiled at: 2014-07-27 01:42:14
from pkg_resources import get_distribution, DistributionNotFound
import os.path
try:
    _dist = get_distribution('foobar')
    if not __file__.startswith(os.path.join(_dist.location, 'foobar')):
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'Please install this project with setup.py'
else:
    __version__ = _dist.version

from .driver import Py2OpenCL
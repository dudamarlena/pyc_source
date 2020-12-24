# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
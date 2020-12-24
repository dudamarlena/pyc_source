# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mburger/Work/Research/NeutralCloudModel/nexoclom/build/lib/nexoclom/__init__.py
# Compiled at: 2019-02-21 11:34:07
# Size of source mod 2**32: 1115 bytes
from ._astropy_init import *
import sys
name = 'nexoclam'
__minimum_python_version__ = '3.6'

class UnsupportedPythonError(Exception):
    pass


if sys.version_info < tuple((int(val) for val in __minimum_python_version__.split('.'))):
    raise UnsupportedPythonError('nexoclom does not support Python < {}'.format(__minimum_python_version__))
from .Input import Input
from .Output import Output
from .modeldriver import modeldriver
from .LOSResult import LOSResult
from .configure_model import configfile
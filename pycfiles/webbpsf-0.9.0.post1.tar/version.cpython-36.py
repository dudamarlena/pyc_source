# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rgeda/project/repo/webbpsf/astropy_helpers/astropy_helpers/version.py
# Compiled at: 2019-07-20 17:47:22
# Size of source mod 2**32: 567 bytes
from __future__ import unicode_literals
import datetime
version = '3.0.2'
githash = 'ca630405b54d40695b7bbd2824cb0f142b5811b6'
major = 3
minor = 0
bugfix = 2
release = True
timestamp = datetime.datetime(2019, 7, 20, 21, 47, 22)
debug = False
astropy_helpers_version = ''
try:
    from ._compiler import compiler
except ImportError:
    compiler = 'unknown'

try:
    from .cython_version import cython_version
except ImportError:
    cython_version = 'unknown'
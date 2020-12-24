# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/async_pokepy/__init__.py
# Compiled at: 2019-05-20 16:37:56
# Size of source mod 2**32: 668 bytes
"""
PokeAPI.co API Wrapper
~~~~~~~~~~~~~~~~~~~
A basic wrapper for the PokeAPI.co API.
:copyright: (c) 2019 Lorenzo
:license: MIT, see LICENSE for more details.
"""
__title__ = 'async_pokepy'
__author__ = 'Lorenzo'
__docformat__ = 'restructuredtext en'
__license__ = 'MIT'
__copyright__ = 'Copyright 2019 Lorenzo'
__version__ = '0.1.5a'
from collections import namedtuple
from .client import Client
from .exceptions import *
from .types import *
VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel')
version_info = VersionInfo(major=0, minor=1, micro=5, releaselevel='alpha')
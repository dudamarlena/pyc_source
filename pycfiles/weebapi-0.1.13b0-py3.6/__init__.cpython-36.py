# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\weebapi\__init__.py
# Compiled at: 2018-05-20 05:37:14
# Size of source mod 2**32: 771 bytes
"""Weeb.sh API Wrapper for discord.py integration
"""
__title__ = 'weebapi'
__author__ = 'AndyTempel'
__license__ = 'MIT'
__copyright__ = 'Copyright 2018 AndyTempel'
__version__ = '0.1.13b'
import logging
from collections import namedtuple
from weebapi.data_objects import *
from weebapi.errors import *
from weebapi.client import Client
VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
version_info = VersionInfo(major=0, minor=1, micro=12, releaselevel='beta', serial=0)
try:
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):

        def emit(self, record):
            pass


logging.getLogger(__name__).addHandler(NullHandler())
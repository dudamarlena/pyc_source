# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ksoftapi\__init__.py
# Compiled at: 2020-04-19 15:04:11
# Size of source mod 2**32: 837 bytes
"""
KSoft.Si API Wrapper with discord.py integration
"""
__title__ = 'ksoftapi'
__author__ = 'AndyTempel'
__license__ = 'GNU'
__copyright__ = 'Copyright 2018-2020 AndyTempel'
__version__ = '0.2.2a'
import logging
from collections import namedtuple
from .client import Client
from .errors import APIError, Forbidden, NoResults
from .events import BanUpdateEvent
VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
version_info = VersionInfo(major=0, minor=2, micro=2, releaselevel='alpha', serial=0)
try:
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):

        def emit(self, record):
            pass


else:
    logging.getLogger(__name__).addHandler(NullHandler())
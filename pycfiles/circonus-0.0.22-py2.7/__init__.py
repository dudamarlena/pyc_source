# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/circonus/__init__.py
# Compiled at: 2015-02-14 15:08:43
__title__ = 'circonus'
__version__ = '0.0.22'
from logging import NullHandler
import logging
from circonus.client import CirconusClient
logging.getLogger(__name__).addHandler(NullHandler())
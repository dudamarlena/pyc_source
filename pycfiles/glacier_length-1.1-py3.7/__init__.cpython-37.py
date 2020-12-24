# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\glacier_length\__init__.py
# Compiled at: 2019-11-12 01:32:15
# Size of source mod 2**32: 205 bytes
import logging
from ._src import get_all_length
__version__ = '1.1'
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
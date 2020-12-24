# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/sdb1/Documents/workspace/piwigo/piwigo/__init__.py
# Compiled at: 2016-01-19 13:21:07
"""
    Module piwigo
"""
from piwigo.ws import Piwigo, WsNotExistException, WsErrorException, WsPiwigoException
__version_info__ = (1, 0, 0)
__version__ = ('.').join([ str(val) for val in __version_info__ ])
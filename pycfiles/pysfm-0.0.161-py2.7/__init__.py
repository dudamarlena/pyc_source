# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pysfm\__init__.py
# Compiled at: 2018-02-22 21:11:59
from pysfm_module import *
import core.pysfm_version
try:
    __version__ = core.pysfm_version.get_version()
except Exception as e:
    __version__ = 'Test version for Local installation. (develop)'

VERSION = __version__
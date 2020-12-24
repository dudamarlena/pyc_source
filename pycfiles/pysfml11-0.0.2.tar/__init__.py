# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\pysfm\__init__.py
# Compiled at: 2018-02-22 21:11:59
from pysfm_module import *
import core.pysfm_version
try:
    __version__ = core.pysfm_version.get_version()
except Exception as e:
    __version__ = 'Test version for Local installation. (develop)'

VERSION = __version__
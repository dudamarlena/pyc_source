# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\swapdate\__init__.py
# Compiled at: 2016-10-17 16:51:56
import pkg_resources
from swapdate import get
try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'
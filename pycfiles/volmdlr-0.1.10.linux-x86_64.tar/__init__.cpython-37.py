# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/volmdlr/__init__.py
# Compiled at: 2020-03-11 05:21:08
# Size of source mod 2**32: 126 bytes
import pkg_resources
__version__ = pkg_resources.require('volmdlr')[0].version
from .core import *
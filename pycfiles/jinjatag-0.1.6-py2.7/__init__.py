# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jinjatag/__init__.py
# Compiled at: 2012-03-30 16:05:37
from .version import __version__
try:
    from .decorators import *
    from .extension import *
except ImportError:
    pass
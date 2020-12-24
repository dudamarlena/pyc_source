# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyclamd/__init__.py
# Compiled at: 2014-07-14 13:23:56
import sys
if sys.version_info[0] <= 2:
    from pyclamd import __version__
    from pyclamd import *
elif sys.version_info[0] >= 3:
    from .pyclamd import __version__
    from .pyclamd import *
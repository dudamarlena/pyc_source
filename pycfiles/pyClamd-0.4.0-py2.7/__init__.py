# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyclamd/__init__.py
# Compiled at: 2014-07-14 13:23:56
import sys
if sys.version_info[0] <= 2:
    from pyclamd import __version__
    from pyclamd import *
elif sys.version_info[0] >= 3:
    from .pyclamd import __version__
    from .pyclamd import *
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pymodelfit/__init__.py
# Compiled at: 2011-05-10 05:46:57
"""
pymodelfit -- a pythonic, object-oriented framework and GUI tool for fitting
data to models.
"""
_release = True
_majorversion = 0
_minorversion = 1
_bugfix = 2
version = str(_majorversion) + '.' + str(_minorversion) + ('' if _bugfix is None else '.' + str(_bugfix)) + ('' if _release else 'dev')
from core import *
from builtins import *
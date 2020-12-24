# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymodelfit/__init__.py
# Compiled at: 2011-05-10 05:46:57
__doc__ = '\npymodelfit -- a pythonic, object-oriented framework and GUI tool for fitting\ndata to models.\n'
_release = True
_majorversion = 0
_minorversion = 1
_bugfix = 2
version = str(_majorversion) + '.' + str(_minorversion) + ('' if _bugfix is None else '.' + str(_bugfix)) + ('' if _release else 'dev')
from core import *
from builtins import *
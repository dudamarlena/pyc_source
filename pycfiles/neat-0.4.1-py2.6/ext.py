# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.openbsd-4.7-i386/egg/neat/ext.py
# Compiled at: 2010-09-02 10:23:20
"""Add included modules here.
"""
import os
__all__ = []
project = os.path.basename(os.path.dirname(__file__))
ext = project + '._ext'
(name, module) = (None, None)
for name in __all__:
    try:
        module = __import__(name)
    except ImportError:
        module = __import__(('.').join((ext, name)), fromlist=[ext])

    locals()[name] = module

del ext
del module
del name
del project
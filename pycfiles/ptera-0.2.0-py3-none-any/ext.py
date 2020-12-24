# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.openbsd-4.7-i386/egg/ptemplate/ext.py
# Compiled at: 2011-08-05 07:54:56
__doc__ = 'Add included modules here.\n'
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
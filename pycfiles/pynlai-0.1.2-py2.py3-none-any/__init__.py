# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pynk/__init__.py
# Compiled at: 2019-01-03 04:37:50
__doc__ = "\nPython-nuklear integration library.\n\nNuklear is exposed via the 'cffi' library; you make calls via the 'lib'\nand 'ffi' objects.  'lib' exposes the nuklear api, while 'ffi' is used\nfor interfacing with C.  Note that this is a very low level interface;\nyou must understand both C and Python, and the 'cffi' library.\n\nFor details of the API, see nuklear.h.  You can also do help(lib) to\nsee what methods are exposed, but it won't tell you about their arguments.\n\nFor how to use the foreign function interface, see the documentation for\nthe 'cffi' library.\n\nFor an example, see 'demo.py'.\n"
from _nuklear import lib, ffi
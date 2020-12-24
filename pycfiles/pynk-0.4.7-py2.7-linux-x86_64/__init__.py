# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynk/__init__.py
# Compiled at: 2019-01-03 04:37:50
"""
Python-nuklear integration library.

Nuklear is exposed via the 'cffi' library; you make calls via the 'lib'
and 'ffi' objects.  'lib' exposes the nuklear api, while 'ffi' is used
for interfacing with C.  Note that this is a very low level interface;
you must understand both C and Python, and the 'cffi' library.

For details of the API, see nuklear.h.  You can also do help(lib) to
see what methods are exposed, but it won't tell you about their arguments.

For how to use the foreign function interface, see the documentation for
the 'cffi' library.

For an example, see 'demo.py'.
"""
from _nuklear import lib, ffi
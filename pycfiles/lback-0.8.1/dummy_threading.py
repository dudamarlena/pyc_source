# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: dummy_threading.pyc
# Compiled at: 2011-03-08 12:43:14
"""Faux ``threading`` version using ``dummy_thread`` instead of ``thread``.

The module ``_dummy_threading`` is added to ``sys.modules`` in order
to not have ``threading`` considered imported.  Had ``threading`` been
directly imported it would have made all subsequent imports succeed
regardless of whether ``thread`` was available which is not desired.

"""
from sys import modules as sys_modules
import dummy_thread
holding_thread = False
holding_threading = False
holding__threading_local = False
try:
    if 'thread' in sys_modules:
        held_thread = sys_modules['thread']
        holding_thread = True
    sys_modules['thread'] = sys_modules['dummy_thread']
    if 'threading' in sys_modules:
        held_threading = sys_modules['threading']
        holding_threading = True
        del sys_modules['threading']
    if '_threading_local' in sys_modules:
        held__threading_local = sys_modules['_threading_local']
        holding__threading_local = True
        del sys_modules['_threading_local']
    import threading
    sys_modules['_dummy_threading'] = sys_modules['threading']
    del sys_modules['threading']
    sys_modules['_dummy__threading_local'] = sys_modules['_threading_local']
    del sys_modules['_threading_local']
    from _dummy_threading import *
    from _dummy_threading import __all__
finally:
    if holding_threading:
        sys_modules['threading'] = held_threading
        del held_threading
    del holding_threading
    if holding__threading_local:
        sys_modules['_threading_local'] = held__threading_local
        del held__threading_local
    del holding__threading_local
    if holding_thread:
        sys_modules['thread'] = held_thread
        del held_thread
    else:
        del sys_modules['thread']
    del holding_thread
    del dummy_thread
    del sys_modules
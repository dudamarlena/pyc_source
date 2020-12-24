# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/makina/pasteStage/pasteFunBot/Paste-1.7.2-py2.6.egg/paste/util/killthread.py
# Compiled at: 2009-07-20 09:44:04
"""
Kill a thread, from http://sebulba.wikispaces.com/recipe+thread2
"""
import types
try:
    import ctypes
except ImportError:
    raise ImportError('You cannot use paste.util.killthread without ctypes installed')

if not hasattr(ctypes, 'pythonapi'):
    raise ImportError('You cannot use paste.util.killthread without ctypes.pythonapi')

def async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed.

    tid is the value given by thread.get_ident() (an integer).
    Raise SystemExit to kill a thread."""
    if not isinstance(exctype, (types.ClassType, type)):
        raise TypeError('Only types can be raised (not instances)')
    if not isinstance(tid, int):
        raise TypeError('tid must be an integer')
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError('invalid thread id')
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError('PyThreadState_SetAsyncExc failed')
# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/Paste-1.7.5.1-py2.6.egg/paste/util/killthread.py
# Compiled at: 2012-02-27 07:41:58
__doc__ = '\nKill a thread, from http://sebulba.wikispaces.com/recipe+thread2\n'
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
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError('invalid thread id')
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), 0)
        raise SystemError('PyThreadState_SetAsyncExc failed')
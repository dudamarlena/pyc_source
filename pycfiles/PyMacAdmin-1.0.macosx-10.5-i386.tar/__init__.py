# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/Development/pymacadmin-env/lib/python2.5/site-packages/PyMacAdmin/__init__.py
# Compiled at: 2009-06-07 22:49:10
from functools import wraps
import ctypes

def mac_strerror(errno):
    """Returns an error string for a classic MacOS error return code"""
    try:
        import MacOS
        return MacOS.GetErrorString(errno)
    except ImportError:
        return 'Unknown error %d: MacOS.GetErrorString is not available by this Python'


def carbon_errcheck(rc, func, args):
    if rc < 0:
        raise RuntimeError('%s(%s) returned %d: %s' % (func.__name__, map(repr, args), rc, mac_strerror(rc)))
    return rc


def carbon_call(f, *args):
    """
    Wrapper for Carbon calls inspired by subprocess.check_call(): a negative
    rc will generate a RuntimeError with a [hopefully] informative message.
    """
    rc = f(*args)
    return carbon_errcheck(rc, f, args)


def load_carbon_framework(f_path):
    """
    Load a Carbon framework using ctypes.CDLL and add an errcheck wrapper to
    replace traditional errno-style error checks with exception handling.

    Example:
    >>> load_carbon_framework('/System/Library/Frameworks/Security.framework/Versions/Current/Security') # doctest: +ELLIPSIS
    <CDLL '/System/Library/Frameworks/Security.framework/Versions/Current/Security', handle ... at ...>
    """
    framework = ctypes.cdll.LoadLibrary(f_path)
    old_getitem = framework.__getitem__

    @wraps(old_getitem)
    def new_getitem(k):
        v = old_getitem(k)
        if hasattr(v, 'errcheck') and not v.errcheck:
            v.errcheck = carbon_errcheck
        return v

    framework.__getitem__ = new_getitem
    return framework
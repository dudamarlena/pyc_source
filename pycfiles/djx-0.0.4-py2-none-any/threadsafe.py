# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/gis/geos/prototypes/threadsafe.py
# Compiled at: 2019-02-14 00:35:16
import threading
from django.contrib.gis.geos.base import GEOSBase
from django.contrib.gis.geos.libgeos import CONTEXT_PTR, error_h, lgeos, notice_h

class GEOSContextHandle(GEOSBase):
    """
    Python object representing a GEOS context handle.
    """
    ptr_type = CONTEXT_PTR
    destructor = lgeos.finishGEOS_r

    def __init__(self):
        self.ptr = lgeos.initGEOS_r(notice_h, error_h)


class GEOSContext(threading.local):
    handle = None


thread_context = GEOSContext()

class GEOSFunc(object):
    """
    Class that serves as a wrapper for GEOS C Functions, and will
    use thread-safe function variants when available.
    """

    def __init__(self, func_name):
        try:
            self.cfunc = getattr(lgeos, func_name + '_r')
            self.threaded = True
            self.thread_context = thread_context
        except AttributeError:
            self.cfunc = getattr(lgeos, func_name)
            self.threaded = False

    def __call__(self, *args):
        if self.threaded:
            if not self.thread_context.handle:
                self.thread_context.handle = GEOSContextHandle()
            return self.cfunc(self.thread_context.handle.ptr, *args)
        else:
            return self.cfunc(*args)

    def __str__(self):
        return self.cfunc.__name__

    def _get_argtypes(self):
        return self.cfunc.argtypes

    def _set_argtypes(self, argtypes):
        if self.threaded:
            new_argtypes = [
             CONTEXT_PTR]
            new_argtypes.extend(argtypes)
            self.cfunc.argtypes = new_argtypes
        else:
            self.cfunc.argtypes = argtypes

    argtypes = property(_get_argtypes, _set_argtypes)

    def _get_restype(self):
        return self.cfunc.restype

    def _set_restype(self, restype):
        self.cfunc.restype = restype

    restype = property(_get_restype, _set_restype)

    def _get_errcheck(self):
        return self.cfunc.errcheck

    def _set_errcheck(self, errcheck):
        self.cfunc.errcheck = errcheck

    errcheck = property(_get_errcheck, _set_errcheck)
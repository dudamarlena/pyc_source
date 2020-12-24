# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/gis/ptr.py
# Compiled at: 2019-02-14 00:35:16
from ctypes import c_void_p

class CPointerBase(object):
    """
    Base class for objects that have a pointer access property
    that controls access to the underlying C pointer.
    """
    _ptr = None
    ptr_type = c_void_p
    destructor = None
    null_ptr_exception_class = AttributeError

    @property
    def ptr(self):
        if self._ptr:
            return self._ptr
        raise self.null_ptr_exception_class('NULL %s pointer encountered.' % self.__class__.__name__)

    @ptr.setter
    def ptr(self, ptr):
        if not (ptr is None or isinstance(ptr, self.ptr_type)):
            raise TypeError('Incompatible pointer type: %s.' % type(ptr))
        self._ptr = ptr
        return

    def __del__(self):
        """
        Free the memory used by the C++ object.
        """
        if self.destructor and self._ptr:
            try:
                self.destructor(self.ptr)
            except (AttributeError, TypeError):
                pass
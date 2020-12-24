# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lameiro/projects/cx_oracle_on_ctypes/cx_Oracle/buffer.py
# Compiled at: 2015-08-21 16:35:45
import ctypes
from custom_exceptions import CXORA_TYPE_ERROR
from utils import bytes, python2
import oci

class cxBuffer(object):

    def __init__(self, ptr, size, num_characters, obj):
        self.ptr = ptr
        self.size = size
        self.num_characters = num_characters
        self.obj = obj
        self.cast_ptr = ctypes.cast(ptr, ctypes.POINTER(oci.ub1))

    @staticmethod
    def new_as_copy(copy_from_buf):
        """Copy the contents of the buffer."""
        result = cxBuffer(copy_from_buf.ptr, copy_from_buf.size, copy_from_buf.num_characters, copy_from_buf.obj)
        return result

    @staticmethod
    def new_from_object(obj, encoding):
        """Populate the string buffer from a unicode object."""
        if obj is None:
            return cxBuffer.new_null()
        if isinstance(obj, unicode):
            as_bytes = obj.encode(encoding)
        elif isinstance(obj, bytes):
            as_bytes = obj
        elif python2() and isinstance(obj, buffer):
            as_bytes = str(obj)
        else:
            raise TypeError(CXORA_TYPE_ERROR)
        typed_ptr = ctypes.create_string_buffer(as_bytes)
        result = cxBuffer(typed_ptr, len(as_bytes), len(obj), obj)
        result.keepalive = typed_ptr
        return result

    @staticmethod
    def new_null():
        result = cxBuffer(ctypes.c_void_p(), 0, 0, None)
        return result
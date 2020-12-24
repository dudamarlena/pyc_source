# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lameiro/projects/cx_oracle_on_ctypes/cx_Oracle/error.py
# Compiled at: 2015-05-19 16:59:20
from ctypes import byref
import ctypes
from custom_exceptions import InternalError
import oci
from utils import python3_or_better

class Error(object):

    def __init__(self, environment, context, retrieve_error):
        self.context = context
        if retrieve_error:
            if environment.error_handle:
                handle = environment.error_handle
                handle_type = oci.OCI_HTYPE_ERROR
            else:
                handle = environment.handle
                handle_type = oci.OCI_HTYPE_ENV
            error_text = ctypes.create_string_buffer(4096)
            error_text_as_ub1_pointer = ctypes.cast(error_text, oci.POINTER(oci.ub1))
            c_code = oci.sb4()
            argtypes = oci.OCIErrorGet.argtypes
            status = oci.OCIErrorGet(handle, 1, argtypes[2](), byref(c_code), error_text_as_ub1_pointer, len(error_text), handle_type)
            self.code = c_code.value
            if status != oci.OCI_SUCCESS:
                raise InternalError('No Oracle error?')
            if not python3_or_better():
                self.message = error_text.value
            else:
                self.message = error_text.decode(environment.encoding)

    def __str__(self):
        return self.message

    __repr__ = __str__
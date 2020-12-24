# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lameiro/projects/cx_oracle_on_ctypes/cx_Oracle/pythonic_oci.py
# Compiled at: 2015-10-04 18:10:52
import ctypes
from ctypes import byref, cast, c_void_p, POINTER
import oci

def OCIAttrGet(param, oci_function, oci_type, oci_subfunction, environment, context):
    c_result = oci_type()
    argtypes = oci.OCIAttrGet.argtypes
    status = oci.OCIAttrGet(param, oci_function, byref(c_result), argtypes[3](), oci_subfunction, environment.error_handle)
    environment.check_for_error(status, context)
    return c_result.value


def OCIParamGet(handle, htype, environment, pos, context):
    param_type = oci.POINTER(oci.OCIParam)
    param = ctypes.c_void_p()
    status = oci.OCIParamGet(handle, htype, environment.error_handle, byref(param), pos)
    environment.check_for_error(status, context)
    result = ctypes.cast(param, param_type)
    return result


def OCIHandleAlloc(environment, handle, handle_type, error_message):
    argtypes = oci.OCIHandleAlloc.argtypes
    status = oci.OCIHandleAlloc(environment.handle, cast(byref(handle), POINTER(c_void_p)), handle_type, 0, argtypes[4]())
    environment.check_for_error(status, error_message)
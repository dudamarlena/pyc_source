# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lameiro/projects/cx_oracle_on_ctypes/cx_Oracle/descriptor_manager.py
# Compiled at: 2015-10-04 18:18:15
import oci
from ctypes import byref, cast, POINTER, c_void_p

class DescriptorManager(object):

    def finalize(self, variable_type, var, oracle_descriptor_type):
        typed_data = variable_type.get_typed_data(var)
        for i in xrange(var.allocelems):
            if typed_data[i]:
                oci.OCIDescriptorFree(typed_data[i], oracle_descriptor_type)

    def initialize(self, variable_type, var, cursor, oracle_descriptor_type, message):
        typed_data = variable_type.get_typed_data(var)
        arg4 = oci.OCIDescriptorAlloc.argtypes[4]()
        for i in xrange(var.allocelems):
            element = typed_data[i]
            element_cast = cast(byref(element), POINTER(c_void_p))
            status = oci.OCIDescriptorAlloc(var.environment.handle, element_cast, oracle_descriptor_type, 0, arg4)
            var.environment.check_for_error(status, message)
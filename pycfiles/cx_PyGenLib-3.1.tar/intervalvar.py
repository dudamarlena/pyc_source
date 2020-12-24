# uncompyle6 version 3.6.7
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/lameiro/projects/cx_oracle_on_ctypes/cx_Oracle/intervalvar.py
# Compiled at: 2015-05-19 16:59:20
import oci, ctypes
from ctypes import byref
from datetime import timedelta
from descriptor_manager import DescriptorManager
from variable import Variable
from variable_type import VariableType
from transforms import oracle_interval_to_python_delta

class INTERVAL(Variable):
    pass


class IntervalVariableType(VariableType):

    def __init__(self):
        VariableType.__init__(self)
        self.oci_type = oci.POINTER(oci.OCIInterval)
        self.pre_define_proc = None
        self.post_define_proc = None
        self.pre_fetch_proc = None
        self.is_null_proc = None
        self.get_buffer_size_proc = None
        self.python_type = INTERVAL
        self.oracle_type = oci.SQLT_INTERVAL_DS
        self.charset_form = oci.SQLCS_IMPLICIT
        self.size = ctypes.sizeof(self.oci_type)
        self.is_character_data = False
        self.is_variable_length = False
        self.can_be_copied = True
        self.can_be_in_array = True
        self.descriptor_manager = DescriptorManager()

    def initialize_proc(self, var, cursor):
        self.descriptor_manager.initialize(self, var, cursor, oci.OCI_DTYPE_INTERVAL_DS, 'IntervalVar_Initialize()')

    def finalize_proc(self, var):
        self.descriptor_manager.finalize(self, var, oci.OCI_DTYPE_INTERVAL_DS)

    def set_value_proc(self, var, pos, value):
        typed_data = self.get_typed_data(var)
        if not isinstance(value, timedelta):
            raise TypeError('expecting timedelta data')
        hours, seconds = divmod(value.seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        status = oci.OCIIntervalSetDaySecond(var.environment.handle, var.environment.error_handle, value.days, hours, minutes, seconds, value.microseconds, typed_data[pos])
        var.environment.check_for_error(status, 'IntervalVar_SetValue()')

    def get_value_proc(self, var, pos):
        typed_data = self.get_typed_data(var)
        return oracle_interval_to_python_delta(var.environment, typed_data[pos])


vt_Interval = IntervalVariableType()
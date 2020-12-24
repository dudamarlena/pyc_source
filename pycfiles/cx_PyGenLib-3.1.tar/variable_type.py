# uncompyle6 version 3.6.7
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/lameiro/projects/cx_oracle_on_ctypes/cx_Oracle/variable_type.py
# Compiled at: 2015-05-19 16:59:20
import ctypes, oci

class VariableType(object):

    def __init__(self):
        self.python_type = None
        self.oracle_type = None
        self.charset_form = None
        self.size = None
        self.is_character_data = None
        self.is_variable_length = None
        self.can_be_copied = None
        self.can_be_in_array = None

    def initialize_proc(self, var, cursor):
        raise NotImplementedError()

    def get_buffer_size_proc(self, var):
        raise NotImplementedError()

    def finalize_proc(self, var):
        raise NotImplementedError()

    def pre_define_proc(self, *args, **kwargs):
        raise NotImplementedError()

    def post_define_proc(self, *args, **kwargs):
        raise NotImplementedError()

    def pre_fetch_proc(self, var):
        raise NotImplementedError()

    def is_null_proc(self, *args, **kwargs):
        raise NotImplementedError()

    def set_value_proc(self, var, pos, value):
        raise NotImplementedError()

    def get_value_proc(self, var, pos):
        raise NotImplementedError()

    def get_typed_data(self, var):
        return ctypes.cast(var.data, oci.POINTER(self.oci_type))
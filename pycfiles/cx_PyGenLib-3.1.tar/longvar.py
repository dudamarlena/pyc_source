# uncompyle6 version 3.6.7
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/lameiro/projects/cx_oracle_on_ctypes/cx_Oracle/longvar.py
# Compiled at: 2015-05-19 16:59:20
import ctypes
from ctypes import byref
import oci
from variable_type import VariableType
from variable import Variable
from buffer import cxBuffer
from utils import cxString_from_encoded_string, bytes

class LONG_STRING(Variable):
    pass


class LONG_BINARY(Variable):
    pass


class LongVarBaseType(VariableType):

    def __init__(self):
        VariableType.__init__(self)
        self.initialize_proc = None
        self.finalize_proc = None
        self.pre_define_proc = None
        self.post_define_proc = None
        self.pre_fetch_proc = None
        self.is_null_proc = None
        self.set_value_proc = self.set_value
        self.get_value_proc = self.get_value
        self.get_buffer_size_proc = self.get_buffer_size
        self.charset_form = oci.SQLCS_IMPLICIT
        self.size = 131072
        self.is_variable_length = True
        self.can_be_copied = True
        self.can_be_in_array = False

    def set_value(self, var, pos, value):
        buffer = cxBuffer.new_from_object(value, var.environment.encoding)
        if buffer.num_characters > var.size:
            var.resize(buffer.num_characters)
        base_ptr_address = ctypes.addressof(var.data) + var.bufferSize * pos
        c_length = oci.ub4.from_address(base_ptr_address)
        c_length.value = buffer.size
        string_address = base_ptr_address + ctypes.sizeof(oci.ub4)
        string_ptr = ctypes.c_void_p(string_address)
        if buffer.size:
            ctypes.memmove(string_ptr, buffer.ptr, buffer.size)

    def get_value(self, var, pos):
        base_ptr_address = ctypes.addressof(var.data) + var.bufferSize * pos
        c_length = oci.ub4.from_address(base_ptr_address)
        length = c_length.value
        start_address = var.bufferSize * pos + ctypes.sizeof(oci.ub4)
        the_contents = var.data[start_address:start_address + length]
        if var.type == vt_LongBinary:
            return bytes(the_contents)
        return cxString_from_encoded_string(the_contents, var.environment.encoding)

    def get_buffer_size(self, var):
        """Returns the size of the buffer to use for data of the given size."""
        if not var.type.is_character_data:
            return var.size + ctypes.sizeof(oci.ub4)
        return ctypes.sizeof(oci.ub4) + var.size * var.environment.maxBytesPerCharacter


class LongStringVariableType(LongVarBaseType):

    def __init__(self):
        LongVarBaseType.__init__(self)
        self.python_type = LONG_STRING
        self.oracle_type = oci.SQLT_LVC
        self.is_character_data = True


class LongBinaryVariableType(LongVarBaseType):

    def __init__(self):
        LongVarBaseType.__init__(self)
        self.python_type = LONG_BINARY
        self.oracle_type = oci.SQLT_LVB
        self.is_character_data = False


vt_LongString = LongStringVariableType()
vt_LongBinary = LongBinaryVariableType()
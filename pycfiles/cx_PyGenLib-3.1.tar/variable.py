# uncompyle6 version 3.6.7
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/lameiro/projects/cx_oracle_on_ctypes/cx_Oracle/variable.py
# Compiled at: 2015-05-19 16:59:20
from ctypes import byref
import ctypes, sys
from utils import python3_or_better
from custom_exceptions import NotSupportedError, DatabaseError
from error import Error
from buffer import cxBuffer
import oci

class Variable(object):

    def __init__(self, cursor, num_elements, type, size):
        self.environment = cursor.connection.environment
        self.bind_handle = oci.POINTER(oci.OCIBind)()
        self.define_handle = oci.POINTER(oci.OCIDefine)()
        self.bound_cursor_handle = oci.POINTER(oci.OCIStmt)()
        self.bound_name = None
        self.inconverter = None
        self.outconverter = None
        self.bound_pos = 0
        if num_elements < 1:
            self.numElements = self.allocelems = 1
        else:
            self.numElements = self.allocelems = num_elements
        self.c_actual_elements = oci.ub4(0)
        self.internal_fetch_num = 0
        self.is_array = False
        self.is_allocated_internally = True
        self.type = type
        self.actual_length = oci.POINTER(oci.ub2)()
        self.return_code = oci.POINTER(oci.ub2)()
        self.size = type.size
        if type.is_variable_length:
            if size < ctypes.sizeof(oci.ub2):
                size = ctypes.sizeof(oci.ub2)
            self.size = size
        self.allocate_data()
        self.indicator = (self.numElements * oci.sb2)()
        for i in xrange(self.numElements):
            self.indicator[i] = oci.OCI_IND_NULL

        if type.is_variable_length:
            self.return_code = (self.numElements * oci.ub2)()
        if self.type.initialize_proc:
            self.type.initialize_proc(self, cursor)

    def get_actual_elements(self):
        return self.c_actual_elements.value

    def set_actual_elements(self, value):
        self.c_actual_elements.value = value

    actual_elements = property(get_actual_elements, set_actual_elements)

    def get_maxlength(self):
        return self.bufferSize

    def set_maxlength(self, value):
        self.bufferSize = value

    maxlength = property(get_maxlength, set_maxlength)

    def allocate_data(self):
        """Allocate the data for the variable."""
        if self.type.get_buffer_size_proc:
            self.bufferSize = self.type.get_buffer_size_proc(self)
        else:
            self.bufferSize = self.size
        data_length = self.numElements * self.bufferSize
        if data_length > sys.maxint:
            raise ValueError('array size too large')
        self.data = ctypes.create_string_buffer(data_length)

    def get_single_value(self, array_pos):
        """Return the value of the variable at the given position."""
        if array_pos >= self.numElements:
            raise (
             IndexError, 'Variable_GetSingleValue: array size exceeded')
        if self.type.is_null_proc:
            is_null = self.type.is_null_proc(self, array_pos)
        else:
            is_null = self.indicator[array_pos] == oci.OCI_IND_NULL
        if is_null:
            return
        self.verify_fetch(array_pos)
        value = self.type.get_value_proc(self, array_pos)
        if self.outconverter is not None:
            result = self.outconverter(value)
            return result
        return value

    def _get_value(self, array_pos):
        """Return the value of the variable."""
        if self.is_array:
            return self.get_array_value(self.actual_elements)
        return self.get_single_value(array_pos)

    def getvalue(self, pos=0):
        """Return the value of the variable at the given position."""
        return self._get_value(pos)

    def verify_fetch(self, array_pos):
        """Verifies that truncation or other problems did not take place on retrieve."""
        if self.type.is_variable_length:
            if self.return_code[array_pos] != 0:
                error = Error(self.environment, 'Variable_VerifyFetch()', 0)
                error.code = self.return_code[array_pos]
                error.message = 'column at array pos %d fetched with error: %d' % (array_pos, self.return_code[array_pos])
                raise DatabaseError(error)

    def get_array_value(self, num_elements):
        """Return the value of the variable as an array."""
        return [ self.get_single_value(i) ]

    def bind(self, cursor, name, pos):
        """Allocate a variable and bind it to the given statement."""
        if self.bind_handle and name == self.bound_name and pos == self.bound_pos:
            return
        self.bound_pos = pos
        self.bound_cursor_handle = cursor.handle
        self.bound_name = name
        self.internal_bind()

    def internal_bind(self):
        """Allocate a variable and bind it to the given statement."""
        if self.is_array:
            alloc_elems = self.allocelems
            actual_elements_ref = byref(self.c_actual_elements)
        else:
            alloc_elems = 0
            actual_elements_ref = oci.POINTER(oci.ub4)()
        if self.bound_name:
            buffer = cxBuffer.new_from_object(self.bound_name, self.environment.encoding)
            status = oci.OCIBindByName(self.bound_cursor_handle, byref(self.bind_handle), self.environment.error_handle, buffer.cast_ptr, buffer.size, self.data, self.bufferSize, self.type.oracle_type, self.indicator, self.actual_length, self.return_code, alloc_elems, actual_elements_ref, oci.OCI_DEFAULT)
        else:
            status = oci.OCIBindByPos(self.bound_cursor_handle, byref(self.bind_handle), self.environment.error_handle, self.bound_pos, self.data, self.bufferSize, self.type.oracle_type, self.indicator, self.actual_length, self.return_code, alloc_elems, actual_elements_ref, oci.OCI_DEFAULT)
        self.environment.check_for_error(status, 'Variable_InternalBind()')
        if not python3_or_better():
            if self.type.charset_form != oci.SQLCS_IMPLICIT:
                c_charset_form = oci.ub1(self.type.charset_form)
                status = oci.OCIAttrSet(self.bind_handle, oci.OCI_HTYPE_BIND, byref(c_charset_form), 0, oci.OCI_ATTR_CHARSET_FORM, self.environment.error_handle)
                self.environment.check_for_error(status, 'Variable_InternalBind(): set charset form')
                self.type.charset_form = c_charset_form.value
                c_buffer_size = oci.ub4(self.bufferSize)
                status = oci.OCIAttrSet(self.bind_handle, oci.OCI_HTYPE_BIND, byref(c_buffer_size), 0, oci.OCI_ATTR_MAXDATA_SIZE, self.environment.error_handle)
                self.environment.check_for_error(status, 'Variable_InternalBind(): set max data size')
                self.bufferSize = self.maxlength = c_buffer_size.value
        self.set_max_data_size()

    def set_max_data_size(self):
        pass

    def make_array(self):
        """Make the variable an array, ensuring that the type supports arrays."""
        if not self.type.can_be_in_array:
            raise NotSupportedError('Variable_MakeArray(): type does not support arrays')
        self.is_array = True

    def set_value(self, array_pos, value):
        """Set the value of the variable."""
        if self.is_array:
            if array_pos > 0:
                raise NotSupportedError('arrays of arrays are not supported by the OCI')
            return self.set_array_value(value)
        return self.set_single_value(array_pos, value)

    setvalue = set_value

    def set_single_value(self, array_pos, value):
        """Set a single value in the variable."""
        if array_pos >= self.numElements:
            raise IndexError('Variable_SetSingleValue: array size exceeded')
        if self.inconverter is not None:
            value = self.inconverter(value)
        if value is None:
            self.indicator[array_pos] = oci.OCI_IND_NULL
            return
        self.indicator[array_pos] = oci.OCI_IND_NOTNULL
        if self.type.is_variable_length:
            self.return_code[array_pos] = 0
        self.type.set_value_proc(self, array_pos, value)

    def set_array_value(self, value):
        """Set all of the array values for the variable."""
        if not isinstance(value, list):
            raise TypeError('expecting array data')
        num_elements = len(value)
        if num_elements > self.numElements:
            raise IndexError('Variable_SetArrayValue: array size exceeded')
        self.actual_elements = num_elements
        for i, element_value in enumerate(value):
            self.set_single_value(i, element_value)

    def resize(self, size):
        """Resize the variable."""
        orig_data = self.data
        orig_buffer_size = self.bufferSize
        self.size = size
        self.allocate_data()
        for i in xrange(self.allocelems):
            to = ctypes.c_void_p(ctypes.addressof(self.data) + self.bufferSize * i)
            frm = ctypes.c_void_p(ctypes.addressof(orig_data) + orig_buffer_size * i)
            ctypes.memmove(to, frm, orig_buffer_size)

        if self.bound_name or self.bound_pos > 0:
            self.internal_bind()

    @staticmethod
    def lookup_precision_and_scale(environment, param):
        return (0, 0)

    @staticmethod
    def get_display_size(precision, scale, char_size, internal_size):
        return -1

    def __del__(self):
        if self.is_allocated_internally:
            if self.type.finalize_proc:
                self.type.finalize_proc(self)
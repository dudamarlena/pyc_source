# uncompyle6 version 3.6.7
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/lameiro/projects/cx_oracle_on_ctypes/cx_Oracle/cursorvar.py
# Compiled at: 2015-05-19 16:59:20
import oci, ctypes
from ctypes import byref
from variable import Variable
from variable_type import VariableType

class CURSOR(Variable):
    pass


class CursorVariableType(VariableType):

    def __init__(self):
        VariableType.__init__(self)
        self.oci_type = oci.POINTER(oci.OCIStmt)
        self.pre_define_proc = None
        self.post_define_proc = None
        self.pre_fetch_proc = None
        self.is_null_proc = None
        self.get_buffer_size_proc = None
        self.python_type = CURSOR
        self.oracle_type = oci.SQLT_RSET
        self.charset_form = oci.SQLCS_IMPLICIT
        self.size = ctypes.sizeof(self.oci_type)
        self.is_character_data = False
        self.is_variable_length = False
        self.can_be_copied = False
        self.can_be_in_array = False

    def initialize_proc(self, var, cursor):
        var.connection = cursor.connection
        var.cursors = [None] * var.allocelems
        typed_data = self.get_typed_data(var)
        for i in xrange(var.allocelems):
            a_cursor = var.connection.cursor()
            a_cursor.allocate_handle()
            var.cursors[i] = a_cursor
            typed_data[i] = a_cursor.handle

    def finalize_proc(self, var):
        var.connection = None
        var.cursors = None

    def set_value_proc(self, var, pos, value):
        from cursor import Cursor
        if not isinstance(value, Cursor):
            raise TypeError('expecting cursor')
        cursor = value
        var.cursors[pos] = cursor
        if not cursor.is_owned:
            cursor.free_handle(True)
            cursor.is_owned = True
            cursor.allocate_handle()
        typed_data = self.get_typed_data(var)
        typed_data[pos] = cursor.handle
        cursor.statement_type = -1

    def get_value_proc(self, var, pos):
        typed_data = self.get_typed_data(var)
        cursor = var.cursors[pos]
        cursor.statement_type = -1
        return cursor


vt_Cursor = CursorVariableType()
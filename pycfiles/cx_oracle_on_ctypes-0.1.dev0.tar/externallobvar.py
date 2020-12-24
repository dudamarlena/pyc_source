# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lameiro/projects/cx_oracle_on_ctypes/cx_Oracle/externallobvar.py
# Compiled at: 2015-05-19 16:59:20
import ctypes
from ctypes import byref
import oci
from utils import bytes, cxString_from_encoded_string
from custom_exceptions import ProgrammingError, DatabaseError

class LOB(object):

    def size(self):
        self._verify()
        return self._internal_size()

    def open(self):
        self._verify()
        self._internal_open(oci.OCI_LOB_READWRITE, 'ExternalLobVar_Open()')

    def close(self):
        self._verify()
        self._internal_close('ExternalLobVar_FileClose()')

    def read(self, offset=-1, amount=-1):
        self._verify()
        return self._value(offset, amount)

    def write(self, data, offset=-1):
        raise NotImplementedError()

    def trim(self, newSize=0):
        self._verify()
        typed_data = self._get_lobvar_typed_data()
        status = oci.OCILobTrim(self.lob_var.connection.handle, self.lob_var.environment.error_handle, typed_data[self.pos], newSize)
        self.lob_var.environment.check_for_error(status, 'ExternalLobVar_Trim()')

    def getchunksize(self):
        raise NotImplementedError()

    def isopen(self):
        raise NotImplementedError()

    def getfilename(self):
        raise NotImplementedError()

    def setfilename(self):
        raise NotImplementedError()

    def fileexists(self):
        raise NotImplementedError()

    def __reduce__(self):
        raise NotImplementedError()

    def __init__(self, var, pos):
        """Create a new external LOB variable."""
        self.pos = pos
        self.internal_fetch_num = var.internal_fetch_num
        self.lob_var = var

    def _value(self, offset, amount):
        from lobvar import vt_CLOB, vt_NCLOB
        lob_type = self.lob_var.type
        if offset < 0:
            offset = 1
        if amount < 0:
            amount = self._internal_size()
            amount = amount - offset + 1
            if amount <= 0:
                amount = 1
        buffer = self._internal_read(offset, amount)
        if lob_type == vt_CLOB:
            result = cxString_from_encoded_string(buffer, self.lob_var.environment.encoding)
        elif lob_type == vt_NCLOB:
            result = buffer.decode(self.lob_var.environment.encoding)
        else:
            result = bytes(buffer)
        return result

    def _verify(self):
        if self.internal_fetch_num != self.lob_var.internal_fetch_num:
            raise ProgrammingError('LOB variable no longer valid after subsequent fetch')

    def _internal_size(self):
        c_length = oci.ub4()
        typed_data = self._get_lobvar_typed_data()
        status = oci.OCILobGetLength(self.lob_var.connection.handle, self.lob_var.environment.error_handle, typed_data[self.pos], byref(c_length))
        self.lob_var.environment.check_for_error(status, 'ExternalLobVar_InternalSize()')
        return c_length.value

    def _get_lobvar_typed_data(self):
        return self.lob_var.type.get_typed_data(self.lob_var)

    def _internal_read(self, offset, amount):
        from lobvar import vt_CLOB, vt_NCLOB
        lob_type = self.lob_var.type
        if self.lob_var.is_file:
            self._internal_open(oci.OCI_FILE_READONLY, 'ExternalLobVar_FileOpen()')
        if lob_type == vt_CLOB:
            buffer_size = amount * self.lob_var.environment.maxBytesPerCharacter
        else:
            if lob_type == vt_NCLOB:
                buffer_size = amount * 2
            else:
                buffer_size = amount
            buffer = ctypes.create_string_buffer(buffer_size)
            typed_data = self._get_lobvar_typed_data()
            c_length = oci.ub4(amount)
            arg8 = oci.OCILobRead.argtypes[8]()
            status = oci.OCILobRead(self.lob_var.connection.handle, self.lob_var.environment.error_handle, typed_data[self.pos], byref(c_length), offset, buffer, buffer_size, None, arg8, 0, self.lob_var.type.charset_form)
            length = c_length.value
            try:
                self.lob_var.environment.check_for_error(status, 'ExternalLobVar_LobRead()')
            except DatabaseError:
                try:
                    self._internal_close('ExternalLobVar_FileClose()')
                except DatabaseError:
                    pass

                raise

        if self.lob_var.is_file:
            self._internal_close('ExternalLobVar_FileClose()')
        return buffer.value

    def _internal_open(self, mode, message):
        typed_data = self._get_lobvar_typed_data()
        status = OCILobFileOpen(var.lob_var.connection.handle, self.lob_var.environment.error_handle, typed_data[var.pos], mode)
        self.lob_var.environment.check_for_error(status, message)

    def _internal_close(self, message):
        typed_data = self._get_lobvar_typed_data()
        status = oci.OCILobFileClose(self.lob_var.connection.handle, self.lob_var.environment.error_handle, typed_data[self.pos])
        self.lob_var.environment.check_for_error(status, message)

    def __str__(self):
        self._verify()
        return self._value(1, -1)
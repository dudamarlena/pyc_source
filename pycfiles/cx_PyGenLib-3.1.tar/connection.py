# uncompyle6 version 3.6.7
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/lameiro/projects/cx_oracle_on_ctypes/cx_Oracle/connection.py
# Compiled at: 2015-06-14 08:26:24
import ctypes
from ctypes import byref
import oci
from buffer import cxBuffer
from environment import Environment
from cursor import Cursor
from custom_exceptions import Error, InterfaceError
from variable import Variable
from stringvar import STRING, vt_String
from utils import DRIVER_NAME
from pythonic_oci import OCIHandleAlloc

class Connection(object):

    def __init__(self, user=None, password=None, dsn=None, mode=None, handle=None, pool=None, threaded=True, twophase=True, events=True, cclass=None, purity=None, newpassword=None, encoding=None, nencoding=None):
        self.server_handle = None
        self.handle = None
        self.session_handle = None
        self.autocommit = None
        self.inputtypehandler = None
        self.outputtypehandler = None
        self.version_cache = None
        self.release = False
        self.attached = False
        self.commit_mode = oci.OCI_DEFAULT
        if oci.ORACLE_11:
            if purity is None:
                purity = oci.OCI_ATTR_PURITY_DEFAULT
        else:
            purity = 0
        if mode is None:
            mode = oci.OCI_DEFAULT
        if pool:
            self.environment = pool.environment.clone()
        else:
            self.environment = Environment.new_from_scratch(threaded, events, encoding, nencoding)
        if user and '/' in user:
            user, password = user.split('/', 1)
        if password and '@' in password:
            password, dsn = password.split('@', 1)
        self.username = user
        self.password = password
        self.tnsentry = self.dsn = dsn
        if handle:
            self.attach(handle)
        if pool or cclass:
            self.get_connection(pool, cclass, purity)
        self.connect(mode, twophase, newpassword)

    def connect(self, mode, twophase, newpassword):
        """Create a new connection object by connecting to the database."""
        credential_type = oci.OCI_CRED_EXT
        self.server_handle = oci.POINTER(oci.OCIServer)()
        OCIHandleAlloc(self.environment, self.server_handle, oci.OCI_HTYPE_SERVER, 'Connection_Connect(): allocate server handle')
        buffer = cxBuffer.new_from_object(self.dsn, self.environment.encoding)
        status = oci.OCIServerAttach(self.server_handle, self.environment.error_handle, buffer.cast_ptr, buffer.size, oci.OCI_DEFAULT)
        self.environment.check_for_error(status, 'Connection_Connect(): server attach')
        self.handle = oci.POINTER(oci.OCISvcCtx)()
        OCIHandleAlloc(self.environment, self.handle, oci.OCI_HTYPE_SVCCTX, 'Connection_Connect(): allocate service context handle')
        status = oci.OCIAttrSet(self.handle, oci.OCI_HTYPE_SVCCTX, self.server_handle, 0, oci.OCI_ATTR_SERVER, self.environment.error_handle)
        self.environment.check_for_error(status, 'Connection_Connect(): set server handle')
        if twophase:
            status = oci.OCIAttrSet(self.server_handle, oci.OCI_HTYPE_SERVER, 'cx_Oracle', 0, oci.OCI_ATTR_INTERNAL_NAME, self.environment.error_handle)
            self.environment.check_for_error(status, 'Connection_Connect(): set internal name')
            status = oci.OCIAttrSet(self.server_handle, oci.OCI_HTYPE_SERVER, 'cx_Oracle', 0, oci.OCI_ATTR_EXTERNAL_NAME, self.environment.error_handle)
            self.environment.check_for_error(status, 'Connection_Connect(): set external name')
        self.session_handle = oci.POINTER(oci.OCISession)()
        OCIHandleAlloc(self.environment, self.session_handle, oci.OCI_HTYPE_SESSION, 'Connection_Connect(): allocate session handle')
        buffer = cxBuffer.new_from_object(self.username, self.environment.encoding)
        if buffer.size > 0:
            credential_type = oci.OCI_CRED_RDBMS
            status = oci.OCIAttrSet(self.session_handle, oci.OCI_HTYPE_SESSION, buffer.ptr, buffer.size, oci.OCI_ATTR_USERNAME, self.environment.error_handle)
            self.environment.check_for_error(status, 'Connection_Connect(): set user name')
        buffer = cxBuffer.new_from_object(self.password, self.environment.encoding)
        if buffer.size > 0:
            credential_type = oci.OCI_CRED_RDBMS
            status = oci.OCIAttrSet(self.session_handle, oci.OCI_HTYPE_SESSION, buffer.ptr, buffer.size, oci.OCI_ATTR_PASSWORD, self.environment.error_handle)
            self.environment.check_for_error(status, 'Connection_Connect(): set password')
        if hasattr(oci, 'OCI_ATTR_DRIVER_NAME'):
            buffer = cxBuffer.new_from_object(DRIVER_NAME, self.environment.encoding)
            status = oci.OCIAttrSet(self.session_handle, oci.OCI_HTYPE_SESSION, buffer.ptr, buffer.size, oci.OCI_ATTR_DRIVER_NAME, self.environment.error_handle)
            self.environment.check_for_error(status, 'Connection_Connect(): set driver name')
        status = oci.OCIAttrSet(self.handle, oci.OCI_HTYPE_SVCCTX, self.session_handle, 0, oci.OCI_ATTR_SESSION, self.environment.error_handle)
        self.environment.check_for_error(status, 'Connection_Connect(): set session handle')
        if newpassword:
            return self.change_password(self.password)
        status = oci.OCISessionBegin(self.handle, self.environment.error_handle, self.session_handle, credential_type, mode)
        try:
            self.environment.check_for_error(status, 'Connection_Connect(): begin session')
        except Error:
            self.session_handle = oci.POINTER(oci.OCISession)()
            raise

    def raise_if_not_connected(self):
        if not self.handle:
            raise InterfaceError('not connected')

    def close(self):
        """Close the connection, disconnecting from the database."""
        self.rollback()
        if self.session_handle:
            status = oci.OCISessionEnd(self.handle, self.environment.error_handle, self.session_handle, oci.OCI_DEFAULT)
            self.environment.check_for_error(status, 'Connection_Close(): end session')
        oci.OCIHandleFree(self.handle, oci.OCI_HTYPE_SVCCTX)
        self.handle = oci.POINTER(oci.OCISvcCtx)()

    def rollback(self):
        self.raise_if_not_connected()
        status = oci.OCITransRollback(self.handle, self.environment.error_handle, oci.OCI_DEFAULT)
        self.environment.check_for_error(status, 'Connection_Rollback()')

    def cursor(self):
        return Cursor(self)

    @property
    def version(self):
        """Retrieve the version of the database and return it. Note that this
            function also places the result in the associated dictionary so it is only
            calculated once."""
        if self.version_cache:
            return self.version_cache
        cursor = self.cursor()
        version_var = Variable(cursor, cursor.arraysize, vt_String, vt_String.size)
        compat_var = Variable(cursor, cursor.arraysize, vt_String, vt_String.size)
        list_of_arguments = [
         version_var, compat_var]
        cursor.callproc('dbms_utility.db_version', list_of_arguments)
        self.version_cache = version_var.getvalue(0)
        return self.version_cache

    def __del__(self):
        """Deallocate the connection, disconnecting from the database if necessary."""
        if self.release:
            oci.OCITransRollback(self.handle, self.environment.error_handle, oci.OCI_DEFAULT)
            oci.OCISessionRelease(self.handle, self.environment.error_handle, None, 0, oci.OCI_DEFAULT)
        elif not self.attached:
            if self.session_handle:
                oci.OCITransRollback(self.handle, self.environment.error_handle, oci.OCI_DEFAULT)
                oci.OCISessionEnd(self.handle, self.environment.error_handle, self.session_handle, oci.OCI_DEFAULT)
            if self.server_handle:
                oci.OCIServerDetach(self.server_handle, self.environment.error_handle, oci.OCI_DEFAULT)
        self.environment = None

    def commit(self):
        """Commit the transaction on the connection."""
        self.raise_if_not_connected()
        status = oci.OCITransCommit(self.handle, self.environment.error_handle, self.commit_mode)
        self.environment.check_for_error(status, 'Connection_Commit()')
        self.commit_mode = oci.OCI_DEFAULT

    @property
    def maxBytesPerCharacter(self):
        """Return the maximum number of bytes per character."""
        return self.environment.maxBytesPerCharacter

    def attach(self, handle):
        raise NotImplementedError()

    def get_connection(self, pool, cclass, purity):
        raise NotImplementedError()

    def change_password(self, password):
        raise NotImplementedError()
# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lameiro/projects/cx_oracle_on_ctypes/cx_Oracle/__init__.py
# Compiled at: 2015-08-14 18:33:00
from decimal import Decimal
from datetime import datetime, date
import sys, ctypes
from ctypes import c_int, byref
from custom_exceptions import Warning, Error, InterfaceError, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError
from utils import python3_or_better
from utils import cxBinary as Binary
from connection import Connection
from cursor import Cursor
from datetime import datetime as Timestamp
from datetime import date as Date
from error import Error as _Error
connect = Connection
from numbervar import NUMBER
from stringvar import STRING, BINARY, FIXED_CHAR, FIXED_UNICODE, ROWID, UNICODE
from longvar import LONG_BINARY, LONG_STRING
from datetimevar import DATETIME
from lobvar import NCLOB, CLOB, BLOB, BFILE
from externallobvar import LOB
from timestampvar import TIMESTAMP
from intervalvar import INTERVAL
from cursorvar import CURSOR

def symbol_exists(symbol_name):
    pass


def makedsn(host, port, sid='', service_name=''):
    if sid == '' and service_name == '':
        raise TypeError('makedsn requires either sid or servicename, but both were passed empty')
    if sid:
        connect_data_obj = sid
        dsn_format = '(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=%s)(PORT=%s)))(CONNECT_DATA=(SID=%s)))'
    else:
        connect_data_obj = service_name
        dsn_format = '(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=%s)(PORT=%s)))(CONNECT_DATA=(SERVICE_NAME=%s)))'
    return dsn_format % (host, port, connect_data_obj)


ORACLE_VERSION_10G, ORACLE_VERSION_10GR2, ORACLE_VERSION_11G = range(3)
ORACLE_VERSION = ORACLE_VERSION_11G
if symbol_exists('OCI_ATTR_MODULE'):
    ORACLE_VERSION = ORACLE_VERSION_10G
if symbol_exists('OCI_MAJOR_VERSION'):
    ORACLE_VERSION = ORACLE_VERSION_10GR2
if symbol_exists('OCI_ATTR_CONNECTION_CLASS'):
    ORACLE_VERSION = ORACLE_VERSION_11G
if ORACLE_VERSION >= ORACLE_VERSION_10GR2:

    def clientversion--- This code section failed: ---

 L.  66         0  LOAD_GLOBAL           0  'c_int'
                3  CALL_FUNCTION_0       0  None
                6  LOAD_GLOBAL           0  'c_int'
                9  CALL_FUNCTION_0       0  None
               12  LOAD_GLOBAL           0  'c_int'
               15  CALL_FUNCTION_0       0  None
               18  LOAD_GLOBAL           0  'c_int'
               21  CALL_FUNCTION_0       0  None
               24  LOAD_GLOBAL           0  'c_int'
               27  CALL_FUNCTION_0       0  None
               30  STORE_FAST            0  'port_update_num'
               33  STORE_FAST            1  'patch_num'
               36  STORE_FAST            2  'update_num'
               39  STORE_FAST            3  'minor_version'
               42  STORE_FAST            4  'major_version'

 L.  67        45  LOAD_GLOBAL           1  'the_so'
               48  LOOKUP_METHOD         2  'OCIClientVersion'
               51  LOAD_GLOBAL           3  'byref'
               54  LOAD_FAST             4  'major_version'
               57  CALL_FUNCTION_1       1  None
               60  LOAD_GLOBAL           3  'byref'
               63  LOAD_FAST             3  'minor_version'
               66  CALL_FUNCTION_1       1  None
               69  LOAD_GLOBAL           3  'byref'
               72  LOAD_FAST             2  'update_num'
               75  CALL_FUNCTION_1       1  None
               78  LOAD_GLOBAL           3  'byref'
               81  LOAD_FAST             1  'patch_num'
               84  CALL_FUNCTION_1       1  None
               87  LOAD_GLOBAL           3  'byref'
               90  LOAD_FAST             0  'port_update_num'
               93  CALL_FUNCTION_1       1  None
               96  CALL_METHOD_5         5  None
               99  POP_TOP          

 L.  69       100  LOAD_FAST             4  'major_version'
              103  LOAD_ATTR             4  'value'
              106  LOAD_FAST             3  'minor_version'
              109  LOAD_ATTR             4  'value'
              112  LOAD_FAST             2  'update_num'
              115  LOAD_ATTR             4  'value'
              118  LOAD_FAST             1  'patch_num'
              121  LOAD_ATTR             4  'value'
              124  LOAD_FAST             0  'port_update_num'
              127  LOAD_ATTR             4  'value'
              130  BUILD_TUPLE_5         5 
              133  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def Time(*args):
    raise NotSupportedError('Oracle does not support time only variables')


TimeFromTicks = Time

def DateFromTicks(args):
    return date.fromtimestamp(args)


def TimestampFromTicks(args):
    return datetime.fromtimestamp(args)


apilevel = '2.0'
threadsafety = 2
paramstyle = 'named'
buildtime = ''
version = '0.1'
from oci import OCI_SYSDBA as SYSDBA, OCI_SYSOPER as SYSOPER, OCI_FNCODE_BINDBYNAME as FNCODE_BINDBYNAME, OCI_FNCODE_BINDBYPOS as FNCODE_BINDBYPOS, OCI_FNCODE_DEFINEBYPOS as FNCODE_DEFINEBYPOS, OCI_FNCODE_STMTEXECUTE as FNCODE_STMTEXECUTE, OCI_FNCODE_STMTFETCH as FNCODE_STMTFETCH, OCI_FNCODE_STMTPREPARE as FNCODE_STMTPREPARE, OCI_UCBTYPE_ENTRY as UCBTYPE_ENTRY, OCI_UCBTYPE_EXIT as UCBTYPE_EXIT, OCI_UCBTYPE_REPLACE as UCBTYPE_REPLACE, OCI_SPOOL_ATTRVAL_WAIT as SPOOL_ATTRVAL_WAIT, OCI_SPOOL_ATTRVAL_NOWAIT as SPOOL_ATTRVAL_NOWAIT, OCI_SPOOL_ATTRVAL_FORCEGET as SPOOL_ATTRVAL_FORCEGET
if ORACLE_VERSION >= ORACLE_VERSION_10GR2:
    from oci import OCI_PRELIM_AUTH as PRELIM_AUTH, OCI_DBSHUTDOWN_ABORT as DBSHUTDOWN_ABORT, OCI_DBSHUTDOWN_FINAL as DBSHUTDOWN_FINAL, OCI_DBSHUTDOWN_IMMEDIATE as DBSHUTDOWN_IMMEDIATE, OCI_DBSHUTDOWN_TRANSACTIONAL as DBSHUTDOWN_TRANSACTIONAL, OCI_DBSHUTDOWN_TRANSACTIONAL_LOCAL as DBSHUTDOWN_TRANSACTIONAL_LOCAL, OCI_EVENT_NONE as EVENT_NONE, OCI_EVENT_STARTUP as EVENT_STARTUP, OCI_EVENT_SHUTDOWN as EVENT_SHUTDOWN, OCI_EVENT_SHUTDOWN_ANY as EVENT_SHUTDOWN_ANY, OCI_EVENT_DEREG as EVENT_DEREG, OCI_EVENT_OBJCHANGE as EVENT_OBJCHANGE, OCI_OPCODE_ALLOPS as OPCODE_ALLOPS, OCI_OPCODE_ALLROWS as OPCODE_ALLROWS, OCI_OPCODE_INSERT as OPCODE_INSERT, OCI_OPCODE_UPDATE as OPCODE_UPDATE, OCI_OPCODE_DELETE as OPCODE_DELETE, OCI_OPCODE_ALTER as OPCODE_ALTER, OCI_OPCODE_DROP as OPCODE_DROP, OCI_SUBSCR_NAMESPACE_DBCHANGE as SUBSCR_NAMESPACE_DBCHANGE, OCI_SUBSCR_PROTO_OCI as SUBSCR_PROTO_OCI, OCI_SUBSCR_PROTO_MAIL as SUBSCR_PROTO_MAIL, OCI_SUBSCR_PROTO_SERVER as SUBSCR_PROTO_SERVER, OCI_SUBSCR_PROTO_HTTP as SUBSCR_PROTO_HTTP
if ORACLE_VERSION >= ORACLE_VERSION_11G:
    from oci import OCI_ATTR_PURITY_DEFAULT as ATTR_PURITY_DEFAULT, OCI_ATTR_PURITY_NEW as ATTR_PURITY_NEW, OCI_ATTR_PURITY_SELF as ATTR_PURITY_SELF
__all__ = [
 'makedsn', 'Time', 'DateFromTicks', 'TimeFromTicks', 'TimestampFromTicks', 'Binary']
if ORACLE_VERSION >= ORACLE_VERSION_10GR2:
    __all__ += ['clientversion']
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/drizzle/libdrizzle.py
# Compiled at: 2010-03-22 03:04:06
from sys import version_info
if version_info >= (3, 0, 0):
    new_instancemethod = lambda func, inst, cls: _libdrizzle.SWIG_PyInstanceMethod_New(func)
else:
    from new import instancemethod as new_instancemethod
if version_info >= (2, 6, 0):

    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            (fp, pathname, description) = imp.find_module('_libdrizzle', [dirname(__file__)])
        except ImportError:
            import _libdrizzle
            return _libdrizzle

        if fp is not None:
            try:
                _mod = imp.load_module('_libdrizzle', fp, pathname, description)
            finally:
                fp.close()

            return _mod
        else:
            return


    _libdrizzle = swig_import_helper()
    del swig_import_helper
else:
    import _libdrizzle
del version_info
try:
    _swig_property = property
except NameError:
    pass

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if name == 'thisown':
        return self.this.own(value)
    else:
        if name == 'this':
            if type(value).__name__ == 'SwigPyObject':
                self.__dict__[name] = value
                return
        method = class_type.__swig_setmethods__.get(name, None)
        if method:
            return method(self, value)
        if not static or hasattr(self, name):
            self.__dict__[name] = value
        else:
            raise AttributeError('You cannot add attributes to %s' % self)
        return


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if name == 'thisown':
        return self.this.own()
    else:
        method = class_type.__swig_getmethods__.get(name, None)
        if method:
            return method(self)
        raise AttributeError(name)
        return


def _swig_repr(self):
    try:
        strthis = 'proxy of ' + self.this.__repr__()
    except:
        strthis = ''

    return '<%s.%s; %s >' % (self.__class__.__module__, self.__class__.__name__, strthis)


try:
    _object = object
    _newclass = 1
except AttributeError:

    class _object:
        pass


    _newclass = 0

def _swig_setattr_nondynamic_method(set):

    def set_attr(self, name, value):
        if name == 'thisown':
            return self.this.own(value)
        if hasattr(self, name) or name == 'this':
            set(self, name, value)
        else:
            raise AttributeError('You cannot add attributes to %s' % self)

    return set_attr


DRIZZLE_COLUMN_TYPE_VIRTUAL = _libdrizzle.DRIZZLE_COLUMN_TYPE_VIRTUAL
DRIZZLE_DEFAULT_TCP_HOST = _libdrizzle.DRIZZLE_DEFAULT_TCP_HOST
DRIZZLE_DEFAULT_TCP_PORT = _libdrizzle.DRIZZLE_DEFAULT_TCP_PORT
DRIZZLE_DEFAULT_TCP_PORT_MYSQL = _libdrizzle.DRIZZLE_DEFAULT_TCP_PORT_MYSQL
DRIZZLE_DEFAULT_UDS = _libdrizzle.DRIZZLE_DEFAULT_UDS
DRIZZLE_DEFAULT_UDS_MYSQL = _libdrizzle.DRIZZLE_DEFAULT_UDS_MYSQL
DRIZZLE_DEFAULT_BACKLOG = _libdrizzle.DRIZZLE_DEFAULT_BACKLOG
DRIZZLE_MAX_ERROR_SIZE = _libdrizzle.DRIZZLE_MAX_ERROR_SIZE
DRIZZLE_MAX_USER_SIZE = _libdrizzle.DRIZZLE_MAX_USER_SIZE
DRIZZLE_MAX_PASSWORD_SIZE = _libdrizzle.DRIZZLE_MAX_PASSWORD_SIZE
DRIZZLE_MAX_DB_SIZE = _libdrizzle.DRIZZLE_MAX_DB_SIZE
DRIZZLE_MAX_INFO_SIZE = _libdrizzle.DRIZZLE_MAX_INFO_SIZE
DRIZZLE_MAX_SQLSTATE_SIZE = _libdrizzle.DRIZZLE_MAX_SQLSTATE_SIZE
DRIZZLE_MAX_CATALOG_SIZE = _libdrizzle.DRIZZLE_MAX_CATALOG_SIZE
DRIZZLE_MAX_TABLE_SIZE = _libdrizzle.DRIZZLE_MAX_TABLE_SIZE
DRIZZLE_MAX_COLUMN_NAME_SIZE = _libdrizzle.DRIZZLE_MAX_COLUMN_NAME_SIZE
DRIZZLE_MAX_DEFAULT_VALUE_SIZE = _libdrizzle.DRIZZLE_MAX_DEFAULT_VALUE_SIZE
DRIZZLE_MAX_BUFFER_SIZE = _libdrizzle.DRIZZLE_MAX_BUFFER_SIZE
DRIZZLE_BUFFER_COPY_THRESHOLD = _libdrizzle.DRIZZLE_BUFFER_COPY_THRESHOLD
DRIZZLE_MAX_SERVER_VERSION_SIZE = _libdrizzle.DRIZZLE_MAX_SERVER_VERSION_SIZE
DRIZZLE_MAX_SCRAMBLE_SIZE = _libdrizzle.DRIZZLE_MAX_SCRAMBLE_SIZE
DRIZZLE_STATE_STACK_SIZE = _libdrizzle.DRIZZLE_STATE_STACK_SIZE
DRIZZLE_ROW_GROW_SIZE = _libdrizzle.DRIZZLE_ROW_GROW_SIZE
DRIZZLE_DEFAULT_SOCKET_TIMEOUT = _libdrizzle.DRIZZLE_DEFAULT_SOCKET_TIMEOUT
DRIZZLE_DEFAULT_SOCKET_SEND_SIZE = _libdrizzle.DRIZZLE_DEFAULT_SOCKET_SEND_SIZE
DRIZZLE_DEFAULT_SOCKET_RECV_SIZE = _libdrizzle.DRIZZLE_DEFAULT_SOCKET_RECV_SIZE
DRIZZLE_RETURN_OK = _libdrizzle.DRIZZLE_RETURN_OK
DRIZZLE_RETURN_IO_WAIT = _libdrizzle.DRIZZLE_RETURN_IO_WAIT
DRIZZLE_RETURN_PAUSE = _libdrizzle.DRIZZLE_RETURN_PAUSE
DRIZZLE_RETURN_ROW_BREAK = _libdrizzle.DRIZZLE_RETURN_ROW_BREAK
DRIZZLE_RETURN_MEMORY = _libdrizzle.DRIZZLE_RETURN_MEMORY
DRIZZLE_RETURN_ERRNO = _libdrizzle.DRIZZLE_RETURN_ERRNO
DRIZZLE_RETURN_INTERNAL_ERROR = _libdrizzle.DRIZZLE_RETURN_INTERNAL_ERROR
DRIZZLE_RETURN_GETADDRINFO = _libdrizzle.DRIZZLE_RETURN_GETADDRINFO
DRIZZLE_RETURN_NOT_READY = _libdrizzle.DRIZZLE_RETURN_NOT_READY
DRIZZLE_RETURN_BAD_PACKET_NUMBER = _libdrizzle.DRIZZLE_RETURN_BAD_PACKET_NUMBER
DRIZZLE_RETURN_BAD_HANDSHAKE_PACKET = _libdrizzle.DRIZZLE_RETURN_BAD_HANDSHAKE_PACKET
DRIZZLE_RETURN_BAD_PACKET = _libdrizzle.DRIZZLE_RETURN_BAD_PACKET
DRIZZLE_RETURN_PROTOCOL_NOT_SUPPORTED = _libdrizzle.DRIZZLE_RETURN_PROTOCOL_NOT_SUPPORTED
DRIZZLE_RETURN_UNEXPECTED_DATA = _libdrizzle.DRIZZLE_RETURN_UNEXPECTED_DATA
DRIZZLE_RETURN_NO_SCRAMBLE = _libdrizzle.DRIZZLE_RETURN_NO_SCRAMBLE
DRIZZLE_RETURN_AUTH_FAILED = _libdrizzle.DRIZZLE_RETURN_AUTH_FAILED
DRIZZLE_RETURN_NULL_SIZE = _libdrizzle.DRIZZLE_RETURN_NULL_SIZE
DRIZZLE_RETURN_ERROR_CODE = _libdrizzle.DRIZZLE_RETURN_ERROR_CODE
DRIZZLE_RETURN_TOO_MANY_COLUMNS = _libdrizzle.DRIZZLE_RETURN_TOO_MANY_COLUMNS
DRIZZLE_RETURN_ROW_END = _libdrizzle.DRIZZLE_RETURN_ROW_END
DRIZZLE_RETURN_LOST_CONNECTION = _libdrizzle.DRIZZLE_RETURN_LOST_CONNECTION
DRIZZLE_RETURN_COULD_NOT_CONNECT = _libdrizzle.DRIZZLE_RETURN_COULD_NOT_CONNECT
DRIZZLE_RETURN_NO_ACTIVE_CONNECTIONS = _libdrizzle.DRIZZLE_RETURN_NO_ACTIVE_CONNECTIONS
DRIZZLE_RETURN_HANDSHAKE_FAILED = _libdrizzle.DRIZZLE_RETURN_HANDSHAKE_FAILED
DRIZZLE_RETURN_TIMEOUT = _libdrizzle.DRIZZLE_RETURN_TIMEOUT
DRIZZLE_RETURN_MAX = _libdrizzle.DRIZZLE_RETURN_MAX
DRIZZLE_VERBOSE_NEVER = _libdrizzle.DRIZZLE_VERBOSE_NEVER
DRIZZLE_VERBOSE_FATAL = _libdrizzle.DRIZZLE_VERBOSE_FATAL
DRIZZLE_VERBOSE_ERROR = _libdrizzle.DRIZZLE_VERBOSE_ERROR
DRIZZLE_VERBOSE_INFO = _libdrizzle.DRIZZLE_VERBOSE_INFO
DRIZZLE_VERBOSE_DEBUG = _libdrizzle.DRIZZLE_VERBOSE_DEBUG
DRIZZLE_VERBOSE_CRAZY = _libdrizzle.DRIZZLE_VERBOSE_CRAZY
DRIZZLE_VERBOSE_MAX = _libdrizzle.DRIZZLE_VERBOSE_MAX
DRIZZLE_NONE = _libdrizzle.DRIZZLE_NONE
DRIZZLE_ALLOCATED = _libdrizzle.DRIZZLE_ALLOCATED
DRIZZLE_NON_BLOCKING = _libdrizzle.DRIZZLE_NON_BLOCKING
DRIZZLE_FREE_OBJECTS = _libdrizzle.DRIZZLE_FREE_OBJECTS
DRIZZLE_ASSERT_DANGLING = _libdrizzle.DRIZZLE_ASSERT_DANGLING
DRIZZLE_CON_NONE = _libdrizzle.DRIZZLE_CON_NONE
DRIZZLE_CON_ALLOCATED = _libdrizzle.DRIZZLE_CON_ALLOCATED
DRIZZLE_CON_MYSQL = _libdrizzle.DRIZZLE_CON_MYSQL
DRIZZLE_CON_RAW_PACKET = _libdrizzle.DRIZZLE_CON_RAW_PACKET
DRIZZLE_CON_RAW_SCRAMBLE = _libdrizzle.DRIZZLE_CON_RAW_SCRAMBLE
DRIZZLE_CON_READY = _libdrizzle.DRIZZLE_CON_READY
DRIZZLE_CON_NO_RESULT_READ = _libdrizzle.DRIZZLE_CON_NO_RESULT_READ
DRIZZLE_CON_IO_READY = _libdrizzle.DRIZZLE_CON_IO_READY
DRIZZLE_CON_LISTEN = _libdrizzle.DRIZZLE_CON_LISTEN
DRIZZLE_CON_EXPERIMENTAL = _libdrizzle.DRIZZLE_CON_EXPERIMENTAL
DRIZZLE_CON_SOCKET_TCP = _libdrizzle.DRIZZLE_CON_SOCKET_TCP
DRIZZLE_CON_SOCKET_UDS = _libdrizzle.DRIZZLE_CON_SOCKET_UDS
DRIZZLE_CON_STATUS_NONE = _libdrizzle.DRIZZLE_CON_STATUS_NONE
DRIZZLE_CON_STATUS_IN_TRANS = _libdrizzle.DRIZZLE_CON_STATUS_IN_TRANS
DRIZZLE_CON_STATUS_AUTOCOMMIT = _libdrizzle.DRIZZLE_CON_STATUS_AUTOCOMMIT
DRIZZLE_CON_STATUS_MORE_RESULTS_EXISTS = _libdrizzle.DRIZZLE_CON_STATUS_MORE_RESULTS_EXISTS
DRIZZLE_CON_STATUS_QUERY_NO_GOOD_INDEX_USED = _libdrizzle.DRIZZLE_CON_STATUS_QUERY_NO_GOOD_INDEX_USED
DRIZZLE_CON_STATUS_QUERY_NO_INDEX_USED = _libdrizzle.DRIZZLE_CON_STATUS_QUERY_NO_INDEX_USED
DRIZZLE_CON_STATUS_CURSOR_EXISTS = _libdrizzle.DRIZZLE_CON_STATUS_CURSOR_EXISTS
DRIZZLE_CON_STATUS_LAST_ROW_SENT = _libdrizzle.DRIZZLE_CON_STATUS_LAST_ROW_SENT
DRIZZLE_CON_STATUS_DB_DROPPED = _libdrizzle.DRIZZLE_CON_STATUS_DB_DROPPED
DRIZZLE_CON_STATUS_NO_BACKSLASH_ESCAPES = _libdrizzle.DRIZZLE_CON_STATUS_NO_BACKSLASH_ESCAPES
DRIZZLE_CON_STATUS_QUERY_WAS_SLOW = _libdrizzle.DRIZZLE_CON_STATUS_QUERY_WAS_SLOW
DRIZZLE_CAPABILITIES_NONE = _libdrizzle.DRIZZLE_CAPABILITIES_NONE
DRIZZLE_CAPABILITIES_LONG_PASSWORD = _libdrizzle.DRIZZLE_CAPABILITIES_LONG_PASSWORD
DRIZZLE_CAPABILITIES_FOUND_ROWS = _libdrizzle.DRIZZLE_CAPABILITIES_FOUND_ROWS
DRIZZLE_CAPABILITIES_LONG_FLAG = _libdrizzle.DRIZZLE_CAPABILITIES_LONG_FLAG
DRIZZLE_CAPABILITIES_CONNECT_WITH_DB = _libdrizzle.DRIZZLE_CAPABILITIES_CONNECT_WITH_DB
DRIZZLE_CAPABILITIES_NO_SCHEMA = _libdrizzle.DRIZZLE_CAPABILITIES_NO_SCHEMA
DRIZZLE_CAPABILITIES_COMPRESS = _libdrizzle.DRIZZLE_CAPABILITIES_COMPRESS
DRIZZLE_CAPABILITIES_ODBC = _libdrizzle.DRIZZLE_CAPABILITIES_ODBC
DRIZZLE_CAPABILITIES_LOCAL_FILES = _libdrizzle.DRIZZLE_CAPABILITIES_LOCAL_FILES
DRIZZLE_CAPABILITIES_IGNORE_SPACE = _libdrizzle.DRIZZLE_CAPABILITIES_IGNORE_SPACE
DRIZZLE_CAPABILITIES_PROTOCOL_41 = _libdrizzle.DRIZZLE_CAPABILITIES_PROTOCOL_41
DRIZZLE_CAPABILITIES_INTERACTIVE = _libdrizzle.DRIZZLE_CAPABILITIES_INTERACTIVE
DRIZZLE_CAPABILITIES_SSL = _libdrizzle.DRIZZLE_CAPABILITIES_SSL
DRIZZLE_CAPABILITIES_IGNORE_SIGPIPE = _libdrizzle.DRIZZLE_CAPABILITIES_IGNORE_SIGPIPE
DRIZZLE_CAPABILITIES_TRANSACTIONS = _libdrizzle.DRIZZLE_CAPABILITIES_TRANSACTIONS
DRIZZLE_CAPABILITIES_RESERVED = _libdrizzle.DRIZZLE_CAPABILITIES_RESERVED
DRIZZLE_CAPABILITIES_SECURE_CONNECTION = _libdrizzle.DRIZZLE_CAPABILITIES_SECURE_CONNECTION
DRIZZLE_CAPABILITIES_MULTI_STATEMENTS = _libdrizzle.DRIZZLE_CAPABILITIES_MULTI_STATEMENTS
DRIZZLE_CAPABILITIES_MULTI_RESULTS = _libdrizzle.DRIZZLE_CAPABILITIES_MULTI_RESULTS
DRIZZLE_CAPABILITIES_SSL_VERIFY_SERVER_CERT = _libdrizzle.DRIZZLE_CAPABILITIES_SSL_VERIFY_SERVER_CERT
DRIZZLE_CAPABILITIES_REMEMBER_OPTIONS = _libdrizzle.DRIZZLE_CAPABILITIES_REMEMBER_OPTIONS
DRIZZLE_CAPABILITIES_CLIENT = _libdrizzle.DRIZZLE_CAPABILITIES_CLIENT
DRIZZLE_COMMAND_SLEEP = _libdrizzle.DRIZZLE_COMMAND_SLEEP
DRIZZLE_COMMAND_QUIT = _libdrizzle.DRIZZLE_COMMAND_QUIT
DRIZZLE_COMMAND_INIT_DB = _libdrizzle.DRIZZLE_COMMAND_INIT_DB
DRIZZLE_COMMAND_QUERY = _libdrizzle.DRIZZLE_COMMAND_QUERY
DRIZZLE_COMMAND_FIELD_LIST = _libdrizzle.DRIZZLE_COMMAND_FIELD_LIST
DRIZZLE_COMMAND_CREATE_DB = _libdrizzle.DRIZZLE_COMMAND_CREATE_DB
DRIZZLE_COMMAND_DROP_DB = _libdrizzle.DRIZZLE_COMMAND_DROP_DB
DRIZZLE_COMMAND_REFRESH = _libdrizzle.DRIZZLE_COMMAND_REFRESH
DRIZZLE_COMMAND_SHUTDOWN = _libdrizzle.DRIZZLE_COMMAND_SHUTDOWN
DRIZZLE_COMMAND_STATISTICS = _libdrizzle.DRIZZLE_COMMAND_STATISTICS
DRIZZLE_COMMAND_PROCESS_INFO = _libdrizzle.DRIZZLE_COMMAND_PROCESS_INFO
DRIZZLE_COMMAND_CONNECT = _libdrizzle.DRIZZLE_COMMAND_CONNECT
DRIZZLE_COMMAND_PROCESS_KILL = _libdrizzle.DRIZZLE_COMMAND_PROCESS_KILL
DRIZZLE_COMMAND_DEBUG = _libdrizzle.DRIZZLE_COMMAND_DEBUG
DRIZZLE_COMMAND_PING = _libdrizzle.DRIZZLE_COMMAND_PING
DRIZZLE_COMMAND_TIME = _libdrizzle.DRIZZLE_COMMAND_TIME
DRIZZLE_COMMAND_DELAYED_INSERT = _libdrizzle.DRIZZLE_COMMAND_DELAYED_INSERT
DRIZZLE_COMMAND_CHANGE_USER = _libdrizzle.DRIZZLE_COMMAND_CHANGE_USER
DRIZZLE_COMMAND_BINLOG_DUMP = _libdrizzle.DRIZZLE_COMMAND_BINLOG_DUMP
DRIZZLE_COMMAND_TABLE_DUMP = _libdrizzle.DRIZZLE_COMMAND_TABLE_DUMP
DRIZZLE_COMMAND_CONNECT_OUT = _libdrizzle.DRIZZLE_COMMAND_CONNECT_OUT
DRIZZLE_COMMAND_REGISTER_SLAVE = _libdrizzle.DRIZZLE_COMMAND_REGISTER_SLAVE
DRIZZLE_COMMAND_STMT_PREPARE = _libdrizzle.DRIZZLE_COMMAND_STMT_PREPARE
DRIZZLE_COMMAND_STMT_EXECUTE = _libdrizzle.DRIZZLE_COMMAND_STMT_EXECUTE
DRIZZLE_COMMAND_STMT_SEND_LONG_DATA = _libdrizzle.DRIZZLE_COMMAND_STMT_SEND_LONG_DATA
DRIZZLE_COMMAND_STMT_CLOSE = _libdrizzle.DRIZZLE_COMMAND_STMT_CLOSE
DRIZZLE_COMMAND_STMT_RESET = _libdrizzle.DRIZZLE_COMMAND_STMT_RESET
DRIZZLE_COMMAND_SET_OPTION = _libdrizzle.DRIZZLE_COMMAND_SET_OPTION
DRIZZLE_COMMAND_STMT_FETCH = _libdrizzle.DRIZZLE_COMMAND_STMT_FETCH
DRIZZLE_COMMAND_DAEMON = _libdrizzle.DRIZZLE_COMMAND_DAEMON
DRIZZLE_COMMAND_END = _libdrizzle.DRIZZLE_COMMAND_END
DRIZZLE_COMMAND_DRIZZLE_SLEEP = _libdrizzle.DRIZZLE_COMMAND_DRIZZLE_SLEEP
DRIZZLE_COMMAND_DRIZZLE_QUIT = _libdrizzle.DRIZZLE_COMMAND_DRIZZLE_QUIT
DRIZZLE_COMMAND_DRIZZLE_INIT_DB = _libdrizzle.DRIZZLE_COMMAND_DRIZZLE_INIT_DB
DRIZZLE_COMMAND_DRIZZLE_QUERY = _libdrizzle.DRIZZLE_COMMAND_DRIZZLE_QUERY
DRIZZLE_COMMAND_DRIZZLE_SHUTDOWN = _libdrizzle.DRIZZLE_COMMAND_DRIZZLE_SHUTDOWN
DRIZZLE_COMMAND_DRIZZLE_CONNECT = _libdrizzle.DRIZZLE_COMMAND_DRIZZLE_CONNECT
DRIZZLE_COMMAND_DRIZZLE_PING = _libdrizzle.DRIZZLE_COMMAND_DRIZZLE_PING
DRIZZLE_COMMAND_DRIZZLE_END = _libdrizzle.DRIZZLE_COMMAND_DRIZZLE_END
DRIZZLE_QUERY_ALLOCATED = _libdrizzle.DRIZZLE_QUERY_ALLOCATED
DRIZZLE_QUERY_STATE_INIT = _libdrizzle.DRIZZLE_QUERY_STATE_INIT
DRIZZLE_QUERY_STATE_QUERY = _libdrizzle.DRIZZLE_QUERY_STATE_QUERY
DRIZZLE_QUERY_STATE_RESULT = _libdrizzle.DRIZZLE_QUERY_STATE_RESULT
DRIZZLE_QUERY_STATE_DONE = _libdrizzle.DRIZZLE_QUERY_STATE_DONE
DRIZZLE_RESULT_NONE = _libdrizzle.DRIZZLE_RESULT_NONE
DRIZZLE_RESULT_ALLOCATED = _libdrizzle.DRIZZLE_RESULT_ALLOCATED
DRIZZLE_RESULT_SKIP_COLUMN = _libdrizzle.DRIZZLE_RESULT_SKIP_COLUMN
DRIZZLE_RESULT_BUFFER_COLUMN = _libdrizzle.DRIZZLE_RESULT_BUFFER_COLUMN
DRIZZLE_RESULT_BUFFER_ROW = _libdrizzle.DRIZZLE_RESULT_BUFFER_ROW
DRIZZLE_RESULT_EOF_PACKET = _libdrizzle.DRIZZLE_RESULT_EOF_PACKET
DRIZZLE_RESULT_ROW_BREAK = _libdrizzle.DRIZZLE_RESULT_ROW_BREAK
DRIZZLE_COLUMN_ALLOCATED = _libdrizzle.DRIZZLE_COLUMN_ALLOCATED
DRIZZLE_COLUMN_TYPE_DECIMAL = _libdrizzle.DRIZZLE_COLUMN_TYPE_DECIMAL
DRIZZLE_COLUMN_TYPE_TINY = _libdrizzle.DRIZZLE_COLUMN_TYPE_TINY
DRIZZLE_COLUMN_TYPE_SHORT = _libdrizzle.DRIZZLE_COLUMN_TYPE_SHORT
DRIZZLE_COLUMN_TYPE_LONG = _libdrizzle.DRIZZLE_COLUMN_TYPE_LONG
DRIZZLE_COLUMN_TYPE_FLOAT = _libdrizzle.DRIZZLE_COLUMN_TYPE_FLOAT
DRIZZLE_COLUMN_TYPE_DOUBLE = _libdrizzle.DRIZZLE_COLUMN_TYPE_DOUBLE
DRIZZLE_COLUMN_TYPE_NULL = _libdrizzle.DRIZZLE_COLUMN_TYPE_NULL
DRIZZLE_COLUMN_TYPE_TIMESTAMP = _libdrizzle.DRIZZLE_COLUMN_TYPE_TIMESTAMP
DRIZZLE_COLUMN_TYPE_LONGLONG = _libdrizzle.DRIZZLE_COLUMN_TYPE_LONGLONG
DRIZZLE_COLUMN_TYPE_INT24 = _libdrizzle.DRIZZLE_COLUMN_TYPE_INT24
DRIZZLE_COLUMN_TYPE_DATE = _libdrizzle.DRIZZLE_COLUMN_TYPE_DATE
DRIZZLE_COLUMN_TYPE_TIME = _libdrizzle.DRIZZLE_COLUMN_TYPE_TIME
DRIZZLE_COLUMN_TYPE_DATETIME = _libdrizzle.DRIZZLE_COLUMN_TYPE_DATETIME
DRIZZLE_COLUMN_TYPE_YEAR = _libdrizzle.DRIZZLE_COLUMN_TYPE_YEAR
DRIZZLE_COLUMN_TYPE_NEWDATE = _libdrizzle.DRIZZLE_COLUMN_TYPE_NEWDATE
DRIZZLE_COLUMN_TYPE_VARCHAR = _libdrizzle.DRIZZLE_COLUMN_TYPE_VARCHAR
DRIZZLE_COLUMN_TYPE_BIT = _libdrizzle.DRIZZLE_COLUMN_TYPE_BIT
DRIZZLE_COLUMN_TYPE_NEWDECIMAL = _libdrizzle.DRIZZLE_COLUMN_TYPE_NEWDECIMAL
DRIZZLE_COLUMN_TYPE_ENUM = _libdrizzle.DRIZZLE_COLUMN_TYPE_ENUM
DRIZZLE_COLUMN_TYPE_SET = _libdrizzle.DRIZZLE_COLUMN_TYPE_SET
DRIZZLE_COLUMN_TYPE_TINY_BLOB = _libdrizzle.DRIZZLE_COLUMN_TYPE_TINY_BLOB
DRIZZLE_COLUMN_TYPE_MEDIUM_BLOB = _libdrizzle.DRIZZLE_COLUMN_TYPE_MEDIUM_BLOB
DRIZZLE_COLUMN_TYPE_LONG_BLOB = _libdrizzle.DRIZZLE_COLUMN_TYPE_LONG_BLOB
DRIZZLE_COLUMN_TYPE_BLOB = _libdrizzle.DRIZZLE_COLUMN_TYPE_BLOB
DRIZZLE_COLUMN_TYPE_VAR_STRING = _libdrizzle.DRIZZLE_COLUMN_TYPE_VAR_STRING
DRIZZLE_COLUMN_TYPE_STRING = _libdrizzle.DRIZZLE_COLUMN_TYPE_STRING
DRIZZLE_COLUMN_TYPE_GEOMETRY = _libdrizzle.DRIZZLE_COLUMN_TYPE_GEOMETRY
DRIZZLE_COLUMN_TYPE_DRIZZLE_TINY = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_TINY
DRIZZLE_COLUMN_TYPE_DRIZZLE_LONG = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_LONG
DRIZZLE_COLUMN_TYPE_DRIZZLE_DOUBLE = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_DOUBLE
DRIZZLE_COLUMN_TYPE_DRIZZLE_NULL = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_NULL
DRIZZLE_COLUMN_TYPE_DRIZZLE_TIMESTAMP = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_TIMESTAMP
DRIZZLE_COLUMN_TYPE_DRIZZLE_LONGLONG = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_LONGLONG
DRIZZLE_COLUMN_TYPE_DRIZZLE_DATETIME = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_DATETIME
DRIZZLE_COLUMN_TYPE_DRIZZLE_DATE = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_DATE
DRIZZLE_COLUMN_TYPE_DRIZZLE_VARCHAR = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_VARCHAR
DRIZZLE_COLUMN_TYPE_DRIZZLE_NEWDECIMAL = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_NEWDECIMAL
DRIZZLE_COLUMN_TYPE_DRIZZLE_ENUM = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_ENUM
DRIZZLE_COLUMN_TYPE_DRIZZLE_BLOB = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_BLOB
DRIZZLE_COLUMN_TYPE_DRIZZLE_MAX = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_MAX
DRIZZLE_COLUMN_FLAGS_NONE = _libdrizzle.DRIZZLE_COLUMN_FLAGS_NONE
DRIZZLE_COLUMN_FLAGS_NOT_NULL = _libdrizzle.DRIZZLE_COLUMN_FLAGS_NOT_NULL
DRIZZLE_COLUMN_FLAGS_PRI_KEY = _libdrizzle.DRIZZLE_COLUMN_FLAGS_PRI_KEY
DRIZZLE_COLUMN_FLAGS_UNIQUE_KEY = _libdrizzle.DRIZZLE_COLUMN_FLAGS_UNIQUE_KEY
DRIZZLE_COLUMN_FLAGS_MULTIPLE_KEY = _libdrizzle.DRIZZLE_COLUMN_FLAGS_MULTIPLE_KEY
DRIZZLE_COLUMN_FLAGS_BLOB = _libdrizzle.DRIZZLE_COLUMN_FLAGS_BLOB
DRIZZLE_COLUMN_FLAGS_UNSIGNED = _libdrizzle.DRIZZLE_COLUMN_FLAGS_UNSIGNED
DRIZZLE_COLUMN_FLAGS_ZEROFILL = _libdrizzle.DRIZZLE_COLUMN_FLAGS_ZEROFILL
DRIZZLE_COLUMN_FLAGS_BINARY = _libdrizzle.DRIZZLE_COLUMN_FLAGS_BINARY
DRIZZLE_COLUMN_FLAGS_ENUM = _libdrizzle.DRIZZLE_COLUMN_FLAGS_ENUM
DRIZZLE_COLUMN_FLAGS_AUTO_INCREMENT = _libdrizzle.DRIZZLE_COLUMN_FLAGS_AUTO_INCREMENT
DRIZZLE_COLUMN_FLAGS_TIMESTAMP = _libdrizzle.DRIZZLE_COLUMN_FLAGS_TIMESTAMP
DRIZZLE_COLUMN_FLAGS_SET = _libdrizzle.DRIZZLE_COLUMN_FLAGS_SET
DRIZZLE_COLUMN_FLAGS_NO_DEFAULT_VALUE = _libdrizzle.DRIZZLE_COLUMN_FLAGS_NO_DEFAULT_VALUE
DRIZZLE_COLUMN_FLAGS_ON_UPDATE_NOW = _libdrizzle.DRIZZLE_COLUMN_FLAGS_ON_UPDATE_NOW
DRIZZLE_COLUMN_FLAGS_PART_KEY = _libdrizzle.DRIZZLE_COLUMN_FLAGS_PART_KEY
DRIZZLE_COLUMN_FLAGS_NUM = _libdrizzle.DRIZZLE_COLUMN_FLAGS_NUM
DRIZZLE_COLUMN_FLAGS_GROUP = _libdrizzle.DRIZZLE_COLUMN_FLAGS_GROUP
DRIZZLE_COLUMN_FLAGS_UNIQUE = _libdrizzle.DRIZZLE_COLUMN_FLAGS_UNIQUE
DRIZZLE_COLUMN_FLAGS_BINCMP = _libdrizzle.DRIZZLE_COLUMN_FLAGS_BINCMP
DRIZZLE_COLUMN_FLAGS_GET_FIXED_FIELDS = _libdrizzle.DRIZZLE_COLUMN_FLAGS_GET_FIXED_FIELDS
DRIZZLE_COLUMN_FLAGS_IN_PART_FUNC = _libdrizzle.DRIZZLE_COLUMN_FLAGS_IN_PART_FUNC
DRIZZLE_COLUMN_FLAGS_IN_ADD_INDEX = _libdrizzle.DRIZZLE_COLUMN_FLAGS_IN_ADD_INDEX
DRIZZLE_COLUMN_FLAGS_RENAMED = _libdrizzle.DRIZZLE_COLUMN_FLAGS_RENAMED

def drizzle_version():
    """drizzle_version() -> char"""
    return _libdrizzle.drizzle_version()


class Drizzle(object):
    """Proxy of C Drizzle struct"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, d=None):
        """__init__(self,  d = None) -> Drizzle"""
        _libdrizzle.Drizzle_swiginit(self, _libdrizzle.new_Drizzle(d))

    __swig_destroy__ = _libdrizzle.delete_Drizzle

    def copy(self):
        """copy(self)"""
        return _libdrizzle.Drizzle_copy(self)

    def error(self):
        """error(self) -> unicode"""
        return _libdrizzle.Drizzle_error(self)

    def errno(self):
        """errno(self) -> int"""
        return _libdrizzle.Drizzle_errno(self)

    def options(self):
        """options(self) -> drizzle_options_t"""
        return _libdrizzle.Drizzle_options(self)

    def set_options(self, *args):
        """set_options(self, drizzle_options_t options)"""
        return _libdrizzle.Drizzle_set_options(self, *args)

    def add_options(self, *args):
        """add_options(self, drizzle_options_t options)"""
        return _libdrizzle.Drizzle_add_options(self, *args)

    def remove_options(self, *args):
        """remove_options(self, drizzle_options_t options)"""
        return _libdrizzle.Drizzle_remove_options(self, *args)

    def create_connection(self):
        """create_connection(self)"""
        return _libdrizzle.Drizzle_create_connection(self)

    def con_wait(self):
        """con_wait(self) -> drizzle_return_t"""
        return _libdrizzle.Drizzle_con_wait(self)

    def con_ready(self):
        """con_ready(self)"""
        return _libdrizzle.Drizzle_con_ready(self)

    def add_tcp(self, *args):
        """
        add_tcp(self, char host, in_port_t port, char user, char password, 
            char db, drizzle_con_options_t options)
        """
        return _libdrizzle.Drizzle_add_tcp(self, *args)

    def add_uds(self, *args):
        """add_uds(self, char uds, char user, char password, char db, drizzle_con_options_t options)"""
        return _libdrizzle.Drizzle_add_uds(self, *args)

    def create_query(self):
        """create_query(self)"""
        return _libdrizzle.Drizzle_create_query(self)

    def add_query(self, *args):
        """
        add_query(self,  query,  con, char query_string, size_t len, drizzle_query_options_t options, 
            void context)
        """
        return _libdrizzle.Drizzle_add_query(self, *args)

    def run(self):
        """run(self)"""
        return _libdrizzle.Drizzle_run(self)

    def run_all_queries(self):
        """run_all_queries(self) -> drizzle_return_t"""
        return _libdrizzle.Drizzle_run_all_queries(self)


Drizzle.copy = new_instancemethod(_libdrizzle.Drizzle_copy, None, Drizzle)
Drizzle.error = new_instancemethod(_libdrizzle.Drizzle_error, None, Drizzle)
Drizzle.errno = new_instancemethod(_libdrizzle.Drizzle_errno, None, Drizzle)
Drizzle.options = new_instancemethod(_libdrizzle.Drizzle_options, None, Drizzle)
Drizzle.set_options = new_instancemethod(_libdrizzle.Drizzle_set_options, None, Drizzle)
Drizzle.add_options = new_instancemethod(_libdrizzle.Drizzle_add_options, None, Drizzle)
Drizzle.remove_options = new_instancemethod(_libdrizzle.Drizzle_remove_options, None, Drizzle)
Drizzle.create_connection = new_instancemethod(_libdrizzle.Drizzle_create_connection, None, Drizzle)
Drizzle.con_wait = new_instancemethod(_libdrizzle.Drizzle_con_wait, None, Drizzle)
Drizzle.con_ready = new_instancemethod(_libdrizzle.Drizzle_con_ready, None, Drizzle)
Drizzle.add_tcp = new_instancemethod(_libdrizzle.Drizzle_add_tcp, None, Drizzle)
Drizzle.add_uds = new_instancemethod(_libdrizzle.Drizzle_add_uds, None, Drizzle)
Drizzle.create_query = new_instancemethod(_libdrizzle.Drizzle_create_query, None, Drizzle)
Drizzle.add_query = new_instancemethod(_libdrizzle.Drizzle_add_query, None, Drizzle)
Drizzle.run = new_instancemethod(_libdrizzle.Drizzle_run, None, Drizzle)
Drizzle.run_all_queries = new_instancemethod(_libdrizzle.Drizzle_run_all_queries, None, Drizzle)
Drizzle_swigregister = _libdrizzle.Drizzle_swigregister
Drizzle_swigregister(Drizzle)

class Connection(object):
    """Proxy of C Connection struct"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def host(self):
        """host(self) -> unicode"""
        return _libdrizzle.Connection_host(self)

    def port(self):
        """port(self) -> in_port_t"""
        return _libdrizzle.Connection_port(self)

    def set_tcp(self, *args):
        """set_tcp(self, char host, in_port_t port)"""
        return _libdrizzle.Connection_set_tcp(self, *args)

    def uds(self):
        """uds(self) -> unicode"""
        return _libdrizzle.Connection_uds(self)

    def set_uds(self, *args):
        """set_uds(self, char uds)"""
        return _libdrizzle.Connection_set_uds(self, *args)

    def user(self):
        """user(self) -> unicode"""
        return _libdrizzle.Connection_user(self)

    def password(self):
        """password(self) -> unicode"""
        return _libdrizzle.Connection_password(self)

    def set_auth(self, *args):
        """set_auth(self, char user, char password)"""
        return _libdrizzle.Connection_set_auth(self, *args)

    def db(self):
        """db(self) -> unicode"""
        return _libdrizzle.Connection_db(self)

    def set_db(self, *args):
        """set_db(self, char db)"""
        return _libdrizzle.Connection_set_db(self, *args)

    def options(self):
        """options(self) -> drizzle_con_options_t"""
        return _libdrizzle.Connection_options(self)

    def set_options(self, *args):
        """set_options(self, drizzle_con_options_t options)"""
        return _libdrizzle.Connection_set_options(self, *args)

    def add_options(self, *args):
        """add_options(self, drizzle_con_options_t options)"""
        return _libdrizzle.Connection_add_options(self, *args)

    def remove_options(self, *args):
        """remove_options(self, drizzle_con_options_t options)"""
        return _libdrizzle.Connection_remove_options(self, *args)

    def connect(self):
        """connect(self) -> drizzle_return_t"""
        return _libdrizzle.Connection_connect(self)

    def close(self):
        """close(self)"""
        return _libdrizzle.Connection_close(self)

    def protocol_version(self):
        """protocol_version(self) -> uint8_t"""
        return _libdrizzle.Connection_protocol_version(self)

    def server_version(self):
        """server_version(self) -> unicode"""
        return _libdrizzle.Connection_server_version(self)

    def server_version_number(self):
        """server_version_number(self) -> uint32_t"""
        return _libdrizzle.Connection_server_version_number(self)

    def thread_id(self):
        """thread_id(self) -> uint32_t"""
        return _libdrizzle.Connection_thread_id(self)

    def scramble(self):
        """scramble(self) -> uint8_t"""
        return _libdrizzle.Connection_scramble(self)

    def capabilities(self):
        """capabilities(self) -> drizzle_capabilities_t"""
        return _libdrizzle.Connection_capabilities(self)

    def charset(self):
        """charset(self) -> drizzle_charset_t"""
        return _libdrizzle.Connection_charset(self)

    def status(self):
        """status(self) -> drizzle_con_status_t"""
        return _libdrizzle.Connection_status(self)

    def max_packet_size(self):
        """max_packet_size(self) -> uint32_t"""
        return _libdrizzle.Connection_max_packet_size(self)

    def query(self, *args):
        """query(self, char query)"""
        return _libdrizzle.Connection_query(self, *args)

    def query_incremental(self, *args):
        """query_incremental(self, char query, size_t total)"""
        return _libdrizzle.Connection_query_incremental(self, *args)

    def quit(self):
        """quit(self)"""
        return _libdrizzle.Connection_quit(self)

    def select_db(self, *args):
        """select_db(self, char db)"""
        return _libdrizzle.Connection_select_db(self, *args)

    def shutdown(self, *args):
        """shutdown(self, uint32_t level)"""
        return _libdrizzle.Connection_shutdown(self, *args)

    def ping(self):
        """ping(self)"""
        return _libdrizzle.Connection_ping(self)

    def result_read(self, to=None):
        """result_read(self, drizzle_result_st to = None)"""
        return _libdrizzle.Connection_result_read(self, to)

    def write(self, *args):
        """
        write(self, drizzle_command_t command, uint8_t data, size_t size, 
            size_t total)
        """
        return _libdrizzle.Connection_write(self, *args)

    def result_create(self, to=None):
        """result_create(self, drizzle_result_st to = None)"""
        return _libdrizzle.Connection_result_create(self, to)

    def result_clone(self, *args):
        """result_clone(self, drizzle_result_st clone_from)"""
        return _libdrizzle.Connection_result_clone(self, *args)

    def result_write(self, *args):
        """result_write(self, drizzle_result_st to, bool flush) -> drizzle_return_t"""
        return _libdrizzle.Connection_result_write(self, *args)

    def set_protocol_version(self, *args):
        """set_protocol_version(self, uint8_t protocol_version)"""
        return _libdrizzle.Connection_set_protocol_version(self, *args)

    def set_server_version(self, *args):
        """set_server_version(self, char server_version)"""
        return _libdrizzle.Connection_set_server_version(self, *args)

    def set_thread_id(self, *args):
        """set_thread_id(self, uint32_t thread_id)"""
        return _libdrizzle.Connection_set_thread_id(self, *args)

    def set_scramble(self, *args):
        """set_scramble(self, uint8_t scramble)"""
        return _libdrizzle.Connection_set_scramble(self, *args)

    def set_capabilities(self, *args):
        """set_capabilities(self, drizzle_capabilities_t capabilities)"""
        return _libdrizzle.Connection_set_capabilities(self, *args)

    def set_charset(self, *args):
        """set_charset(self, drizzle_charset_t charset)"""
        return _libdrizzle.Connection_set_charset(self, *args)

    def set_status(self, *args):
        """set_status(self, drizzle_con_status_t status)"""
        return _libdrizzle.Connection_set_status(self, *args)

    def set_max_packet_size(self, *args):
        """set_max_packet_size(self, uint32_t max_packet_size)"""
        return _libdrizzle.Connection_set_max_packet_size(self, *args)

    def copy_handshake(self, *args):
        """copy_handshake(self, drizzle_con_st source)"""
        return _libdrizzle.Connection_copy_handshake(self, *args)

    def __init__(self):
        """__init__(self) -> Connection"""
        _libdrizzle.Connection_swiginit(self, _libdrizzle.new_Connection())

    __swig_destroy__ = _libdrizzle.delete_Connection


Connection.host = new_instancemethod(_libdrizzle.Connection_host, None, Connection)
Connection.port = new_instancemethod(_libdrizzle.Connection_port, None, Connection)
Connection.set_tcp = new_instancemethod(_libdrizzle.Connection_set_tcp, None, Connection)
Connection.uds = new_instancemethod(_libdrizzle.Connection_uds, None, Connection)
Connection.set_uds = new_instancemethod(_libdrizzle.Connection_set_uds, None, Connection)
Connection.user = new_instancemethod(_libdrizzle.Connection_user, None, Connection)
Connection.password = new_instancemethod(_libdrizzle.Connection_password, None, Connection)
Connection.set_auth = new_instancemethod(_libdrizzle.Connection_set_auth, None, Connection)
Connection.db = new_instancemethod(_libdrizzle.Connection_db, None, Connection)
Connection.set_db = new_instancemethod(_libdrizzle.Connection_set_db, None, Connection)
Connection.options = new_instancemethod(_libdrizzle.Connection_options, None, Connection)
Connection.set_options = new_instancemethod(_libdrizzle.Connection_set_options, None, Connection)
Connection.add_options = new_instancemethod(_libdrizzle.Connection_add_options, None, Connection)
Connection.remove_options = new_instancemethod(_libdrizzle.Connection_remove_options, None, Connection)
Connection.connect = new_instancemethod(_libdrizzle.Connection_connect, None, Connection)
Connection.close = new_instancemethod(_libdrizzle.Connection_close, None, Connection)
Connection.protocol_version = new_instancemethod(_libdrizzle.Connection_protocol_version, None, Connection)
Connection.server_version = new_instancemethod(_libdrizzle.Connection_server_version, None, Connection)
Connection.server_version_number = new_instancemethod(_libdrizzle.Connection_server_version_number, None, Connection)
Connection.thread_id = new_instancemethod(_libdrizzle.Connection_thread_id, None, Connection)
Connection.scramble = new_instancemethod(_libdrizzle.Connection_scramble, None, Connection)
Connection.capabilities = new_instancemethod(_libdrizzle.Connection_capabilities, None, Connection)
Connection.charset = new_instancemethod(_libdrizzle.Connection_charset, None, Connection)
Connection.status = new_instancemethod(_libdrizzle.Connection_status, None, Connection)
Connection.max_packet_size = new_instancemethod(_libdrizzle.Connection_max_packet_size, None, Connection)
Connection.query = new_instancemethod(_libdrizzle.Connection_query, None, Connection)
Connection.query_incremental = new_instancemethod(_libdrizzle.Connection_query_incremental, None, Connection)
Connection.quit = new_instancemethod(_libdrizzle.Connection_quit, None, Connection)
Connection.select_db = new_instancemethod(_libdrizzle.Connection_select_db, None, Connection)
Connection.shutdown = new_instancemethod(_libdrizzle.Connection_shutdown, None, Connection)
Connection.ping = new_instancemethod(_libdrizzle.Connection_ping, None, Connection)
Connection.result_read = new_instancemethod(_libdrizzle.Connection_result_read, None, Connection)
Connection.write = new_instancemethod(_libdrizzle.Connection_write, None, Connection)
Connection.result_create = new_instancemethod(_libdrizzle.Connection_result_create, None, Connection)
Connection.result_clone = new_instancemethod(_libdrizzle.Connection_result_clone, None, Connection)
Connection.result_write = new_instancemethod(_libdrizzle.Connection_result_write, None, Connection)
Connection.set_protocol_version = new_instancemethod(_libdrizzle.Connection_set_protocol_version, None, Connection)
Connection.set_server_version = new_instancemethod(_libdrizzle.Connection_set_server_version, None, Connection)
Connection.set_thread_id = new_instancemethod(_libdrizzle.Connection_set_thread_id, None, Connection)
Connection.set_scramble = new_instancemethod(_libdrizzle.Connection_set_scramble, None, Connection)
Connection.set_capabilities = new_instancemethod(_libdrizzle.Connection_set_capabilities, None, Connection)
Connection.set_charset = new_instancemethod(_libdrizzle.Connection_set_charset, None, Connection)
Connection.set_status = new_instancemethod(_libdrizzle.Connection_set_status, None, Connection)
Connection.set_max_packet_size = new_instancemethod(_libdrizzle.Connection_set_max_packet_size, None, Connection)
Connection.copy_handshake = new_instancemethod(_libdrizzle.Connection_copy_handshake, None, Connection)
Connection_swigregister = _libdrizzle.Connection_swigregister
Connection_swigregister(Connection)

class Query(object):
    """Proxy of C Query struct"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    __swig_destroy__ = _libdrizzle.delete_Query

    def con(self):
        """con(self)"""
        return _libdrizzle.Query_con(self)

    def set_con(self, *args):
        """set_con(self,  con)"""
        return _libdrizzle.Query_set_con(self, *args)

    def buffer_result(self):
        """buffer_result(self)"""
        return _libdrizzle.Query_buffer_result(self)

    def result(self):
        """result(self)"""
        return _libdrizzle.Query_result(self)

    def set_result(self, *args):
        """set_result(self,  result)"""
        return _libdrizzle.Query_set_result(self, *args)

    def string(self, *args):
        """string(self, size_t size) -> char"""
        return _libdrizzle.Query_string(self, *args)

    def set_string(self, *args):
        """set_string(self, char string, size_t size)"""
        return _libdrizzle.Query_set_string(self, *args)

    def query_options(self):
        """query_options(self) -> drizzle_query_options_t"""
        return _libdrizzle.Query_query_options(self)

    def context(self):
        """context(self) -> void"""
        return _libdrizzle.Query_context(self)

    def set_context(self, *args):
        """set_context(self, void context)"""
        return _libdrizzle.Query_set_context(self, *args)

    def __init__(self):
        """__init__(self) -> Query"""
        _libdrizzle.Query_swiginit(self, _libdrizzle.new_Query())


Query.con = new_instancemethod(_libdrizzle.Query_con, None, Query)
Query.set_con = new_instancemethod(_libdrizzle.Query_set_con, None, Query)
Query.buffer_result = new_instancemethod(_libdrizzle.Query_buffer_result, None, Query)
Query.result = new_instancemethod(_libdrizzle.Query_result, None, Query)
Query.set_result = new_instancemethod(_libdrizzle.Query_set_result, None, Query)
Query.string = new_instancemethod(_libdrizzle.Query_string, None, Query)
Query.set_string = new_instancemethod(_libdrizzle.Query_set_string, None, Query)
Query.query_options = new_instancemethod(_libdrizzle.Query_query_options, None, Query)
Query.context = new_instancemethod(_libdrizzle.Query_context, None, Query)
Query.set_context = new_instancemethod(_libdrizzle.Query_set_context, None, Query)
Query_swigregister = _libdrizzle.Query_swigregister
Query_swigregister(Query)

class Result(object):
    """Proxy of C Result struct"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    __swig_destroy__ = _libdrizzle.delete_Result

    def connection(self):
        """connection(self)"""
        return _libdrizzle.Result_connection(self)

    def row_field_sizes(self):
        """row_field_sizes(self) -> size_t"""
        return _libdrizzle.Result_row_field_sizes(self)

    def next_row(self):
        """next_row(self) -> drizzle_row_t"""
        return _libdrizzle.Result_next_row(self)

    def prev_row(self):
        """prev_row(self) -> drizzle_row_t"""
        return _libdrizzle.Result_prev_row(self)

    def get_row_field(self, *args):
        """get_row_field(self, drizzle_row_t row, int pos) -> char"""
        return _libdrizzle.Result_get_row_field(self, *args)

    def row_seek(self, *args):
        """row_seek(self, uint64_t row)"""
        return _libdrizzle.Result_row_seek(self, *args)

    def row_index(self, *args):
        """row_index(self, uint64_t row)"""
        return _libdrizzle.Result_row_index(self, *args)

    def row_current(self):
        """row_current(self) -> uint64_t"""
        return _libdrizzle.Result_row_current(self)

    def skip_column(self):
        """skip_column(self) -> drizzle_return_t"""
        return _libdrizzle.Result_skip_column(self)

    def read_column(self, column=None):
        """read_column(self,  column = None)"""
        return _libdrizzle.Result_read_column(self, column)

    def buffer_column(self):
        """buffer_column(self) -> drizzle_return_t"""
        return _libdrizzle.Result_buffer_column(self)

    def next_column(self):
        """next_column(self)"""
        return _libdrizzle.Result_next_column(self)

    def prev_column(self):
        """prev_column(self)"""
        return _libdrizzle.Result_prev_column(self)

    def seek_column(self, *args):
        """seek_column(self, uint16_t column)"""
        return _libdrizzle.Result_seek_column(self, *args)

    def column_index(self, *args):
        """column_index(self, uint16_t column)"""
        return _libdrizzle.Result_column_index(self, *args)

    def current_column(self):
        """current_column(self) -> uint16_t"""
        return _libdrizzle.Result_current_column(self)

    def buffer_result(self):
        """buffer_result(self)"""
        return _libdrizzle.Result_buffer_result(self)

    def buffer_field(self, *args):
        """buffer_field(self, size_t size) -> Field"""
        return _libdrizzle.Result_buffer_field(self, *args)

    def field_read(self, *args):
        """field_read(self, size_t offset, size_t size, size_t total) -> Field"""
        return _libdrizzle.Result_field_read(self, *args)

    def read_row(self):
        """read_row(self) -> uint64_t"""
        return _libdrizzle.Result_read_row(self)

    def buffer_row(self):
        """buffer_row(self) -> drizzle_row_t"""
        return _libdrizzle.Result_buffer_row(self)

    def free_row(self, *args):
        """free_row(self, drizzle_row_t row)"""
        return _libdrizzle.Result_free_row(self, *args)

    def current_row(self):
        """current_row(self) -> uint64_t"""
        return _libdrizzle.Result_current_row(self)

    def free_field(self, *args):
        """free_field(self, Field field)"""
        return _libdrizzle.Result_free_field(self, *args)

    def eof(self):
        """eof(self) -> bool"""
        return _libdrizzle.Result_eof(self)

    def info(self):
        """info(self) -> unicode"""
        return _libdrizzle.Result_info(self)

    def error(self):
        """error(self) -> unicode"""
        return _libdrizzle.Result_error(self)

    def error_code(self):
        """error_code(self) -> uint16_t"""
        return _libdrizzle.Result_error_code(self)

    def sqlstate(self):
        """sqlstate(self) -> char"""
        return _libdrizzle.Result_sqlstate(self)

    def warning_count(self):
        """warning_count(self) -> uint16_t"""
        return _libdrizzle.Result_warning_count(self)

    def insert_id(self):
        """insert_id(self) -> uint64_t"""
        return _libdrizzle.Result_insert_id(self)

    def affected_rows(self):
        """affected_rows(self) -> uint64_t"""
        return _libdrizzle.Result_affected_rows(self)

    def column_count(self):
        """column_count(self) -> uint16_t"""
        return _libdrizzle.Result_column_count(self)

    def row_count(self):
        """row_count(self) -> uint64_t"""
        return _libdrizzle.Result_row_count(self)

    def set_eof(self, *args):
        """set_eof(self, bool eof)"""
        return _libdrizzle.Result_set_eof(self, *args)

    def set_info(self, *args):
        """set_info(self, char info)"""
        return _libdrizzle.Result_set_info(self, *args)

    def set_error(self, *args):
        """set_error(self, char error)"""
        return _libdrizzle.Result_set_error(self, *args)

    def set_error_code(self, *args):
        """set_error_code(self, uint16_t error_code)"""
        return _libdrizzle.Result_set_error_code(self, *args)

    def set_sqlstate(self, *args):
        """set_sqlstate(self, char sqlstate)"""
        return _libdrizzle.Result_set_sqlstate(self, *args)

    def set_warning_count(self, *args):
        """set_warning_count(self, uint16_t warning_count)"""
        return _libdrizzle.Result_set_warning_count(self, *args)

    def set_insert_id(self, *args):
        """set_insert_id(self, uint64_t insert_id)"""
        return _libdrizzle.Result_set_insert_id(self, *args)

    def set_affected_rows(self, *args):
        """set_affected_rows(self, uint64_t affected_rows)"""
        return _libdrizzle.Result_set_affected_rows(self, *args)

    def set_column_count(self, *args):
        """set_column_count(self, uint16_t column_count)"""
        return _libdrizzle.Result_set_column_count(self, *args)

    def create_column(self):
        """create_column(self)"""
        return _libdrizzle.Result_create_column(self)

    def write_column(self, *args):
        """write_column(self,  column) -> drizzle_return_t"""
        return _libdrizzle.Result_write_column(self, *args)

    def write_row(self):
        """write_row(self) -> drizzle_return_t"""
        return _libdrizzle.Result_write_row(self)

    def buffer_multiple_rows(self, *args):
        """buffer_multiple_rows(self, uint64_t count) -> PyObject"""
        return _libdrizzle.Result_buffer_multiple_rows(self, *args)

    def __init__(self):
        """__init__(self) -> Result"""
        _libdrizzle.Result_swiginit(self, _libdrizzle.new_Result())


Result.connection = new_instancemethod(_libdrizzle.Result_connection, None, Result)
Result.row_field_sizes = new_instancemethod(_libdrizzle.Result_row_field_sizes, None, Result)
Result.next_row = new_instancemethod(_libdrizzle.Result_next_row, None, Result)
Result.prev_row = new_instancemethod(_libdrizzle.Result_prev_row, None, Result)
Result.get_row_field = new_instancemethod(_libdrizzle.Result_get_row_field, None, Result)
Result.row_seek = new_instancemethod(_libdrizzle.Result_row_seek, None, Result)
Result.row_index = new_instancemethod(_libdrizzle.Result_row_index, None, Result)
Result.row_current = new_instancemethod(_libdrizzle.Result_row_current, None, Result)
Result.skip_column = new_instancemethod(_libdrizzle.Result_skip_column, None, Result)
Result.read_column = new_instancemethod(_libdrizzle.Result_read_column, None, Result)
Result.buffer_column = new_instancemethod(_libdrizzle.Result_buffer_column, None, Result)
Result.next_column = new_instancemethod(_libdrizzle.Result_next_column, None, Result)
Result.prev_column = new_instancemethod(_libdrizzle.Result_prev_column, None, Result)
Result.seek_column = new_instancemethod(_libdrizzle.Result_seek_column, None, Result)
Result.column_index = new_instancemethod(_libdrizzle.Result_column_index, None, Result)
Result.current_column = new_instancemethod(_libdrizzle.Result_current_column, None, Result)
Result.buffer_result = new_instancemethod(_libdrizzle.Result_buffer_result, None, Result)
Result.buffer_field = new_instancemethod(_libdrizzle.Result_buffer_field, None, Result)
Result.field_read = new_instancemethod(_libdrizzle.Result_field_read, None, Result)
Result.read_row = new_instancemethod(_libdrizzle.Result_read_row, None, Result)
Result.buffer_row = new_instancemethod(_libdrizzle.Result_buffer_row, None, Result)
Result.free_row = new_instancemethod(_libdrizzle.Result_free_row, None, Result)
Result.current_row = new_instancemethod(_libdrizzle.Result_current_row, None, Result)
Result.free_field = new_instancemethod(_libdrizzle.Result_free_field, None, Result)
Result.eof = new_instancemethod(_libdrizzle.Result_eof, None, Result)
Result.info = new_instancemethod(_libdrizzle.Result_info, None, Result)
Result.error = new_instancemethod(_libdrizzle.Result_error, None, Result)
Result.error_code = new_instancemethod(_libdrizzle.Result_error_code, None, Result)
Result.sqlstate = new_instancemethod(_libdrizzle.Result_sqlstate, None, Result)
Result.warning_count = new_instancemethod(_libdrizzle.Result_warning_count, None, Result)
Result.insert_id = new_instancemethod(_libdrizzle.Result_insert_id, None, Result)
Result.affected_rows = new_instancemethod(_libdrizzle.Result_affected_rows, None, Result)
Result.column_count = new_instancemethod(_libdrizzle.Result_column_count, None, Result)
Result.row_count = new_instancemethod(_libdrizzle.Result_row_count, None, Result)
Result.set_eof = new_instancemethod(_libdrizzle.Result_set_eof, None, Result)
Result.set_info = new_instancemethod(_libdrizzle.Result_set_info, None, Result)
Result.set_error = new_instancemethod(_libdrizzle.Result_set_error, None, Result)
Result.set_error_code = new_instancemethod(_libdrizzle.Result_set_error_code, None, Result)
Result.set_sqlstate = new_instancemethod(_libdrizzle.Result_set_sqlstate, None, Result)
Result.set_warning_count = new_instancemethod(_libdrizzle.Result_set_warning_count, None, Result)
Result.set_insert_id = new_instancemethod(_libdrizzle.Result_set_insert_id, None, Result)
Result.set_affected_rows = new_instancemethod(_libdrizzle.Result_set_affected_rows, None, Result)
Result.set_column_count = new_instancemethod(_libdrizzle.Result_set_column_count, None, Result)
Result.create_column = new_instancemethod(_libdrizzle.Result_create_column, None, Result)
Result.write_column = new_instancemethod(_libdrizzle.Result_write_column, None, Result)
Result.write_row = new_instancemethod(_libdrizzle.Result_write_row, None, Result)
Result.buffer_multiple_rows = new_instancemethod(_libdrizzle.Result_buffer_multiple_rows, None, Result)
Result_swigregister = _libdrizzle.Result_swigregister
Result_swigregister(Result)

class Column(object):
    """Proxy of C Column struct"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    __swig_destroy__ = _libdrizzle.delete_Column

    def result(self):
        """result(self)"""
        return _libdrizzle.Column_result(self)

    def catalog(self):
        """catalog(self) -> unicode"""
        return _libdrizzle.Column_catalog(self)

    def db(self):
        """db(self) -> unicode"""
        return _libdrizzle.Column_db(self)

    def table(self):
        """table(self) -> unicode"""
        return _libdrizzle.Column_table(self)

    def orig_table(self):
        """orig_table(self) -> unicode"""
        return _libdrizzle.Column_orig_table(self)

    def name(self):
        """name(self) -> unicode"""
        return _libdrizzle.Column_name(self)

    def orig_name(self):
        """orig_name(self) -> unicode"""
        return _libdrizzle.Column_orig_name(self)

    def charset(self):
        """charset(self) -> uint16_t"""
        return _libdrizzle.Column_charset(self)

    def size(self):
        """size(self) -> uint32_t"""
        return _libdrizzle.Column_size(self)

    def max_size(self):
        """max_size(self) -> size_t"""
        return _libdrizzle.Column_max_size(self)

    def column_type(self):
        """column_type(self) -> drizzle_column_type_t"""
        return _libdrizzle.Column_column_type(self)

    def flags(self):
        """flags(self) -> drizzle_column_flags_t"""
        return _libdrizzle.Column_flags(self)

    def decimals(self):
        """decimals(self) -> uint8_t"""
        return _libdrizzle.Column_decimals(self)

    def default_value(self):
        """default_value(self)"""
        return _libdrizzle.Column_default_value(self)

    def set_catalog(self, *args):
        """set_catalog(self, char catalog)"""
        return _libdrizzle.Column_set_catalog(self, *args)

    def set_db(self, *args):
        """set_db(self, char db)"""
        return _libdrizzle.Column_set_db(self, *args)

    def set_table(self, *args):
        """set_table(self, drizzle_column_st column, char table)"""
        return _libdrizzle.Column_set_table(self, *args)

    def set_orig_table(self, *args):
        """set_orig_table(self, char orig_table)"""
        return _libdrizzle.Column_set_orig_table(self, *args)

    def set_name(self, *args):
        """set_name(self, char name)"""
        return _libdrizzle.Column_set_name(self, *args)

    def set_orig_name(self, *args):
        """set_orig_name(self, char orig_name)"""
        return _libdrizzle.Column_set_orig_name(self, *args)

    def set_charset(self, *args):
        """set_charset(self, drizzle_charset_t charset)"""
        return _libdrizzle.Column_set_charset(self, *args)

    def set_size(self, *args):
        """set_size(self, uint32_t size)"""
        return _libdrizzle.Column_set_size(self, *args)

    def set_type(self, *args):
        """set_type(self, drizzle_column_type_t type)"""
        return _libdrizzle.Column_set_type(self, *args)

    def set_flags(self, *args):
        """set_flags(self, drizzle_column_flags_t flags)"""
        return _libdrizzle.Column_set_flags(self, *args)

    def set_decimals(self, *args):
        """set_decimals(self, uint8_t decimals)"""
        return _libdrizzle.Column_set_decimals(self, *args)

    def set_default_value(self, *args):
        """set_default_value(self, uint8_t default_value, size_t size)"""
        return _libdrizzle.Column_set_default_value(self, *args)

    def __init__(self):
        """__init__(self) -> Column"""
        _libdrizzle.Column_swiginit(self, _libdrizzle.new_Column())


Column.result = new_instancemethod(_libdrizzle.Column_result, None, Column)
Column.catalog = new_instancemethod(_libdrizzle.Column_catalog, None, Column)
Column.db = new_instancemethod(_libdrizzle.Column_db, None, Column)
Column.table = new_instancemethod(_libdrizzle.Column_table, None, Column)
Column.orig_table = new_instancemethod(_libdrizzle.Column_orig_table, None, Column)
Column.name = new_instancemethod(_libdrizzle.Column_name, None, Column)
Column.orig_name = new_instancemethod(_libdrizzle.Column_orig_name, None, Column)
Column.charset = new_instancemethod(_libdrizzle.Column_charset, None, Column)
Column.size = new_instancemethod(_libdrizzle.Column_size, None, Column)
Column.max_size = new_instancemethod(_libdrizzle.Column_max_size, None, Column)
Column.column_type = new_instancemethod(_libdrizzle.Column_column_type, None, Column)
Column.flags = new_instancemethod(_libdrizzle.Column_flags, None, Column)
Column.decimals = new_instancemethod(_libdrizzle.Column_decimals, None, Column)
Column.default_value = new_instancemethod(_libdrizzle.Column_default_value, None, Column)
Column.set_catalog = new_instancemethod(_libdrizzle.Column_set_catalog, None, Column)
Column.set_db = new_instancemethod(_libdrizzle.Column_set_db, None, Column)
Column.set_table = new_instancemethod(_libdrizzle.Column_set_table, None, Column)
Column.set_orig_table = new_instancemethod(_libdrizzle.Column_set_orig_table, None, Column)
Column.set_name = new_instancemethod(_libdrizzle.Column_set_name, None, Column)
Column.set_orig_name = new_instancemethod(_libdrizzle.Column_set_orig_name, None, Column)
Column.set_charset = new_instancemethod(_libdrizzle.Column_set_charset, None, Column)
Column.set_size = new_instancemethod(_libdrizzle.Column_set_size, None, Column)
Column.set_type = new_instancemethod(_libdrizzle.Column_set_type, None, Column)
Column.set_flags = new_instancemethod(_libdrizzle.Column_set_flags, None, Column)
Column.set_decimals = new_instancemethod(_libdrizzle.Column_set_decimals, None, Column)
Column.set_default_value = new_instancemethod(_libdrizzle.Column_set_default_value, None, Column)
Column_swigregister = _libdrizzle.Column_swigregister
Column_swigregister(Column)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_mysql\lib\mysql\connector\constants.py
# Compiled at: 2017-12-07 02:34:36
# Size of source mod 2**32: 25349 bytes
"""Various MySQL constants and character sets
"""
from .errors import ProgrammingError
from .charsets import MYSQL_CHARACTER_SETS
MAX_PACKET_LENGTH = 16777215
NET_BUFFER_LENGTH = 8192
MAX_MYSQL_TABLE_COLUMNS = 4096
DEFAULT_CONFIGURATION = {'database':None, 
 'user':'', 
 'password':'', 
 'host':'127.0.0.1', 
 'port':3306, 
 'unix_socket':None, 
 'use_unicode':True, 
 'charset':'utf8', 
 'collation':None, 
 'converter_class':None, 
 'autocommit':False, 
 'time_zone':None, 
 'sql_mode':None, 
 'get_warnings':False, 
 'raise_on_warnings':False, 
 'connection_timeout':None, 
 'client_flags':0, 
 'compress':False, 
 'buffered':False, 
 'raw':False, 
 'ssl_ca':None, 
 'ssl_cert':None, 
 'ssl_key':None, 
 'ssl_verify_cert':False, 
 'ssl_cipher':None, 
 'ssl_disabled':False, 
 'passwd':None, 
 'db':None, 
 'connect_timeout':None, 
 'dsn':None, 
 'force_ipv6':False, 
 'auth_plugin':None, 
 'allow_local_infile':True, 
 'consume_results':False}
CNX_POOL_ARGS = ('pool_name', 'pool_size', 'pool_reset_session')
CNX_FABRIC_ARGS = ['fabric_host', 'fabric_username', 'fabric_password',
 'fabric_port', 'fabric_connect_attempts',
 'fabric_connect_delay', 'fabric_report_errors',
 'fabric_ssl_ca', 'fabric_ssl_key', 'fabric_ssl_cert',
 'fabric_user']

def flag_is_set(flag, flags):
    """Checks if the flag is set

    Returns boolean"""
    if flags & flag > 0:
        return True
    else:
        return False


class _Constants(object):
    __doc__ = '\n    Base class for constants\n    '
    prefix = ''
    desc = {}

    def __new__(cls):
        raise TypeError('Can not instanciate from %s' % cls.__name__)

    @classmethod
    def get_desc(cls, name):
        """Get description of given constant"""
        try:
            return cls.desc[name][1]
        except:
            return

    @classmethod
    def get_info(cls, num):
        """Get information about given constant"""
        for name, info in cls.desc.items():
            if info[0] == num:
                return name

    @classmethod
    def get_full_info(cls):
        """get full information about given constant"""
        res = ()
        try:
            res = ['%s : %s' % (k, v[1]) for k, v in cls.desc.items()]
        except Exception as err:
            res = 'No information found in constant class.%s' % err

        return res


class _Flags(_Constants):
    __doc__ = 'Base class for classes describing flags\n    '

    @classmethod
    def get_bit_info(cls, value):
        """Get the name of all bits set

        Returns a list of strings."""
        res = []
        for name, info in cls.desc.items():
            if value & info[0]:
                res.append(name)

        return res


class FieldType(_Constants):
    __doc__ = 'MySQL Field Types\n    '
    prefix = 'FIELD_TYPE_'
    DECIMAL = 0
    TINY = 1
    SHORT = 2
    LONG = 3
    FLOAT = 4
    DOUBLE = 5
    NULL = 6
    TIMESTAMP = 7
    LONGLONG = 8
    INT24 = 9
    DATE = 10
    TIME = 11
    DATETIME = 12
    YEAR = 13
    NEWDATE = 14
    VARCHAR = 15
    BIT = 16
    NEWDECIMAL = 246
    ENUM = 247
    SET = 248
    TINY_BLOB = 249
    MEDIUM_BLOB = 250
    LONG_BLOB = 251
    BLOB = 252
    VAR_STRING = 253
    STRING = 254
    GEOMETRY = 255
    desc = {'DECIMAL':(0, 'DECIMAL'), 
     'TINY':(1, 'TINY'), 
     'SHORT':(2, 'SHORT'), 
     'LONG':(3, 'LONG'), 
     'FLOAT':(4, 'FLOAT'), 
     'DOUBLE':(5, 'DOUBLE'), 
     'NULL':(6, 'NULL'), 
     'TIMESTAMP':(7, 'TIMESTAMP'), 
     'LONGLONG':(8, 'LONGLONG'), 
     'INT24':(9, 'INT24'), 
     'DATE':(10, 'DATE'), 
     'TIME':(11, 'TIME'), 
     'DATETIME':(12, 'DATETIME'), 
     'YEAR':(13, 'YEAR'), 
     'NEWDATE':(14, 'NEWDATE'), 
     'VARCHAR':(15, 'VARCHAR'), 
     'BIT':(16, 'BIT'), 
     'NEWDECIMAL':(246, 'NEWDECIMAL'), 
     'ENUM':(247, 'ENUM'), 
     'SET':(248, 'SET'), 
     'TINY_BLOB':(249, 'TINY_BLOB'), 
     'MEDIUM_BLOB':(250, 'MEDIUM_BLOB'), 
     'LONG_BLOB':(251, 'LONG_BLOB'), 
     'BLOB':(252, 'BLOB'), 
     'VAR_STRING':(253, 'VAR_STRING'), 
     'STRING':(254, 'STRING'), 
     'GEOMETRY':(255, 'GEOMETRY')}

    @classmethod
    def get_string_types(cls):
        """Get the list of all string types"""
        return [
         cls.VARCHAR,
         cls.ENUM,
         cls.VAR_STRING, cls.STRING]

    @classmethod
    def get_binary_types(cls):
        """Get the list of all binary types"""
        return [
         cls.TINY_BLOB, cls.MEDIUM_BLOB,
         cls.LONG_BLOB, cls.BLOB]

    @classmethod
    def get_number_types(cls):
        """Get the list of all number types"""
        return [
         cls.DECIMAL, cls.NEWDECIMAL,
         cls.TINY, cls.SHORT, cls.LONG,
         cls.FLOAT, cls.DOUBLE,
         cls.LONGLONG, cls.INT24,
         cls.BIT,
         cls.YEAR]

    @classmethod
    def get_timestamp_types(cls):
        """Get the list of all timestamp types"""
        return [
         cls.DATETIME, cls.TIMESTAMP]


class FieldFlag(_Flags):
    __doc__ = 'MySQL Field Flags\n\n    Field flags as found in MySQL sources mysql-src/include/mysql_com.h\n    '
    _prefix = ''
    NOT_NULL = 1
    PRI_KEY = 2
    UNIQUE_KEY = 4
    MULTIPLE_KEY = 8
    BLOB = 16
    UNSIGNED = 32
    ZEROFILL = 64
    BINARY = 128
    ENUM = 256
    AUTO_INCREMENT = 512
    TIMESTAMP = 1024
    SET = 2048
    NO_DEFAULT_VALUE = 4096
    ON_UPDATE_NOW = 8192
    NUM = 16384
    PART_KEY = 32768
    GROUP = 16384
    UNIQUE = 65536
    BINCMP = 131072
    GET_FIXED_FIELDS = 262144
    FIELD_IN_PART_FUNC = 524288
    FIELD_IN_ADD_INDEX = 1048576
    FIELD_IS_RENAMED = 2097152
    desc = {'NOT_NULL':(1, "Field can't be NULL"), 
     'PRI_KEY':(2, 'Field is part of a primary key'), 
     'UNIQUE_KEY':(4, 'Field is part of a unique key'), 
     'MULTIPLE_KEY':(8, 'Field is part of a key'), 
     'BLOB':(16, 'Field is a blob'), 
     'UNSIGNED':(32, 'Field is unsigned'), 
     'ZEROFILL':(64, 'Field is zerofill'), 
     'BINARY':(128, 'Field is binary  '), 
     'ENUM':(256, 'field is an enum'), 
     'AUTO_INCREMENT':(512, 'field is a autoincrement field'), 
     'TIMESTAMP':(1024, 'Field is a timestamp'), 
     'SET':(2048, 'field is a set'), 
     'NO_DEFAULT_VALUE':(4096, "Field doesn't have default value"), 
     'ON_UPDATE_NOW':(8192, 'Field is set to NOW on UPDATE'), 
     'NUM':(16384, 'Field is num (for clients)'), 
     'PART_KEY':(32768, 'Intern; Part of some key'), 
     'GROUP':(16384, 'Intern: Group field'), 
     'UNIQUE':(65536, 'Intern: Used by sql_yacc'), 
     'BINCMP':(131072, 'Intern: Used by sql_yacc'), 
     'GET_FIXED_FIELDS':(262144, 'Used to get fields in item tree'), 
     'FIELD_IN_PART_FUNC':(524288, 'Field part of partition func'), 
     'FIELD_IN_ADD_INDEX':(1048576, 'Intern: Field used in ADD INDEX'), 
     'FIELD_IS_RENAMED':(2097152, 'Intern: Field is being renamed')}


class ServerCmd(_Constants):
    __doc__ = 'MySQL Server Commands\n    '
    _prefix = 'COM_'
    SLEEP = 0
    QUIT = 1
    INIT_DB = 2
    QUERY = 3
    FIELD_LIST = 4
    CREATE_DB = 5
    DROP_DB = 6
    REFRESH = 7
    SHUTDOWN = 8
    STATISTICS = 9
    PROCESS_INFO = 10
    CONNECT = 11
    PROCESS_KILL = 12
    DEBUG = 13
    PING = 14
    TIME = 15
    DELAYED_INSERT = 16
    CHANGE_USER = 17
    BINLOG_DUMP = 18
    TABLE_DUMP = 19
    CONNECT_OUT = 20
    REGISTER_SLAVE = 21
    STMT_PREPARE = 22
    STMT_EXECUTE = 23
    STMT_SEND_LONG_DATA = 24
    STMT_CLOSE = 25
    STMT_RESET = 26
    SET_OPTION = 27
    STMT_FETCH = 28
    DAEMON = 29
    BINLOG_DUMP_GTID = 30
    RESET_CONNECTION = 31
    desc = {'SLEEP':(0, 'SLEEP'), 
     'QUIT':(1, 'QUIT'), 
     'INIT_DB':(2, 'INIT_DB'), 
     'QUERY':(3, 'QUERY'), 
     'FIELD_LIST':(4, 'FIELD_LIST'), 
     'CREATE_DB':(5, 'CREATE_DB'), 
     'DROP_DB':(6, 'DROP_DB'), 
     'REFRESH':(7, 'REFRESH'), 
     'SHUTDOWN':(8, 'SHUTDOWN'), 
     'STATISTICS':(9, 'STATISTICS'), 
     'PROCESS_INFO':(10, 'PROCESS_INFO'), 
     'CONNECT':(11, 'CONNECT'), 
     'PROCESS_KILL':(12, 'PROCESS_KILL'), 
     'DEBUG':(13, 'DEBUG'), 
     'PING':(14, 'PING'), 
     'TIME':(15, 'TIME'), 
     'DELAYED_INSERT':(16, 'DELAYED_INSERT'), 
     'CHANGE_USER':(17, 'CHANGE_USER'), 
     'BINLOG_DUMP':(18, 'BINLOG_DUMP'), 
     'TABLE_DUMP':(19, 'TABLE_DUMP'), 
     'CONNECT_OUT':(20, 'CONNECT_OUT'), 
     'REGISTER_SLAVE':(21, 'REGISTER_SLAVE'), 
     'STMT_PREPARE':(22, 'STMT_PREPARE'), 
     'STMT_EXECUTE':(23, 'STMT_EXECUTE'), 
     'STMT_SEND_LONG_DATA':(24, 'STMT_SEND_LONG_DATA'), 
     'STMT_CLOSE':(25, 'STMT_CLOSE'), 
     'STMT_RESET':(26, 'STMT_RESET'), 
     'SET_OPTION':(27, 'SET_OPTION'), 
     'STMT_FETCH':(28, 'STMT_FETCH'), 
     'DAEMON':(29, 'DAEMON'), 
     'BINLOG_DUMP_GTID':(30, 'BINLOG_DUMP_GTID'), 
     'RESET_CONNECTION':(31, 'RESET_CONNECTION')}


class ClientFlag(_Flags):
    __doc__ = 'MySQL Client Flags\n\n    Client options as found in the MySQL sources mysql-src/include/mysql_com.h\n    '
    LONG_PASSWD = 1
    FOUND_ROWS = 2
    LONG_FLAG = 4
    CONNECT_WITH_DB = 8
    NO_SCHEMA = 16
    COMPRESS = 32
    ODBC = 64
    LOCAL_FILES = 128
    IGNORE_SPACE = 256
    PROTOCOL_41 = 512
    INTERACTIVE = 1024
    SSL = 2048
    IGNORE_SIGPIPE = 4096
    TRANSACTIONS = 8192
    RESERVED = 16384
    SECURE_CONNECTION = 32768
    MULTI_STATEMENTS = 65536
    MULTI_RESULTS = 131072
    PS_MULTI_RESULTS = 262144
    PLUGIN_AUTH = 524288
    CONNECT_ARGS = 1048576
    PLUGIN_AUTH_LENENC_CLIENT_DATA = 2097152
    CAN_HANDLE_EXPIRED_PASSWORDS = 4194304
    SESION_TRACK = 8388608
    DEPRECATE_EOF = 16777216
    SSL_VERIFY_SERVER_CERT = 1073741824
    REMEMBER_OPTIONS = 2147483648
    desc = {'LONG_PASSWD':(1, 'New more secure passwords'), 
     'FOUND_ROWS':(2, 'Found instead of affected rows'), 
     'LONG_FLAG':(4, 'Get all column flags'), 
     'CONNECT_WITH_DB':(8, 'One can specify db on connect'), 
     'NO_SCHEMA':(16, "Don't allow database.table.column"), 
     'COMPRESS':(32, 'Can use compression protocol'), 
     'ODBC':(64, 'ODBC client'), 
     'LOCAL_FILES':(128, 'Can use LOAD DATA LOCAL'), 
     'IGNORE_SPACE':(256, "Ignore spaces before ''"), 
     'PROTOCOL_41':(512, 'New 4.1 protocol'), 
     'INTERACTIVE':(1024, 'This is an interactive client'), 
     'SSL':(2048, 'Switch to SSL after handshake'), 
     'IGNORE_SIGPIPE':(4096, 'IGNORE sigpipes'), 
     'TRANSACTIONS':(8192, 'Client knows about transactions'), 
     'RESERVED':(16384, 'Old flag for 4.1 protocol'), 
     'SECURE_CONNECTION':(32768, 'New 4.1 authentication'), 
     'MULTI_STATEMENTS':(65536, 'Enable/disable multi-stmt support'), 
     'MULTI_RESULTS':(131072, 'Enable/disable multi-results'), 
     'PS_MULTI_RESULTS':(262144, 'Multi-results in PS-protocol'), 
     'PLUGIN_AUTH':(524288, 'Client supports plugin authentication'), 
     'CONNECT_ARGS':(1048576, 'Client supports connection attributes'), 
     'PLUGIN_AUTH_LENENC_CLIENT_DATA':(2097152, 'Enable authentication response packet to be larger than 255 bytes'), 
     'CAN_HANDLE_EXPIRED_PASSWORDS':(4194304, "Don't close the connection for a connection with expired password"), 
     'SESION_TRACK':(8388608, 'Capable of handling server state change information'), 
     'DEPRECATE_EOF':(16777216, 'Client no longer needs EOF packet'), 
     'SSL_VERIFY_SERVER_CERT':(1073741824, ''), 
     'REMEMBER_OPTIONS':(2147483648, '')}
    default = [
     LONG_PASSWD,
     LONG_FLAG,
     CONNECT_WITH_DB,
     PROTOCOL_41,
     TRANSACTIONS,
     SECURE_CONNECTION,
     MULTI_STATEMENTS,
     MULTI_RESULTS,
     LOCAL_FILES]

    @classmethod
    def get_default(cls):
        """Get the default client options set

        Returns a flag with all the default client options set"""
        flags = 0
        for option in cls.default:
            flags |= option

        return flags


class ServerFlag(_Flags):
    __doc__ = 'MySQL Server Flags\n\n    Server flags as found in the MySQL sources mysql-src/include/mysql_com.h\n    '
    _prefix = 'SERVER_'
    STATUS_IN_TRANS = 1
    STATUS_AUTOCOMMIT = 2
    MORE_RESULTS_EXISTS = 8
    QUERY_NO_GOOD_INDEX_USED = 16
    QUERY_NO_INDEX_USED = 32
    STATUS_CURSOR_EXISTS = 64
    STATUS_LAST_ROW_SENT = 128
    STATUS_DB_DROPPED = 256
    STATUS_NO_BACKSLASH_ESCAPES = 512
    SERVER_STATUS_METADATA_CHANGED = 1024
    SERVER_QUERY_WAS_SLOW = 2048
    SERVER_PS_OUT_PARAMS = 4096
    SERVER_STATUS_IN_TRANS_READONLY = 8192
    SERVER_SESSION_STATE_CHANGED = 16384
    desc = {'SERVER_STATUS_IN_TRANS':(1, 'Transaction has started'), 
     'SERVER_STATUS_AUTOCOMMIT':(2, 'Server in auto_commit mode'), 
     'SERVER_MORE_RESULTS_EXISTS':(8, 'Multi query - next query exists'), 
     'SERVER_QUERY_NO_GOOD_INDEX_USED':(16, ''), 
     'SERVER_QUERY_NO_INDEX_USED':(32, ''), 
     'SERVER_STATUS_CURSOR_EXISTS':(64, 'Set when server opened a read-only non-scrollable cursor for a query.'), 
     'SERVER_STATUS_LAST_ROW_SENT':(128, 'Set when a read-only cursor is exhausted'), 
     'SERVER_STATUS_DB_DROPPED':(256, 'A database was dropped'), 
     'SERVER_STATUS_NO_BACKSLASH_ESCAPES':(512, ''), 
     'SERVER_STATUS_METADATA_CHANGED':(1024, 'Set if after a prepared statement reprepare we discovered that the new statement returns a different number of result set columns.'), 
     'SERVER_QUERY_WAS_SLOW':(2048, ''), 
     'SERVER_PS_OUT_PARAMS':(4096, 'To mark ResultSet containing output parameter values.'), 
     'SERVER_STATUS_IN_TRANS_READONLY':(8192, 'Set if multi-statement transaction is a read-only transaction.'), 
     'SERVER_SESSION_STATE_CHANGED':(16384, 'Session state has changed on the server because of the execution of the last statement')}


class RefreshOption(_Constants):
    __doc__ = 'MySQL Refresh command options\n\n    Options used when sending the COM_REFRESH server command.\n    '
    _prefix = 'REFRESH_'
    GRANT = 1
    LOG = 2
    TABLES = 4
    HOST = 8
    STATUS = 16
    THREADS = 32
    SLAVE = 64
    desc = {'GRANT':(1, 'Refresh grant tables'), 
     'LOG':(2, 'Start on new log file'), 
     'TABLES':(4, 'close all tables'), 
     'HOSTS':(8, 'Flush host cache'), 
     'STATUS':(16, 'Flush status variables'), 
     'THREADS':(32, 'Flush thread cache'), 
     'SLAVE':(64, 'Reset master info and restart slave thread')}


class ShutdownType(_Constants):
    __doc__ = 'MySQL Shutdown types\n\n    Shutdown types used by the COM_SHUTDOWN server command.\n    '
    _prefix = ''
    SHUTDOWN_DEFAULT = 0
    SHUTDOWN_WAIT_CONNECTIONS = 1
    SHUTDOWN_WAIT_TRANSACTIONS = 2
    SHUTDOWN_WAIT_UPDATES = 8
    SHUTDOWN_WAIT_ALL_BUFFERS = 16
    SHUTDOWN_WAIT_CRITICAL_BUFFERS = 17
    KILL_QUERY = 254
    KILL_CONNECTION = 255
    desc = {'SHUTDOWN_DEFAULT':(
      SHUTDOWN_DEFAULT,
      'defaults to SHUTDOWN_WAIT_ALL_BUFFERS'), 
     'SHUTDOWN_WAIT_CONNECTIONS':(
      SHUTDOWN_WAIT_CONNECTIONS,
      'wait for existing connections to finish'), 
     'SHUTDOWN_WAIT_TRANSACTIONS':(
      SHUTDOWN_WAIT_TRANSACTIONS,
      'wait for existing trans to finish'), 
     'SHUTDOWN_WAIT_UPDATES':(
      SHUTDOWN_WAIT_UPDATES,
      'wait for existing updates to finish'), 
     'SHUTDOWN_WAIT_ALL_BUFFERS':(
      SHUTDOWN_WAIT_ALL_BUFFERS,
      'flush InnoDB and other storage engine buffers'), 
     'SHUTDOWN_WAIT_CRITICAL_BUFFERS':(
      SHUTDOWN_WAIT_CRITICAL_BUFFERS,
      "don't flush InnoDB buffers, flush other storage engines' buffers"), 
     'KILL_QUERY':(
      KILL_QUERY,
      '(no description)'), 
     'KILL_CONNECTION':(
      KILL_CONNECTION,
      '(no description)')}


class CharacterSet(_Constants):
    __doc__ = 'MySQL supported character sets and collations\n\n    List of character sets with their collations supported by MySQL. This\n    maps to the character set we get from the server within the handshake\n    packet.\n\n    The list is hardcode so we avoid a database query when getting the\n    name of the used character set or collation.\n    '
    desc = MYSQL_CHARACTER_SETS
    slash_charsets = (1, 13, 28, 84, 87, 88)

    @classmethod
    def get_info(cls, setid):
        """Retrieves character set information as tuple using an ID

        Retrieves character set and collation information based on the
        given MySQL ID.

        Raises ProgrammingError when character set is not supported.

        Returns a tuple.
        """
        try:
            return cls.desc[setid][0:2]
        except IndexError:
            raise ProgrammingError("Character set '{0}' unsupported".format(setid))

    @classmethod
    def get_desc(cls, setid):
        """Retrieves character set information as string using an ID

        Retrieves character set and collation information based on the
        given MySQL ID.

        Returns a tuple.
        """
        try:
            return '%s/%s' % cls.get_info(setid)
        except:
            raise

    @classmethod
    def get_default_collation(cls, charset):
        """Retrieves the default collation for given character set

        Raises ProgrammingError when character set is not supported.

        Returns list (collation, charset, index)
        """
        if isinstance(charset, int):
            try:
                info = cls.desc[charset]
                return (info[1], info[0], charset)
            except:
                ProgrammingError("Character set ID '%s' unsupported." % charset)

        for cid, info in enumerate(cls.desc):
            if info is None:
                pass
            else:
                if info[0] == charset:
                    if info[2] is True:
                        return (
                         info[1], info[0], cid)

        raise ProgrammingError("Character set '%s' unsupported." % charset)

    @classmethod
    def get_charset_info(cls, charset=None, collation=None):
        """Get character set information using charset name and/or collation

        Retrieves character set and collation information given character
        set name and/or a collation name.
        If charset is an integer, it will look up the character set based
        on the MySQL's ID.
        For example:
            get_charset_info('utf8',None)
            get_charset_info(collation='utf8_general_ci')
            get_charset_info(47)

        Raises ProgrammingError when character set is not supported.

        Returns a tuple with (id, characterset name, collation)
        """
        if isinstance(charset, int):
            try:
                info = cls.desc[charset]
                return (charset, info[0], info[1])
            except IndexError:
                ProgrammingError('Character set ID {0} unknown.'.format(charset))

            if charset is not None:
                if collation is None:
                    info = cls.get_default_collation(charset)
                    return (info[2], info[1], info[0])
        elif charset is None and collation is not None:
            for cid, info in enumerate(cls.desc):
                if info is None:
                    pass
                else:
                    if collation == info[1]:
                        return (
                         cid, info[0], info[1])

            raise ProgrammingError("Collation '{0}' unknown.".format(collation))
        else:
            for cid, info in enumerate(cls.desc):
                if info is None:
                    pass
                else:
                    if info[0] == charset:
                        if info[1] == collation:
                            return (
                             cid, info[0], info[1])

            raise ProgrammingError("Character set '{0}' unknown.".format(charset))

    @classmethod
    def get_supported(cls):
        """Retrieves a list with names of all supproted character sets

        Returns a tuple.
        """
        res = []
        for info in cls.desc:
            if info and info[0] not in res:
                res.append(info[0])

        return tuple(res)


class SQLMode(_Constants):
    __doc__ = 'MySQL SQL Modes\n\n    The numeric values of SQL Modes are not interesting, only the names\n    are used when setting the SQL_MODE system variable using the MySQL\n    SET command.\n\n    See http://dev.mysql.com/doc/refman/5.6/en/server-sql-mode.html\n    '
    _prefix = 'MODE_'
    REAL_AS_FLOAT = 'REAL_AS_FLOAT'
    PIPES_AS_CONCAT = 'PIPES_AS_CONCAT'
    ANSI_QUOTES = 'ANSI_QUOTES'
    IGNORE_SPACE = 'IGNORE_SPACE'
    NOT_USED = 'NOT_USED'
    ONLY_FULL_GROUP_BY = 'ONLY_FULL_GROUP_BY'
    NO_UNSIGNED_SUBTRACTION = 'NO_UNSIGNED_SUBTRACTION'
    NO_DIR_IN_CREATE = 'NO_DIR_IN_CREATE'
    POSTGRESQL = 'POSTGRESQL'
    ORACLE = 'ORACLE'
    MSSQL = 'MSSQL'
    DB2 = 'DB2'
    MAXDB = 'MAXDB'
    NO_KEY_OPTIONS = 'NO_KEY_OPTIONS'
    NO_TABLE_OPTIONS = 'NO_TABLE_OPTIONS'
    NO_FIELD_OPTIONS = 'NO_FIELD_OPTIONS'
    MYSQL323 = 'MYSQL323'
    MYSQL40 = 'MYSQL40'
    ANSI = 'ANSI'
    NO_AUTO_VALUE_ON_ZERO = 'NO_AUTO_VALUE_ON_ZERO'
    NO_BACKSLASH_ESCAPES = 'NO_BACKSLASH_ESCAPES'
    STRICT_TRANS_TABLES = 'STRICT_TRANS_TABLES'
    STRICT_ALL_TABLES = 'STRICT_ALL_TABLES'
    NO_ZERO_IN_DATE = 'NO_ZERO_IN_DATE'
    NO_ZERO_DATE = 'NO_ZERO_DATE'
    INVALID_DATES = 'INVALID_DATES'
    ERROR_FOR_DIVISION_BY_ZERO = 'ERROR_FOR_DIVISION_BY_ZERO'
    TRADITIONAL = 'TRADITIONAL'
    NO_AUTO_CREATE_USER = 'NO_AUTO_CREATE_USER'
    HIGH_NOT_PRECEDENCE = 'HIGH_NOT_PRECEDENCE'
    NO_ENGINE_SUBSTITUTION = 'NO_ENGINE_SUBSTITUTION'
    PAD_CHAR_TO_FULL_LENGTH = 'PAD_CHAR_TO_FULL_LENGTH'

    @classmethod
    def get_desc(cls, name):
        raise NotImplementedError

    @classmethod
    def get_info(cls, number):
        raise NotImplementedError

    @classmethod
    def get_full_info(cls):
        """Returns a sequence of all available SQL Modes

        This class method returns a tuple containing all SQL Mode names. The
        names will be alphabetically sorted.

        Returns a tuple.
        """
        res = []
        for key in vars(cls).keys():
            if not key.startswith('_') and not hasattr(getattr(cls, key), '__call__'):
                res.append(key)

        return tuple(sorted(res))
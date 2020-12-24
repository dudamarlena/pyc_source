# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/hs2client/hs2client.py
# Compiled at: 2018-05-31 09:48:43
import logging, sys
from .genthrift.TCLIService import TCLIService
from .genthrift.TCLIService import constants
from .genthrift.TCLIService import ttypes
from .commons import DBAPICursor, ParamEscaper
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket
from thrift.transport import TTransport
from future.utils import iteritems
DEFAULT_PORT = 10000
_logger = logging.getLogger(__name__)

def _check_status(response):
    """Raise an OperationalError if the status is not success"""
    _logger.debug(response)
    if response.status.statusCode != ttypes.TStatusCode.SUCCESS_STATUS:
        raise ValueError(response)


class HiveParamEscaper(ParamEscaper):

    def escape_string(self, item):
        if isinstance(item, bytes):
            item = item.decode('utf-8')
        return ("'{}'").format(item.replace('\\', '\\\\').replace("'", "\\'").replace('\r', '\\r').replace('\n', '\\n').replace('\t', '\\t'))


_escaper = HiveParamEscaper()

class HS2Client(TCLIService.Client):
    __client = None
    __isOpened = False

    def __init__(self, host=None, port=None, username=None, database='default', auth=None, configuration=None, kerberos_service_name=None, password=None, thrift_transport=None):
        self.logger = logging.getLogger(__name__)
        configuration = configuration or {}
        if (password is not None) != (auth in ('LDAP', 'CUSTOM')):
            raise ValueError('Password should be set if and only if in LDAP or CUSTOM mode; Remove password or use one of those modes')
        if (kerberos_service_name is not None) != (auth == 'KERBEROS'):
            raise ValueError('kerberos_service_name should be set if and only if in KERBEROS mode')
        if thrift_transport is not None:
            has_incompatible_arg = host is not None or port is not None or auth is not None or kerberos_service_name is not None or password is not None
            if has_incompatible_arg:
                raise ValueError('thrift_transport cannot be used with host/port/auth/kerberos_service_name/password')
        if thrift_transport is not None:
            self._transport = thrift_transport
        else:
            port = port or 10000
            auth = auth or 'NONE'
            socket = TSocket.TSocket(host, port)
            if auth == 'NOSASL':
                self._transport = TTransport.TBufferedTransport(socket)
            elif auth in ('LDAP', 'KERBEROS', 'NONE', 'CUSTOM'):
                import sasl, thrift_sasl
                if auth == 'KERBEROS':
                    sasl_auth = 'GSSAPI'
                else:
                    sasl_auth = 'PLAIN'
                    if password is None:
                        password = 'x'
                    if username is None:
                        username = 'mr.who'

                def sasl_factory():
                    sasl_client = sasl.Client()
                    sasl_client.setAttr('host', host)
                    if sasl_auth == 'GSSAPI':
                        sasl_client.setAttr('service', kerberos_service_name)
                    elif sasl_auth == 'PLAIN':
                        sasl_client.setAttr('username', username)
                        sasl_client.setAttr('password', password)
                    else:
                        raise AssertionError
                    sasl_client.init()
                    return sasl_client

                self._transport = thrift_sasl.TSaslClientTransport(sasl_factory, sasl_auth, socket)
            else:
                raise NotImplementedError(('Only NONE, NOSASL, LDAP, KERBEROS, CUSTOM authentication are supported, got {}').format(auth))
            protocol = TBinaryProtocol.TBinaryProtocol(self._transport)
            super(HS2Client, self).__init__(protocol)
            protocol_version = ttypes.TProtocolVersion.HIVE_CLI_SERVICE_PROTOCOL_V6
            try:
                self._oprot.trans.open()
                self.__isOpened = True
                open_session_req = ttypes.TOpenSessionReq(client_protocol=protocol_version, configuration=configuration, username=username)
                response = self.OpenSession(open_session_req)
                _check_status(response)
                assert response.sessionHandle is not None, 'Expected a session from OpenSession'
                self._sessionHandle = response.sessionHandle
                assert response.serverProtocolVersion == protocol_version, ('Unable to handle protocol version {}').format(response.serverProtocolVersion)
                with self.cursor() as (cursor):
                    cursor.execute(('USE `{}`').format(database))
            except:
                self._oprot.trans.close()
                raise

        return

    def open(self):
        return self

    def __enter__(self):
        return self.open()

    def close(self):
        self._oprot.trans.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def cursor(self, *args, **kwargs):
        """Return a new :py:class:`Cursor` object using the connection."""
        return Cursor(self, *args, **kwargs)


class Cursor(DBAPICursor):
    """These objects represent a database cursor, which is used to manage the context of a fetch
    operation.
    Cursors are not isolated, i.e., any changes done to the database by a cursor are immediately
    visible by other cursors or connections.
    """

    def __init__(self, connection, arraysize=1000):
        self._operationHandle = None
        super(Cursor, self).__init__()
        self.arraysize = arraysize
        self._connection = connection
        return

    def _reset_state(self):
        """Reset state about the previous query in preparation for running another query"""
        super(Cursor, self)._reset_state()
        self._description = None
        if self._operationHandle is not None:
            request = ttypes.TCloseOperationReq(self._operationHandle)
            try:
                response = self._connection.CloseOperation(request)
                _check_status(response)
            finally:
                self._operationHandle = None

        return

    @property
    def description(self):
        """This read-only attribute is a sequence of 7-item sequences.
        Each of these sequences contains information describing one result column:
        - name
        - type_code
        - display_size (None in current implementation)
        - internal_size (None in current implementation)
        - precision (None in current implementation)
        - scale (None in current implementation)
        - null_ok (always True in current implementation)
        This attribute will be ``None`` for operations that do not return rows or if the cursor has
        not had an operation invoked via the :py:meth:`execute` method yet.
        The ``type_code`` can be interpreted by comparing it to the Type Objects specified in the
        section below.
        """
        if self._operationHandle is None or not self._operationHandle.hasResultSet:
            return
        if self._description is None:
            req = ttypes.TGetResultSetMetadataReq(self._operationHandle)
            response = self._connection.GetResultSetMetadata(req)
            _check_status(response)
            columns = response.schema.columns
            self._description = []
            for col in columns:
                primary_type_entry = col.typeDesc.types[0]
                if primary_type_entry.primitiveEntry is None:
                    type_code = ttypes.TTypeId._VALUES_TO_NAMES[ttypes.TTypeId.STRING_TYPE]
                else:
                    type_id = primary_type_entry.primitiveEntry.type
                    type_code = ttypes.TTypeId._VALUES_TO_NAMES[type_id]
                self._description.append((
                 col.columnName.decode('utf-8') if sys.version_info[0] == 2 else col.columnName,
                 type_code.decode('utf-8') if sys.version_info[0] == 2 else type_code,
                 None, None, None, None, True))

        return self._description

    def open(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the operation handle"""
        self._reset_state()

    def execute(self, operation, parameters=None, async=False):
        """Prepare and execute a database operation (query or command).
        Return values are not defined.
        """
        if parameters is None:
            sql = operation
        else:
            sql = operation % _escaper.escape_args(parameters)
        self._reset_state()
        self._state = self._STATE_RUNNING
        _logger.info('%s', sql)
        req = ttypes.TExecuteStatementReq(self._connection._sessionHandle, sql, runAsync=async)
        _logger.debug(req)
        response = self._connection.ExecuteStatement(req)
        _check_status(response)
        self._operationHandle = response.operationHandle
        return

    def cancel(self):
        req = ttypes.TCancelOperationReq(operationHandle=self._operationHandle)
        response = self._connection.CancelOperation(req)
        _check_status(response)

    def _fetch_more(self):
        """Send another TFetchResultsReq and update state"""
        if not self._state == self._STATE_RUNNING:
            raise AssertionError('Should be running when in _fetch_more')
            if not self._operationHandle is not None:
                raise AssertionError('Should have an op handle in _fetch_more')
                raise (self._operationHandle.hasResultSet or ValueError)('No result set')
            req = ttypes.TFetchResultsReq(operationHandle=self._operationHandle, orientation=ttypes.TFetchOrientation.FETCH_NEXT, maxRows=self.arraysize)
            response = self._connection.FetchResults(req)
            _check_status(response)
            assert not response.results.rows, 'expected data in columnar format'
            columns = map(_unwrap_column, response.results.columns)
            new_data = list(zip(*columns))
            self._data += new_data
            self._state = new_data or self._STATE_FINISHED
        return

    def poll(self, get_progress_update=True):
        """Poll for and return the raw status data provided by the Hive Thrift REST API.
        :returns: ``ttypes.TGetOperationStatusResp``
        :raises: ``ProgrammingError`` when no query has been started
        .. note::
            This is not a part of DB-API.
        """
        if self._state == self._STATE_NONE:
            raise ValueError('No query yet')
        req = ttypes.TGetOperationStatusReq(operationHandle=self._operationHandle, getProgressUpdate=get_progress_update)
        response = self._connection.GetOperationStatus(req)
        _check_status(response)
        return response

    def fetch_logs(self):
        """Retrieve the logs produced by the execution of the query.
        Can be called multiple times to fetch the logs produced after the previous call.
        :returns: list<str>
        :raises: ``ProgrammingError`` when no query has been started
        .. note::
            This is not a part of DB-API.
        """
        if self._state == self._STATE_NONE:
            raise ValueError('No query yet')
        try:
            req = ttypes.TGetLogReq(operationHandle=self._operationHandle)
            logs = self._connection.GetLog(req).log.splitlines()
        except ttypes.TApplicationException as e:
            if e.type != ttypes.TApplicationException.UNKNOWN_METHOD:
                raise
            logs = []
            while True:
                req = ttypes.TFetchResultsReq(operationHandle=self._operationHandle, orientation=ttypes.TFetchOrientation.FETCH_NEXT, maxRows=self.arraysize, fetchType=1)
                response = self._connection.FetchResults(req)
                _check_status(response)
                assert not response.results.rows, 'expected data in columnar format'
                assert len(response.results.columns) == 1, response.results.columns
                new_logs = _unwrap_column(response.results.columns[0])
                logs += new_logs
                if not new_logs:
                    break

        return logs


def _unwrap_column(col):
    """Return a list of raw values from a TColumn instance."""
    for attr, wrapper in iteritems(col.__dict__):
        if wrapper is not None:
            result = wrapper.values
            nulls = wrapper.nulls
            if not isinstance(nulls, bytes):
                raise AssertionError
                for i, char in enumerate(nulls):
                    byte = ord(char) if sys.version_info[0] == 2 else char
                    for b in range(8):
                        if byte & 1 << b:
                            result[i * 8 + b] = None

                return result

    raise ValueError(('Got empty column value {}').format(col))
    return
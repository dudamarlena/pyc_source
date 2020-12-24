# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Work\jep\src\jep-python\build\lib\test\test_frontend.py
# Compiled at: 2016-01-04 11:09:11
# Size of source mod 2**32: 36746 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from os import path
import queue
from unittest import mock
import datetime, itertools, pytest
from jep_py.config import TIMEOUT_LAST_MESSAGE
from jep_py.frontend import Frontend, State, BackendConnection, TIMEOUT_BACKEND_STARTUP, TIMEOUT_BACKEND_SHUTDOWN
from jep_py.schema import Shutdown, BackendAlive, CompletionResponse, CompletionRequest
from test.logconfig import configure_test_logger

def setup_function(function):
    configure_test_logger()
    os.chdir(os.path.join(os.path.dirname(__file__), 'input'))


def test_provide_connection_unhandled_file():
    frontend = Frontend()
    @py_assert1 = frontend.get_connection
    @py_assert3 = 'some.unknown'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = ('' + 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get_connection\n}(%(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(frontend) if 'frontend' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frontend) else 'frontend', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_provide_connection_first_time():
    mock_service_config = mock.MagicMock()
    mock_service_config.selector = mock.sentinel.CONFIG_SELECTOR
    mock_service_config_provider = mock.MagicMock()
    mock_service_config_provider.provide_for = mock.MagicMock(return_value=mock_service_config)
    mock_connection = mock.MagicMock()
    mock_provide_backend_connection = mock.MagicMock(return_value=mock_connection)
    frontend = Frontend(mock.sentinel.LISTENERS, service_config_provider=mock_service_config_provider, provide_backend_connection=mock_provide_backend_connection)
    connection = frontend.get_connection(mock.sentinel.FILE_NAME)
    mock_service_config_provider.provide_for.assert_called_once_with(mock.sentinel.FILE_NAME)
    mock_provide_backend_connection.assert_called_once_with(frontend, mock_service_config, mock.sentinel.LISTENERS)
    @py_assert1 = mock_connection.connect
    @py_assert3 = @py_assert1.call_count
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.connect\n}.call_count\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(mock_connection) if 'mock_connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_connection) else 'mock_connection', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = mock_connection.disconnect
    @py_assert3 = @py_assert1.called
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.disconnect\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_connection) if 'mock_connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_connection) else 'mock_connection', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = connection is mock_connection
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (connection, mock_connection)) % {'py2': @pytest_ar._saferepr(mock_connection) if 'mock_connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_connection) else 'mock_connection', 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_provide_connected_connection_second_time_with_matching_selector_and_matching_checksum():
    mock_service_config = mock.MagicMock()
    mock_service_config.selector = mock.sentinel.CONFIG_SELECTOR
    mock_service_config_provider = mock.MagicMock()
    mock_service_config_provider.provide_for = mock.MagicMock(return_value=mock_service_config)
    mock_service_config_provider.checksum = mock.MagicMock(return_value=mock.sentinel.CONFIG_CHECKSUM)
    mock_connection = mock.MagicMock()
    mock_connection.service_config.checksum = mock.sentinel.CONFIG_CHECKSUM
    mock_provide_backend_connection = mock.MagicMock(return_value=mock_connection)
    frontend = Frontend(mock.sentinel.LISTENERS, service_config_provider=mock_service_config_provider, provide_backend_connection=mock_provide_backend_connection)
    connection1 = frontend.get_connection(mock.sentinel.FILE_NAME1)
    @py_assert1 = mock_connection.connect
    @py_assert3 = @py_assert1.called
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.connect\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_connection) if 'mock_connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_connection) else 'mock_connection', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    mock_connection.connect.reset_mock()
    mock_connection.state = State.Connected
    connection2 = frontend.get_connection(mock.sentinel.FILE_NAME2)
    @py_assert1 = connection1 is connection2
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (connection1, connection2)) % {'py2': @pytest_ar._saferepr(connection2) if 'connection2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection2) else 'connection2', 'py0': @pytest_ar._saferepr(connection1) if 'connection1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection1) else 'connection1'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = mock_connection.connect
    @py_assert3 = @py_assert1.called
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.connect\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_connection) if 'mock_connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_connection) else 'mock_connection', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = mock_connection.disconnect
    @py_assert3 = @py_assert1.called
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.disconnect\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_connection) if 'mock_connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_connection) else 'mock_connection', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = [mock.call.provide_for(mock.sentinel.FILE_NAME1), mock.call.provide_for(mock.sentinel.FILE_NAME2)]
    @py_assert4 = mock_service_config_provider.method_calls
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.method_calls\n}', ), (@py_assert0, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(mock_service_config_provider) if 'mock_service_config_provider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_service_config_provider) else 'mock_service_config_provider'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert1 = mock_provide_backend_connection.call_count
    @py_assert4 = 1
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call_count\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_provide_backend_connection) if 'mock_provide_backend_connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_provide_backend_connection) else 'mock_provide_backend_connection'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_provide_disconnected_connection_second_time_with_matching_selector_and_matching_checksum():
    mock_service_config = mock.MagicMock()
    mock_service_config.selector = mock.sentinel.CONFIG_SELECTOR
    mock_service_config_provider = mock.MagicMock()
    mock_service_config_provider.provide_for = mock.MagicMock(return_value=mock_service_config)
    mock_service_config_provider.checksum = mock.MagicMock(return_value=mock.sentinel.CONFIG_CHECKSUM)
    mock_connection = mock.MagicMock()
    mock_connection.service_config.checksum = mock.sentinel.CONFIG_CHECKSUM
    mock_provide_backend_connection = mock.MagicMock(return_value=mock_connection)
    frontend = Frontend(mock.sentinel.LISTENERS, service_config_provider=mock_service_config_provider, provide_backend_connection=mock_provide_backend_connection)
    connection1 = frontend.get_connection(mock.sentinel.FILE_NAME1)
    @py_assert1 = mock_connection.connect
    @py_assert3 = @py_assert1.called
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.connect\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_connection) if 'mock_connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_connection) else 'mock_connection', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    mock_connection.connect.reset_mock()
    mock_connection.state = State.Disconnected
    connection2 = frontend.get_connection(mock.sentinel.FILE_NAME2)
    @py_assert1 = connection1 is connection2
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (connection1, connection2)) % {'py2': @pytest_ar._saferepr(connection2) if 'connection2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection2) else 'connection2', 'py0': @pytest_ar._saferepr(connection1) if 'connection1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection1) else 'connection1'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = mock_connection.connect
    @py_assert3 = @py_assert1.called
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.connect\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_connection) if 'mock_connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_connection) else 'mock_connection', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = mock_connection.disconnect
    @py_assert3 = @py_assert1.called
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.disconnect\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_connection) if 'mock_connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_connection) else 'mock_connection', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_provide_connection_second_time_with_matching_selector_and_new_checksum():
    mock_service_config = mock.MagicMock()
    mock_service_config.selector = mock.sentinel.CONFIG_SELECTOR
    mock_service_config_provider = mock.MagicMock()
    mock_service_config_provider.provide_for = mock.MagicMock(return_value=mock_service_config)
    mock_service_config_provider.checksum = mock.MagicMock(return_value=mock.sentinel.CONFIG_CHECKSUM)
    mock_connection = mock.MagicMock()
    mock_connection.service_config.checksum = mock.sentinel.CONFIG_CHECKSUM
    mock_provide_backend_connection = mock.MagicMock(return_value=mock_connection)
    frontend = Frontend(mock.sentinel.LISTENERS, service_config_provider=mock_service_config_provider, provide_backend_connection=mock_provide_backend_connection)
    connection1 = frontend.get_connection(mock.sentinel.FILE_NAME1)
    @py_assert1 = mock_connection.connect
    @py_assert3 = @py_assert1.called
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.connect\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_connection) if 'mock_connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_connection) else 'mock_connection', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    mock_connection.reset_mock()
    mock_service_config2 = mock.MagicMock()
    mock_service_config2.selector = mock.sentinel.CONFIG_SELECTOR
    mock_service_config_provider.provide_for.return_value = mock_service_config2
    mock_service_config_provider.checksum.return_value = mock.sentinel.CONFIG_CHECKSUM2
    connection2 = frontend.get_connection(mock.sentinel.FILE_NAME2)
    @py_assert1 = connection1 is connection2
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (connection1, connection2)) % {'py2': @pytest_ar._saferepr(connection2) if 'connection2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection2) else 'connection2', 'py0': @pytest_ar._saferepr(connection1) if 'connection1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection1) else 'connection1'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = mock_connection.reconnect
    @py_assert3 = @py_assert1.called
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.reconnect\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_connection) if 'mock_connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_connection) else 'mock_connection', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    mock_connection.reconnect.assert_called_once_with(mock_service_config2)
    @py_assert1 = mock_provide_backend_connection.call_count
    @py_assert4 = 1
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call_count\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_provide_backend_connection) if 'mock_provide_backend_connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_provide_backend_connection) else 'mock_provide_backend_connection'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_provide_connection_second_time_with_other_selector():
    mock_service_config = mock.MagicMock()
    mock_service_config.selector = mock.sentinel.CONFIG_SELECTOR
    mock_service_config_provider = mock.MagicMock()
    mock_service_config_provider.provide_for = mock.MagicMock(return_value=mock_service_config)
    mock_connection = mock.MagicMock()
    mock_provide_backend_connection = mock.MagicMock(return_value=mock_connection)
    frontend = Frontend(mock.sentinel.LISTENERS, service_config_provider=mock_service_config_provider, provide_backend_connection=mock_provide_backend_connection)
    frontend.get_connection(mock.sentinel.FILE_NAME1)
    @py_assert1 = mock_connection.connect
    @py_assert3 = @py_assert1.called
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.connect\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_connection) if 'mock_connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_connection) else 'mock_connection', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    mock_connection.connect.reset_mock()
    mock_service_config.selector = mock.sentinel.CONFIG_SELECTOR2
    frontend.get_connection(mock.sentinel.FILE_NAME2)
    @py_assert1 = mock_provide_backend_connection.call_count
    @py_assert4 = 2
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call_count\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_provide_backend_connection) if 'mock_provide_backend_connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_provide_backend_connection) else 'mock_provide_backend_connection'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_backend_connection_initial_state():
    connection = BackendConnection(mock.sentinel.FRONTEND, mock.sentinel.SERVICE_CONFIG, mock.sentinel.LISTENERS)
    @py_assert1 = connection.state
    @py_assert5 = State.Disconnected
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Disconnected\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_backend_connection_send_message_ok():
    mock_serializer = mock.MagicMock()
    mock_serializer.serialize = mock.MagicMock(return_value=mock.sentinel.SERIALIZED)
    mock_socket = mock.MagicMock()
    mock_socket.send = mock.MagicMock()
    connection = BackendConnection(mock.sentinel.FRONTEND, mock.sentinel.SERVICE_CONFIG, [], serializer=mock_serializer)
    connection._socket = mock_socket
    connection.state = State.Connected
    connection.send_message(mock.sentinel.MESSAGE)
    mock_serializer.serialize.assert_called_once_with(mock.sentinel.MESSAGE)
    mock_socket.send.assert_called_once_with(mock.sentinel.SERIALIZED)


def test_backend_connection_send_message_wrong_state():
    mock_serializer = mock.MagicMock()
    mock_serializer.serialize = mock.MagicMock(return_value=mock.sentinel.SERIALIZED)
    mock_socket = mock.MagicMock()
    mock_socket.send = mock.MagicMock()
    connection = BackendConnection(mock.sentinel.FRONTEND, mock.sentinel.SERVICE_CONFIG, [], serializer=mock_serializer)
    connection._socket = mock_socket
    for state in {State.Disconnected, State.Connecting, State.Disconnecting}:
        connection.state = state
        connection.send_message(mock.sentinel.MESSAGE)
        @py_assert1 = mock_serializer.serialize
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.serialize\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_serializer) if 'mock_serializer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_serializer) else 'mock_serializer', 'py4': @pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = mock_socket.send
        @py_assert3 = @py_assert1.called
        @py_assert5 = not @py_assert3
        if not @py_assert5:
            @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.send\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_socket) if 'mock_socket' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_socket) else 'mock_socket', 'py4': @pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert3 = @py_assert5 = None


def test_backend_connection_send_message_serialization_failed():
    mock_serializer = mock.MagicMock()
    mock_serializer.serialize = mock.MagicMock(side_effect=NotImplementedError)
    mock_socket = mock.MagicMock()
    mock_socket.send = mock.MagicMock()
    connection = BackendConnection(mock.sentinel.FRONTEND, mock.sentinel.SERVICE_CONFIG, [], serializer=mock_serializer)
    connection._socket = mock_socket
    connection.state = State.Connected
    connection.send_message(mock.sentinel.MESSAGE)
    @py_assert1 = mock_socket.send
    @py_assert3 = @py_assert1.called
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.send\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_socket) if 'mock_socket' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_socket) else 'mock_socket', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_backend_connection_send_message_send_failed():
    mock_serializer = mock.MagicMock()
    mock_serializer.serialize = mock.MagicMock(return_value=mock.sentinel.SERIALIZED)
    mock_socket = mock.MagicMock()
    mock_socket.send = mock.MagicMock(NotImplementedError)
    connection = BackendConnection(mock.sentinel.FRONTEND, mock.sentinel.SERVICE_CONFIG, [], serializer=mock_serializer)
    connection._socket = mock_socket
    connection.state = State.Connected
    connection.send_message(mock.sentinel.MESSAGE)


def prepare_connecting_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module, now):
    mock_service_config = mock.MagicMock()
    mock_service_config.command = 'folder/somecommand.ext someparameter somethingelse'
    mock_service_config.config_file_path = path.abspath('somedir/.jep')
    mock_async_reader = mock.MagicMock()
    mock_async_reader.queue_ = queue.Queue()
    mock_provide_async_reader = mock.MagicMock(return_value=mock_async_reader)
    mock_process = mock.MagicMock()
    mock_datetime_module.datetime.now = mock.MagicMock(return_value=now)
    mock_socket_module.create_connection = mock.MagicMock()
    mock_subprocess_module.Popen = mock.MagicMock(return_value=mock_process)
    return (mock_async_reader, mock_process, mock_provide_async_reader, mock_service_config)


def decorate_connection_state_dispatch(connection, delay_sec, mock_datetime_module):
    """Each dispatch of connector state takes delay_sec seconds of virtual time."""
    original_dispatch = connection._dispatch

    def _dispatch(*args):
        now = mock_datetime_module.datetime.now.return_value
        original_dispatch(*args)
        mock_datetime_module.datetime.now.return_value = now + datetime.timedelta(seconds=delay_sec)

    connection._dispatch = _dispatch


@mock.patch('jep_py.frontend.subprocess')
@mock.patch('jep_py.frontend.socket')
@mock.patch('jep_py.frontend.datetime')
@mock.patch('jep_py.frontend.os')
def test_backend_connection_connect(mock_os_module, mock_datetime_module, mock_socket_module, mock_subprocess_module):
    now = datetime.datetime.now()
    mock_async_reader, mock_process, mock_provide_async_reader, mock_service_config = prepare_connecting_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module, now)
    mock_os_module.path = path
    mock_listener = mock.MagicMock()
    connection = BackendConnection(mock.sentinel.FRONTEND, mock_service_config, [mock_listener], serializer=mock.sentinel.SERIALIZER, provide_async_reader=mock_provide_async_reader)
    connection.connect()
    @py_assert0 = mock_subprocess_module.Popen.call_args[0][0][0]
    @py_assert3 = 'folder/somecommand.ext'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = mock_subprocess_module.Popen.call_args[1]['cwd']
    @py_assert4 = path.abspath
    @py_assert6 = 'somedir'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert2 = @py_assert0 == @py_assert8
    if not @py_assert2:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.abspath\n}(%(py7)s)\n}', ), (@py_assert0, @py_assert8)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py9': @pytest_ar._saferepr(@py_assert8), 'py3': @pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert1 = mock_async_reader.start
    @py_assert3 = @py_assert1.call_count
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.start\n}.call_count\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(mock_async_reader) if 'mock_async_reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_async_reader) else 'mock_async_reader', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = connection.state
    @py_assert5 = State.Connecting
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Connecting\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = connection._process
    @py_assert3 = @py_assert1 is mock_process
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s._process\n} is %(py4)s', ), (@py_assert1, mock_process)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(mock_process) if 'mock_process' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_process) else 'mock_process'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    mock_subprocess_module.Popen.reset_mock()
    mock_provide_async_reader.reset_mock()
    connection.connect()
    @py_assert1 = mock_subprocess_module.Popen
    @py_assert3 = @py_assert1.called
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.Popen\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_subprocess_module) if 'mock_subprocess_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_subprocess_module) else 'mock_subprocess_module', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = mock_provide_async_reader.called
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_provide_async_reader) if 'mock_provide_async_reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_provide_async_reader) else 'mock_provide_async_reader'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = connection._process
    @py_assert3 = @py_assert1 is mock_process
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s._process\n} is %(py4)s', ), (@py_assert1, mock_process)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(mock_process) if 'mock_process' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_process) else 'mock_process'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    mock_async_reader.queue_.put('Nothing special to say.')
    mock_async_reader.queue_.put('This is the JEP service, listening on port 4711. Yes really!')
    decorate_connection_state_dispatch(connection, 0.6, mock_datetime_module)
    connection.run(datetime.timedelta(seconds=0.5))
    @py_assert1 = mock_socket_module.create_connection
    @py_assert3 = @py_assert1.called
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.create_connection\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_socket_module) if 'mock_socket_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_socket_module) else 'mock_socket_module', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = mock_socket_module.create_connection.call_args[0][0]
    @py_assert3 = ('localhost', 4711)
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert1 = connection.state
    @py_assert5 = State.Connected
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Connected\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    mock_listener.on_connection_state_changed.assert_has_calls([mock.call(State.Disconnected, State.Connecting, connection),
     mock.call(State.Connecting, State.Connected, connection)])


@mock.patch('jep_py.frontend.subprocess')
@mock.patch('jep_py.frontend.socket')
@mock.patch('jep_py.frontend.datetime')
@mock.patch('jep_py.frontend.os')
def test_backend_connection_connect_no_port_announcement(mock_os_module, mock_datetime_module, mock_socket_module, mock_subprocess_module):
    now = datetime.datetime.now()
    mock_async_reader, mock_process, mock_provide_async_reader, mock_service_config = prepare_connecting_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module, now)
    connection = BackendConnection(mock.sentinel.FRONTEND, mock_service_config, [], serializer=mock.sentinel.SERIALIZER, provide_async_reader=mock_provide_async_reader)
    connection.connect()
    mock_async_reader.queue_.put('Nothing special to say.')
    mock_async_reader.queue_.put('No port announcement whatsoever.')
    @py_assert3 = datetime.timedelta
    @py_assert5 = 0
    @py_assert7 = @py_assert3(seconds=@py_assert5)
    @py_assert1 = TIMEOUT_BACKEND_STARTUP > @py_assert7
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('>', ), (@py_assert1,), ('%(py0)s > %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.timedelta\n}(seconds=%(py6)s)\n}', ), (TIMEOUT_BACKEND_STARTUP, @py_assert7)) % {'py2': @pytest_ar._saferepr(datetime) if 'datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime) else 'datetime', 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(TIMEOUT_BACKEND_STARTUP) if 'TIMEOUT_BACKEND_STARTUP' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TIMEOUT_BACKEND_STARTUP) else 'TIMEOUT_BACKEND_STARTUP', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    decorate_connection_state_dispatch(connection, 1, mock_datetime_module)
    connection.run(TIMEOUT_BACKEND_STARTUP)
    @py_assert1 = connection.state
    @py_assert5 = State.Connecting
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Connecting\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    connection.run(datetime.timedelta(seconds=2))
    @py_assert1 = connection.state
    @py_assert5 = State.Disconnected
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Disconnected\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = mock_process.kill
    @py_assert3 = @py_assert1.call_count
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.kill\n}.call_count\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(mock_process) if 'mock_process' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_process) else 'mock_process', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = mock_async_reader.join
    @py_assert3 = @py_assert1.call_count
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}.call_count\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(mock_async_reader) if 'mock_async_reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_async_reader) else 'mock_async_reader', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = connection._process
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s._process\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = connection._process_output_reader
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s._process_output_reader\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None


@mock.patch('jep_py.frontend.subprocess')
@mock.patch('jep_py.frontend.socket')
@mock.patch('jep_py.frontend.datetime')
@mock.patch('jep_py.frontend.os')
def test_backend_connection_connect_connection_none(mock_os_module, mock_datetime_module, mock_socket_module, mock_subprocess_module):
    now = datetime.datetime.now()
    mock_async_reader, mock_process, mock_provide_async_reader, mock_service_config = prepare_connecting_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module, now)
    connection = BackendConnection(mock.sentinel.FRONTEND, mock_service_config, [], serializer=mock.sentinel.SERIALIZER, provide_async_reader=mock_provide_async_reader)
    connection.connect()
    mock_async_reader.queue_.put('This is the JEP service, listening on port 4711.')
    @py_assert3 = datetime.timedelta
    @py_assert5 = 0
    @py_assert7 = @py_assert3(seconds=@py_assert5)
    @py_assert1 = TIMEOUT_BACKEND_STARTUP > @py_assert7
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('>', ), (@py_assert1,), ('%(py0)s > %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.timedelta\n}(seconds=%(py6)s)\n}', ), (TIMEOUT_BACKEND_STARTUP, @py_assert7)) % {'py2': @pytest_ar._saferepr(datetime) if 'datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime) else 'datetime', 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(TIMEOUT_BACKEND_STARTUP) if 'TIMEOUT_BACKEND_STARTUP' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TIMEOUT_BACKEND_STARTUP) else 'TIMEOUT_BACKEND_STARTUP', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    decorate_connection_state_dispatch(connection, 1, mock_datetime_module)
    mock_socket_module.create_connection = mock.MagicMock(return_value=None)
    connection.run(datetime.timedelta(seconds=2))
    @py_assert1 = connection.state
    @py_assert5 = State.Disconnected
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Disconnected\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = mock_process.kill
    @py_assert3 = @py_assert1.call_count
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.kill\n}.call_count\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(mock_process) if 'mock_process' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_process) else 'mock_process', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = mock_async_reader.join
    @py_assert3 = @py_assert1.call_count
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}.call_count\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(mock_async_reader) if 'mock_async_reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_async_reader) else 'mock_async_reader', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = connection._process
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s._process\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = connection._process_output_reader
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s._process_output_reader\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None


@mock.patch('jep_py.frontend.subprocess')
@mock.patch('jep_py.frontend.socket')
@mock.patch('jep_py.frontend.datetime')
@mock.patch('jep_py.frontend.os')
def test_backend_connection_connect_connection_exception(mock_os_module, mock_datetime_module, mock_socket_module, mock_subprocess_module):
    now = datetime.datetime.now()
    mock_async_reader, mock_process, mock_provide_async_reader, mock_service_config = prepare_connecting_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module, now)
    connection = BackendConnection(mock.sentinel.FRONTEND, mock_service_config, [], serializer=mock.sentinel.SERIALIZER, provide_async_reader=mock_provide_async_reader)
    connection.connect()
    mock_async_reader.queue_.put('This is the JEP service, listening on port 4711.')
    @py_assert3 = datetime.timedelta
    @py_assert5 = 0
    @py_assert7 = @py_assert3(seconds=@py_assert5)
    @py_assert1 = TIMEOUT_BACKEND_STARTUP > @py_assert7
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('>', ), (@py_assert1,), ('%(py0)s > %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.timedelta\n}(seconds=%(py6)s)\n}', ), (TIMEOUT_BACKEND_STARTUP, @py_assert7)) % {'py2': @pytest_ar._saferepr(datetime) if 'datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime) else 'datetime', 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(TIMEOUT_BACKEND_STARTUP) if 'TIMEOUT_BACKEND_STARTUP' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TIMEOUT_BACKEND_STARTUP) else 'TIMEOUT_BACKEND_STARTUP', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    decorate_connection_state_dispatch(connection, 1, mock_datetime_module)
    mock_socket_module.create_connection = mock.MagicMock(side_effect=NotImplementedError)
    connection.run(datetime.timedelta(seconds=2))
    @py_assert1 = connection.state
    @py_assert5 = State.Disconnected
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Disconnected\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = mock_process.kill
    @py_assert3 = @py_assert1.call_count
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.kill\n}.call_count\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(mock_process) if 'mock_process' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_process) else 'mock_process', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = mock_async_reader.join
    @py_assert3 = @py_assert1.call_count
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}.call_count\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(mock_async_reader) if 'mock_async_reader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_async_reader) else 'mock_async_reader', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = connection._process
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s._process\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = connection._process_output_reader
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s._process_output_reader\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None


def prepare_connected_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module):
    now = datetime.datetime.now()
    mock_async_reader, mock_process, mock_provide_async_reader, mock_service_config = prepare_connecting_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module, now)
    mock_serializer = mock.MagicMock()
    mock_serializer.serialize = mock.MagicMock(return_value=mock.sentinel.SERIALIZED_SHUTDOWN)
    connection = BackendConnection(mock.sentinel.FRONTEND, mock_service_config, [], serializer=mock_serializer, provide_async_reader=mock_provide_async_reader)
    connection.connect()
    mock_async_reader.queue_.put('This is the JEP service, listening on port 4711')
    mock_socket = mock.MagicMock()
    mock_socket_module.create_connection.return_value = mock_socket
    decorate_connection_state_dispatch(connection, 0.5, mock_datetime_module)
    connection.run(datetime.timedelta(seconds=0.4))
    @py_assert1 = connection.state
    @py_assert5 = State.Connected
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Connected\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    return (connection, mock_process, mock_serializer, mock_socket)


@mock.patch('jep_py.frontend.subprocess')
@mock.patch('jep_py.frontend.socket')
@mock.patch('jep_py.frontend.datetime')
@mock.patch('jep_py.frontend.os')
def test_backend_connected_disconnect_backend_shutdown_ok(mock_os_module, mock_datetime_module, mock_socket_module, mock_subprocess_module):
    connection, mock_process, mock_serializer, mock_socket = prepare_connected_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module)
    connection.disconnect()
    @py_assert1 = mock_serializer.serialize.call_args[0][0]
    @py_assert4 = isinstance(@py_assert1, Shutdown)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}') % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py3': @pytest_ar._saferepr(Shutdown) if 'Shutdown' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Shutdown) else 'Shutdown'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    mock_socket.send.assert_called_once_with(mock.sentinel.SERIALIZED_SHUTDOWN)
    mock_process.poll = mock.MagicMock(return_value=0)
    connection.run(datetime.timedelta(seconds=0.4))
    @py_assert1 = connection.state
    @py_assert5 = State.Disconnected
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Disconnected\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = connection._process
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s._process\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = connection._process_output_reader
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s._process_output_reader\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None


@mock.patch('jep_py.frontend.subprocess')
@mock.patch('jep_py.frontend.socket')
@mock.patch('jep_py.frontend.datetime')
@mock.patch('jep_py.frontend.os')
def test_backend_connected_reconnect(mock_os_module, mock_datetime_module, mock_socket_module, mock_subprocess_module):
    connection, mock_process, mock_serializer, mock_socket = prepare_connected_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module)
    mock_os_module.path = path
    mock_service_config2 = mock.MagicMock()
    mock_service_config2.command = 'folder/somenewcommand.ext someparameter somethingelse'
    mock_service_config2.config_file_path = path.abspath('somenewdir/.jep')
    connection.reconnect(mock_service_config2)
    @py_assert1 = mock_serializer.serialize.call_args[0][0]
    @py_assert4 = isinstance(@py_assert1, Shutdown)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}') % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py3': @pytest_ar._saferepr(Shutdown) if 'Shutdown' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Shutdown) else 'Shutdown'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    mock_socket.send.assert_called_once_with(mock.sentinel.SERIALIZED_SHUTDOWN)
    mock_process.poll = mock.MagicMock(return_value=0)
    connection.run(datetime.timedelta(seconds=0.4))
    @py_assert1 = connection.state
    @py_assert5 = State.Connecting
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Connecting\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = mock_subprocess_module.Popen.call_args[0][0][0]
    @py_assert3 = 'folder/somenewcommand.ext'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = mock_subprocess_module.Popen.call_args[1]['cwd']
    @py_assert4 = path.abspath
    @py_assert6 = 'somenewdir'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert2 = @py_assert0 == @py_assert8
    if not @py_assert2:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.abspath\n}(%(py7)s)\n}', ), (@py_assert0, @py_assert8)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py9': @pytest_ar._saferepr(@py_assert8), 'py3': @pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None


@mock.patch('jep_py.frontend.subprocess')
@mock.patch('jep_py.frontend.socket')
@mock.patch('jep_py.frontend.datetime')
@mock.patch('jep_py.frontend.os')
def test_backend_connected_disconnect_backend_shutdown_timeout(mock_os_module, mock_datetime_module, mock_socket_module, mock_subprocess_module):
    connection, mock_process, mock_serializer, mock_socket = prepare_connected_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module)
    connection.disconnect()
    @py_assert3 = datetime.timedelta
    @py_assert5 = 0
    @py_assert7 = @py_assert3(seconds=@py_assert5)
    @py_assert1 = TIMEOUT_BACKEND_SHUTDOWN > @py_assert7
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('>', ), (@py_assert1,), ('%(py0)s > %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.timedelta\n}(seconds=%(py6)s)\n}', ), (TIMEOUT_BACKEND_SHUTDOWN, @py_assert7)) % {'py2': @pytest_ar._saferepr(datetime) if 'datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime) else 'datetime', 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(TIMEOUT_BACKEND_SHUTDOWN) if 'TIMEOUT_BACKEND_SHUTDOWN' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TIMEOUT_BACKEND_SHUTDOWN) else 'TIMEOUT_BACKEND_SHUTDOWN', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    mock_process.poll = mock.MagicMock(return_value=None)
    connection.run(TIMEOUT_BACKEND_SHUTDOWN)
    @py_assert1 = connection.state
    @py_assert5 = State.Disconnecting
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Disconnecting\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    connection.run(datetime.timedelta(seconds=1))
    @py_assert1 = mock_socket.close
    @py_assert3 = @py_assert1.call_count
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.close\n}.call_count\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(mock_socket) if 'mock_socket' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_socket) else 'mock_socket', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = connection.state
    @py_assert5 = State.Disconnected
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Disconnected\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = connection._socket
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s._socket\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = connection._process
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s._process\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = connection._process_output_reader
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s._process_output_reader\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None


@mock.patch('jep_py.frontend.subprocess')
@mock.patch('jep_py.frontend.socket')
@mock.patch('jep_py.frontend.select')
@mock.patch('jep_py.frontend.datetime')
@mock.patch('jep_py.frontend.os')
def test_backend_connected_receive_no_data_until_alive_timeout_and_reconnect(mock_os_module, mock_datetime_module, mock_select_module, mock_socket_module, mock_subprocess_module):
    connection, mock_process, mock_serializer, mock_socket = prepare_connected_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module)
    mock_select_module.select = mock.MagicMock(return_value=([], [], []))
    connection.run(TIMEOUT_LAST_MESSAGE)
    @py_assert1 = connection.state
    @py_assert5 = State.Connected
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Connected\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    mock_process.poll = mock.MagicMock(return_value=0)
    connection.run(datetime.timedelta(seconds=1))
    @py_assert1 = mock_socket.close
    @py_assert3 = @py_assert1.call_count
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.close\n}.call_count\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(mock_socket) if 'mock_socket' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_socket) else 'mock_socket', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = connection.state
    @py_assert5 = State.Connecting
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Connecting\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = connection._socket
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s._socket\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = connection._process
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s._process\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    @py_assert1 = connection._process_output_reader
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s._process_output_reader\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None


def iterate_first_and_then(first, then):
    return itertools.chain([first], itertools.repeat(then))


@mock.patch('jep_py.frontend.subprocess')
@mock.patch('jep_py.frontend.socket')
@mock.patch('jep_py.frontend.select')
@mock.patch('jep_py.frontend.datetime')
@mock.patch('jep_py.frontend.os')
def test_backend_connected_receive_data(mock_os_module, mock_datetime_module, mock_select_module, mock_socket_module, mock_subprocess_module):
    connection, mock_process, mock_serializer, mock_socket = prepare_connected_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module)
    connection.frontend = mock.MagicMock()
    mock_select_module.select = mock.MagicMock(return_value=([mock_socket], [], []))
    mock_socket.recv = mock.MagicMock(side_effect=iterate_first_and_then(mock.sentinel.SERIALIZED, BlockingIOError))
    mock_serializer.__iter__ = mock.Mock(return_value=iter([BackendAlive()]))
    mock_listener = mock.MagicMock()
    connection.listeners.append(mock_listener)
    connection.run(TIMEOUT_LAST_MESSAGE / 2)
    @py_assert1 = connection.state
    @py_assert5 = State.Connected
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Connected\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = mock_listener.on_backend_alive
    @py_assert3 = @py_assert1.called
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.on_backend_alive\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_listener) if 'mock_listener' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_listener) else 'mock_listener', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = connection.frontend
    @py_assert3 = @py_assert1.on_backend_alive
    @py_assert5 = @py_assert3.called
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.frontend\n}.on_backend_alive\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None


@mock.patch('jep_py.frontend.subprocess')
@mock.patch('jep_py.frontend.socket')
@mock.patch('jep_py.frontend.select')
@mock.patch('jep_py.frontend.datetime')
@mock.patch('jep_py.frontend.os')
def test_backend_connected_receive_data_resets_alive_timeout(mock_os_module, mock_datetime_module, mock_select_module, mock_socket_module, mock_subprocess_module):
    connection, mock_process, mock_serializer, mock_socket = prepare_connected_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module)
    connection.frontend = mock.MagicMock()
    mock_select_module.select = mock.MagicMock(return_value=([], [], []))
    connection.run(TIMEOUT_LAST_MESSAGE)
    @py_assert1 = connection.state
    @py_assert5 = State.Connected
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Connected\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    mock_select_module.select = mock.MagicMock(return_value=([mock_socket], [], []))
    mock_socket.recv = mock.MagicMock(side_effect=iterate_first_and_then(mock.sentinel.SERIALIZED, BlockingIOError))
    mock_serializer.__iter__ = mock.Mock(return_value=iter([BackendAlive()]))
    connection.run(TIMEOUT_LAST_MESSAGE)
    @py_assert1 = connection.state
    @py_assert5 = State.Connected
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Connected\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


@mock.patch('jep_py.frontend.subprocess')
@mock.patch('jep_py.frontend.socket')
@mock.patch('jep_py.frontend.select')
@mock.patch('jep_py.frontend.datetime')
@mock.patch('jep_py.frontend.os')
def test_backend_connected_receive_data_none(mock_os_module, mock_datetime_module, mock_select_module, mock_socket_module, mock_subprocess_module):
    connection, mock_process, mock_serializer, mock_socket = prepare_connected_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module)
    mock_select_module.select = mock.MagicMock(return_value=([mock_socket], [], []))
    mock_socket.recv = mock.MagicMock(return_value=None)
    connection.run(datetime.timedelta(seconds=2))
    @py_assert1 = connection.state
    @py_assert5 = State.Connecting
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Connecting\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


@mock.patch('jep_py.frontend.subprocess')
@mock.patch('jep_py.frontend.socket')
@mock.patch('jep_py.frontend.select')
@mock.patch('jep_py.frontend.datetime')
@mock.patch('jep_py.frontend.os')
def test_backend_connected_receive_data_exception(mock_os_module, mock_datetime_module, mock_select_module, mock_socket_module, mock_subprocess_module):
    connection, mock_process, mock_serializer, mock_socket = prepare_connected_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module)
    mock_select_module.select = mock.MagicMock(return_value=([mock_socket], [], []))
    mock_socket.recv = mock.MagicMock(side_effect=ConnectionResetError)
    connection.run(datetime.timedelta(seconds=2))
    @py_assert1 = connection.state
    @py_assert5 = State.Connecting
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Connecting\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(connection) if 'connection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(connection) else 'connection', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_backend_connection_request_message_no_token_attribute():
    connection = BackendConnection(mock.sentinel.FRONTEND, mock.sentinel.SERVICE_CONFIG, [])
    connection.state = State.Connected
    with pytest.raises(AttributeError):
        connection.request_message(Shutdown(), mock.sentinel.DURATION)


@mock.patch('jep_py.frontend.subprocess')
@mock.patch('jep_py.frontend.socket')
@mock.patch('jep_py.frontend.select')
@mock.patch('jep_py.frontend.datetime')
@mock.patch('jep_py.frontend.os')
def test_backend_connected_run_for_duration(mock_os_module, mock_datetime_module, mock_select_module, mock_socket_module, mock_subprocess_module):
    connection, mock_process, mock_serializer, mock_socket = prepare_connected_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module)
    mock_select_module.select = mock.MagicMock(return_value=([], [], []))
    decorate_connection_state_dispatch(connection, 0.1, mock_datetime_module)
    now = mock_datetime_module.datetime.now()
    connection.run(datetime.timedelta(seconds=1))
    @py_assert1 = mock_datetime_module.datetime
    @py_assert3 = @py_assert1.now
    @py_assert5 = @py_assert3()
    @py_assert10 = datetime.timedelta
    @py_assert12 = 1
    @py_assert14 = @py_assert10(seconds=@py_assert12)
    @py_assert16 = now + @py_assert14
    @py_assert7 = @py_assert5 == @py_assert16
    if not @py_assert7:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.datetime\n}.now\n}()\n} == (%(py8)s + %(py15)s\n{%(py15)s = %(py11)s\n{%(py11)s = %(py9)s.timedelta\n}(seconds=%(py13)s)\n})',), (@py_assert5, @py_assert16)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_datetime_module) if 'mock_datetime_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_datetime_module) else 'mock_datetime_module', 'py4': @pytest_ar._saferepr(@py_assert3), 'py15': @pytest_ar._saferepr(@py_assert14), 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(datetime) if 'datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime) else 'datetime', 'py8': @pytest_ar._saferepr(now) if 'now' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(now) else 'now', 
         'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = None


@mock.patch('jep_py.frontend.subprocess')
@mock.patch('jep_py.frontend.socket')
@mock.patch('jep_py.frontend.select')
@mock.patch('jep_py.frontend.datetime')
@mock.patch('jep_py.frontend.os')
def test_backend_connected_run_without_response_received(mock_os_module, mock_datetime_module, mock_select_module, mock_socket_module, mock_subprocess_module):
    connection, mock_process, mock_serializer, mock_socket = prepare_connected_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module)
    connection.frontend = mock.MagicMock()
    connection._current_request_token = mock.sentinel.TOKEN
    connection._current_request_response = None
    mock_select_module.select = mock.MagicMock(return_value=([], [], []))
    decorate_connection_state_dispatch(connection, 0.1, mock_datetime_module)
    now = mock_datetime_module.datetime.now()
    connection.run(datetime.timedelta(seconds=1))
    @py_assert1 = mock_datetime_module.datetime
    @py_assert3 = @py_assert1.now
    @py_assert5 = @py_assert3()
    @py_assert10 = datetime.timedelta
    @py_assert12 = 1
    @py_assert14 = @py_assert10(seconds=@py_assert12)
    @py_assert16 = now + @py_assert14
    @py_assert7 = @py_assert5 == @py_assert16
    if not @py_assert7:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.datetime\n}.now\n}()\n} == (%(py8)s + %(py15)s\n{%(py15)s = %(py11)s\n{%(py11)s = %(py9)s.timedelta\n}(seconds=%(py13)s)\n})',), (@py_assert5, @py_assert16)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_datetime_module) if 'mock_datetime_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_datetime_module) else 'mock_datetime_module', 'py4': @pytest_ar._saferepr(@py_assert3), 'py15': @pytest_ar._saferepr(@py_assert14), 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(datetime) if 'datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime) else 'datetime', 'py8': @pytest_ar._saferepr(now) if 'now' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(now) else 'now', 
         'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = None


@mock.patch('jep_py.frontend.subprocess')
@mock.patch('jep_py.frontend.socket')
@mock.patch('jep_py.frontend.select')
@mock.patch('jep_py.frontend.datetime')
@mock.patch('jep_py.frontend.os')
def test_backend_connected_run_wit__other_response_received(mock_os_module, mock_datetime_module, mock_select_module, mock_socket_module, mock_subprocess_module):
    connection, mock_process, mock_serializer, mock_socket = prepare_connected_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module)
    connection.frontend = mock.MagicMock()
    connection._current_request_token = mock.sentinel.TOKEN
    connection._current_request_response = None
    mock_select_module.select = mock.MagicMock(return_value=([mock_socket], [], []))
    mock_socket.recv = mock.MagicMock(side_effect=iterate_first_and_then(mock.sentinel.SERIALIZED, BlockingIOError))
    mock_serializer.__iter__ = mock.Mock(return_value=iter([CompletionResponse(0, 1, token=mock.sentinel.OTHER_TOKEN)]))
    decorate_connection_state_dispatch(connection, 0.1, mock_datetime_module)
    now = mock_datetime_module.datetime.now()
    connection.run(datetime.timedelta(seconds=1))
    @py_assert1 = mock_datetime_module.datetime
    @py_assert3 = @py_assert1.now
    @py_assert5 = @py_assert3()
    @py_assert10 = datetime.timedelta
    @py_assert12 = 1
    @py_assert14 = @py_assert10(seconds=@py_assert12)
    @py_assert16 = now + @py_assert14
    @py_assert7 = @py_assert5 == @py_assert16
    if not @py_assert7:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.datetime\n}.now\n}()\n} == (%(py8)s + %(py15)s\n{%(py15)s = %(py11)s\n{%(py11)s = %(py9)s.timedelta\n}(seconds=%(py13)s)\n})',), (@py_assert5, @py_assert16)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_datetime_module) if 'mock_datetime_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_datetime_module) else 'mock_datetime_module', 'py4': @pytest_ar._saferepr(@py_assert3), 'py15': @pytest_ar._saferepr(@py_assert14), 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(datetime) if 'datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime) else 'datetime', 'py8': @pytest_ar._saferepr(now) if 'now' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(now) else 'now', 
         'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = None


@mock.patch('jep_py.frontend.subprocess')
@mock.patch('jep_py.frontend.socket')
@mock.patch('jep_py.frontend.select')
@mock.patch('jep_py.frontend.datetime')
@mock.patch('jep_py.frontend.os')
def test_backend_connected_run_with_response_received(mock_os_module, mock_datetime_module, mock_select_module, mock_socket_module, mock_subprocess_module):
    connection, mock_process, mock_serializer, mock_socket = prepare_connected_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module)
    connection.frontend = mock.MagicMock()
    connection._current_request_token = mock.sentinel.TOKEN
    connection._current_request_response = None
    mock_select_module.select = mock.MagicMock(return_value=([mock_socket], [], []))
    mock_socket.recv = mock.MagicMock(side_effect=iterate_first_and_then(mock.sentinel.SERIALIZED, BlockingIOError))
    mock_serializer.__iter__ = mock.Mock(return_value=iter([CompletionResponse(0, 1, token=mock.sentinel.TOKEN)]))
    decorate_connection_state_dispatch(connection, 0.1, mock_datetime_module)
    now = mock_datetime_module.datetime.now()
    connection.run(datetime.timedelta(seconds=1))
    @py_assert1 = mock_datetime_module.datetime
    @py_assert3 = @py_assert1.now
    @py_assert5 = @py_assert3()
    @py_assert10 = datetime.timedelta
    @py_assert12 = 0.1
    @py_assert14 = @py_assert10(seconds=@py_assert12)
    @py_assert16 = now + @py_assert14
    @py_assert7 = @py_assert5 == @py_assert16
    if not @py_assert7:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.datetime\n}.now\n}()\n} == (%(py8)s + %(py15)s\n{%(py15)s = %(py11)s\n{%(py11)s = %(py9)s.timedelta\n}(seconds=%(py13)s)\n})',), (@py_assert5, @py_assert16)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_datetime_module) if 'mock_datetime_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_datetime_module) else 'mock_datetime_module', 'py4': @pytest_ar._saferepr(@py_assert3), 'py15': @pytest_ar._saferepr(@py_assert14), 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(datetime) if 'datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime) else 'datetime', 'py8': @pytest_ar._saferepr(now) if 'now' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(now) else 'now', 
         'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = None


@mock.patch('jep_py.frontend.subprocess')
@mock.patch('jep_py.frontend.socket')
@mock.patch('jep_py.frontend.select')
@mock.patch('jep_py.frontend.datetime')
@mock.patch('jep_py.frontend.os')
def test_backend_connected_request_message_without_response(mock_os_module, mock_datetime_module, mock_select_module, mock_socket_module, mock_subprocess_module):
    connection, mock_process, mock_serializer, mock_socket = prepare_connected_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module)
    connection.frontend = mock.MagicMock()
    mock_select_module.select = mock.MagicMock(return_value=([], [], []))
    request = CompletionRequest('file', 0)
    decorate_connection_state_dispatch(connection, 0.1, mock_datetime_module)
    now = mock_datetime_module.datetime.now()
    connection.request_message(request, datetime.timedelta(seconds=1))
    @py_assert1 = request.token
    @py_assert4 = None
    @py_assert3 = @py_assert1 is not @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is not',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.token\n} is not %(py5)s',), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request'}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    mock_serializer.serialize.assert_called_once_with(request)
    @py_assert1 = mock_datetime_module.datetime
    @py_assert3 = @py_assert1.now
    @py_assert5 = @py_assert3()
    @py_assert10 = datetime.timedelta
    @py_assert12 = 1
    @py_assert14 = @py_assert10(seconds=@py_assert12)
    @py_assert16 = now + @py_assert14
    @py_assert7 = @py_assert5 == @py_assert16
    if not @py_assert7:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.datetime\n}.now\n}()\n} == (%(py8)s + %(py15)s\n{%(py15)s = %(py11)s\n{%(py11)s = %(py9)s.timedelta\n}(seconds=%(py13)s)\n})',), (@py_assert5, @py_assert16)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_datetime_module) if 'mock_datetime_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_datetime_module) else 'mock_datetime_module', 'py4': @pytest_ar._saferepr(@py_assert3), 'py15': @pytest_ar._saferepr(@py_assert14), 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(datetime) if 'datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime) else 'datetime', 'py8': @pytest_ar._saferepr(now) if 'now' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(now) else 'now', 
         'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = None


@mock.patch('jep_py.frontend.subprocess')
@mock.patch('jep_py.frontend.socket')
@mock.patch('jep_py.frontend.select')
@mock.patch('jep_py.frontend.datetime')
@mock.patch('jep_py.frontend.os')
def test_backend_connected_request_message_with_response(mock_os_module, mock_datetime_module, mock_select_module, mock_socket_module, mock_subprocess_module):
    connection, mock_process, mock_serializer, mock_socket = prepare_connected_mocks(mock_datetime_module, mock_socket_module, mock_subprocess_module)
    connection.frontend = mock.MagicMock()
    mock_select_module.select = mock.MagicMock(return_value=([mock_socket], [], []))
    mock_socket.recv = mock.MagicMock(side_effect=iterate_first_and_then(mock.sentinel.SERIALIZED, BlockingIOError))
    mock_serializer.__iter__ = mock.Mock(return_value=iter([CompletionResponse(0, 1, token=mock.sentinel.TOKEN)]))
    request = CompletionRequest('file', 0, token=mock.sentinel.TOKEN)
    decorate_connection_state_dispatch(connection, 0.1, mock_datetime_module)
    now = mock_datetime_module.datetime.now()
    connection.request_message(request, datetime.timedelta(seconds=1))
    @py_assert1 = mock_datetime_module.datetime
    @py_assert3 = @py_assert1.now
    @py_assert5 = @py_assert3()
    @py_assert10 = datetime.timedelta
    @py_assert12 = 0.1
    @py_assert14 = @py_assert10(seconds=@py_assert12)
    @py_assert16 = now + @py_assert14
    @py_assert7 = @py_assert5 == @py_assert16
    if not @py_assert7:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.datetime\n}.now\n}()\n} == (%(py8)s + %(py15)s\n{%(py15)s = %(py11)s\n{%(py11)s = %(py9)s.timedelta\n}(seconds=%(py13)s)\n})',), (@py_assert5, @py_assert16)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_datetime_module) if 'mock_datetime_module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_datetime_module) else 'mock_datetime_module', 'py4': @pytest_ar._saferepr(@py_assert3), 'py15': @pytest_ar._saferepr(@py_assert14), 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(datetime) if 'datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime) else 'datetime', 'py8': @pytest_ar._saferepr(now) if 'now' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(now) else 'now', 
         'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = None
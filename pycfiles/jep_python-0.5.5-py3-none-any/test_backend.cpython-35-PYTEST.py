# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Work\jep\src\jep-python\build\lib\test\test_backend.py
# Compiled at: 2016-01-04 11:08:28
# Size of source mod 2**32: 11603 bytes
"""Tests of backend features (no integration with frontend)."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from unittest import mock
import datetime, pytest
from jep_py.backend import Backend, State, NoPortFoundError, PORT_RANGE, FrontendConnection, TIMEOUT_BACKEND_ALIVE, TIMEOUT_LAST_MESSAGE
from jep_py.content import SynchronizationResult
from jep_py.protocol import MessageSerializer
from jep_py.schema import Shutdown, BackendAlive, CompletionRequest, ContentSync, StaticSyntaxList, StaticSyntax
from jep_py.syntax import SyntaxFile
from test.logconfig import configure_test_logger

def setup_function(function):
    configure_test_logger()


def test_initial_state():
    backend = Backend()
    @py_assert1 = backend.serversocket
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.serversocket\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(backend) if 'backend' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(backend) else 'backend'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = backend.state
    @py_assert5 = State.Stopped
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Stopped\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(backend) if 'backend' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(backend) else 'backend', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


@mock.patch('jep_py.backend.socket')
def test_find_server_port(mock_socket_mod):
    mock_socket_mod.socket().bind = mock.MagicMock(side_effect=OSError)
    backend = Backend()
    with pytest.raises(NoPortFoundError):
        backend.start()
    @py_assert0 = PORT_RANGE[0]
    @py_assert3 = PORT_RANGE[1]
    @py_assert2 = @py_assert0 < @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('<',), (@py_assert2,), ('%(py1)s < %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = (@pytest_ar._format_assertmsg('At lest one port should be testable.') + '\n>assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    for port in range(PORT_RANGE[0], PORT_RANGE[1]):
        @py_assert1 = mock.call
        @py_assert3 = (
         'localhost', port)
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert9 = mock_socket_mod.socket
        @py_assert11 = @py_assert9()
        @py_assert13 = @py_assert11.bind
        @py_assert15 = @py_assert13.call_args_list
        @py_assert7 = @py_assert5 in @py_assert15
        if not @py_assert7:
            @py_format17 = @pytest_ar._call_reprcompare(('in',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.call\n}(%(py4)s)\n} in %(py16)s\n{%(py16)s = %(py14)s\n{%(py14)s = %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s.socket\n}()\n}.bind\n}.call_args_list\n}',), (@py_assert5, @py_assert15)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py4': @pytest_ar._saferepr(@py_assert3), 'py16': @pytest_ar._saferepr(@py_assert15), 'py10': @pytest_ar._saferepr(@py_assert9), 'py12': @pytest_ar._saferepr(@py_assert11), 'py8': @pytest_ar._saferepr(mock_socket_mod) if 'mock_socket_mod' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_socket_mod) else 'mock_socket_mod', 'py14': @pytest_ar._saferepr(@py_assert13), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
            raise AssertionError(@pytest_ar._format_explanation(@py_format19))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None

    @py_assert1 = backend.state
    @py_assert5 = State.Stopped
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Stopped\n}',), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(backend) if 'backend' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(backend) else 'backend', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def set_backend_state(backend, state, return_value=None):
    """Utility to set backend state from outside as mock side-effect."""

    def _(*args):
        backend.state = state
        return return_value

    return _


@mock.patch('jep_py.backend.socket')
@mock.patch('jep_py.backend.select')
def test_bind_and_listen_and_accept_and_disconnect(mock_select_mod, mock_socket_mod, capsys):
    backend = Backend()
    server_socket = mock_socket_mod.socket()
    mock_select_mod.select = mock.MagicMock(return_value=([server_socket], [], []))
    client_socket = mock.MagicMock()
    server_socket.accept = mock.MagicMock(side_effect=set_backend_state(backend, State.ShutdownPending, [client_socket]))
    backend.start()
    @py_assert1 = backend.state
    @py_assert5 = State.Stopped
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.Stopped\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(backend) if 'backend' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(backend) else 'backend', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = server_socket.close
    @py_assert3 = @py_assert1.call_count
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.close\n}.call_count\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(server_socket) if 'server_socket' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(server_socket) else 'server_socket', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = client_socket.close
    @py_assert3 = @py_assert1.call_count
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.close\n}.call_count\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(client_socket) if 'client_socket' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(client_socket) else 'client_socket', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    out, *_ = capsys.readouterr()
    @py_assert0 = 'JEP service, listening on port 9001'
    @py_assert2 = @py_assert0 in out
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, out)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_receive_shutdown():
    mock_clientsocket = mock.MagicMock()
    mock_clientsocket.recv = mock.MagicMock(side_effect=[MessageSerializer().serialize(Shutdown()), BlockingIOError])
    mock_listener1 = mock.MagicMock()
    mock_listener2 = mock.MagicMock()
    backend = Backend([mock_listener1, mock_listener2])
    backend.connection[mock_clientsocket] = FrontendConnection(backend, mock_clientsocket)
    @py_assert1 = backend.state
    @py_assert5 = State.ShutdownPending
    @py_assert3 = @py_assert1 is not @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is not %(py6)s\n{%(py6)s = %(py4)s.ShutdownPending\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(backend) if 'backend' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(backend) else 'backend', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    backend._receive(mock_clientsocket)
    @py_assert1 = mock_listener1.on_shutdown
    @py_assert3 = @py_assert1.call_count
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.on_shutdown\n}.call_count\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(mock_listener1) if 'mock_listener1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_listener1) else 'mock_listener1', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = mock_listener2.on_shutdown
    @py_assert3 = @py_assert1.call_count
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.on_shutdown\n}.call_count\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(mock_listener2) if 'mock_listener2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_listener2) else 'mock_listener2', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = backend.state
    @py_assert5 = State.ShutdownPending
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.state\n} is %(py6)s\n{%(py6)s = %(py4)s.ShutdownPending\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(backend) if 'backend' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(backend) else 'backend', 'py4': @pytest_ar._saferepr(State) if 'State' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(State) else 'State', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_receive_empty():
    mock_clientsocket = mock.MagicMock()
    mock_clientsocket.recv = mock.MagicMock(return_value=None)
    backend = Backend()
    backend.connection[mock_clientsocket] = FrontendConnection(backend, mock_clientsocket)
    backend.sockets.append(mock_clientsocket)
    backend._receive(mock_clientsocket)
    @py_assert1 = mock_clientsocket.close
    @py_assert3 = @py_assert1.call_count
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.close\n}.call_count\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(mock_clientsocket) if 'mock_clientsocket' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_clientsocket) else 'mock_clientsocket', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_message_context():
    mock_clientsocket = mock.MagicMock()
    mock_clientsocket.recv = mock.MagicMock(side_effect=[MessageSerializer().serialize(Shutdown()), BlockingIOError])
    mock_listener = mock.MagicMock()
    backend = Backend([mock_listener])
    backend.connection[mock_clientsocket] = FrontendConnection(backend, mock_clientsocket)
    backend._receive(mock_clientsocket)
    message_context = mock_listener.on_shutdown.call_args[0][0]
    @py_assert1 = message_context.service
    @py_assert3 = @py_assert1 is backend
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.service\n} is %(py4)s', ), (@py_assert1, backend)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(message_context) if 'message_context' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(message_context) else 'message_context', 'py4': @pytest_ar._saferepr(backend) if 'backend' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(backend) else 'backend'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = message_context.sock
    @py_assert3 = @py_assert1 is mock_clientsocket
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.sock\n} is %(py4)s', ), (@py_assert1, mock_clientsocket)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(message_context) if 'message_context' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(message_context) else 'message_context', 'py4': @pytest_ar._saferepr(mock_clientsocket) if 'mock_clientsocket' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_clientsocket) else 'mock_clientsocket'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    message_context.send_message(BackendAlive())
    @py_assert1 = mock_clientsocket.send
    @py_assert3 = @py_assert1.call_count
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.send\n}.call_count\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(mock_clientsocket) if 'mock_clientsocket' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_clientsocket) else 'mock_clientsocket', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


@mock.patch('jep_py.backend.datetime')
def test_backend_alive_cycle(mock_datetime_mod):
    now = datetime.datetime.now()
    mock_datetime_mod.datetime.now = mock.MagicMock(side_effect=lambda : now)
    @py_assert3 = datetime.timedelta
    @py_assert5 = 0
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert1 = TIMEOUT_BACKEND_ALIVE > @py_assert7
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('>', ), (@py_assert1,), ('%(py0)s > %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.timedelta\n}(%(py6)s)\n}', ), (TIMEOUT_BACKEND_ALIVE, @py_assert7)) % {'py2': @pytest_ar._saferepr(datetime) if 'datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime) else 'datetime', 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(TIMEOUT_BACKEND_ALIVE) if 'TIMEOUT_BACKEND_ALIVE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TIMEOUT_BACKEND_ALIVE) else 'TIMEOUT_BACKEND_ALIVE', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    mock_clientsocket1 = mock.MagicMock()
    mock_clientsocket2 = mock.MagicMock()
    backend = Backend()
    backend.sockets = [mock.sentinel.SERVER_SOCKET, mock_clientsocket1, mock_clientsocket2]
    backend.connection[mock_clientsocket1] = FrontendConnection(backend, mock_clientsocket1)
    backend.connection[mock_clientsocket2] = FrontendConnection(backend, mock_clientsocket2)
    backend._cyclic()
    @py_assert0 = b'BackendAlive'
    @py_assert3 = mock_clientsocket1.send.call_args[0][0]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = b'BackendAlive'
    @py_assert3 = mock_clientsocket2.send.call_args[0][0]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    now += TIMEOUT_BACKEND_ALIVE * 0.9
    mock_clientsocket1.send.reset_mock()
    mock_clientsocket2.send.reset_mock()
    backend._cyclic()
    @py_assert1 = mock_clientsocket1.called
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_clientsocket1) if 'mock_clientsocket1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_clientsocket1) else 'mock_clientsocket1'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = mock_clientsocket2.called
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_clientsocket2) if 'mock_clientsocket2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_clientsocket2) else 'mock_clientsocket2'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    now += TIMEOUT_BACKEND_ALIVE * 0.15
    mock_clientsocket1.send.reset_mock()
    mock_clientsocket2.send.reset_mock()
    backend._cyclic()
    @py_assert0 = b'BackendAlive'
    @py_assert3 = mock_clientsocket1.send.call_args[0][0]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = b'BackendAlive'
    @py_assert3 = mock_clientsocket2.send.call_args[0][0]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


@mock.patch('jep_py.backend.datetime')
def test_frontend_timeout(mock_datetime_mod):
    now = datetime.datetime.now()
    mock_datetime_mod.datetime.now = mock.MagicMock(side_effect=lambda : now)
    mock_clientsocket1 = mock.MagicMock()
    mock_clientsocket2 = mock.MagicMock()
    backend = Backend()
    backend.sockets = [mock.sentinel.SERVER_SOCKET, mock_clientsocket1, mock_clientsocket2]
    backend.connection[mock_clientsocket1] = FrontendConnection(backend, mock_clientsocket1)
    backend.connection[mock_clientsocket2] = FrontendConnection(backend, mock_clientsocket2)
    @py_assert3 = datetime.timedelta
    @py_assert5 = 0
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert1 = TIMEOUT_LAST_MESSAGE > @py_assert7
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('>', ), (@py_assert1,), ('%(py0)s > %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.timedelta\n}(%(py6)s)\n}', ), (TIMEOUT_LAST_MESSAGE, @py_assert7)) % {'py2': @pytest_ar._saferepr(datetime) if 'datetime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(datetime) else 'datetime', 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(TIMEOUT_LAST_MESSAGE) if 'TIMEOUT_LAST_MESSAGE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TIMEOUT_LAST_MESSAGE) else 'TIMEOUT_LAST_MESSAGE', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    backend.ts_alive_sent = now
    backend._cyclic()
    @py_assert1 = mock_clientsocket1.close
    @py_assert3 = @py_assert1.called
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.close\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_clientsocket1) if 'mock_clientsocket1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_clientsocket1) else 'mock_clientsocket1', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = mock_clientsocket2.close
    @py_assert3 = @py_assert1.called
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.close\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_clientsocket2) if 'mock_clientsocket2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_clientsocket2) else 'mock_clientsocket2', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    now += 0.9 * TIMEOUT_LAST_MESSAGE
    backend.ts_alive_sent = now
    backend._cyclic()
    @py_assert1 = mock_clientsocket1.close
    @py_assert3 = @py_assert1.called
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.close\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_clientsocket1) if 'mock_clientsocket1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_clientsocket1) else 'mock_clientsocket1', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = mock_clientsocket2.close
    @py_assert3 = @py_assert1.called
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.close\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_clientsocket2) if 'mock_clientsocket2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_clientsocket2) else 'mock_clientsocket2', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    mock_clientsocket1.recv = mock.MagicMock(side_effect=[MessageSerializer().serialize(CompletionRequest('t', 'g', 10)), BlockingIOError])
    backend._receive(mock_clientsocket1)
    now += 0.2 * TIMEOUT_LAST_MESSAGE
    backend.ts_alive_sent = now
    backend._cyclic()
    @py_assert1 = mock_clientsocket1.close
    @py_assert3 = @py_assert1.called
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.close\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_clientsocket1) if 'mock_clientsocket1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_clientsocket1) else 'mock_clientsocket1', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = mock_clientsocket2.close
    @py_assert3 = @py_assert1.called
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.close\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_clientsocket2) if 'mock_clientsocket2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_clientsocket2) else 'mock_clientsocket2', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    now += TIMEOUT_LAST_MESSAGE
    backend.ts_alive_sent = now
    backend._cyclic()
    @py_assert1 = mock_clientsocket1.close
    @py_assert3 = @py_assert1.called
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.close\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_clientsocket1) if 'mock_clientsocket1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_clientsocket1) else 'mock_clientsocket1', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_propagate_content_sync():
    mock_clientsocket = mock.MagicMock()
    mock_clientsocket.recv = mock.MagicMock(side_effect=[MessageSerializer().serialize(ContentSync('/path/to/file', 'new content', 17, 21)), BlockingIOError])
    mock_clientsocket.send = mock.MagicMock()
    mock_listener = mock.MagicMock()
    backend = Backend([mock_listener])
    mock_content_monitor = mock.MagicMock()
    mock_content_monitor.synchronize = mock.MagicMock(return_value=SynchronizationResult.Updated)
    backend.connection[mock_clientsocket] = FrontendConnection(backend, mock_clientsocket, content_monitor=mock_content_monitor)
    backend._receive(mock_clientsocket)
    @py_assert1 = mock_listener.on_content_sync
    @py_assert3 = @py_assert1.call_count
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.on_content_sync\n}.call_count\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(mock_listener) if 'mock_listener' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_listener) else 'mock_listener', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    mock_content_monitor.synchronize.assert_called_once_with('/path/to/file', 'new content', 17, 21)
    @py_assert1 = mock_clientsocket.send
    @py_assert3 = @py_assert1.called
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.send\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_clientsocket) if 'mock_clientsocket' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_clientsocket) else 'mock_clientsocket', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    arg = mock_listener.on_content_sync.call_args[0][0]
    @py_assert3 = isinstance(arg, ContentSync)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py2': @pytest_ar._saferepr(ContentSync) if 'ContentSync' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ContentSync) else 'ContentSync', 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(arg) if 'arg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(arg) else 'arg'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert1 = arg.file
    @py_assert4 = '/path/to/file'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.file\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(arg) if 'arg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(arg) else 'arg'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = arg.data
    @py_assert4 = 'new content'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.data\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(arg) if 'arg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(arg) else 'arg'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = arg.start
    @py_assert4 = 17
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.start\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(arg) if 'arg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(arg) else 'arg'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = arg.end
    @py_assert4 = 21
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.end\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(arg) if 'arg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(arg) else 'arg'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_propagate_content_sync_out_of_sync():
    mock_clientsocket = mock.MagicMock()
    mock_clientsocket.recv = mock.MagicMock(side_effect=[MessageSerializer().serialize(ContentSync('/path/to/file', 'new content', 17, 21)), BlockingIOError])
    mock_clientsocket.send = mock.MagicMock()
    mock_listener = mock.MagicMock()
    backend = Backend([mock_listener])
    mock_content_monitor = mock.MagicMock()
    mock_content_monitor.synchronize = mock.MagicMock(return_value=SynchronizationResult.OutOfSync)
    backend.connection[mock_clientsocket] = FrontendConnection(backend, mock_clientsocket, content_monitor=mock_content_monitor)
    backend._receive(mock_clientsocket)
    @py_assert1 = mock_listener.on_content_sync
    @py_assert3 = @py_assert1.call_count
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.on_content_sync\n}.call_count\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(mock_listener) if 'mock_listener' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_listener) else 'mock_listener', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    mock_content_monitor.synchronize.assert_called_once_with('/path/to/file', 'new content', 17, 21)
    @py_assert1 = mock_clientsocket.send
    @py_assert3 = @py_assert1.call_count
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.send\n}.call_count\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(mock_clientsocket) if 'mock_clientsocket' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_clientsocket) else 'mock_clientsocket', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    arg = mock_clientsocket.send.call_args[0][0]
    @py_assert0 = b'OutOfSync'
    @py_assert2 = @py_assert0 in arg
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, arg)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(arg) if 'arg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(arg) else 'arg'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_static_syntax_registration():
    mock_syntax_fileset = mock.MagicMock()
    backend = Backend(syntax_fileset=mock_syntax_fileset)
    backend.register_static_syntax(mock.sentinel.NAME1, mock.sentinel.PATH1, mock.sentinel.FORMAT1, mock.sentinel.extensions)
    mock_syntax_fileset.add_syntax_file.assert_called_once_with(mock.sentinel.NAME1, mock.sentinel.PATH1, mock.sentinel.FORMAT1, (mock.sentinel.extensions,))


def test_on_static_syntax_request_none():
    mock_syntax_fileset = mock.MagicMock()
    mock_context = mock.MagicMock()
    backend = Backend(syntax_fileset=mock_syntax_fileset)
    mock_syntax_fileset.filtered = mock.MagicMock(return_value=None)
    backend.on_static_syntax_request(mock.sentinel.FORMAT, ['ext1', 'ext2'], mock_context)
    mock_syntax_fileset.filtered.assert_called_once_with(mock.sentinel.FORMAT, ['ext1', 'ext2'])
    @py_assert1 = mock_context.send_message
    @py_assert3 = @py_assert1.called
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.send_message\n}.called\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(mock_context) if 'mock_context' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_context) else 'mock_context', 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_on_static_syntax_request_found():
    mock_syntax_fileset = mock.MagicMock()
    mock_context = mock.MagicMock()
    mock_context.send_message = mock.MagicMock()
    backend = Backend(syntax_fileset=mock_syntax_fileset)
    mock_syntax_file = mock.MagicMock()
    mock_syntax_file.name = mock.sentinel.NAME1
    mock_syntax_file.extensions = mock.sentinel.EXTENSIONS
    mock_syntax_file.definition = mock.sentinel.DEFINITION
    mock_syntax_fileset.filtered = mock.MagicMock(return_value=(mock_syntax_file,))
    mock_syntax_fileset.format = mock.sentinel.FORMAT
    backend.on_static_syntax_request(mock.sentinel.FORMAT, ['ext1', 'ext2'], mock_context)
    @py_assert1 = mock_context.send_message
    @py_assert3 = @py_assert1.call_count
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.send_message\n}.call_count\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(mock_context) if 'mock_context' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_context) else 'mock_context', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    arg = mock_context.send_message.call_args[0][0]
    @py_assert3 = isinstance(arg, StaticSyntaxList)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py2': @pytest_ar._saferepr(StaticSyntaxList) if 'StaticSyntaxList' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(StaticSyntaxList) else 'StaticSyntaxList', 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(arg) if 'arg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(arg) else 'arg'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert1 = arg.format
    @py_assert5 = mock.sentinel
    @py_assert7 = @py_assert5.FORMAT
    @py_assert3 = @py_assert1 is @py_assert7
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.format\n} is %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.sentinel\n}.FORMAT\n}', ), (@py_assert1, @py_assert7)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(arg) if 'arg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(arg) else 'arg', 'py4': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert2 = arg.syntaxes
    @py_assert4 = len(@py_assert2)
    @py_assert7 = 1
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.syntaxes\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(arg) if 'arg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(arg) else 'arg', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    syntax = arg.syntaxes[0]
    @py_assert3 = isinstance(syntax, StaticSyntax)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py2': @pytest_ar._saferepr(StaticSyntax) if 'StaticSyntax' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(StaticSyntax) else 'StaticSyntax', 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(syntax) if 'syntax' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(syntax) else 'syntax'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert1 = syntax.name
    @py_assert5 = mock.sentinel
    @py_assert7 = @py_assert5.NAME1
    @py_assert3 = @py_assert1 == @py_assert7
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.sentinel\n}.NAME1\n}', ), (@py_assert1, @py_assert7)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(syntax) if 'syntax' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(syntax) else 'syntax', 'py4': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = syntax.fileExtensions
    @py_assert5 = mock.sentinel
    @py_assert7 = @py_assert5.EXTENSIONS
    @py_assert3 = @py_assert1 is @py_assert7
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.fileExtensions\n} is %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.sentinel\n}.EXTENSIONS\n}', ), (@py_assert1, @py_assert7)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(syntax) if 'syntax' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(syntax) else 'syntax', 'py4': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = syntax.definition
    @py_assert5 = mock.sentinel
    @py_assert7 = @py_assert5.DEFINITION
    @py_assert3 = @py_assert1 is @py_assert7
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.definition\n} is %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.sentinel\n}.DEFINITION\n}', ), (@py_assert1, @py_assert7)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(syntax) if 'syntax' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(syntax) else 'syntax', 'py4': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
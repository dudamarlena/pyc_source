# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/charman/src/concrete-python/tests/test_store_wrapper.py
# Compiled at: 2017-07-18 13:12:53
# Size of source mod 2**32: 3080 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, mock
from mock import sentinel
from pytest import fixture
from concrete.access import StoreCommunicationService
from concrete.util import StoreCommunicationServiceWrapper, StoreCommunicationClientWrapper
from concrete.util import ThriftFactory

@fixture
def store_client_wrapper_triple():
    host = 'fake-host'
    port = 2
    return (
     host, port, StoreCommunicationClientWrapper(host, port))


@fixture
def store_service_wrapper():

    class Implementation(StoreCommunicationService.Iface):

        def store(self, communication):
            raise NotImplementedError

        def about(self):
            raise NotImplementedError

        def alive(self):
            raise NotImplementedError

    implementation = Implementation()
    return StoreCommunicationServiceWrapper(implementation)


@mock.patch('concrete.access.StoreCommunicationService.Client')
@mock.patch.object(ThriftFactory, 'createProtocol', return_value=sentinel.protocol)
@mock.patch.object(ThriftFactory, 'createTransport')
@mock.patch.object(ThriftFactory, 'createSocket', return_value=sentinel.socket)
def test_enter(mock_create_socket, mock_create_transport, mock_create_protocol, mock_client, store_client_wrapper_triple):
    host, port, store_client_wrapper = store_client_wrapper_triple
    mock_transport = mock.Mock()
    mock_create_transport.return_value = mock_transport
    mock_client.return_value = sentinel.client
    client = store_client_wrapper.__enter__()
    @py_assert1 = sentinel.client
    @py_assert3 = @py_assert1 == client
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.client\n} == %(py4)s', ), (@py_assert1, client)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(client) if 'client' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(client) else 'client', 'py0': @pytest_ar._saferepr(sentinel) if 'sentinel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentinel) else 'sentinel'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    mock_create_socket.assert_called_once_with(host, port)
    mock_create_transport.assert_called_once_with(mock_create_socket.return_value)
    mock_create_protocol.assert_called_once_with(mock_create_transport.return_value)
    mock_client.assert_called_once_with(mock_create_protocol.return_value)
    mock_transport.open.assert_called_once_with()


def test_exit(store_client_wrapper_triple):
    host, port, store_client_wrapper = store_client_wrapper_triple
    mock_transport = mock.Mock()
    store_client_wrapper.transport = mock_transport
    store_client_wrapper.__exit__(mock.ANY, mock.ANY, mock.ANY)
    mock_transport.close.assert_called_once_with()


@mock.patch.object(ThriftFactory, 'createServer')
def test_serve(mock_create_server, store_service_wrapper):
    mock_server = mock.Mock()
    mock_create_server.return_value = mock_server
    host = 'fake-host'
    port = 2
    store_service_wrapper.serve(host, port)
    mock_create_server.assert_called_once_with(store_service_wrapper.processor, host, port)
    mock_server.serve.assert_called_once_with()
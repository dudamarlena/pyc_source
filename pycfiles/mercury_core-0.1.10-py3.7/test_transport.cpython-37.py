# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/common/unit/test_transport.py
# Compiled at: 2018-10-31 15:58:09
# Size of source mod 2**32: 6648 bytes
import mock, msgpack, pytest, zmq
from mercury.common.exceptions import MercuryClientException
from mercury.common import transport
from .base import MercuryCommonUnitTest

@mock.patch.object(transport, 'get_ctx_and_connect_req_socket')
def test_full_req_transceiver(mock_get_ctx):
    ctx = mock.Mock(spec_set=(zmq.Context))
    socket = ctx.socket.return_value
    mock_get_ctx.return_value = (ctx, socket)
    socket.recv.return_value = msgpack.packb('response')
    unpacked = transport.full_req_transceiver('localhost', 'data')
    assert unpacked == 'response'
    socket.send_multipart.assert_called_once_with([msgpack.packb('data')])
    socket.recv.assert_called_once()
    socket.close.assert_called_once()
    ctx.term.assert_called_once()


def test_get_ctx_and_connect_req_socket():
    with mock.patch('zmq.Context.socket') as (mock_socket):
        ctx, socket = transport.get_ctx_and_connect_req_socket('zmq_url')
    assert isinstance(ctx, zmq.Context)
    mock_socket.assert_called_once()


def test_parse_multipart_message():
    """Test parse_multipart_message()"""
    message = [
     'addr', '', 'msg']
    parsed_message = transport.parse_multipart_message(message)
    assert parsed_message == {'address':['addr', ''],  'message':'msg'}


def test_parse_multipart_message_error():
    """Test parse_multipart_message() with a 2-parts message."""
    message = [
     'addr', '']
    parsed_message = transport.parse_multipart_message(message)
    assert parsed_message == {}


def test_serialize_addresses():
    """Test serialize_addresses()"""
    multipart_address = [
     'addr', 'addr2', '']
    addresses = transport.serialize_addresses(multipart_address)
    assert addresses == ['addr', 'addr2']


class SimpleRouterReqServiceUnitTest(MercuryCommonUnitTest):
    __doc__ = 'Tests for mercury.common.transport.SimpleRouterReqService.'

    def setUp(self):
        super(SimpleRouterReqServiceUnitTest, self).setUp()
        self.patch_context = mock.patch('mercury.common.transport.zmq.Context')
        self.mock_context = mock.Mock(spec=(zmq.Context))
        mock_context_callable = self.patch_context.start()
        mock_context_callable.return_value = self.mock_context
        self.req_service = transport.SimpleRouterReqService('localhost')

    def tearDown(self):
        super(SimpleRouterReqServiceUnitTest, self).tearDown()
        self.patch_context.stop()

    def test_receive(self):
        """Test receive()"""
        payload = {'endpoint':'insert_one', 
         'args':['fake_info']}
        multipart_message = ['addr', '', msgpack.packb(payload)]
        self.req_service.socket.recv_multipart.return_value = multipart_message
        received_msg = self.req_service.receive()
        expected_msg = (
         [
          'addr', ''],
         {'endpoint':'insert_one', 
          'args':['fake_info']})
        assert received_msg == expected_msg

    def test_receive_no_message(self):
        """Test receive() fails when received message is empty."""
        self.req_service.socket.recv_multipart.return_value = []
        self.assertRaises(MercuryClientException, self.req_service.receive)

    @mock.patch('msgpack.unpackb')
    def test_receive_wrong_type(self, mock_unpack):
        """Test receive() fails when received message cannot be unpacked"""
        payload = {'endpoint':'insert_one', 
         'args':['fake_info']}
        multipart_message = ['addr', '', payload]
        self.req_service.socket.recv_multipart.return_value = multipart_message
        mock_unpack.side_effect = [
         TypeError]
        with mock.patch.object(self.req_service, 'send_error'):
            self.assertRaises(MercuryClientException, self.req_service.receive)

    @mock.patch('msgpack.unpackb')
    def test_receive_unpack_error(self, mock_unpack):
        """Test receive() fails when unpacking fails"""
        payload = {'endpoint':'insert_one', 
         'args':['fake_info']}
        multipart_message = ['addr', '', payload]
        self.req_service.socket.recv_multipart.return_value = multipart_message
        mock_unpack.side_effect = [
         msgpack.UnpackException]
        with mock.patch.object(self.req_service, 'send_error') as (mock_error):
            self.assertRaises(MercuryClientException, self.req_service.receive)

    def test_send_error(self):
        address = ['addr', '']
        message = {'endpoint': 'insert_one'}
        with mock.patch.object(self.req_service, 'send') as (mock_send):
            self.req_service.send_error(address, message)
        mock_send.assert_called_once_with(address, {'error':True, 
         'message':message})

    def test_send(self):
        address = [
         'addr', '']
        data = {'error':True,  'message':'fake_message'}
        expected_arg = [
         'addr', '', msgpack.packb(data)]
        self.req_service.send(address, data)
        self.req_service.socket.send_multipart.assert_called_once_with(expected_arg)

    def test_get_key(self):
        """Test get_key()"""
        data = {'key': 'value'}
        returned_value = self.req_service.get_key('key', data)
        assert returned_value == 'value'

    def test_get_key_error(self):
        """Test get_key() when key is missing from the dict"""
        data = {'key': 'value'}
        with pytest.raises(MercuryClientException):
            self.req_service.get_key('wrong_key', data)

    def test_validate_required_error(self):
        """Test validate_required() when a key is missing."""
        required = [
         'key1', 'key2']
        data = {'key1': 'val1'}
        with pytest.raises(MercuryClientException) as (exc_info):
            self.req_service.validate_required(required, data)
            if hasattr(exc_info.value, 'message') and not exc_info.value.message == "Message is missing required data: ['key2']":
                raise AssertionError
            else:
                assert exc_info.value.msg == "Message is missing required data: ['key2']"
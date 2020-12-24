# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_units.py
# Compiled at: 2018-03-12 20:04:44
from mock import patch, call, Mock
import socket, time, unittest
from kiddiepool import KiddieConnection, KiddiePool, TidePool
from kiddiepool.fake import FakeConnection, FakeKazooClient
from kiddiepool.exceptions import KiddieConnectionRecvFailure, KiddiePoolEmpty, KiddiePoolMaxAttempts
from kazoo.exceptions import NoNodeError

class TestKiddieConnection(unittest.TestCase):

    def setUp(self):
        super(TestKiddieConnection, self).setUp()
        self.conn = KiddieConnection()

    def _patch_recv(self):
        recv_patch = patch.object(self.conn, 'recv')
        self.addCleanup(recv_patch.stop)
        return recv_patch.start()

    def test_simple_recvall(self):
        recv_mock = self._patch_recv()
        recv_mock.return_value = '123'
        data = self.conn.recvall(3)
        self.assertEqual('123', data)
        recv_mock.assert_called_with(3)

    def test_multi_read_recvall(self):
        recv_mock = self._patch_recv()
        recv_mock.side_effect = [
         '123',
         '456',
         '789',
         '0']
        data = self.conn.recvall(10)
        self.assertEqual('1234567890', data)
        self.assertEqual(recv_mock.call_args_list, [
         call(10), call(7), call(4), call(1)])

    def test_failed_recvall(self):
        recv_mock = self._patch_recv()
        recv_mock.side_effect = [
         '123',
         '456',
         '789',
         '']
        with self.assertRaises(KiddieConnectionRecvFailure):
            self.conn.recvall(10)

    def test_broken_pipe(self):
        recv_mock = self._patch_recv()
        recv_mock.side_effect = socket.error(socket.errno.EPIPE, 'Broken pipe')
        with self.assertRaises(KiddieConnectionRecvFailure):
            self.conn.recvall(10)

    def test_socket_error_conversion_to_kiddiepool_socket_error(self):
        arbitrary_size = 10
        arbitrary_flags = 0
        with patch.object(self.conn, 'socket') as (socket_mock):
            socket_mock.recv = Mock(side_effect=socket.error)
            with self.assertRaises(KiddieConnectionRecvFailure):
                self.conn.recv(arbitrary_size, arbitrary_flags)

    @patch.object(socket, 'create_connection')
    def test_connection_valid(self, mock_conn):
        self.conn = KiddieConnection(max_idle=999, lifetime=None)
        self.conn.connect('lol', 643)
        self.assertTrue(self.conn.validate())
        self.assertEqual(mock_conn.call_count, 1)
        args, kwargs = mock_conn.call_args
        self.assertEqual(args, (('lol', 643), ))
        return

    @patch.object(socket, 'create_connection')
    def test_max_idle(self, _):
        self.conn = KiddieConnection(max_idle=0, lifetime=None)
        self.conn.connect('foo', 123)
        self.assertFalse(self.conn.validate())
        return

    @patch.object(socket, 'create_connection')
    def test_connection_end_of_life(self, _):
        self.conn = KiddieConnection(max_idle=999, lifetime=0)
        self.conn.connect('bar', 321)
        self.assertFalse(self.conn.validate())

    @patch.object(socket, 'create_connection')
    def test_timeout(self, mock_conn):
        self.conn = KiddieConnection(timeout=987)
        self.conn.connect('baz', 222)
        self.assertEqual(mock_conn.call_count, 1)
        self.assertEqual(mock_conn.call_args, call(('baz', 222), timeout=987))


class TestKiddiePool(unittest.TestCase):

    def setUp(self):
        super(TestKiddiePool, self).setUp()
        self.pool = KiddiePool([
         'foo:123', 'bar:321'], connection_factory=FakeConnection, connection_options={'tcp_keepalives': False}, max_size=2, pool_timeout=0.1, connect_attempts=2)

    def test_max_size_and_pool_timeout(self):
        self.pool.get()
        self.pool.get()
        start = time.time()
        self.assertRaises(KiddiePoolEmpty, self.pool.get)
        self.assertTrue(time.time() - start > self.pool.pool_timeout)

    def test_connect_attempts(self):
        conn = FakeConnection()
        with patch.object(conn, 'connect') as (mock_connect):
            mock_connect.return_value = False
            with self.assertRaises(KiddiePoolMaxAttempts):
                self.pool._connect(conn)
            self.assertEqual(sorted(mock_connect.call_args_list), sorted([
             call('foo', 123),
             call('foo', 123),
             call('bar', 321),
             call('bar', 321)]))

    def test_connection_options(self):
        self.assertFalse(self.pool.connection_pool.get().tcp_keepalives)

    def test_reset_hosts(self):
        orig_conn1 = self.pool.get()
        orig_conn2 = self.pool.get()
        self.pool.put(orig_conn1)
        self.pool.put(orig_conn2)
        self.pool.set_hosts(['baz:666'])
        conn1 = self.pool.get()
        conn2 = self.pool.get()
        self.assertEqual(conn1.host, 'baz')
        self.assertEqual(conn2.host, 'baz')
        self.assertEqual(conn1.port, 666)
        self.assertEqual(conn2.port, 666)


class TestTidePool(unittest.TestCase):
    """Don't test kazoo. Test the implementation of kazoo, though."""

    def setUp(self):
        super(TestTidePool, self).setUp()
        self.zk_session = FakeKazooClient()
        self.zk_session.start()
        self.tide_pool = TidePool(self.zk_session, 'bar', deferred_bind=True, connection_factory=FakeConnection)

    def test_bind_calls_DataWatch(self):
        self.tide_pool.bind()
        self.assertTrue(self.tide_pool._data_watcher._watcher in self.zk_session._data_watchers['bar'])
        self.assertTrue(self.tide_pool._data_watcher._session_watcher in self.zk_session.state_listeners)
        self.tide_pool.unbind()
        self.assertTrue(self.tide_pool._data_watcher not in self.zk_session._data_watchers['bar'])

    def test_handle_znode_parent_change_calls_ChildrenWatch(self):
        with patch.object(self.zk_session, 'ChildrenWatch') as (mock_watch):
            mock_watch.side_effect = NoNodeError
            self.tide_pool._handle_znode_parent_change('herp,derp', {})
            mock_watch.assert_called_with(self.tide_pool._znode_parent, func=self.tide_pool.set_hosts)
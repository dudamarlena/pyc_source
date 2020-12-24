# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\entransit\common\client.py
# Compiled at: 2008-03-07 16:10:41
"""
$Id: __init__.py 732 2005-01-21 19:43:40Z sidnei $
"""
import os, sys, socket, types
from entransit.common.logger import log, DEBUG
from ZEO.zrpc.client import ConnectionManager
from ZEO.Exceptions import ClientDisconnected
CHUNKSIZE = 1 << 16

class DisconnectedServerStub(object):
    """Internal helper class used as a faux RPC stub when disconnected.

    This raises ClientDisconnected on all attribute accesses.

    This is a singleton class -- there should be only one instance,
    the global disconnected_stub, os it can be tested by identity.
    """
    __module__ = __name__

    def __init__(self, addr):
        self.addr = addr

    def __getattr__(self, attr):
        if attr in ('addr', ):
            return object.__getattribute__(self, attr)
        raise ClientDisconnected(self.addr)


class ServerStub:
    """An RPC stub class for the interface exported by Client.

    This is the interface presented by the Server to the
    Client; i.e. the Client calls these methods and they
    are executed in the Server.

    See the Server module for documentation on these methods.
    """
    __module__ = __name__

    def __init__(self, rpc):
        """Constructor.

        The argument is a connection: an instance of the
        zrpc.connection.Connection class.
        """
        self.rpc = rpc
        while rpc.peer_protocol_version is None:
            rpc.pending()

        return

    def deploy(self, archivefilename, keep=False):
        self.rpc.call('startDeploy')
        archive = open(archivefilename, 'rb')
        try:
            chunk = archive.read(CHUNKSIZE)
            while chunk:
                self.rpc.call('receiveArchiveChunk', chunk)
                chunk = archive.read(CHUNKSIZE)

        finally:
            archive.close()
        if not keep:
            os.remove(archivefilename)
        self.rpc.call('finishDeploy')

    def ping(self):
        self.rpc.call('ping')

    def close(self):
        self.rpc.close()


class Client(object):
    __module__ = __name__
    ConnectionManagerClass = ConnectionManager
    ServerStubClass = ServerStub

    def __init__(self, addr, min_disconnect_poll=5, max_disconnect_poll=300):
        self._rpc_mgr = self.ConnectionManagerClass(addr, self, tmin=min_disconnect_poll, tmax=max_disconnect_poll)
        self._disconnected = self._server = DisconnectedServerStub(addr)
        if not self._rpc_mgr.attempt_connect():
            self._rpc_mgr.connect()

    def notifyConnected(self, conn):
        """Internal: start using the given connection.

        This is called by ConnectionManager after it has decided which
        connection should be used.
        """
        self.set_server_addr(conn.get_addr())
        stub = self.ServerStubClass(conn)
        self._server = stub

    def set_server_addr(self, addr):
        if isinstance(addr, types.StringType):
            self._server_addr = addr
        else:
            assert isinstance(addr, types.TupleType)
            host = addr[0]
            try:
                (canonical, aliases, addrs) = socket.gethostbyaddr(host)
            except socket.error, err:
                log('Error resolving host: %s (%s)' % (host, err), level=DEBUG)
                canonical = host

            self._server_addr = str((canonical, addr[1]))

    def notifyDisconnected(self):
        """Internal: notify that the server connection was terminated.

        This is called by ConnectionManager when the connection is
        closed or when certain problems with the connection occur.
        """
        log('Disconnected from storage: %s' % repr(self._server_addr))
        self._server = self._disconnected

    def testConnection(self, conn):
        return True

    def deploy(self, fpath, keep=False):
        return self._server.deploy(fpath, keep=keep)

    def close(self):
        self._rpc_mgr.close()

    def ping(self):
        self._server.ping()


if __name__ == '__main__':
    from time import time, sleep
    now = time()
    if len(sys.argv) > 2:
        addr = (
         sys.argv[1], int(sys.argv[2]))
    else:
        addr = ('127.0.0.1', 9101)
    handler = Client(addr)
    try:
        try:
            handler.deploy(sys.argv[1], keep=True)
        except:
            import traceback
            traceback.print_exc()
            raw_input('Press a key to continue...')

    finally:
        handler.close()
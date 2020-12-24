# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/tcp.py
# Compiled at: 2017-07-20 12:27:55
"""
TCP Communications Module
"""
import asyncore, socket, errno, cPickle as pickle
from time import time as _time, sleep as _sleep
from StringIO import StringIO
from .debugging import ModuleLogger, DebugContents, bacpypes_debugging
from .core import deferred
from .task import FunctionTask, OneShotFunction
from .comm import PDU, Client, Server
from .comm import ServiceAccessPoint, ApplicationServiceElement
_debug = 0
_log = ModuleLogger(globals())
REBIND_SLEEP_INTERVAL = 2.0
CONNECT_TIMEOUT = 30.0

@bacpypes_debugging
class PickleActorMixIn:

    def __init__(self, *args):
        if _debug:
            PickleActorMixIn._debug('__init__ %r', args)
        super(PickleActorMixIn, self).__init__(*args)
        self.pickleBuffer = ''

    def indication(self, pdu):
        if _debug:
            PickleActorMixIn._debug('indication %r', pdu)
        pdu.pduData = pickle.dumps(pdu.pduData)
        super(PickleActorMixIn, self).indication(pdu)

    def response(self, pdu):
        if _debug:
            PickleActorMixIn._debug('response %r', pdu)
        self.pickleBuffer += pdu.pduData
        strm = StringIO(self.pickleBuffer)
        pos = 0
        while pos < strm.len:
            try:
                msg = pickle.load(strm)
            except:
                break

            rpdu = PDU(msg)
            rpdu.update(pdu)
            super(PickleActorMixIn, self).response(rpdu)
            pos = strm.tell()

        if pos < strm.len:
            self.pickleBuffer = self.pickleBuffer[pos:]
        else:
            self.pickleBuffer = ''


@bacpypes_debugging
class TCPClient(asyncore.dispatcher):
    _connect_timeout = CONNECT_TIMEOUT

    def __init__(self, peer):
        if _debug:
            TCPClient._debug('__init__ %r', peer)
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(0)
        if _debug:
            TCPClient._debug('    - non-blocking')
        self.peer = peer
        self.connected = False
        self.request = ''
        try:
            rslt = self.socket.connect_ex(peer)
            if rslt == 0:
                if _debug:
                    TCPClient._debug('    - connected')
                self.connected = True
            elif rslt == errno.EINPROGRESS:
                if _debug:
                    TCPClient._debug('    - in progress')
            elif rslt == errno.ECONNREFUSED:
                if _debug:
                    TCPClient._debug('    - connection refused')
                self.handle_error(rslt)
            elif _debug:
                TCPClient._debug('    - connect_ex: %r', rslt)
        except socket.error as err:
            if _debug:
                TCPClient._debug('    - connect socket error: %r', err)
            self.handle_error(err)

    def handle_accept(self):
        if _debug:
            TCPClient._debug('handle_accept')

    def handle_connect(self):
        if _debug:
            TCPClient._debug('handle_connect')
        self.connected = True

    def handle_connect_event(self):
        if _debug:
            TCPClient._debug('handle_connect_event')
        err = self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        if _debug:
            TCPClient._debug('    - err: %r', err)
        if err == 0:
            if _debug:
                TCPClient._debug('    - no error')
            self.connected = True
        elif err == errno.ECONNREFUSED:
            if _debug:
                TCPClient._debug('    - connection to %r refused', self.peer)
            self.handle_error(socket.error(errno.ECONNREFUSED, 'connection refused'))
            return
        asyncore.dispatcher.handle_connect_event(self)

    def readable(self):
        return self.connected

    def handle_read(self):
        if _debug:
            TCPClient._debug('handle_read')
        try:
            msg = self.recv(65536)
            if _debug:
                TCPClient._debug('    - received %d octets', len(msg))
            if not self.socket:
                if _debug:
                    TCPClient._debug('    - socket was closed')
            else:
                deferred(self.response, PDU(msg))
        except socket.error as err:
            if err.args[0] == errno.ECONNREFUSED:
                if _debug:
                    TCPClient._debug('    - connection to %r refused', self.peer)
            elif _debug:
                TCPClient._debug('    - recv socket error: %r', err)
            self.handle_error(err)

    def writable(self):
        if not self.connected:
            return True
        return len(self.request) != 0

    def handle_write(self):
        if _debug:
            TCPClient._debug('handle_write')
        try:
            sent = self.send(self.request)
            if _debug:
                TCPClient._debug('    - sent %d octets, %d remaining', sent, len(self.request) - sent)
            self.request = self.request[sent:]
        except socket.error as err:
            if err.args[0] == errno.EPIPE:
                if _debug:
                    TCPClient._debug('    - broken pipe to %r', self.peer)
                return
            if err.args[0] == errno.ECONNREFUSED:
                if _debug:
                    TCPClient._debug('    - connection to %r refused', self.peer)
            elif _debug:
                TCPClient._debug('    - send socket error: %s', err)
            self.handle_error(err)

    def handle_write_event(self):
        if _debug:
            TCPClient._debug('handle_write_event')
        err = self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        if _debug:
            TCPClient._debug('    - err: %r', err)
        if err == 0:
            if not self.connected:
                if _debug:
                    TCPClient._debug('    - connected')
                self.handle_connect()
        else:
            if _debug:
                TCPClient._debug('    - peer: %r', self.peer)
            if err == errno.ECONNREFUSED:
                socket_error = socket.error(err, 'connection refused')
            elif err == errno.ETIMEDOUT:
                socket_error = socket.error(err, 'timed out')
            elif err == errno.EHOSTUNREACH:
                socket_error = socket.error(err, 'host unreachable')
            else:
                socket_error = socket.error(err, 'other unknown: %r' % (err,))
            if _debug:
                TCPClient._debug('    - socket_error: %r', socket_error)
            self.handle_error(socket_error)
            return
        asyncore.dispatcher.handle_write_event(self)

    def handle_close(self):
        if _debug:
            TCPClient._debug('handle_close')
        self.close()
        self.connected = False
        self.socket = None
        return

    def handle_error(self, error=None):
        """Trap for TCPClient errors, otherwise continue."""
        if _debug:
            TCPClient._debug('handle_error %r', error)
        if not self.socket:
            if _debug:
                TCPClient._debug('    - error already handled')
            return
        asyncore.dispatcher.handle_error(self)

    def indication(self, pdu):
        """Requests are queued for delivery."""
        if _debug:
            TCPClient._debug('indication %r', pdu)
        self.request += pdu.pduData


@bacpypes_debugging
class TCPClientActor(TCPClient):

    def __init__(self, director, peer):
        if _debug:
            TCPClientActor._debug('__init__ %r %r', director, peer)
        self.director = None
        self._connection_error = None
        self._connect_timeout = director.connect_timeout
        if self._connect_timeout:
            self.connect_timeout_task = FunctionTask(self.connect_timeout)
            self.connect_timeout_task.install_task(_time() + self._connect_timeout)
        else:
            self.connect_timeout_task = None
        TCPClient.__init__(self, peer)
        self.director = director
        self._idle_timeout = director.idle_timeout
        if self._idle_timeout:
            self.idle_timeout_task = FunctionTask(self.idle_timeout)
            self.idle_timeout_task.install_task(_time() + self._idle_timeout)
        else:
            self.idle_timeout_task = None
        self.flush_task = None
        self.director.add_actor(self)
        if self._connection_error:
            if _debug:
                TCPClientActor._debug('    - had connection error')
            self.director.actor_error(self, self._connection_error)
        return

    def handle_connect(self):
        if _debug:
            TCPClientActor._debug('handle_connect')
        if self.connected:
            if _debug:
                TCPClientActor._debug('    - already connected')
            return
        if self.connect_timeout_task:
            if _debug:
                TCPClientActor._debug('    - canceling connection timeout')
            self.connect_timeout_task.suspend_task()
            self.connect_timeout_task = None
        TCPClient.handle_connect(self)
        return

    def handle_error(self, error=None):
        """Trap for TCPClient errors, otherwise continue."""
        if _debug:
            TCPClientActor._debug('handle_error %r', error)
        if error is not None:
            if not self.director:
                self._connection_error = error
            else:
                self.director.actor_error(self, error)
        else:
            TCPClient.handle_error(self)
        return

    def handle_close(self):
        if _debug:
            TCPClientActor._debug('handle_close')
        if self.flush_task:
            self.flush_task.suspend_task()
        if self.connect_timeout_task:
            if _debug:
                TCPClientActor._debug('    - canceling connection timeout')
            self.connect_timeout_task.suspend_task()
            self.connect_timeout_task = None
        if self.idle_timeout_task:
            if _debug:
                TCPClientActor._debug('    - canceling idle timeout')
            self.idle_timeout_task.suspend_task()
            self.idle_timeout_task = None
        self.director.del_actor(self)
        TCPClient.handle_close(self)
        return

    def connect_timeout(self):
        if _debug:
            TCPClientActor._debug('connect_timeout')
        self.handle_close()

    def idle_timeout(self):
        if _debug:
            TCPClientActor._debug('idle_timeout')
        self.handle_close()

    def indication(self, pdu):
        if _debug:
            TCPClientActor._debug('indication %r', pdu)
        if self.flush_task:
            if _debug:
                TCPServerActor._debug('    - flushing')
            return
        if self.idle_timeout_task:
            self.idle_timeout_task.install_task(_time() + self._idle_timeout)
        TCPClient.indication(self, pdu)

    def response(self, pdu):
        if _debug:
            TCPClientActor._debug('response %r', pdu)
        pdu.pduSource = self.peer
        if self.idle_timeout_task:
            self.idle_timeout_task.install_task(_time() + self._idle_timeout)
        self.director.response(pdu)

    def flush(self):
        if _debug:
            TCPClientActor._debug('flush')
        self.flush_task = None
        if self.request:
            self.flush_task = OneShotFunction(self.flush)
            return
        else:
            self.handle_close()
            return


class TCPPickleClientActor(PickleActorMixIn, TCPClientActor):
    pass


@bacpypes_debugging
class TCPClientDirector(Server, ServiceAccessPoint, DebugContents):
    _debug_contents = ('connect_timeout', 'idle_timeout', 'actorClass', 'clients',
                       'reconnect')

    def __init__(self, connect_timeout=None, idle_timeout=None, actorClass=TCPClientActor, sid=None, sapID=None):
        if _debug:
            TCPClientDirector._debug('__init__ connect_timeout=%r idle_timeout=%r actorClass=%r sid=%r sapID=%r', connect_timeout, idle_timeout, actorClass, sid, sapID)
        Server.__init__(self, sid)
        ServiceAccessPoint.__init__(self, sapID)
        if not issubclass(actorClass, TCPClientActor):
            raise TypeError('actorClass must be a subclass of TCPClientActor')
        self.actorClass = actorClass
        self.connect_timeout = connect_timeout
        self.idle_timeout = idle_timeout
        self.clients = {}
        self.reconnect = {}

    def add_actor(self, actor):
        """Add an actor when a new one is connected."""
        if _debug:
            TCPClientDirector._debug('add_actor %r', actor)
        self.clients[actor.peer] = actor
        if self.serviceElement:
            self.sap_request(add_actor=actor)

    def del_actor(self, actor):
        """Remove an actor when the socket is closed."""
        if _debug:
            TCPClientDirector._debug('del_actor %r', actor)
        del self.clients[actor.peer]
        if self.serviceElement:
            self.sap_request(del_actor=actor)
        if actor.peer in self.reconnect:
            connect_task = FunctionTask(self.connect, actor.peer)
            connect_task.install_task(_time() + self.reconnect[actor.peer])

    def actor_error(self, actor, error):
        if _debug:
            TCPClientDirector._debug('actor_error %r %r', actor, error)
        if self.serviceElement:
            self.sap_request(actor_error=actor, error=error)

    def get_actor(self, address):
        """ Get the actor associated with an address or None. """
        return self.clients.get(address, None)

    def connect(self, address, reconnect=0):
        if _debug:
            TCPClientDirector._debug('connect %r reconnect=%r', address, reconnect)
        if address in self.clients:
            return
        client = self.actorClass(self, address)
        if _debug:
            TCPClientDirector._debug('    - client: %r', client)
        if reconnect:
            self.reconnect[address] = reconnect

    def disconnect(self, address):
        if _debug:
            TCPClientDirector._debug('disconnect %r', address)
        if address not in self.clients:
            return
        if address in self.reconnect:
            del self.reconnect[address]
        self.clients[address].handle_close()

    def indication(self, pdu):
        """Direct this PDU to the appropriate server, create a
        connection if one hasn't already been created."""
        if _debug:
            TCPClientDirector._debug('indication %r', pdu)
        addr = pdu.pduDestination
        client = self.clients.get(addr, None)
        if not client:
            client = self.actorClass(self, addr)
        client.indication(pdu)
        return


@bacpypes_debugging
class TCPServer(asyncore.dispatcher):

    def __init__(self, sock, peer):
        if _debug:
            TCPServer._debug('__init__ %r %r', sock, peer)
        asyncore.dispatcher.__init__(self, sock)
        self.peer = peer
        self.request = ''

    def handle_connect(self):
        if _debug:
            TCPServer._debug('handle_connect')

    def readable(self):
        return self.connected

    def handle_read(self):
        if _debug:
            TCPServer._debug('handle_read')
        try:
            msg = self.recv(65536)
            if _debug:
                TCPServer._debug('    - received %d octets', len(msg))
            if not self.socket:
                if _debug:
                    TCPServer._debug('    - socket was closed')
            else:
                deferred(self.response, PDU(msg))
        except socket.error as err:
            if err.args[0] == errno.ECONNREFUSED:
                if _debug:
                    TCPServer._debug('    - connection to %r refused', self.peer)
            elif _debug:
                TCPServer._debug('    - recv socket error: %r', err)
            self.handle_error(err)

    def writable(self):
        return len(self.request) != 0

    def handle_write(self):
        if _debug:
            TCPServer._debug('handle_write')
        try:
            sent = self.send(self.request)
            if _debug:
                TCPServer._debug('    - sent %d octets, %d remaining', sent, len(self.request) - sent)
            self.request = self.request[sent:]
        except socket.error as err:
            if err.args[0] == errno.ECONNREFUSED:
                if _debug:
                    TCPServer._debug('    - connection to %r refused', self.peer)
            elif _debug:
                TCPServer._debug('    - send socket error: %s', err)
            self.handle_error(err)

    def handle_close(self):
        if _debug:
            TCPServer._debug('handle_close')
        if not self:
            if _debug:
                TCPServer._debug('    - self is None')
            return
        if not self.socket:
            if _debug:
                TCPServer._debug('    - socket already closed')
            return
        self.close()
        self.socket = None
        return

    def handle_error(self, error=None):
        """Trap for TCPServer errors, otherwise continue."""
        if _debug:
            TCPServer._debug('handle_error %r', error)
        asyncore.dispatcher.handle_error(self)

    def indication(self, pdu):
        """Requests are queued for delivery."""
        if _debug:
            TCPServer._debug('indication %r', pdu)
        self.request += pdu.pduData


@bacpypes_debugging
class TCPServerActor(TCPServer):

    def __init__(self, director, sock, peer):
        if _debug:
            TCPServerActor._debug('__init__ %r %r %r', director, sock, peer)
        TCPServer.__init__(self, sock, peer)
        self.director = director
        self._idle_timeout = director.idle_timeout
        if self._idle_timeout:
            self.idle_timeout_task = FunctionTask(self.idle_timeout)
            self.idle_timeout_task.install_task(_time() + self._idle_timeout)
        else:
            self.idle_timeout_task = None
        self.flush_task = None
        self.director.add_actor(self)
        return

    def handle_error(self, error=None):
        """Trap for TCPServer errors, otherwise continue."""
        if _debug:
            TCPServerActor._debug('handle_error %r', error)
        if error is not None:
            self.director.actor_error(self, error)
        else:
            TCPServer.handle_error(self)
        return

    def handle_close(self):
        if _debug:
            TCPServerActor._debug('handle_close')
        if self.flush_task:
            self.flush_task.suspend_task()
        if self.idle_timeout_task:
            if _debug:
                TCPServerActor._debug('    - canceling idle timeout')
            self.idle_timeout_task.suspend_task()
            self.idle_timeout_task = None
        self.director.del_actor(self)
        TCPServer.handle_close(self)
        return

    def idle_timeout(self):
        if _debug:
            TCPServerActor._debug('idle_timeout')
        self.handle_close()

    def indication(self, pdu):
        if _debug:
            TCPServerActor._debug('indication %r', pdu)
        if self.flush_task:
            if _debug:
                TCPServerActor._debug('    - flushing')
            return
        if self.idle_timeout_task:
            self.idle_timeout_task.install_task(_time() + self._idle_timeout)
        TCPServer.indication(self, pdu)

    def response(self, pdu):
        if _debug:
            TCPServerActor._debug('response %r', pdu)
        if self.flush_task:
            if _debug:
                TCPServerActor._debug('    - flushing')
            return
        pdu.pduSource = self.peer
        if self.idle_timeout_task:
            self.idle_timeout_task.install_task(_time() + self._idle_timeout)
        self.director.response(pdu)

    def flush(self):
        if _debug:
            TCPServerActor._debug('flush')
        self.flush_task = None
        if self.request:
            self.flush_task = OneShotFunction(self.flush)
            return
        else:
            self.handle_close()
            return


class TCPPickleServerActor(PickleActorMixIn, TCPServerActor):
    pass


@bacpypes_debugging
class TCPServerDirector(asyncore.dispatcher, Server, ServiceAccessPoint, DebugContents):
    _debug_contents = ('port', 'idle_timeout', 'actorClass', 'servers')

    def __init__(self, address, listeners=5, idle_timeout=0, reuse=False, actorClass=TCPServerActor, cid=None, sapID=None):
        if _debug:
            TCPServerDirector._debug('__init__ %r listeners=%r idle_timeout=%r reuse=%r actorClass=%r cid=%r sapID=%r', address, listeners, idle_timeout, reuse, actorClass, cid, sapID)
        Server.__init__(self, cid)
        ServiceAccessPoint.__init__(self, sapID)
        self.port = address
        self.idle_timeout = idle_timeout
        if not issubclass(actorClass, TCPServerActor):
            raise TypeError('actorClass must be a subclass of TCPServerActor')
        self.actorClass = actorClass
        self.servers = {}
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        if reuse:
            self.set_reuse_addr()
        hadBindErrors = False
        for i in range(30):
            try:
                self.bind(address)
                break
            except socket.error as err:
                hadBindErrors = True
                TCPServerDirector._warning('bind error %r, sleep and try again', err)
                _sleep(REBIND_SLEEP_INTERVAL)

        else:
            TCPServerDirector._error('unable to bind')
            raise RuntimeError('unable to bind')

        if hadBindErrors:
            TCPServerDirector._info('bind successful')
        self.listen(listeners)

    def handle_accept(self):
        if _debug:
            TCPServerDirector._debug('handle_accept')
        try:
            client, addr = self.accept()
        except socket.error:
            TCPServerDirector._warning('accept() threw an exception')
            return
        except TypeError:
            TCPServerDirector._warning('accept() threw EWOULDBLOCK')
            return

        if _debug:
            TCPServerDirector._debug('    - connection %r, %r', client, addr)
        server = self.actorClass(self, client, addr)
        self.servers[addr] = server
        return server

    def handle_close(self):
        if _debug:
            TCPServerDirector._debug('handle_close')
        self.close()

    def add_actor(self, actor):
        if _debug:
            TCPServerDirector._debug('add_actor %r', actor)
        self.servers[actor.peer] = actor
        if self.serviceElement:
            self.sap_request(add_actor=actor)

    def del_actor(self, actor):
        if _debug:
            TCPServerDirector._debug('del_actor %r', actor)
        try:
            del self.servers[actor.peer]
        except KeyError:
            TCPServerDirector._warning('del_actor: %r not an actor', actor)

        if self.serviceElement:
            self.sap_request(del_actor=actor)

    def actor_error(self, actor, error):
        if _debug:
            TCPServerDirector._debug('actor_error %r %r', actor, error)
        if self.serviceElement:
            self.sap_request(actor_error=actor, error=error)

    def get_actor(self, address):
        """ Get the actor associated with an address or None. """
        return self.servers.get(address, None)

    def indication(self, pdu):
        """Direct this PDU to the appropriate server."""
        if _debug:
            TCPServerDirector._debug('indication %r', pdu)
        addr = pdu.pduDestination
        server = self.servers.get(addr, None)
        if not server:
            raise RuntimeError('not a connected server')
        server.indication(pdu)
        return


@bacpypes_debugging
class StreamToPacket(Client, Server):

    def __init__(self, fn, cid=None, sid=None):
        if _debug:
            StreamToPacket._debug('__init__ %r cid=%r, sid=%r', fn, cid, sid)
        Client.__init__(self, cid)
        Server.__init__(self, sid)
        self.packetFn = fn
        self.upstreamBuffer = {}
        self.downstreamBuffer = {}

    def packetize(self, pdu, streamBuffer):
        if _debug:
            StreamToPacket._debug('packetize %r ...', pdu)

        def chop(addr):
            if _debug:
                StreamToPacket._debug('chop %r', addr)
            buff = streamBuffer.get(addr, '') + pdu.pduData
            if _debug:
                StreamToPacket._debug('    - buff: %r', buff)
            while 1:
                packet = self.packetFn(buff)
                if _debug:
                    StreamToPacket._debug('    - packet: %r', packet)
                if packet is None:
                    break
                yield PDU(packet[0], source=pdu.pduSource, destination=pdu.pduDestination, user_data=pdu.pduUserData)
                buff = packet[1]

            streamBuffer[addr] = buff
            return

        if pdu.pduSource:
            for pdu in chop(pdu.pduSource):
                yield pdu

        if pdu.pduDestination:
            for pdu in chop(pdu.pduDestination):
                yield pdu

    def indication(self, pdu):
        """Message going downstream."""
        if _debug:
            StreamToPacket._debug('indication %r', pdu)
        for packet in self.packetize(pdu, self.downstreamBuffer):
            self.request(packet)

    def confirmation(self, pdu):
        """Message going upstream."""
        if _debug:
            StreamToPacket._debug('StreamToPacket.confirmation %r', pdu)
        for packet in self.packetize(pdu, self.upstreamBuffer):
            self.response(packet)


@bacpypes_debugging
class StreamToPacketSAP(ApplicationServiceElement, ServiceAccessPoint):

    def __init__(self, stp, aseID=None, sapID=None):
        if _debug:
            StreamToPacketSAP._debug('__init__ %r aseID=%r, sapID=%r', stp, aseID, sapID)
        ApplicationServiceElement.__init__(self, aseID)
        ServiceAccessPoint.__init__(self, sapID)
        self.stp = stp

    def indication(self, add_actor=None, del_actor=None, actor_error=None, error=None):
        if _debug:
            StreamToPacketSAP._debug('indication add_actor=%r del_actor=%r', add_actor, del_actor)
        if add_actor:
            self.stp.upstreamBuffer[add_actor.peer] = ''
            self.stp.downstreamBuffer[add_actor.peer] = ''
        if del_actor:
            del self.stp.upstreamBuffer[del_actor.peer]
            del self.stp.downstreamBuffer[del_actor.peer]
        if self.serviceElement:
            self.sap_request(add_actor=add_actor, del_actor=del_actor, actor_error=actor_error, error=error)
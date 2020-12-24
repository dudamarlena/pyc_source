# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/udp.py
# Compiled at: 2020-01-29 15:49:52
"""
UDP Communications Module
"""
import asyncore, socket, cPickle as pickle, Queue as queue
from time import time as _time
from .debugging import ModuleLogger, bacpypes_debugging
from .core import deferred
from .task import FunctionTask
from .comm import PDU, Server
from .comm import ServiceAccessPoint
_debug = 0
_log = ModuleLogger(globals())

@bacpypes_debugging
class UDPActor:

    def __init__(self, director, peer):
        if _debug:
            UDPActor._debug('__init__ %r %r', director, peer)
        self.director = director
        self.peer = peer
        self.timeout = director.timeout
        if self.timeout > 0:
            self.timer = FunctionTask(self.idle_timeout)
            self.timer.install_task(_time() + self.timeout)
        else:
            self.timer = None
        self.director.add_actor(self)
        return

    def idle_timeout(self):
        if _debug:
            UDPActor._debug('idle_timeout')
        self.director.del_actor(self)

    def indication(self, pdu):
        if _debug:
            UDPActor._debug('indication %r', pdu)
        if self.timer:
            self.timer.install_task(_time() + self.timeout)
        self.director.request.put(pdu)

    def response(self, pdu):
        if _debug:
            UDPActor._debug('response %r', pdu)
        if self.timer:
            self.timer.install_task(_time() + self.timeout)
        self.director.response(pdu)

    def handle_error(self, error=None):
        if _debug:
            UDPActor._debug('handle_error %r', error)
        if error is not None:
            self.director.actor_error(self, error)
        return


@bacpypes_debugging
class UDPPickleActor(UDPActor):

    def __init__(self, *args):
        if _debug:
            UDPPickleActor._debug('__init__ %r', args)
        UDPActor.__init__(self, *args)

    def indication(self, pdu):
        if _debug:
            UDPPickleActor._debug('indication %r', pdu)
        pdu.pduData = pickle.dumps(pdu.pduData)
        UDPActor.indication(self, pdu)

    def response(self, pdu):
        if _debug:
            UDPPickleActor._debug('response %r', pdu)
        try:
            pdu.pduData = pickle.loads(pdu.pduData)
        except:
            UDPPickleActor._exception('pickle error')
            return

        UDPActor.response(self, pdu)


@bacpypes_debugging
class UDPDirector(asyncore.dispatcher, Server, ServiceAccessPoint):

    def __init__(self, address, timeout=0, reuse=False, actorClass=UDPActor, sid=None, sapID=None):
        if _debug:
            UDPDirector._debug('__init__ %r timeout=%r reuse=%r actorClass=%r sid=%r sapID=%r', address, timeout, reuse, actorClass, sid, sapID)
        Server.__init__(self, sid)
        ServiceAccessPoint.__init__(self, sapID)
        if not issubclass(actorClass, UDPActor):
            raise TypeError('actorClass must be a subclass of UDPActor')
        self.actorClass = actorClass
        self.timeout = timeout
        self.address = address
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        if reuse:
            self.set_reuse_addr()
        try:
            self.bind(address)
        except socket.error as err:
            if _debug:
                UDPDirector._debug('    - bind error: %r', err)
            self.close()
            raise

        if _debug:
            UDPDirector._debug('    - getsockname: %r', self.socket.getsockname())
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.request = queue.Queue()
        self.peers = {}

    def add_actor(self, actor):
        """Add an actor when a new one is connected."""
        if _debug:
            UDPDirector._debug('add_actor %r', actor)
        self.peers[actor.peer] = actor
        if self.serviceElement:
            self.sap_request(add_actor=actor)

    def del_actor(self, actor):
        """Remove an actor when the socket is closed."""
        if _debug:
            UDPDirector._debug('del_actor %r', actor)
        del self.peers[actor.peer]
        if self.serviceElement:
            self.sap_request(del_actor=actor)

    def actor_error(self, actor, error):
        if _debug:
            UDPDirector._debug('actor_error %r %r', actor, error)
        if self.serviceElement:
            self.sap_request(actor_error=actor, error=error)

    def get_actor(self, address):
        return self.peers.get(address, None)

    def handle_connect(self):
        if _debug:
            UDPDirector._debug('handle_connect')

    def readable(self):
        return 1

    def handle_read(self):
        if _debug:
            UDPDirector._debug('handle_read')
        try:
            msg, addr = self.socket.recvfrom(65536)
            if _debug:
                UDPDirector._debug('    - received %d octets from %s', len(msg), addr)
            deferred(self._response, PDU(msg, source=addr))
        except socket.timeout as err:
            if _debug:
                UDPDirector._debug('    - socket timeout: %s', err)
        except socket.error as err:
            if err.args[0] == 11:
                pass
            else:
                if _debug:
                    UDPDirector._debug('    - socket error: %s', err)
                self.handle_error(err)

    def writable(self):
        """Return true iff there is a request pending."""
        return not self.request.empty()

    def handle_write(self):
        """get a PDU from the queue and send it."""
        if _debug:
            UDPDirector._debug('handle_write')
        try:
            pdu = self.request.get()
            sent = self.socket.sendto(pdu.pduData, pdu.pduDestination)
            if _debug:
                UDPDirector._debug('    - sent %d octets to %s', sent, pdu.pduDestination)
        except socket.error as err:
            if _debug:
                UDPDirector._debug('    - socket error: %s', err)
            peer = self.peers.get(pdu.pduDestination, None)
            if peer:
                peer.handle_error(err)
            else:
                self.handle_error(err)

        return

    def close_socket(self):
        """Close the socket."""
        if _debug:
            UDPDirector._debug('close_socket')
        self.socket.close()
        self.close()
        self.socket = None
        return

    def handle_close(self):
        """Remove this from the monitor when it's closed."""
        if _debug:
            UDPDirector._debug('handle_close')
        self.close()
        self.socket = None
        return

    def handle_error(self, error=None):
        """Handle an error..."""
        if _debug:
            UDPDirector._debug('handle_error %r', error)

    def indication(self, pdu):
        """Client requests are queued for delivery."""
        if _debug:
            UDPDirector._debug('indication %r', pdu)
        addr = pdu.pduDestination
        peer = self.peers.get(addr, None)
        if not peer:
            peer = self.actorClass(self, addr)
        peer.indication(pdu)
        return

    def _response(self, pdu):
        """Incoming datagrams are routed through an actor."""
        if _debug:
            UDPDirector._debug('_response %r', pdu)
        addr = pdu.pduSource
        peer = self.peers.get(addr, None)
        if not peer:
            peer = self.actorClass(self, addr)
        peer.response(pdu)
        return
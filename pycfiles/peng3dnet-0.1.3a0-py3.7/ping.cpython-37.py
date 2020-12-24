# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/peng3dnet/ext/ping.py
# Compiled at: 2017-10-21 08:08:42
# Size of source mod 2**32: 10212 bytes
"""
The ping extension was designed to allow a client to check on various values the server provides without much effort.
It allows the client to check on metrics such as latency and additional values able to be customized by the server.

This extension is named after the UNIX :command:`ping` utility, though it can do much more than just check on availability and latency.
"""
import time, threading
from ..constants import *
from .. import version
from .. import net
from .. import errors
from .. import conntypes
WRITEBACK = True

class PingConnectionType(conntypes.ConnectionType):
    __doc__ = '\n    Connection type to be used by ping connections.\n    \n    This connection type prevents any synchronization of the registry to allow\n    clients only supporting a subset of the peng3dnet protocol to still ping a server.\n    \n    Additonally, conventional processing of packets will be disabled by this connection type,\n    making it uneccessary to register packets with the client or server.\n    '

    def init(self, cid):
        """
        Called whenever a new ping connection is established.
        
        On the client, this calls :py:meth:`PingableClientMixin._ping()` and updates
        the connection state, while on the server only the connection state is updated.
        """
        if cid is None:
            self.peer._ping()
            self.peer.remote_state = STATE_ACTIVE
        else:
            self.peer.clients[cid].state = STATE_ACTIVE

    def receive(self, msg, pid, flags, cid):
        """
        Called whenever a packet is received via this connection type.
        
        Handles any ping requests and pong answers and always returns ``True`` to skip any further processing.
        """
        if pid == 64:
            if cid is None:
                self.peer.close_connection(cid, 'pinginvalidside')
            else:
                self.peer.clients[cid].mode = MODE_PING
                if WRITEBACK:
                    data = {'oldmsg': msg}
                else:
                    data = {}
            if hasattr(self.peer, 'getPingData'):
                if callable(self.peer.getPingData):
                    data.update(self.peer.getPingData(msg, cid))
            if hasattr(self.peer, 'pingdata'):
                data.update(self.peer.pingdata)
            data.update(self.getPingData(msg, cid))
            self.peer.send_message(65, data, cid)
        else:
            if pid == 65:
                if cid is not None:
                    self.peer.close_connection(cid, 'pinginvalidside')
                try:
                    if hasattr(self.peer, 'on_pong'):
                        if callable(self.peer.on_pong):
                            self.peer.on_pong(msg)
                    self.peer._pong(msg)
                finally:
                    self.peer.close_connection(reason='pingcomplete')

            else:
                self.peer.close_connection(cid, 'invalidpingpacket')
        return True

    def send(self, msg, pid, cid):
        """
        Called whenever a packet is sent via this connection type.
        """
        if pid == 64:
            self.peer.mode = MODE_PING
        else:
            if pid == 65:
                pass
            else:
                raise ValueError('Invalid packet id %s detected' % pid)
            return True

    def getPingData(self, msg, cid=None):
        """
        Overridable method to create a ping response.
        
        ``msg`` is the ping query, as received from the client.
        
        ``cid`` is the ID of the client.
        
        Called only on the server side.
        """
        return {'peng3dnet': {'version':version.VERSION,  'release':version.RELEASE,  'protoversion':version.PROTOVERSION}}


class PingableServerMixin(object):
    __doc__ = '\n    Mixin for :py:class:`~peng3dnet.net.Server` classes enabling support for pinging the server.\n    \n    Currently automatically adds the ``ping`` connection type.\n    '
    pingdata = {}

    def getPingData(self, msg, cid):
        """
        Overrideable method called to extend the default dictionary returned upon a ping request.
        
        May be overriden to add dynamic data like user count or similiar information.
        
        ``msg`` is the original message as received from the client.
        
        ``cid`` is the client ID that made this request.
        """
        return {}

    def _reg_conntypes_ping(self):
        self.addConnType('ping', PingConnectionType(self))


class PingableClientMixin(object):
    __doc__ = '\n    Mixin for :py:class:`~peng3dnet.net.Client` classes enabling support for pinging the server.\n    \n    Currently automatically adds the ``ping`` connection type.\n    '
    _pingdata = None
    _pongdata = None
    _pong_condition = threading.Condition()

    def _reg_conntypes_ping(self):
        self.addConnType('ping', PingConnectionType(self))

    def setPingData(self, d):
        """
        Sets the data to add to any ping responses.
        
        Repeated calls of this method will overwrite previous data.
        """
        self._pingdata = d

    def _ping(self):
        """
        Handler called by :py:meth:`PingConnectionType.init()` when a ping connection is established.
        
        By default, this sends a ping packet to the server.
        """
        if self._pingdata['time'] == '__AUTO__':
            self._pingdata['time'] = time.time()
        self.send_message(64, self._pingdata)

    def _pong(self, data):
        with self._pong_condition:
            self._pongdata = data
            self._pong_condition.notify_all()

    def wait_for_pong(self, timeout=None):
        """
        Waits up to ``timeout`` seconds for a ping response to arrive.
        
        If a response has already been received, this method returns immediately.
        
        If the ping was successful, the received message is returned.
        """
        with self._pong_condition:
            if self._pongdata is not None:
                return self._pongdata
            if not self._pong_condition.wait_for(lambda : self._pongdata is not None, timeout):
                raise errors.FailedPingError('Timed out')
            return self._pongdata


class _PingClient(PingableClientMixin, net.Client):
    pass


def pingServer(peng=None, addr=None, cfg=None, data=None, clientcls=_PingClient, timeout=10.0):
    r"""
    Pings the specified server.
    
    Internally, this creates a client that supports pinging and listens for any data received back.
    
    ``peng`` may be optionally used to replace the argument of the same name to :py:class:`~peng3dnet.net.Client()`\ .
    
    ``addr`` specifies the address of the server to ping.
    
    ``cfg`` may be used to override the configuration for the client, e.g. SSL settings.
    
    ``data`` is the data sent to the server. Note that the ``time`` key will be overridden for measuring the latency.
    
    ``clientcls`` may be used to override the client class used.
    
    ``timeout`` is maximum amount of time to wait for a response.
    
    The data returned will be the data received from the server, except for
    additional information that has been added. Currently, the ``recvtime`` key
    contains the timestamp that the response was received and the ``delay`` key
    contains the total roundtrip time in seconds.
    """
    cfg = cfg if cfg is not None else {}
    data = data if data is not None else {}
    client = clientcls(peng, addr, cfg, CONNTYPE_PING)
    data['time'] = '__AUTO__'
    client.setPingData(data)
    d = {'data': None}

    def on_pong(msg):
        data = msg
        data['recvtime'] = time.time()
        d['data'] = data
        client.close_connection('pingcomplete')

    client.on_pong = on_pong
    client.runAsync()
    client.process_async()
    client.wait_for_pong(timeout)
    data = d['data']
    if data is None:
        raise errors.FailedPingError('No answer received')
    data['delay'] = data['recvtime'] - data['oldmsg']['time']
    return data
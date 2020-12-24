# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.15/lib/python2.7/site-packages/coolamqp/uplink/connection/connection.py
# Compiled at: 2020-04-03 16:00:47
from __future__ import absolute_import, division, print_function
import collections, logging, socket, time, typing as tp, uuid, monotonic
from coolamqp.exceptions import ConnectionDead
from coolamqp.framing.base import AMQPMethodPayload
from coolamqp.framing.definitions import ConnectionClose, ConnectionCloseOk
from coolamqp.framing.frames import AMQPMethodFrame
from coolamqp.objects import Callable
from coolamqp.uplink.connection.recv_framer import ReceivingFramer
from coolamqp.uplink.connection.send_framer import SendingFramer
from coolamqp.uplink.connection.states import ST_ONLINE, ST_OFFLINE, ST_CONNECTING
from coolamqp.uplink.connection.watches import MethodWatch
from coolamqp.uplink.handshake import Handshaker
logger = logging.getLogger(__name__)

def alert_watches(watches, trigger):
    """
    Notify all watches in this collection.

    Return a list of alive watches.
    :param watches: list of Watch
    :return: tuple of (list of Watch, bool - was any watch fired?)
    """
    watch_handled = False
    alive_watches = []
    while len(watches) > 0:
        watch = watches.pop()
        if watch.cancelled:
            continue
        watch_triggered = watch.is_triggered_by(trigger)
        watch_handled |= watch_triggered
        if watch.cancelled:
            continue
        if not any((watch_triggered, watch.oneshot, watch.cancelled)):
            alive_watches.append(watch)
        elif not watch.oneshot and not watch.cancelled:
            alive_watches.append(watch)
        elif watch.oneshot and not watch_triggered:
            alive_watches.append(watch)

    if set(alive_watches) != set(watches):
        for removed_watch in set(watches) - set(alive_watches):
            logger.debug('Removing watch %s', repr(removed_watch))

    return (
     alive_watches, watch_handled)


class Connection(object):
    """
    An object that manages a connection in a comprehensive way.

    It allows for sending and registering watches for particular things. Watch will
    listen for eg. frame on particular channel, frame on any channel, or connection teardown.
    Watches will also get a callback for connection being non-operational (eg. torn down).

    WARNING: Thread-safety of watch operation hinges on atomicity
    of .append and .pop.

    Lifecycle of connection is such:

        Connection created  ->  state is ST_CONNECTING
        .start() called     ->  state is ST_CONNECTING
        connection.open-ok  ->  state is ST_ONLINE

    This logger is talkative mostly on INFO, and regarding connection state
    """

    def __init__(self, node_definition, listener_thread, extra_properties, log_frames=None, name=None):
        """
        Create an object that links to an AMQP broker.

        No data will be physically sent until you hit .start()

        :param node_definition: NodeDefinition instance to use
        :param listener_thread: ListenerThread to use as async engine
        :type listener_thread: coolamqp.uplink.listener.ListenerThread
        :param extra_properties: extra properties to send to the target server
            must conform to the syntax given in (/coolamqp/uplink/handshake.py)'s CLIENT_PROPERTIES
        """
        self.listener_thread = listener_thread
        self.node_definition = node_definition
        self.uuid = uuid.uuid4().hex[:5]
        self.name = name or 'CoolAMQP'
        self.recvf = ReceivingFramer(self.on_frame)
        self.extra_properties = extra_properties
        self.watches = {}
        self.any_watches = []
        self.finalize = Callable(oneshots=True)
        self.state = ST_CONNECTING
        self.callables_on_connected = []
        self.free_channels = []
        self.frame_max = None
        self.heartbeat = None
        self.extensions = []
        self.listener_socket = None
        self.sendf = None
        self.log_frames = log_frames
        return

    def call_on_connected(self, callable):
        """
        Register a callable to be called when this links to the server.

        If you call it while the connection IS up, callable will be called even before this returns.

        You should be optimally an attached attache to receive this.

        :param callable: callable/0 to call
        """
        if self.state == ST_ONLINE:
            callable()
        else:
            self.callables_on_connected.append(callable)

    def on_connected(self):
        """Called by handshaker upon reception of final connection.open-ok"""
        logger.info('[%s] Connection ready.', self.name)
        self.state = ST_ONLINE
        while len(self.callables_on_connected) > 0:
            self.callables_on_connected.pop()()

    def start(self, timeout):
        """
        Start processing events for this connect. Create the socket,
        transmit 'AMQP\x00\x00        \x01' and roll.

        Warning: This will block for as long as the TCP connection setup takes.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        start_at = monotonic.monotonic()
        while True:
            try:
                sock.connect((
                 self.node_definition.host, self.node_definition.port))
            except socket.error as e:
                time.sleep(0.5)
                if monotonic.monotonic() - start_at > timeout:
                    raise ConnectionDead()
            else:
                break

        logger.debug('[%s] TCP connection established, authentication in progress', self.name)
        sock.settimeout(0)
        header = bytearray('AMQP\x00\x00\t\x01')
        rest = sock.send(header)
        while rest < len(header):
            time.sleep(0.1)
            header = header[rest:]
            rest = sock.send(header)

        self.watch_for_method(0, (ConnectionClose, ConnectionCloseOk), self.on_connection_close)
        self.listener_socket = self.listener_thread.register(sock, on_read=self.recvf.put, on_fail=self.on_fail)
        self.sendf = SendingFramer(self.listener_socket.send)
        Handshaker(self, self.node_definition, self.on_connected, self.extra_properties)
        self.listener_thread.activate(self.listener_socket)

    def on_fail(self):
        """
        Called by event loop when the underlying connection is closed.

        This means the connection is dead, cannot be used anymore, and all operations
        running on it now are aborted, null and void.

        This calls fails all registered watches.
        Called by ListenerThread.

        WARNING: Note that .on_fail can get called twice - once from .on_connection_close,
        and second time from ListenerThread when socket is disposed of
        Therefore we need to make sure callbacks are called EXACTLY once
        """
        logger.info('[%s] Connection lost', self.name)
        self.state = ST_OFFLINE
        watchlists = [ self.watches[channel] for channel in self.watches ]
        for watchlist in watchlists:
            for watch in watchlist:
                if not watch.cancelled:
                    watch.failed()

        for watch in self.any_watches:
            if not watch.cancelled:
                watch.failed()

        self.watches = {}
        self.any_watches = []
        self.finalize()

    def on_connection_close(self, payload):
        """
        Server attempted to close the connection.. or maybe we did?

        Called by ListenerThread.
        """
        self.on_fail()
        if isinstance(payload, ConnectionClose):
            self.send([AMQPMethodFrame(0, ConnectionCloseOk())])
            logger.info('[%s] Broker closed our connection - code %s reason %s', self.name, payload.reply_code, payload.reply_text.tobytes().decode('utf8'))
        elif isinstance(payload, ConnectionCloseOk):
            self.send(None)
        return

    def send(self, frames, priority=False):
        """
        Schedule to send some frames.

        Take care: This won't stop you from sending frames larger tham frame_max.
        Broker will probably close the connection if he sees that.

        :param frames: list of frames or None to close the link
        :param reason: optional human-readable reason for this action
        """
        if self.log_frames is not None:
            for frame in frames:
                self.log_frames.on_frame(time.monotonic(), frame, 'to_server')

        if frames is not None:
            self.sendf.send(frames, priority=priority)
        else:
            self.listener_socket.send(None)
        return

    def on_frame(self, frame):
        """
        Called by event loop upon receiving an AMQP frame.

        This will verify all watches on given channel if they were hit,
        and take appropriate action.

        Unhandled frames will be logged - if they were sent, they probably were important.

        :param frame: AMQPFrame that was received
        """
        if self.log_frames is not None:
            self.log_frames.on_frame(time.monotonic(), frame, 'to_client')
        watch_handled = False
        if isinstance(frame, AMQPMethodFrame):
            logger.debug('[%s] Received %s', self.uuid, frame.payload.NAME)
        if frame.channel in self.watches:
            watches = self.watches[frame.channel]
            self.watches[frame.channel] = []
            alive_watches, f = alert_watches(watches, frame)
            watch_handled |= f
            if frame.channel in self.watches:
                for watch in alive_watches:
                    self.watches[frame.channel].append(watch)

        any_watches = self.any_watches
        self.any_watches = []
        alive_watches, f = alert_watches(any_watches, frame)
        watch_handled |= f
        for watch in alive_watches:
            self.any_watches.append(watch)

        if not watch_handled:
            if isinstance(frame, AMQPMethodFrame):
                logger.warning('[%s] Unhandled method frame %s', self.name, repr(frame.payload))
            else:
                logger.warning('[%s] Unhandled frame %s', self.name, frame)
        return

    def watchdog(self, delay, callback):
        """
        Call callback in delay seconds. One-shot.

        Shall the connection die in the meantime, watchdog will not
        be called, and everything will process according to
        ListenerThread's on_fail callback.

        This is necessary to implement timeout detection when setting up the connection
        and heartbeat is not yet configured.
        """
        try:
            self.listener_socket.oneshot(delay, callback)
        except AttributeError:
            pass

    def unwatch_all(self, channel_id):
        """
        Remove all watches from specified channel
        """
        self.watches.pop(channel_id, None)
        return

    def watch(self, watch):
        """
        Register a watch.
        :param watch: Watch to register
        """
        assert self.state != ST_OFFLINE
        if watch.channel is None:
            self.any_watches.append(watch)
        elif watch.channel not in self.watches:
            self.watches[watch.channel] = collections.deque([watch])
        else:
            self.watches[watch.channel].append(watch)
        return

    def watch_for_method(self, channel, method, callback, on_fail=None):
        """
        :param channel: channel to monitor
        :param method: AMQPMethodPayload class or tuple of AMQPMethodPayload classes
        :param callback: callable(AMQPMethodPayload instance)
        :param on_fail: callable/0 to call when this connection fails
        """
        mw = MethodWatch(channel, method, callback, on_end=on_fail)
        self.watch(mw)
        return mw

    def method_and_watch(self, channel_id, method_payload, method_or_methods, callback):
        """
        A syntactic sugar for

                .watch_for_method(channel_id, method_or_methdods, callback)
                .send([AMQPMethodFrame(channel_id, method_payload)])
        """
        watch = self.watch_for_method(channel_id, method_or_methods, callback)
        self.send([AMQPMethodFrame(channel_id, method_payload)])
        return watch
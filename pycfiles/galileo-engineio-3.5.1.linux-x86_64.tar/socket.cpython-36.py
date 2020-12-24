# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/conrad/prog/galileo-engineio/venv/lib/python3.6/site-packages/engineio/socket.py
# Compiled at: 2019-08-30 19:22:57
# Size of source mod 2**32: 9752 bytes
import six, sys, time
from . import exceptions
from . import packet
from . import payload

class Socket(object):
    __doc__ = 'An Engine.IO socket.'
    upgrade_protocols = ['websocket']

    def __init__(self, server, sid):
        self.server = server
        self.sid = sid
        self.queue = self.server.create_queue()
        self.last_ping = time.time()
        self.connected = False
        self.upgrading = False
        self.upgraded = False
        self.packet_backlog = []
        self.closing = False
        self.closed = False
        self.session = {}

    def poll(self):
        """Wait for packets to send to the client."""
        queue_empty = self.server.get_queue_empty_exception()
        try:
            packets = [
             self.queue.get(timeout=(self.server.ping_timeout))]
            self.queue.task_done()
        except queue_empty:
            raise exceptions.QueueEmpty()

        if packets == [None]:
            return []
        else:
            while True:
                try:
                    packets.append(self.queue.get(block=False))
                    self.queue.task_done()
                except queue_empty:
                    break

            return packets

    def receive(self, pkt):
        """Receive packet from the client."""
        packet_name = packet.packet_names[pkt.packet_type] if pkt.packet_type < len(packet.packet_names) else 'UNKNOWN'
        self.server.logger.info('%s: Received packet %s data %s', self.sid, packet_name, pkt.data if not isinstance(pkt.data, bytes) else '<binary>')
        if pkt.packet_type == packet.PING:
            self.last_ping = time.time()
            self.send(packet.Packet(packet.PONG, pkt.data))
        else:
            if pkt.packet_type == packet.MESSAGE:
                self.server._trigger_event('message', (self.sid), (pkt.data), run_async=(self.server.async_handlers))
            else:
                if pkt.packet_type == packet.UPGRADE:
                    self.send(packet.Packet(packet.NOOP))
                else:
                    if pkt.packet_type == packet.CLOSE:
                        self.close(wait=False, abort=True)
                    else:
                        raise exceptions.UnknownPacketError()

    def check_ping_timeout(self):
        """Make sure the client is still sending pings.

        This helps detect disconnections for long-polling clients.
        """
        if self.closed:
            raise exceptions.SocketIsClosedError()
        if time.time() - self.last_ping > self.server.ping_interval + 5:
            self.server.logger.info('%s: Client is gone, closing socket', self.sid)
            self.close(wait=False, abort=False)
            return False
        else:
            return True

    def send(self, pkt):
        """Send a packet to the client."""
        if not self.check_ping_timeout():
            return
        else:
            if self.upgrading:
                self.packet_backlog.append(pkt)
            else:
                self.queue.put(pkt)
        self.server.logger.info('%s: Sending packet %s data %s', self.sid, packet.packet_names[pkt.packet_type], pkt.data if not isinstance(pkt.data, bytes) else '<binary>')

    def handle_get_request(self, environ, start_response):
        """Handle a long-polling GET request from the client."""
        connections = [s.strip() for s in environ.get('HTTP_CONNECTION', '').lower().split(',')]
        transport = environ.get('HTTP_UPGRADE', '').lower()
        if 'upgrade' in connections and transport in self.upgrade_protocols:
            self.server.logger.info('%s: Received request to upgrade to %s', self.sid, transport)
            return getattr(self, '_upgrade_' + transport)(environ, start_response)
        else:
            try:
                packets = self.poll()
            except exceptions.QueueEmpty:
                exc = sys.exc_info()
                self.close(wait=False)
                (six.reraise)(*exc)

            return packets

    def handle_post_request(self, environ):
        """Handle a long-polling POST request from the client."""
        length = int(environ.get('CONTENT_LENGTH', '0'))
        if length > self.server.max_http_buffer_size:
            raise exceptions.ContentTooLongError()
        else:
            body = environ['wsgi.input'].read(length)
            p = payload.Payload(encoded_payload=body)
            for pkt in p.packets:
                self.receive(pkt)

    def close(self, wait=True, abort=False):
        """Close the socket connection."""
        if not self.closed:
            if not self.closing:
                self.closing = True
                self.server._trigger_event('disconnect', (self.sid), run_async=False)
                if not abort:
                    self.send(packet.Packet(packet.CLOSE))
                self.closed = True
                self.queue.put(None)
                if wait:
                    self.queue.join()

    def _upgrade_websocket(self, environ, start_response):
        """Upgrade the connection from polling to websocket."""
        if self.upgraded:
            raise IOError('Socket has been upgraded already')
        if self.server._async['websocket'] is None:
            return self.server._bad_request()
        else:
            ws = self.server._async['websocket'](self._websocket_handler)
            return ws(environ, start_response)

    def _websocket_handler(self, ws):
        """Engine.IO handler for websocket transport."""
        for attr in ('_sock', 'socket'):
            if hasattr(ws, attr) and hasattr(getattr(ws, attr), 'settimeout'):
                getattr(ws, attr).settimeout(self.server.ping_timeout)

        if self.connected:
            self.upgrading = True
            pkt = ws.wait()
            decoded_pkt = packet.Packet(encoded_packet=pkt)
            if decoded_pkt.packet_type != packet.PING or decoded_pkt.data != 'probe':
                self.server.logger.info('%s: Failed websocket upgrade, no PING packet', self.sid)
                return []
            ws.send(packet.Packet((packet.PONG),
              data=(six.text_type('probe'))).encode(always_bytes=False))
            self.queue.put(packet.Packet(packet.NOOP))
            pkt = ws.wait()
            decoded_pkt = packet.Packet(encoded_packet=pkt)
            if decoded_pkt.packet_type != packet.UPGRADE:
                self.upgraded = False
                self.server.logger.info('%s: Failed websocket upgrade, expected UPGRADE packet, received %s instead.', self.sid, pkt)
                return []
            self.upgraded = True
            for pkt in self.packet_backlog:
                self.queue.put(pkt)

            self.packet_backlog = []
            self.upgrading = False
        else:
            self.connected = True
            self.upgraded = True

        def writer():
            while True:
                packets = None
                try:
                    packets = self.poll()
                except exceptions.QueueEmpty:
                    break

                if not packets:
                    break
                try:
                    for pkt in packets:
                        ws.send(pkt.encode(always_bytes=False))

                except:
                    break

        writer_task = self.server.start_background_task(writer)
        self.server.logger.info('%s: Upgrade to websocket successful', self.sid)
        while 1:
            p = None
            try:
                p = ws.wait()
            except Exception as e:
                if not self.closed:
                    self.server.logger.info('%s: Unexpected error "%s", closing connection', self.sid, str(e))
                break

            if p is None:
                break
            if isinstance(p, six.text_type):
                p = p.encode('utf-8')
            pkt = packet.Packet(encoded_packet=p)
            try:
                self.receive(pkt)
            except exceptions.UnknownPacketError:
                pass
            except exceptions.SocketIsClosedError:
                self.server.logger.info('Receive error -- socket is closed')
                break
            except:
                self.server.logger.exception('Unknown receive error')
                break

        self.queue.put(None)
        writer_task.join()
        self.close(wait=False, abort=True)
        return []
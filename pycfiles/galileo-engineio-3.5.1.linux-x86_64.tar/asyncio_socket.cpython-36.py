# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/conrad/prog/galileo-engineio/venv/lib/python3.6/site-packages/engineio/asyncio_socket.py
# Compiled at: 2019-08-30 19:22:57
# Size of source mod 2**32: 9596 bytes
import asyncio, six, sys, time
from . import exceptions
from . import packet
from . import payload
from . import socket

class AsyncSocket(socket.Socket):

    async def poll(self):
        """Wait for packets to send to the client."""
        try:
            packets = [
             await asyncio.wait_for(self.queue.get(), self.server.ping_timeout)]
            self.queue.task_done()
        except (asyncio.TimeoutError, asyncio.CancelledError):
            raise exceptions.QueueEmpty()

        if packets == [None]:
            return []
        else:
            try:
                packets.append(self.queue.get_nowait())
                self.queue.task_done()
            except asyncio.QueueEmpty:
                pass

            return packets

    async def receive(self, pkt):
        """Receive packet from the client."""
        self.server.logger.info('%s: Received packet %s data %s', self.sid, packet.packet_names[pkt.packet_type], pkt.data if not isinstance(pkt.data, bytes) else '<binary>')
        if pkt.packet_type == packet.PING:
            self.last_ping = time.time()
            await self.send(packet.Packet(packet.PONG, pkt.data))
        else:
            if pkt.packet_type == packet.MESSAGE:
                await self.server._trigger_event('message',
                  (self.sid), (pkt.data), run_async=(self.server.async_handlers))
            else:
                if pkt.packet_type == packet.UPGRADE:
                    await self.send(packet.Packet(packet.NOOP))
                else:
                    if pkt.packet_type == packet.CLOSE:
                        await self.close(wait=False, abort=True)
                    else:
                        raise exceptions.UnknownPacketError()

    async def check_ping_timeout(self):
        """Make sure the client is still sending pings.

        This helps detect disconnections for long-polling clients.
        """
        if self.closed:
            raise exceptions.SocketIsClosedError()
        if time.time() - self.last_ping > self.server.ping_interval + 5:
            self.server.logger.info('%s: Client is gone, closing socket', self.sid)
            await self.close(wait=False, abort=False)
            return False
        else:
            return True

    async def send(self, pkt):
        """Send a packet to the client."""
        if not await self.check_ping_timeout():
            return
        else:
            if self.upgrading:
                self.packet_backlog.append(pkt)
            else:
                await self.queue.put(pkt)
        self.server.logger.info('%s: Sending packet %s data %s', self.sid, packet.packet_names[pkt.packet_type], pkt.data if not isinstance(pkt.data, bytes) else '<binary>')

    async def handle_get_request(self, environ):
        """Handle a long-polling GET request from the client."""
        connections = [s.strip() for s in environ.get('HTTP_CONNECTION', '').lower().split(',')]
        transport = environ.get('HTTP_UPGRADE', '').lower()
        if 'upgrade' in connections and transport in self.upgrade_protocols:
            self.server.logger.info('%s: Received request to upgrade to %s', self.sid, transport)
            return await getattr(self, '_upgrade_' + transport)(environ)
        else:
            try:
                packets = await self.poll()
            except exceptions.QueueEmpty:
                exc = sys.exc_info()
                await self.close(wait=False)
                (six.reraise)(*exc)

            return packets

    async def handle_post_request(self, environ):
        """Handle a long-polling POST request from the client."""
        length = int(environ.get('CONTENT_LENGTH', '0'))
        if length > self.server.max_http_buffer_size:
            raise exceptions.ContentTooLongError()
        else:
            body = await environ['wsgi.input'].read(length)
            p = payload.Payload(encoded_payload=body)
            for pkt in p.packets:
                await self.receive(pkt)

    async def close(self, wait=True, abort=False):
        """Close the socket connection."""
        if not self.closed:
            if not self.closing:
                self.closing = True
                await self.server._trigger_event('disconnect', self.sid)
                if not abort:
                    await self.send(packet.Packet(packet.CLOSE))
                self.closed = True
                if wait:
                    await self.queue.join()

    async def _upgrade_websocket(self, environ):
        """Upgrade the connection from polling to websocket."""
        if self.upgraded:
            raise IOError('Socket has been upgraded already')
        if self.server._async['websocket'] is None:
            return self.server._bad_request()
        else:
            ws = self.server._async['websocket'](self._websocket_handler)
            return await ws(environ)

    async def _websocket_handler(self, ws):
        """Engine.IO handler for websocket transport."""
        if self.connected:
            self.upgrading = True
            try:
                pkt = await ws.wait()
            except IOError:
                return

            decoded_pkt = packet.Packet(encoded_packet=pkt)
            if decoded_pkt.packet_type != packet.PING or decoded_pkt.data != 'probe':
                self.server.logger.info('%s: Failed websocket upgrade, no PING packet', self.sid)
                return
            await ws.send(packet.Packet((packet.PONG),
              data=(six.text_type('probe'))).encode(always_bytes=False))
            await self.queue.put(packet.Packet(packet.NOOP))
            try:
                pkt = await ws.wait()
            except IOError:
                return
            else:
                decoded_pkt = packet.Packet(encoded_packet=pkt)
                if decoded_pkt.packet_type != packet.UPGRADE:
                    self.upgraded = False
                    self.server.logger.info('%s: Failed websocket upgrade, expected UPGRADE packet, received %s instead.', self.sid, pkt)
                    return
                self.upgraded = True
                for pkt in self.packet_backlog:
                    await self.queue.put(pkt)

            self.packet_backlog = []
            self.upgrading = False
        else:
            self.connected = True
            self.upgraded = True

        async def writer():
            while True:
                packets = None
                try:
                    packets = await self.poll()
                except exceptions.QueueEmpty:
                    break

                if not packets:
                    break
                try:
                    for pkt in packets:
                        await ws.send(pkt.encode(always_bytes=False))

                except:
                    break

        writer_task = asyncio.ensure_future(writer())
        self.server.logger.info('%s: Upgrade to websocket successful', self.sid)
        while 1:
            p = None
            wait_task = asyncio.ensure_future(ws.wait())
            try:
                p = await asyncio.wait_for(wait_task, self.server.ping_timeout)
            except asyncio.CancelledError:
                try:
                    wait_task.exception()
                except:
                    pass

                break
            except:
                break

            if p is None:
                break
            if isinstance(p, six.text_type):
                p = p.encode('utf-8')
            pkt = packet.Packet(encoded_packet=p)
            try:
                await self.receive(pkt)
            except exceptions.UnknownPacketError:
                pass
            except exceptions.SocketIsClosedError:
                self.server.logger.info('Receive error -- socket is closed')
                break
            except:
                self.server.logger.exception('Unknown receive error')

        await self.queue.put(None)
        await asyncio.wait_for(writer_task, timeout=None)
        await self.close(wait=False, abort=True)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/drivers/SimPixel/SimpleWebSocketServer.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 21888 bytes
import sys
VER = sys.version_info[0]
if VER >= 3:
    import socketserver
    from http.server import BaseHTTPRequestHandler
    from io import StringIO, BytesIO
else:
    import SocketServer
    from BaseHTTPServer import BaseHTTPRequestHandler
    from StringIO import StringIO
import hashlib, base64, socket, struct, ssl, errno, codecs
from collections import deque
from select import select
__all__ = [
 'WebSocket',
 'SimpleWebSocketServer']

def _check_unicode(val):
    if VER >= 3:
        return isinstance(val, str)
    else:
        return isinstance(val, unicode)


class HTTPRequest(BaseHTTPRequestHandler):

    def __init__(self, request_text):
        if VER >= 3:
            self.rfile = BytesIO(request_text)
        else:
            self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()


_VALID_STATUS_CODES = [
 1000, 1001, 1002, 1003, 1007, 1008,
 1009, 1010, 1011, 3000, 3999, 4000, 4999]
HANDSHAKE_STR = 'HTTP/1.1 101 Switching Protocols\r\nUpgrade: WebSocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: %(acceptstr)s\r\n\r\n'
GUID_STR = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
STREAM = 0
TEXT = 1
BINARY = 2
CLOSE = 8
PING = 9
PONG = 10
HEADERB1 = 1
HEADERB2 = 3
LENGTHSHORT = 4
LENGTHLONG = 5
MASK = 6
PAYLOAD = 7
MAXHEADER = 65536
MAXPAYLOAD = 33554432

class WebSocket(object):

    def __init__(self, server, sock, address):
        self.server = server
        self.client = sock
        self.address = address
        self.handshaked = False
        self.headerbuffer = bytearray()
        self.headertoread = 2048
        self.fin = 0
        self.data = bytearray()
        self.opcode = 0
        self.hasmask = 0
        self.maskarray = None
        self.length = 0
        self.lengtharray = None
        self.index = 0
        self.request = None
        self.usingssl = False
        self.frag_start = False
        self.frag_type = BINARY
        self.frag_buffer = None
        self.frag_decoder = codecs.getincrementaldecoder('utf-8')(errors='strict')
        self.closed = False
        self.sendq = deque()
        self.state = HEADERB1
        self.maxheader = MAXHEADER
        self.maxpayload = MAXPAYLOAD

    def handleMessage(self):
        """
            Called when websocket frame is received.
            To access the frame data call self.data.

            If the frame is Text then self.data is a unicode object.
            If the frame is Binary then self.data is a bytearray object.
        """
        pass

    def handleConnected(self):
        """
            Called when a websocket client connects to the server.
        """
        pass

    def handleClose(self):
        """
            Called when a websocket server gets a Close frame from a client.
        """
        pass

    def _handlePacket(self):
        if self.opcode == CLOSE:
            pass
        else:
            if self.opcode == STREAM:
                pass
            else:
                if self.opcode == TEXT:
                    pass
                else:
                    if self.opcode == BINARY:
                        pass
                    else:
                        if self.opcode == PONG or self.opcode == PING:
                            if len(self.data) > 125:
                                raise Exception('control frame length can not be > 125')
                            else:
                                raise Exception('unknown opcode')
                            if self.opcode == CLOSE:
                                status = 1000
                                reason = ''
                                length = len(self.data)
                                if length == 0:
                                    pass
                                else:
                                    if length >= 2:
                                        status = struct.unpack_from('!H', self.data[:2])[0]
                                        reason = self.data[2:]
                                        if status not in _VALID_STATUS_CODES:
                                            status = 1002
                                        if len(reason) > 0:
                                            try:
                                                reason = reason.decode('utf8', errors='strict')
                                            except:
                                                status = 1002

                                    else:
                                        status = 1002
                                    self.close(status, reason)
                                    return
                            if self.fin == 0:
                                if self.opcode != STREAM:
                                    if self.opcode == PING or self.opcode == PONG:
                                        raise Exception('control messages can not be fragmented')
                                else:
                                    self.frag_type = self.opcode
                                    self.frag_start = True
                                    self.frag_decoder.reset()
                                    if self.frag_type == TEXT:
                                        self.frag_buffer = []
                                        utf_str = self.frag_decoder.decode((self.data), final=False)
                                        if utf_str:
                                            self.frag_buffer.append(utf_str)
                                    else:
                                        self.frag_buffer = bytearray()
                                        self.frag_buffer.extend(self.data)
                            else:
                                if self.frag_start is False:
                                    raise Exception('fragmentation protocol error')
                                if self.frag_type == TEXT:
                                    utf_str = self.frag_decoder.decode((self.data), final=False)
                                    if utf_str:
                                        self.frag_buffer.append(utf_str)
                                else:
                                    self.frag_buffer.extend(self.data)
                        else:
                            if self.opcode == STREAM:
                                if self.frag_start is False:
                                    raise Exception('fragmentation protocol error')
                                else:
                                    if self.frag_type == TEXT:
                                        utf_str = self.frag_decoder.decode((self.data), final=True)
                                        self.frag_buffer.append(utf_str)
                                        self.data = ''.join(self.frag_buffer)
                                    else:
                                        self.frag_buffer.extend(self.data)
                                        self.data = self.frag_buffer
                                self.handleMessage()
                                self.frag_decoder.reset()
                                self.frag_type = BINARY
                                self.frag_start = False
                                self.frag_buffer = None
                            else:
                                if self.opcode == PING:
                                    self._sendMessage(False, PONG, self.data)
                                else:
                                    if self.opcode == PONG:
                                        pass
                                    else:
                                        if self.frag_start is True:
                                            raise Exception('fragmentation protocol error')
                                        if self.opcode == TEXT:
                                            try:
                                                self.data = self.data.decode('utf8', errors='strict')
                                            except Exception:
                                                raise Exception('invalid utf-8 payload')

                                        self.handleMessage()

    def _handleData(self):
        if self.handshaked is False:
            data = self.client.recv(self.headertoread)
            if not data:
                raise Exception('remote socket closed')
            else:
                self.headerbuffer.extend(data)
            if len(self.headerbuffer) >= self.maxheader:
                raise Exception('header exceeded allowable size')
            if b'\r\n\r\n' in self.headerbuffer:
                self.request = HTTPRequest(self.headerbuffer)
                try:
                    key = self.request.headers['Sec-WebSocket-Key']
                    k = key.encode('ascii') + GUID_STR.encode('ascii')
                    k_s = base64.b64encode(hashlib.sha1(k).digest()).decode('ascii')
                    hStr = HANDSHAKE_STR % {'acceptstr': k_s}
                    self.sendq.append((BINARY, hStr.encode('ascii')))
                    self.handshaked = True
                    self.handleConnected()
                except Exception as e:
                    raise Exception('handshake failed: %s', str(e))

        else:
            data = self.client.recv(8192)
            if not data:
                raise Exception('remote socket closed')
            if VER >= 3:
                for d in data:
                    self._parseMessage(d)

            else:
                for d in data:
                    self._parseMessage(ord(d))

    def close(self, status=1000, reason=''):
        """
           Send Close frame to the client. The underlying socket is only closed
           when the client acknowledges the Close frame.

           status is the closing identifier.
           reason is the reason for the close.
         """
        try:
            if self.closed is False:
                close_msg = bytearray()
                close_msg.extend(struct.pack('!H', status))
                if _check_unicode(reason):
                    close_msg.extend(reason.encode('utf-8'))
                else:
                    close_msg.extend(reason)
                self._sendMessage(False, CLOSE, close_msg)
        finally:
            self.closed = True

    def _sendBuffer(self, buff):
        size = len(buff)
        tosend = size
        already_sent = 0
        while tosend > 0:
            try:
                sent = self.client.send(buff[already_sent:])
                if sent == 0:
                    raise RuntimeError('socket connection broken')
                already_sent += sent
                tosend -= sent
            except socket.error as e:
                if e.errno in [errno.EAGAIN, errno.EWOULDBLOCK]:
                    return buff[already_sent:]
                raise e

    def sendFragmentStart(self, data):
        """
            Send the start of a data fragment stream to a websocket client.
            Subsequent data should be sent using sendFragment().
            A fragment stream is completed when sendFragmentEnd() is called.

            If data is a unicode object then the frame is sent as Text.
            If the data is a bytearray object then the frame is sent as Binary.
        """
        opcode = BINARY
        if _check_unicode(data):
            opcode = TEXT
        self._sendMessage(True, opcode, data)

    def sendFragment(self, data):
        """
            see sendFragmentStart()

            If data is a unicode object then the frame is sent as Text.
            If the data is a bytearray object then the frame is sent as Binary.
        """
        self._sendMessage(True, STREAM, data)

    def sendFragmentEnd(self, data):
        """
            see sendFragmentEnd()

            If data is a unicode object then the frame is sent as Text.
            If the data is a bytearray object then the frame is sent as Binary.
        """
        self._sendMessage(False, STREAM, data)

    def sendMessage(self, data):
        """
            Send websocket data frame to the client.

            If data is a unicode object then the frame is sent as Text.
            If the data is a bytearray object then the frame is sent as Binary.
        """
        opcode = BINARY
        if _check_unicode(data):
            opcode = TEXT
        self._sendMessage(False, opcode, data)

    def _sendMessage(self, fin, opcode, data):
        payload = bytearray()
        b1 = 0
        b2 = 0
        if fin is False:
            b1 |= 128
        b1 |= opcode
        if _check_unicode(data):
            data = data.encode('utf-8')
        length = len(data)
        payload.append(b1)
        if length <= 125:
            b2 |= length
            payload.append(b2)
        elif length >= 126:
            if length <= 65535:
                b2 |= 126
                payload.append(b2)
                payload.extend(struct.pack('!H', length))
        else:
            b2 |= 127
            payload.append(b2)
            payload.extend(struct.pack('!Q', length))
        if length > 0:
            payload.extend(data)
        self.sendq.append((opcode, payload))

    def _parseMessage(self, byte):
        if self.state == HEADERB1:
            self.fin = byte & 128
            self.opcode = byte & 15
            self.state = HEADERB2
            self.index = 0
            self.length = 0
            self.lengtharray = bytearray()
            self.data = bytearray()
            rsv = byte & 112
            if rsv != 0:
                raise Exception('RSV bit must be 0')
        else:
            if self.state == HEADERB2:
                mask = byte & 128
                length = byte & 127
                if self.opcode == PING:
                    if length > 125:
                        raise Exception('ping packet is too large')
                if mask == 128:
                    self.hasmask = True
                else:
                    self.hasmask = False
                if length <= 125:
                    self.length = length
                    if self.hasmask is True:
                        self.maskarray = bytearray()
                        self.state = MASK
                    elif self.length <= 0:
                        try:
                            self._handlePacket()
                        finally:
                            self.state = self.HEADERB1
                            self.data = bytearray()

                    else:
                        self.data = bytearray()
                        self.state = PAYLOAD
                else:
                    if length == 126:
                        self.lengtharray = bytearray()
                        self.state = LENGTHSHORT
                    else:
                        if length == 127:
                            self.lengtharray = bytearray()
                            self.state = LENGTHLONG
            else:
                if self.state == LENGTHSHORT:
                    self.lengtharray.append(byte)
                    if len(self.lengtharray) > 2:
                        raise Exception('short length exceeded allowable size')
                    if len(self.lengtharray) == 2:
                        self.length = struct.unpack_from('!H', self.lengtharray)[0]
                        if self.hasmask is True:
                            self.maskarray = bytearray()
                            self.state = MASK
                        elif self.length <= 0:
                            try:
                                self._handlePacket()
                            finally:
                                self.state = HEADERB1
                                self.data = bytearray()

                        else:
                            self.data = bytearray()
                            self.state = PAYLOAD
                else:
                    if self.state == LENGTHLONG:
                        self.lengtharray.append(byte)
                        if len(self.lengtharray) > 8:
                            raise Exception('long length exceeded allowable size')
                        if len(self.lengtharray) == 8:
                            self.length = struct.unpack_from('!Q', self.lengtharray)[0]
                            if self.hasmask is True:
                                self.maskarray = bytearray()
                                self.state = MASK
                            elif self.length <= 0:
                                try:
                                    self._handlePacket()
                                finally:
                                    self.state = HEADERB1
                                    self.data = bytearray()

                            else:
                                self.data = bytearray()
                                self.state = PAYLOAD
                    else:
                        if self.state == MASK:
                            self.maskarray.append(byte)
                            if len(self.maskarray) > 4:
                                raise Exception('mask exceeded allowable size')
                            if len(self.maskarray) == 4:
                                if self.length <= 0:
                                    try:
                                        self._handlePacket()
                                    finally:
                                        self.state = HEADERB1
                                        self.data = bytearray()

                                else:
                                    self.data = bytearray()
                                    self.state = PAYLOAD
                        elif self.state == PAYLOAD:
                            if self.hasmask is True:
                                self.data.append(byte ^ self.maskarray[(self.index % 4)])
                            else:
                                self.data.append(byte)
                            if len(self.data) >= self.maxpayload:
                                raise Exception('payload exceeded allowable size')
                            if self.index + 1 == self.length:
                                try:
                                    self._handlePacket()
                                finally:
                                    self.state = HEADERB1
                                    self.data = bytearray()

                            else:
                                self.index += 1


class SimpleWebSocketServer(object):

    def __init__(self, host, port, websocketclass, selectInterval=0.1, **kwargs):
        self.websocketclass = websocketclass
        self.websock_kwargs = kwargs
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind((host, port))
        self.serversocket.listen(5)
        self.selectInterval = selectInterval
        self.connections = {}
        self.listeners = [self.serversocket]

    def _decorateSocket(self, sock):
        return sock

    def _constructWebSocket(self, sock, address):
        return (self.websocketclass)(self, sock, address, **self.websock_kwargs)

    def close(self):
        self.serversocket.close()
        for desc, conn in self.connections.items():
            conn.close()
            conn.handleClose()

    def _kill_client(self, client, client_id, exception=True):
        del self.connections[id]
        self.listeners.remove(id)
        client.client.close()
        client.handleClose()
        if exception:
            import traceback
            traceback.print_exc()

    def serveforever(self):
        while True:
            writers = []
            for fileno in self.listeners:
                if fileno == self.serversocket:
                    pass
                else:
                    client = self.connections[fileno]
                    if client.sendq:
                        writers.append(fileno)

            if self.selectInterval:
                rList, wList, xList = select(self.listeners, writers, self.listeners, self.selectInterval)
            else:
                rList, wList, xList = select(self.listeners, writers, self.listeners)
            for ready in wList:
                client = self.connections[ready]
                try:
                    while client.sendq:
                        opcode, payload = client.sendq.popleft()
                        remaining = client._sendBuffer(payload)
                        if remaining is not None:
                            client.sendq.appendleft((opcode, remaining))
                            break
                        elif opcode == CLOSE:
                            raise Exception('received client close')

                except Exception:
                    self._kill_client(client, ready)

            for ready in rList:
                if ready == self.serversocket:
                    try:
                        sock, address = self.serversocket.accept()
                        newsock = self._decorateSocket(sock)
                        newsock.setblocking(0)
                        fileno = newsock.fileno()
                        self.connections[fileno] = self._constructWebSocket(newsock, address)
                        self.listeners.append(fileno)
                    except Exception:
                        if sock is not None:
                            sock.close()

                if ready not in self.connections:
                    pass
                else:
                    client = self.connections[ready]
                    try:
                        client._handleData()
                    except Exception:
                        self._kill_client(client, ready)

            for failed in xList:
                if failed == self.serversocket:
                    self.close()
                    raise Exception('server socket failed')
                if failed in self.connections:
                    self._kill_client(self.connections[failed], failed, False)
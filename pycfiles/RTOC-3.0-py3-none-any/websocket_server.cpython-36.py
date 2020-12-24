# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Benutzer\haschtl\Dokumente\GIT\kellerlogger\RTOC\RTLogger\websocket_server.py
# Compiled at: 2020-01-02 08:37:59
# Size of source mod 2**32: 12991 bytes
import sys, struct, ssl
from base64 import b64encode
from hashlib import sha1
import logging
from socket import error as SocketError
import errno, traceback
if sys.version_info[0] < 3:
    from SocketServer import ThreadingMixIn, TCPServer, StreamRequestHandler
else:
    from socketserver import ThreadingMixIn, TCPServer, StreamRequestHandler
logger = logging.getLogger(__name__)
logging.basicConfig()
FIN = 128
OPCODE = 15
MASKED = 128
PAYLOAD_LEN = 127
PAYLOAD_LEN_EXT16 = 126
PAYLOAD_LEN_EXT64 = 127
OPCODE_CONTINUATION = 0
OPCODE_TEXT = 1
OPCODE_BINARY = 2
OPCODE_CLOSE_CONN = 8
OPCODE_PING = 9
OPCODE_PONG = 10

class API:

    def run_forever(self):
        try:
            logger.info('Listening on port %d for clients..' % self.port)
            self.serve_forever()
        except KeyboardInterrupt:
            self.server_close()
            logger.info('Server terminated.')
        except Exception as e:
            logger.error((str(e)), exc_info=True)

    def new_client(self, client, server):
        pass

    def client_left(self, client, server):
        pass

    def message_received(self, client, server, message):
        pass

    def set_fn_new_client(self, fn):
        self.new_client = fn

    def set_fn_client_left(self, fn):
        self.client_left = fn

    def set_fn_message_received(self, fn):
        self.message_received = fn

    def send_message(self, client, msg):
        self._unicast_(client, msg)

    def send_message_to_all(self, msg):
        self._multicast_(msg)


class WebsocketServer(ThreadingMixIn, TCPServer, API):
    __doc__ = "\n\tA websocket server waiting for clients to connect.\n    Args:\n        port(int): Port to bind to\n        host(str): Hostname or IP to listen for connections. By default 127.0.0.1\n            is being used. To accept connections from any client, you should use\n            0.0.0.0.\n        loglevel: Logging level from logging module to use for logging. By default\n            warnings and errors are being logged.\n    Properties:\n        clients(list): A list of connected clients. A client is a dictionary\n            like below.\n                {\n                 'id'      : id,\n                 'handler' : handler,\n                 'address' : (addr, port)\n                }\n    "
    key = None
    cert = None
    allow_reuse_address = True
    daemon_threads = True
    clients = []
    id_counter = 0

    def __init__(self, port, host='127.0.0.1', loglevel=logging.WARNING, key=None, cert=None):
        logger.setLevel(loglevel)
        TCPServer.__init__(self, (host, port), WebSocketHandler)
        self.port = self.socket.getsockname()[1]
        self.key = key
        self.cert = cert

    def _message_received_(self, handler, msg):
        self.message_received(self.handler_to_client(handler), self, msg)

    def _ping_received_(self, handler, msg):
        handler.send_pong(msg)

    def _pong_received_(self, handler, msg):
        pass

    def _new_client_(self, handler):
        self.id_counter += 1
        client = {'id':self.id_counter, 
         'handler':handler, 
         'address':handler.client_address}
        self.clients.append(client)
        self.new_client(client, self)

    def _client_left_(self, handler):
        client = self.handler_to_client(handler)
        self.client_left(client, self)
        if client in self.clients:
            self.clients.remove(client)

    def _unicast_(self, to_client, msg):
        to_client['handler'].send_message(msg)

    def _multicast_(self, msg):
        for client in self.clients:
            self._unicast_(client, msg)

    def handler_to_client(self, handler):
        for client in self.clients:
            if client['handler'] == handler:
                return client


class WebSocketHandler(StreamRequestHandler):

    def __init__(self, socket, addr, server):
        self.server = server
        if server.key:
            if server.cert:
                try:
                    socket = ssl.wrap_socket(socket, server_side=True, certfile=(server.cert), keyfile=(server.key))
                except Exception as e:
                    tb = traceback.format_exc()
                    logging.warn(tb)
                    logging.warn(e)
                    logger.warn('SSL not available (are the paths {} and {} correct for the key and cert?)'.format(server.key, server.cert))

        StreamRequestHandler.__init__(self, socket, addr, server)

    def setup(self):
        StreamRequestHandler.setup(self)
        self.keep_alive = True
        self.handshake_done = False
        self.valid_client = False

    def handle(self):
        while self.keep_alive:
            if not self.handshake_done:
                self.handshake()
            elif self.valid_client:
                self.read_next_message()

    def read_bytes(self, num):
        bytes = self.rfile.read(num)
        if sys.version_info[0] < 3:
            return map(ord, bytes)
        else:
            return bytes

    def read_next_message(self):
        try:
            b1, b2 = self.read_bytes(2)
        except SocketError as e:
            if e.errno == errno.ECONNRESET:
                logger.info('Client closed connection.')
                self.keep_alive = 0
                return
            b1, b2 = (0, 0)
        except ValueError as e:
            b1, b2 = (0, 0)

        fin = b1 & FIN
        opcode = b1 & OPCODE
        masked = b2 & MASKED
        payload_length = b2 & PAYLOAD_LEN
        if opcode == OPCODE_CLOSE_CONN:
            logger.info('Client asked to close connection.')
            self.keep_alive = 0
            return
        if not masked:
            logger.warn('Client must always be masked.')
            self.keep_alive = 0
            return
        if opcode == OPCODE_CONTINUATION:
            logger.warn('Continuation frames are not supported.')
            return
        if opcode == OPCODE_BINARY:
            logger.warn('Binary frames are not supported.')
            return
        if opcode == OPCODE_TEXT:
            opcode_handler = self.server._message_received_
        else:
            if opcode == OPCODE_PING:
                opcode_handler = self.server._ping_received_
            else:
                if opcode == OPCODE_PONG:
                    opcode_handler = self.server._pong_received_
                else:
                    logger.warn('Unknown opcode %#x.' % opcode)
                    self.keep_alive = 0
                    return
                if payload_length == 126:
                    payload_length = struct.unpack('>H', self.rfile.read(2))[0]
                elif payload_length == 127:
                    payload_length = struct.unpack('>Q', self.rfile.read(8))[0]
        masks = self.read_bytes(4)
        message_bytes = bytearray()
        for message_byte in self.read_bytes(payload_length):
            message_byte ^= masks[(len(message_bytes) % 4)]
            message_bytes.append(message_byte)

        opcode_handler(self, message_bytes.decode('utf8'))

    def send_message(self, message):
        self.send_text(message)

    def send_pong(self, message):
        self.send_text(message, OPCODE_PONG)

    def send_text(self, message, opcode=OPCODE_TEXT):
        """
        Important: Fragmented(=continuation) messages are not supported since
        their usage cases are limited - when we don't know the payload length.
        """
        if isinstance(message, bytes):
            message = try_decode_UTF8(message)
            message or logger.warning("Can't send message, message is not valid UTF-8")
            return False
        elif sys.version_info < (3, 0) and (isinstance(message, str) or isinstance(message, unicode)):
            pass
        else:
            if isinstance(message, str):
                pass
            else:
                logger.warning("Can't send message, message has to be a string or bytes. Given type is %s" % type(message))
                return False
            header = bytearray()
            payload = encode_to_UTF8(message)
            payload_length = len(payload)
            if payload_length <= 125:
                header.append(FIN | opcode)
                header.append(payload_length)
            elif payload_length >= 126 and payload_length <= 65535:
                header.append(FIN | opcode)
                header.append(PAYLOAD_LEN_EXT16)
                header.extend(struct.pack('>H', payload_length))
            else:
                if payload_length < 18446744073709551616:
                    header.append(FIN | opcode)
                    header.append(PAYLOAD_LEN_EXT64)
                    header.extend(struct.pack('>Q', payload_length))
                else:
                    raise Exception('Message is too big. Consider breaking it into chunks.')
                    return
            self.request.send(header + payload)

    def read_http_headers(self):
        headers = {}
        http_get = self.rfile.readline().decode().strip()
        assert http_get.upper().startswith('GET')
        while True:
            header = self.rfile.readline().decode().strip()
            if not header:
                break
            head, value = header.split(':', 1)
            headers[head.lower().strip()] = value.strip()

        return headers

    def handshake(self):
        headers = self.read_http_headers()
        try:
            assert headers['upgrade'].lower() == 'websocket'
        except AssertionError:
            self.keep_alive = False
            return
        except KeyError:
            self.keep_alive = False
            logger.warning(headers)
            logger.warning('Websocket-Header has no contains no "upgrade" key')
            return
        else:
            try:
                key = headers['sec-websocket-key']
            except KeyError:
                logger.warning('Client tried to connect but was missing a key')
                self.keep_alive = False
                return
            else:
                response = self.make_handshake_response(key)
                self.handshake_done = self.request.send(response.encode())
                self.valid_client = True
                self.server._new_client_(self)

    @classmethod
    def make_handshake_response(cls, key):
        return 'HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: %s\r\n\r\n' % cls.calculate_response_key(key)

    @classmethod
    def calculate_response_key(cls, key):
        GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        hash = sha1(key.encode() + GUID.encode())
        response_key = b64encode(hash.digest()).strip()
        return response_key.decode('ASCII')

    def finish(self):
        self.server._client_left_(self)


def encode_to_UTF8(data):
    try:
        return data.encode('UTF-8')
    except UnicodeEncodeError as e:
        logger.error('Could not encode data to UTF-8 -- %s' % e)
        return False
    except Exception as e:
        raise e
        return False


def try_decode_UTF8(data):
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return False
    except Exception as e:
        raise e
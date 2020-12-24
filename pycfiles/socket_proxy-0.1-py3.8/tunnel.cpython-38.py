# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/socket_proxy/tunnel.py
# Compiled at: 2020-05-03 13:30:29
# Size of source mod 2**32: 10793 bytes
import asyncio, collections, ipaddress, logging
from datetime import datetime, timedelta
from .base import INTERVAL_TIME, Ban, ReachedClientLimit, TransportType
from .connection import Connection
from .package import ClientClosePackage, ClientDataPackage, ClientInitPackage, ConfigPackage, InitPackage
from .utils import generate_ssl_context, generate_token, get_unused_port, merge_settings
_logger = logging.getLogger(__name__)

class Tunnel:

    def __init__(self, *, bantime=60, chunk_size=1024, max_clients=0, max_connects=0, **kwargs):
        (super().__init__)(**kwargs)
        self.clients = {}
        self.bantime = bantime
        self.chunk_size = chunk_size
        self.max_clients = max_clients
        self.max_connects = max_connects

    def __contains__(self, token):
        return token in self.clients

    def __getitem__(self, token):
        return self.clients[token]

    def add(self, client):
        if client.token in self.clients:
            return
        if 0 < self.max_clients <= len(self.clients):
            raise ReachedClientLimit()
        self.clients[client.token] = client

    def get(self, token):
        return self.clients.get(token, None)

    def pop(self, token):
        _logger.info('Client %s disconnected', token.hex())
        return self.clients.pop(token, None)

    def config_from_package(self, tunnel, package):
        self.bantime = merge_settings(self.bantime, package.bantime)
        self.max_clients = merge_settings(self.max_clients, package.clients)
        self.max_connects = merge_settings(self.max_connects, package.connects)
        _logger.debug('Tunnel %s ban time: %s', tunnel.uuid, self.bantime)
        _logger.debug('Tunnel %s clients: %s', tunnel.uuid, self.max_clients)
        _logger.debug('Tunnel %s connections per IP: %s', tunnel.uuid, self.max_connects)

    async def _disconnect_client(self, token):
        client = self.pop(token)
        if client:
            await client.close()

    async def close(self):
        for client in list(self.clients.values()):
            await client.close()

    async def idle(self):
        pass

    async def _serve(self):
        asyncio.create_task(self._interval())

    async def _send_config(self, tunnel):
        package = ConfigPackage(self.bantime, self.max_clients, self.max_connects)
        await tunnel.tun_write(package)

    async def _interval(self):
        while True:
            await self.idle()
            await asyncio.sleep(INTERVAL_TIME)


class TunnelClient(Tunnel):

    def __init__(self, host, port, dst_host, dst_port, ca, cert=None, key=None, verify_hostname=True, **kwargs):
        (super().__init__)(**kwargs)
        self.host, self.port = host, port
        self.dst_host, self.dst_port = dst_host, dst_port
        self.running = False
        self.addresses = []
        self.tunnel = None
        self.sc = generate_ssl_context(cert=cert,
          key=key,
          ca=ca,
          check_hostname=verify_hostname)

    async def _client_loop(self, client):
        _logger.info('Client %s connected', client.token.hex())
        while True:
            data = await client.read(self.chunk_size)
            if not data:
                await self._disconnect_client(client.token)
                break
            await self.tunnel.tun_data(client.token, data)

        if self.running:
            await self.tunnel.tun_write(ClientClosePackage(client.token))

    async def _connect_client--- This code section failed: ---

 L. 131         0  LOAD_FAST                'package'
                2  LOAD_ATTR                token
                4  LOAD_FAST                'self'
                6  COMPARE_OP               in
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 132        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 134        14  SETUP_FINALLY        74  'to 74'

 L. 135        16  LOAD_GLOBAL              Connection
               18  LOAD_METHOD              connect

 L. 136        20  LOAD_FAST                'self'
               22  LOAD_ATTR                dst_host

 L. 136        24  LOAD_FAST                'self'
               26  LOAD_ATTR                dst_port

 L. 136        28  LOAD_FAST                'package'
               30  LOAD_ATTR                token

 L. 135        32  CALL_METHOD_3         3  ''
               34  GET_AWAITABLE    
               36  LOAD_CONST               None
               38  YIELD_FROM       
               40  STORE_FAST               'client'

 L. 139        42  LOAD_FAST                'self'
               44  LOAD_METHOD              add
               46  LOAD_FAST                'client'
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          

 L. 140        52  LOAD_GLOBAL              asyncio
               54  LOAD_METHOD              create_task
               56  LOAD_FAST                'self'
               58  LOAD_METHOD              _client_loop
               60  LOAD_FAST                'client'
               62  CALL_METHOD_1         1  ''
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          

 L. 141        68  POP_BLOCK        
               70  LOAD_CONST               None
               72  RETURN_VALUE     
             74_0  COME_FROM_FINALLY    14  '14'

 L. 142        74  DUP_TOP          
               76  LOAD_GLOBAL              Exception
               78  COMPARE_OP               exception-match
               80  POP_JUMP_IF_FALSE   126  'to 126'
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 143        88  LOAD_GLOBAL              _logger
               90  LOAD_METHOD              error
               92  LOAD_STR                 'Client connection failed'
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          

 L. 144        98  LOAD_FAST                'self'
              100  LOAD_ATTR                tunnel
              102  LOAD_METHOD              tun_write
              104  LOAD_GLOBAL              ClientClosePackage
              106  LOAD_FAST                'package'
              108  LOAD_ATTR                token
              110  CALL_FUNCTION_1       1  ''
              112  CALL_METHOD_1         1  ''
              114  GET_AWAITABLE    
              116  LOAD_CONST               None
              118  YIELD_FROM       
              120  POP_TOP          
              122  POP_EXCEPT       
              124  JUMP_FORWARD        128  'to 128'
            126_0  COME_FROM            80  '80'
              126  END_FINALLY      
            128_0  COME_FROM           124  '124'

Parse error at or near `RETURN_VALUE' instruction at offset 72

    async def _send_data(self, package):
        client = self.get(package.token)
        if client:
            client.write(package.data)
            await client.drain()

    async def _serve(self):
        await super()._serve()
        while True:
            package = await self.tunnel.tun_read()
            if isinstance(package, InitPackage):
                self.tunnel.token = package.token
                self.addresses = package.addresses
                fmt = 'Tunnel %s open: %s on port %s'
                for ip_type, port in sorted(self.addresses):
                    _logger.info(fmt, self.tunnel.uuid, ip_type.name, port)

                await self._send_config(self.tunnel)
            elif isinstance(package, ConfigPackage):
                self.config_from_package(self.tunnel, package)
            elif isinstance(package, ClientInitPackage):
                await self._connect_client(package)
            elif isinstance(package, ClientClosePackage):
                await self._disconnect_client(package.token)
            elif isinstance(package, ClientDataPackage):
                await self._send_data(package)
            else:
                _logger.error('Invalid package: %s', package)
                break

    async def loop(self):
        self.tunnel = await Connection.connect((self.host), (self.port), ssl=(self.sc))
        _logger.info('Tunnel %s:%s connected', self.host, self.port)
        _logger.info('Forwarding to %s:%s', self.dst_host, self.dst_port)
        try:
            await self._serve()
        finally:
            await self.close()
            _logger.info('Tunnel %s:%s closed', self.host, self.port)

    def start(self):
        _logger.info('Starting client...')
        asyncio.run(self.loop())

    async def stop(self):
        if self.tunnel:
            await self.tunnel.close()


class TunnelServer(Connection, Tunnel):

    def __init__(self, reader, writer, *, ports=None, **kwargs):
        (super().__init__)(reader, writer, token=generate_token(), **kwargs)
        self.host, self.port = writer.get_extra_info('peername')[:2]
        self.ports = ports
        self.connections = collections.defaultdict(Ban)

    async def idle(self):
        await super().idle()
        dt = datetime.now() - timedelta(seconds=(self.bantime))
        for ip, ban in list(self.connections.items()):
            if ban.first < dt:
                self.connections.pop(ip)
                _logger.info('Connection number of %s resetted', ip)

    async def _client_accept(self, reader, writer):
        host, port = writer.get_extra_info('peername')[:2]
        ip = ipaddress.ip_address(host)
        if 0 < self.max_connects <= self.connections[ip].hits:
            reader.feed_eof()
            writer.close()
            await writer.wait_closed()
            _logger.info('Connection from %s blocked', ip)
            return
        self.connections[ip].hits += 1
        client = Connection(reader, writer, generate_token())
        self.add(client)
        _logger.info('Client %s connected on %s:%s', client.uuid, host, port)
        await self.tun_write(ClientInitPackage(ip, port, client.token))
        while True:
            data = await client.read(self.chunk_size)
            if not data:
                break
            await self.tun_data(client.token, data)

        if self.server.is_serving():
            await self.tun_write(ClientClosePackage(client.token))
        await self._disconnect_client(client.token)

    async def _client_loop--- This code section failed: ---

 L. 259         0  LOAD_LISTCOMP            '<code_object <listcomp>>'
                2  LOAD_STR                 'TunnelServer._client_loop.<locals>.<listcomp>'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  LOAD_FAST                'server'
                8  LOAD_ATTR                sockets
               10  GET_ITER         
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'addresses'

 L. 262        16  LOAD_STR                 ' '
               18  LOAD_METHOD              join
               20  LOAD_GLOBAL              sorted
               22  LOAD_GENEXPR             '<code_object <genexpr>>'
               24  LOAD_STR                 'TunnelServer._client_loop.<locals>.<genexpr>'
               26  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               28  LOAD_FAST                'addresses'
               30  GET_ITER         
               32  CALL_FUNCTION_1       1  ''
               34  CALL_FUNCTION_1       1  ''
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'out'

 L. 263        40  LOAD_GLOBAL              _logger
               42  LOAD_METHOD              info
               44  LOAD_STR                 'Tunnel %s listen on %s'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                uuid
               50  LOAD_FAST                'out'
               52  CALL_METHOD_3         3  ''
               54  POP_TOP          

 L. 265        56  LOAD_LISTCOMP            '<code_object <listcomp>>'
               58  LOAD_STR                 'TunnelServer._client_loop.<locals>.<listcomp>'
               60  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               62  LOAD_FAST                'addresses'
               64  GET_ITER         
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'addresses'

 L. 266        70  LOAD_FAST                'self'
               72  LOAD_METHOD              tun_write
               74  LOAD_GLOBAL              InitPackage
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                token
               80  LOAD_FAST                'addresses'
               82  CALL_FUNCTION_2       2  ''
               84  CALL_METHOD_1         1  ''
               86  GET_AWAITABLE    
               88  LOAD_CONST               None
               90  YIELD_FROM       
               92  POP_TOP          

 L. 269        94  LOAD_FAST                'server'
               96  BEFORE_ASYNC_WITH
               98  GET_AWAITABLE    
              100  LOAD_CONST               None
              102  YIELD_FROM       
              104  SETUP_ASYNC_WITH    126  'to 126'
              106  POP_TOP          

 L. 270       108  LOAD_FAST                'server'
              110  LOAD_METHOD              serve_forever
              112  CALL_METHOD_0         0  ''
              114  GET_AWAITABLE    
              116  LOAD_CONST               None
              118  YIELD_FROM       
              120  POP_TOP          
              122  POP_BLOCK        
              124  BEGIN_FINALLY    
            126_0  COME_FROM_ASYNC_WITH   104  '104'
              126  WITH_CLEANUP_START
              128  GET_AWAITABLE    
              130  LOAD_CONST               None
              132  YIELD_FROM       
              134  WITH_CLEANUP_FINISH
              136  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 126_0

    async def _serve(self):
        await super()._serve()
        while True:
            package = await self.tun_read()
            if isinstance(package, ConfigPackage):
                self.config_from_package(self, package)
                await self._send_config(self)
            elif isinstance(package, ClientClosePackage):
                await self._disconnect_client(package.token)
            elif isinstance(package, ClientDataPackage):
                if package.token not in self:
                    _logger.error('Invalid client token: %s', package.token)
                    break
                conn = self[package.token]
                conn.write(package.data)
                await conn.drain()
            else:
                _logger.error('Invalid package: %s', package)
                break

    async def stop(self):
        await Connection.close(self)
        await Tunnel.close(self)
        self.server.close()
        await self.server.wait_closed()
        _logger.info('Tunnel %s closed', self.uuid)

    async def loop(self):
        _logger.info('Tunnel %s connected %s:%s', self.uuid, self.host, self.port)
        port = get_unused_port(*self.ports) if self.ports else 0
        if port is None:
            _logger.error('All ports are blocked')
            await self.close()
            return
        self.server = await asyncio.start_server(self._client_accept, '', port)
        asyncio.create_task(self._client_loop(self.server))
        try:
            await self._serve()
        finally:
            await self.close()
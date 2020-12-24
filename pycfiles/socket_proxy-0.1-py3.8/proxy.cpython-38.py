# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/socket_proxy/proxy.py
# Compiled at: 2020-05-02 13:24:06
# Size of source mod 2**32: 1789 bytes
import asyncio, logging
from .tunnel import TunnelServer
from .utils import generate_ssl_context
_logger = logging.getLogger(__name__)

class ProxyServer:

    def __init__(self, host, port, cert, key, ca=None, max_tunnels=0, **kwargs):
        self.kwargs = kwargs
        self.host, self.port = host, port
        self.max_tunnels = max_tunnels
        self.tunnels = {}
        self.sc = generate_ssl_context(cert=cert, key=key, ca=ca, server=True)

    async def _accept(self, reader, writer):
        if 0 < self.max_tunnels <= len(self.tunnels):
            return
        tunnel = TunnelServer(reader, writer, **self.kwargs)
        self.tunnels[tunnel.token] = tunnel
        try:
            await tunnel.loop()
        finally:
            self.tunnels.pop(tunnel.token)

    async def loop--- This code section failed: ---

 L.  38         0  LOAD_GLOBAL              asyncio
                2  LOAD_ATTR                start_server

 L.  39         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _accept

 L.  39         8  LOAD_FAST                'self'
               10  LOAD_ATTR                host

 L.  39        12  LOAD_FAST                'self'
               14  LOAD_ATTR                port

 L.  39        16  LOAD_FAST                'self'
               18  LOAD_ATTR                sc

 L.  38        20  LOAD_CONST               ('ssl',)
               22  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               24  GET_AWAITABLE    
               26  LOAD_CONST               None
               28  YIELD_FROM       
               30  LOAD_FAST                'self'
               32  STORE_ATTR               server

 L.  42        34  LOAD_GLOBAL              _logger
               36  LOAD_METHOD              info
               38  LOAD_STR                 'Serving on %s:%s'
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                host
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                port
               48  CALL_METHOD_3         3  ''
               50  POP_TOP          

 L.  43        52  LOAD_FAST                'self'
               54  LOAD_ATTR                server
               56  BEFORE_ASYNC_WITH
               58  GET_AWAITABLE    
               60  LOAD_CONST               None
               62  YIELD_FROM       
               64  SETUP_ASYNC_WITH     88  'to 88'
               66  POP_TOP          

 L.  44        68  LOAD_FAST                'self'
               70  LOAD_ATTR                server
               72  LOAD_METHOD              serve_forever
               74  CALL_METHOD_0         0  ''
               76  GET_AWAITABLE    
               78  LOAD_CONST               None
               80  YIELD_FROM       
               82  POP_TOP          
               84  POP_BLOCK        
               86  BEGIN_FINALLY    
             88_0  COME_FROM_ASYNC_WITH    64  '64'
               88  WITH_CLEANUP_START
               90  GET_AWAITABLE    
               92  LOAD_CONST               None
               94  YIELD_FROM       
               96  WITH_CLEANUP_FINISH
               98  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 88_0

    def start(self):
        _logger.info('Starting server...')
        asyncio.run(self.loop())

    async def stop(self):
        for tunnel in self.tunnels.values():
            await tunnel.stop()
        else:
            self.server.close()
            await self.server.wait_closed()
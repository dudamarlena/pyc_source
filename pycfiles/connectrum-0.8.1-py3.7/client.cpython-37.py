# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/connectrum/client.py
# Compiled at: 2020-03-27 14:54:15
# Size of source mod 2**32: 12546 bytes
from importlib import util as importutil
import json, warnings, asyncio, ssl
from .protocol import StratumProtocol
from . import __version__
if importutil.find_spec('aiosocks') is not None:
    import aiosocks
    have_aiosocks = True
else:
    have_aiosocks = False
from collections import defaultdict
from .exc import ElectrumErrorResponse
import logging
logger = logging.getLogger(__name__)

class StratumClient:

    def __init__(self, loop=None):
        """
            Setup state needed to handle req/resp from a single Stratum server.
            Requires a transport (TransportABC) object to do the communication.
        """
        self.protocol = None
        self.next_id = 1
        self.inflight = {}
        self.subscriptions = defaultdict(list)
        self.my_version_args = ('Connectrum/{__version__}}', '1.4')
        self.server_version = None
        self.protocol_version = None
        self.actual_connection = {}
        self.ka_task = None
        self.loop = loop or asyncio.get_event_loop()
        self.reconnect = None

    def _connection_lost(self, protocol):
        if protocol is not self.protocol:
            return
        self.protocol = None
        logger.warn('Electrum server connection lost')
        if self.ka_task:
            self.ka_task.cancel()
            self.ka_task = None

    def close(self):
        if self.protocol:
            self.protocol.close()
            self.protocol = None
        if self.ka_task:
            self.ka_task.cancel()
            self.ka_task = None

    async def connect(self, server_info, proto_code=None, *, use_tor=False, disable_cert_verify=False, proxy=None, short_term=False):
        """
            Start connection process.
            Destination must be specified in a ServerInfo() record (first arg).
        """
        self.server_info = server_info
        if not proto_code:
            proto_code, *_ = server_info.protocols
        else:
            self.proto_code = proto_code
            logger.debug('Connecting to: %r' % server_info)
            if proto_code == 'g':
                raise NotImplementedError('sorry no WebSocket transport yet')
            hostname, port, use_ssl = server_info.get_port(proto_code)
            if use_tor:
                if have_aiosocks:
                    try:
                        socks_host, socks_port = use_tor
                    except TypeError:
                        socks_host, socks_port = ('localhost', 9050)

                    disable_cert_verify = True
                    if proxy:
                        raise AssertionError('Sorry not yet supporting proxy->tor->dest')
                    logger.debug(' .. using TOR')
                    proxy = aiosocks.Socks5Addr(socks_host, int(socks_port))
                else:
                    logger.debug('Error: want to use tor, but no aiosocks module.')
        if use_ssl == True:
            if disable_cert_verify:
                use_ssl = ssl.create_default_context()
                use_ssl.check_hostname = False
                use_ssl.verify_mode = ssl.CERT_NONE
                logger.debug(' .. SSL cert check disabled')

        async def _reconnect():
            if self.protocol:
                return
            elif proxy:
                if have_aiosocks:
                    transport, protocol = await aiosocks.create_connection(StratumProtocol,
                      proxy=proxy, proxy_auth=None,
                      remote_resolve=True,
                      ssl=use_ssl,
                      dst=(
                     hostname, port))
                else:
                    logger.debug('Error: want to use proxy, but no aiosocks module.')
            else:
                transport, protocol = await self.loop.create_connection(StratumProtocol,
                  host=hostname, port=port,
                  ssl=use_ssl)
            self.protocol = protocol
            protocol.client = self
            self.actual_connection = dict(hostname=hostname, port=(int(port)), ssl=(bool(use_ssl)),
              tor=(bool(proxy)))
            self.actual_connection['ip_addr'] = transport.get_extra_info('peername', default=[
             'unknown'])[0]
            if not short_term:
                self.ka_task = self.loop.create_task(self._keepalive())
            else:
                await self.get_server_version()
                logger.debug(f"Server version/protocol: {self.server_version} / {self.protocol_version}")
            logger.debug('Connected to: %r' % server_info)

        if self.protocol:
            self.protocol.close()
            self.protocol = None
        self.reconnect = _reconnect
        await self.reconnect()

    async def get_server_version(self):
        self.server_version, pv = await (self.RPC)(*('server.version', ), *self.my_version_args)
        self.protocol_version = float(pv)

    async def _keepalive(self):
        """
            Keep our connect to server alive forever, with some 
            pointless traffic.
        """
        while self.protocol:
            await self.RPC('server.ping')
            await asyncio.sleep(300)

    def _send_request(self, method, params=[], is_subscribe=False):
        """
            Send a new request to the server. Serialized the JSON and
            tracks id numbers and optional callbacks.
        """
        if method.startswith('blockchain.address.'):
            if self.protocol_version >= 1.3:
                method, params = self.patch_addr_methods(method, params)
        else:
            self.next_id += 1
            req_id = self.next_id
            msg = {'id':req_id, 
             'method':method,  'params':params}
            if is_subscribe:
                waitQ = asyncio.Queue()
                self.subscriptions[method].append(waitQ)
            else:
                fut = asyncio.Future(loop=(self.loop))
                self.inflight[req_id] = (
                 msg, fut)
                if not self.protocol:
                    logger.debug('Need to reconnect to server')

                    async def connect_first():
                        await self.reconnect()
                        self.protocol.send_data(msg)

                    self.loop.create_task(connect_first())
                else:
                    self.protocol.send_data(msg)
            return is_subscribe or fut
        return (fut, waitQ)

    def _got_response(self, msg):
        """
            Decode and dispatch responses from the server.

            Has already been unframed and deserialized into an object.
        """
        resp_id = msg.get('id', None)
        if resp_id is None:
            method = msg.get('method', None)
            if not method:
                logger.error('Incoming server message had no ID nor method in it', msg)
                return
            result = msg.get('params', None)
            logger.debug('Traffic on subscription: %s' % method)
            subs = self.subscriptions.get(method)
            for q in subs:
                self.loop.create_task(q.put(result))

            return
        if not 'method' not in msg:
            raise AssertionError
        else:
            result = msg.get('result')
            inf = self.inflight.pop(resp_id)
            if not inf:
                logger.error('Incoming server message had unknown ID in it: %s' % resp_id)
                return
                req, rv = inf
                if 'error' in msg:
                    err = msg['error']
                    logger.info("Error response: '%s'" % err)
                    rv.set_exception(ElectrumErrorResponse(err, req))
            else:
                rv.set_result(result)

    def RPC(self, method, *params):
        """
            Perform a remote command.

            Expects a method name, which look like:

                blockchain.address.get_balance

            .. and sometimes take arguments, all of which are positional.
    
            Returns a future which will you should await for
            the result from the server. Failures are returned as exceptions.
        """
        assert '.' in method
        return self._send_request(method, params)

    def patch_addr_methods(self, method, params):
        from hashlib import sha256
        from binascii import b2a_hex
        try:
            import pycoin.symbols.btc as BTC
        except ImportError:
            raise RuntimeError('we can patch obsolete protocol msgs, but need pycoin>=0.90')

        addr = BTC.parse(params[0])
        sh = sha256(addr.script()).digest()[::-1]
        return (
         method.replace('.address.', '.scripthash.'),
         [
          str(b2a_hex(sh), 'ascii')] + list(params[1:]))

    def subscribe(self, method, *params):
        """
            Perform a remote command which will stream events/data to us.

            Expects a method name, which look like:
                server.peers.subscribe
            .. and sometimes take arguments, all of which are positional.
    
            Returns a tuple: (Future, asyncio.Queue).
            The future will have the result of the initial
            call, and the queue will receive additional
            responses as they happen.
        """
        assert '.' in method
        assert method.endswith('subscribe')
        return self._send_request(method, params, is_subscribe=True)


if __name__ == '__main__':
    from transport import SocketTransport
    from svr_info import KnownServers, ServerInfo
    logging.basicConfig(format='%(asctime)-11s %(message)s', datefmt='[%d/%m/%Y-%H:%M:%S]')
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    proto_code = 's'
    which = ServerInfo({'seen_at':1465686119.022801, 
     'ports':'t s', 
     'nickname':'dunp', 
     'pruning_limit':10000, 
     'version':'1.0', 
     'hostname':'erbium1.sytes.net'})
    c = StratumClient(loop=loop)
    loop.run_until_complete(c.connect(which, proto_code, disable_cert_verify=True, use_tor=True))
    rv = loop.run_until_complete(c.RPC('server.peers.subscribe'))
    print('DONE!: this server has %d peers' % len(rv))
    loop.close()
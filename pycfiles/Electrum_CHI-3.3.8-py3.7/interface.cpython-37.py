# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/interface.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 31012 bytes
import os, re, ssl, sys, traceback, asyncio, socket
from typing import Tuple, Union, List, TYPE_CHECKING, Optional
from collections import defaultdict
from ipaddress import IPv4Network, IPv6Network, ip_address
import itertools, logging, aiorpcx
from aiorpcx import RPCSession, Notification, NetAddress
from aiorpcx.curio import timeout_after, TaskTimeout
from aiorpcx.jsonrpc import JSONRPC, CodeMessageError
from aiorpcx.rawsocket import RSClient
import certifi
from .util import ignore_exceptions, log_exceptions, bfh, SilentTaskGroup
from . import util
from . import x509
from . import pem
from . import version
from . import blockchain
from .blockchain import Blockchain
from . import constants
from .i18n import _
from .logging import Logger
if TYPE_CHECKING:
    from .network import Network
ca_path = certifi.where()
BUCKET_NAME_OF_ONION_SERVERS = 'onion'

class NetworkTimeout:

    class Generic:
        NORMAL = 30
        RELAXED = 45
        MOST_RELAXED = 180

    class Urgent(Generic):
        NORMAL = 10
        RELAXED = 20
        MOST_RELAXED = 60


class NotificationSession(RPCSession):

    def __init__(self, *args, **kwargs):
        (super(NotificationSession, self).__init__)(*args, **kwargs)
        self.subscriptions = defaultdict(list)
        self.cache = {}
        self.default_timeout = NetworkTimeout.Generic.NORMAL
        self._msg_counter = itertools.count(start=1)
        self.interface = None
        self.cost_hard_limit = 0

    def default_framer(self):
        framer = super(NotificationSession, self).default_framer()
        framer.max_size = 20000000
        return framer

    async def handle_request--- This code section failed: ---

 L.  98         0  LOAD_FAST                'self'
                2  LOAD_METHOD              maybe_log
                4  LOAD_STR                 '--> '
                6  LOAD_FAST                'request'
                8  FORMAT_VALUE          0  ''
               10  BUILD_STRING_2        2 
               12  CALL_METHOD_1         1  '1 positional argument'
               14  POP_TOP          

 L.  99        16  SETUP_EXCEPT        150  'to 150'

 L. 100        18  LOAD_GLOBAL              isinstance
               20  LOAD_FAST                'request'
               22  LOAD_GLOBAL              Notification
               24  CALL_FUNCTION_2       2  '2 positional arguments'
               26  POP_JUMP_IF_FALSE   138  'to 138'

 L. 101        28  LOAD_FAST                'request'
               30  LOAD_ATTR                args
               32  LOAD_CONST               None
               34  LOAD_CONST               -1
               36  BUILD_SLICE_2         2 
               38  BINARY_SUBSCR    
               40  LOAD_FAST                'request'
               42  LOAD_ATTR                args
               44  LOAD_CONST               -1
               46  BINARY_SUBSCR    
               48  ROT_TWO          
               50  STORE_FAST               'params'
               52  STORE_FAST               'result'

 L. 102        54  LOAD_FAST                'self'
               56  LOAD_METHOD              get_hashable_key_for_rpc_call
               58  LOAD_FAST                'request'
               60  LOAD_ATTR                method
               62  LOAD_FAST                'params'
               64  CALL_METHOD_2         2  '2 positional arguments'
               66  STORE_FAST               'key'

 L. 103        68  LOAD_FAST                'key'
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                subscriptions
               74  COMPARE_OP               in
               76  POP_JUMP_IF_FALSE   128  'to 128'

 L. 104        78  LOAD_FAST                'result'
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                cache
               84  LOAD_FAST                'key'
               86  STORE_SUBSCR     

 L. 105        88  SETUP_LOOP          136  'to 136'
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                subscriptions
               94  LOAD_FAST                'key'
               96  BINARY_SUBSCR    
               98  GET_ITER         
              100  FOR_ITER            124  'to 124'
              102  STORE_FAST               'queue'

 L. 106       104  LOAD_FAST                'queue'
              106  LOAD_METHOD              put
              108  LOAD_FAST                'request'
              110  LOAD_ATTR                args
              112  CALL_METHOD_1         1  '1 positional argument'
              114  GET_AWAITABLE    
              116  LOAD_CONST               None
              118  YIELD_FROM       
              120  POP_TOP          
              122  JUMP_BACK           100  'to 100'
              124  POP_BLOCK        
              126  JUMP_ABSOLUTE       146  'to 146'
            128_0  COME_FROM            76  '76'

 L. 108       128  LOAD_GLOBAL              Exception
              130  LOAD_STR                 'unexpected notification'
              132  CALL_FUNCTION_1       1  '1 positional argument'
              134  RAISE_VARARGS_1       1  'exception instance'
            136_0  COME_FROM_LOOP       88  '88'
              136  JUMP_FORWARD        146  'to 146'
            138_0  COME_FROM            26  '26'

 L. 110       138  LOAD_GLOBAL              Exception
              140  LOAD_STR                 'unexpected request. not a notification'
              142  CALL_FUNCTION_1       1  '1 positional argument'
              144  RAISE_VARARGS_1       1  'exception instance'
            146_0  COME_FROM           136  '136'
              146  POP_BLOCK        
              148  JUMP_FORWARD        228  'to 228'
            150_0  COME_FROM_EXCEPT     16  '16'

 L. 111       150  DUP_TOP          
              152  LOAD_GLOBAL              Exception
              154  COMPARE_OP               exception-match
              156  POP_JUMP_IF_FALSE   226  'to 226'
              158  POP_TOP          
              160  STORE_FAST               'e'
              162  POP_TOP          
              164  SETUP_FINALLY       214  'to 214'

 L. 112       166  LOAD_FAST                'self'
              168  LOAD_ATTR                interface
              170  LOAD_ATTR                logger
              172  LOAD_METHOD              info
              174  LOAD_STR                 'error handling request '
              176  LOAD_FAST                'request'
              178  FORMAT_VALUE          0  ''
              180  LOAD_STR                 '. exc: '
              182  LOAD_GLOBAL              repr
              184  LOAD_FAST                'e'
              186  CALL_FUNCTION_1       1  '1 positional argument'
              188  FORMAT_VALUE          0  ''
              190  BUILD_STRING_4        4 
              192  CALL_METHOD_1         1  '1 positional argument'
              194  POP_TOP          

 L. 113       196  LOAD_FAST                'self'
              198  LOAD_METHOD              close
              200  CALL_METHOD_0         0  '0 positional arguments'
              202  GET_AWAITABLE    
              204  LOAD_CONST               None
              206  YIELD_FROM       
              208  POP_TOP          
              210  POP_BLOCK        
              212  LOAD_CONST               None
            214_0  COME_FROM_FINALLY   164  '164'
              214  LOAD_CONST               None
              216  STORE_FAST               'e'
              218  DELETE_FAST              'e'
              220  END_FINALLY      
              222  POP_EXCEPT       
              224  JUMP_FORWARD        228  'to 228'
            226_0  COME_FROM           156  '156'
              226  END_FINALLY      
            228_0  COME_FROM           224  '224'
            228_1  COME_FROM           148  '148'

Parse error at or near `COME_FROM_LOOP' instruction at offset 136_0

    async def send_request(self, *args, timeout=None, **kwargs):
        msg_id = next(self._msg_counter)
        self.maybe_logf"<-- {args} {kwargs} (id: {msg_id})"
        try:
            response = await asyncio.wait_for(super().send_request)(*args, **kwargs)timeout
        except (TaskTimeout, asyncio.TimeoutError) as e:
            try:
                raise RequestTimedOut(f"request timed out: {args} (id: {msg_id})") from e
            finally:
                e = None
                del e

        except CodeMessageError as e:
            try:
                self.maybe_logf"--> {repr(e)} (id: {msg_id})"
                raise
            finally:
                e = None
                del e

        else:
            self.maybe_logf"--> {response} (id: {msg_id})"
            return response

    def set_default_timeout(self, timeout):
        self.sent_request_timeout = timeout
        self.max_send_delay = timeout

    async def subscribe(self, method: str, params: List, queue: asyncio.Queue):
        key = self.get_hashable_key_for_rpc_callmethodparams
        self.subscriptions[key].appendqueue
        if key in self.cache:
            result = self.cache[key]
        else:
            result = await self.send_requestmethodparams
            self.cache[key] = result
        await queue.put(params + [result])

    def unsubscribe(self, queue):
        """Unsubscribe a callback to free object references to enable GC."""
        for v in self.subscriptions.values():
            if queue in v:
                v.removequeue

    @classmethod
    def get_hashable_key_for_rpc_call(cls, method, params):
        """Hashable index for subscriptions and cache"""
        return str(method) + repr(params)

    def maybe_log(self, msg: str) -> None:
        if not self.interface:
            return
        if self.interface.debug or self.interface.network.debug:
            self.interface.logger.debugmsg


class NetworkException(Exception):
    pass


class GracefulDisconnect(NetworkException):
    log_level = logging.INFO

    def __init__(self, *args, log_level=None, **kwargs):
        (Exception.__init__)(self, *args, **kwargs)
        if log_level is not None:
            self.log_level = log_level


class RequestTimedOut(GracefulDisconnect):

    def __str__(self):
        return _('Network request timed out.')


class ErrorParsingSSLCert(Exception):
    pass


class ErrorGettingSSLCertFromServer(Exception):
    pass


class ConnectError(NetworkException):
    pass


class _RSClient(RSClient):

    async def create_connection(self):
        try:
            return await super().create_connection()
        except OSError as e:
            try:
                raise ConnectError(e) from e
            finally:
                e = None
                del e


def deserialize_server(server_str: str) -> Tuple[(str, str, str)]:
    host, port, protocol = str(server_str).rsplit':'2
    if not host:
        raise ValueError('host must not be empty')
    if protocol not in ('s', 't'):
        raise ValueError('invalid network protocol: {}'.formatprotocol)
    int(port)
    if not 0 < int(port) < 65536:
        raise ValueError('port {} is out of valid range'.formatport)
    return (
     host, port, protocol)


def serialize_server(host: str, port: Union[(str, int)], protocol: str) -> str:
    return str(':'.join[host, str(port), protocol])


class Interface(Logger):
    LOGGING_SHORTCUT = 'i'

    def __init__(self, network: 'Network', server: str, proxy: Optional[dict]):
        self.ready = asyncio.Future()
        self.got_disconnected = asyncio.Future()
        self.server = server
        self.host, self.port, self.protocol = deserialize_server(self.server)
        self.port = int(self.port)
        Logger.__init__self
        assert network.config.path
        self.cert_path = os.path.join(network.config.path, 'certs', self.host)
        self.blockchain = None
        self._requested_chunks = set()
        self.network = network
        self._set_proxyproxy
        self.session = None
        self._ipaddr_bucket = None
        self.tip_header = None
        self.tip = 0
        self.debug = False
        asyncio.run_coroutine_threadsafeself.network.main_taskgroup.spawnself.run()self.network.asyncio_loop
        self.group = SilentTaskGroup()

    def diagnostic_name(self):
        return f"{self.host}:{self.port}"

    def _set_proxy(self, proxy: dict):
        if proxy:
            username, pw = proxy.get'user', proxy.get'password'
            if username:
                auth = pw or None
            else:
                auth = aiorpcx.socks.SOCKSUserAuthusernamepw
            addr = NetAddress(proxy['host'], proxy['port'])
            if proxy['mode'] == 'socks4':
                self.proxy = aiorpcx.socks.SOCKSProxy(addr, aiorpcx.socks.SOCKS4a, auth)
            elif proxy['mode'] == 'socks5':
                self.proxy = aiorpcx.socks.SOCKSProxy(addr, aiorpcx.socks.SOCKS5, auth)
            else:
                raise NotImplementedError
        else:
            self.proxy = None

    async def is_server_ca_signed(self, ca_ssl_context):
        """Given a CA enforcing SSL context, returns True if the connection
        can be established. Returns False if the server has a self-signed
        certificate but otherwise is okay. Any other failures raise.
        """
        try:
            await self.open_session(ca_ssl_context, exit_early=True)
        except ConnectError as e:
            try:
                cause = e.__cause__
                if isinstance(cause, ssl.SSLError):
                    if cause.reason == 'CERTIFICATE_VERIFY_FAILED':
                        return False
                raise
            finally:
                e = None
                del e

        return True

    async def _try_saving_ssl_cert_for_first_time(self, ca_ssl_context):
        ca_signed = await self.is_server_ca_signedca_ssl_context
        if ca_signed:
            with open(self.cert_path, 'w') as (f):
                f.write''
        else:
            await self.save_certificate()

    def _is_saved_ssl_cert_available(self):
        if not os.path.existsself.cert_path:
            return False
            with open(self.cert_path, 'r') as (f):
                contents = f.read()
            if contents == '':
                return True
        else:
            try:
                b = pem.dePemcontents'CERTIFICATE'
            except SyntaxError as e:
                try:
                    self.logger.infof"error parsing already saved cert: {e}"
                    raise ErrorParsingSSLCert(e) from e
                finally:
                    e = None
                    del e

            try:
                x = x509.X509b
            except Exception as e:
                try:
                    self.logger.infof"error parsing already saved cert: {e}"
                    raise ErrorParsingSSLCert(e) from e
                finally:
                    e = None
                    del e

        try:
            x.check_date()
            return True
        except x509.CertificateError as e:
            try:
                self.logger.infof"certificate has expired: {e}"
                os.unlinkself.cert_path
                return False
            finally:
                e = None
                del e

    async def _get_ssl_context(self):
        if self.protocol != 's':
            return
        ca_sslc = ssl.create_default_context(purpose=(ssl.Purpose.SERVER_AUTH), cafile=ca_path)
        if not self._is_saved_ssl_cert_available():
            try:
                await self._try_saving_ssl_cert_for_first_timeca_sslc
            except (OSError, ConnectError, aiorpcx.socks.SOCKSError) as e:
                try:
                    raise ErrorGettingSSLCertFromServer(e) from e
                finally:
                    e = None
                    del e

        siz = os.statself.cert_path.st_size
        if siz == 0:
            sslc = ca_sslc
        else:
            sslc = ssl.create_default_context((ssl.Purpose.SERVER_AUTH), cafile=(self.cert_path))
            sslc.check_hostname = 0
        return sslc

    def handle_disconnect(func):

        async def wrapper_func(self, *args, **kwargs):
            try:
                try:
                    return await func(self, *args, **kwargs)
                except GracefulDisconnect as e:
                    try:
                        self.logger.loge.log_levelf"disconnecting due to {repr(e)}"
                    finally:
                        e = None
                        del e

                except aiorpcx.jsonrpc.RPCError as e:
                    try:
                        self.logger.warningf"disconnecting due to {repr(e)}"
                        self.logger.debug(f"(disconnect) trace for {repr(e)}", exc_info=True)
                    finally:
                        e = None
                        del e

            finally:
                await self.network.connection_downself
                if not self.got_disconnected.done():
                    self.got_disconnected.set_result1
                self.ready.cancel()

        return wrapper_func

    @ignore_exceptions
    @log_exceptions
    @handle_disconnect
    async def run(self):
        try:
            ssl_context = await self._get_ssl_context()
        except (ErrorParsingSSLCert, ErrorGettingSSLCertFromServer) as e:
            try:
                self.logger.infof"disconnecting due to: {repr(e)}"
                return
            finally:
                e = None
                del e

        try:
            await self.open_sessionssl_context
        except (asyncio.CancelledError, ConnectError, aiorpcx.socks.SOCKSError) as e:
            try:
                self.logger.infof"disconnecting due to: {repr(e)}"
                return
            finally:
                e = None
                del e

    def mark_ready(self):
        if self.ready.cancelled():
            raise GracefulDisconnect('conn establishment was too slow; *ready* future was cancelled')
        elif self.ready.done():
            return
            assert self.tip_header
            chain = blockchain.check_headerself.tip_header
            self.blockchain = chain or blockchain.get_best_chain()
        else:
            self.blockchain = chain
        assert self.blockchain is not None
        self.logger.infof"set blockchain with height {self.blockchain.height()}"
        self.ready.set_result1

    async def save_certificate(self):
        if not os.path.existsself.cert_path:
            for _ in range(10):
                dercert = await self.get_certificate()
                if dercert:
                    self.logger.info'succeeded in getting cert'
                    with open(self.cert_path, 'w') as (f):
                        cert = ssl.DER_cert_to_PEM_certdercert
                        cert = re.sub('([^\n])-----END CERTIFICATE-----', '\\1\n-----END CERTIFICATE-----', cert)
                        f.writecert
                        f.flush()
                        os.fsyncf.fileno()
                    break
                await asyncio.sleep1
            else:
                raise GracefulDisconnect('could not get certificate after 10 tries')

    async def get_certificate(self):
        sslc = ssl.SSLContext()
        try:
            async with _RSClient(session_factory=RPCSession, host=(self.host),
              port=(self.port),
              ssl=sslc,
              proxy=(self.proxy)) as session:
                return session.transport._asyncio_transport._ssl_protocol._sslpipe._sslobj.getpeercertTrue
        except ValueError:
            return

    async def get_block_header(self, height, assert_mode):
        self.logger.infof"requesting block header {height} in mode {assert_mode}"
        timeout = self.network.get_network_timeout_secondsNetworkTimeout.Urgent
        cp_height = constants.net.max_checkpoint()
        if height > cp_height:
            cp_height = 0
        res = await self.session.send_request('blockchain.block.header', [height, cp_height], timeout=timeout)
        if cp_height != 0:
            res = res['header']
        return blockchain.deserialize_full_headerbytes.fromhexresheight

    async def request_chunk(self, height, tip=None, *, can_return_early=False):
        index = height // 2016
        if can_return_early:
            if index in self._requested_chunks:
                return
        else:
            self.logger.infof"requesting chunk from height {height}"
            size = 2016
            if tip is not None:
                size = min(size, tip - index * 2016 + 1)
                size = max(size, 0)
            try:
                cp_height = constants.net.max_checkpoint()
                if index * 2016 + size - 1 > cp_height:
                    cp_height = 0
                self._requested_chunks.addindex
                res = await self.session.send_request'blockchain.block.headers'[index * 2016, size, cp_height]
            finally:
                try:
                    self._requested_chunks.removeindex
                except KeyError:
                    pass

            conn = self.blockchain.connect_chunkindexres['hex']
            return conn or (
             conn, 0)
        return (
         conn, res['count'])

    def is_main_server(self) -> bool:
        return self.network.default_server == self.server

    async def open_session(self, sslc, exit_early=False):
        async with _RSClient(session_factory=NotificationSession, host=(self.host),
          port=(self.port),
          ssl=sslc,
          proxy=(self.proxy)) as session:
            self.session = session
            self.session.interface = self
            self.session.set_default_timeoutself.network.get_network_timeout_secondsNetworkTimeout.Generic
            try:
                ver = await session.send_request'server.version'[self.client_name(), version.PROTOCOL_VERSION]
            except aiorpcx.jsonrpc.RPCError as e:
                try:
                    raise GracefulDisconnect(e)
                finally:
                    e = None
                    del e

            if exit_early:
                return
            if not self.network.check_interface_against_healthy_spread_of_connected_serversself:
                raise GracefulDisconnect(f"too many connected servers already in bucket {self.bucket_based_on_ipaddress()}")
            self.logger.infof"connection established. version: {ver}"
            try:
                async with self.group as group:
                    await group.spawnself.ping
                    await group.spawnself.run_fetch_blocks
                    await group.spawnself.monitor_connection
            except aiorpcx.jsonrpc.RPCError as e:
                try:
                    if e.code in (JSONRPC.EXCESSIVE_RESOURCE_USAGE,
                     JSONRPC.SERVER_BUSY,
                     JSONRPC.METHOD_NOT_FOUND):
                        raise GracefulDisconnect(e, log_level=(logging.WARNING)) from e
                    raise
                finally:
                    e = None
                    del e

    async def monitor_connection(self):
        while 1:
            await asyncio.sleep1
            if not self.session or self.session.is_closing():
                raise GracefulDisconnect('session was closed')

    async def ping(self):
        while True:
            await asyncio.sleep300
            await self.session.send_request'server.ping'

    async def close(self):
        if self.session:
            await self.session.close()

    async def run_fetch_blocks(self):
        header_queue = asyncio.Queue()
        await self.session.subscribe('blockchain.headers.subscribe', [], header_queue)
        while True:
            item = await header_queue.get()
            raw_header = item[0]
            height = raw_header['height']
            header = blockchain.deserialize_full_headerbfh(raw_header['hex'])height
            self.tip_header = header
            self.tip = height
            if self.tip < constants.net.max_checkpoint():
                raise GracefulDisconnect('server tip below max checkpoint')
            self.mark_ready()
            await self._process_header_at_tip()
            self.network.trigger_callback'network_updated'
            await self.network.switch_unwanted_fork_interface()
            await self.network.switch_lagging_interface()

    async def _process_header_at_tip(self):
        height, header = self.tip, self.tip_header
        async with self.network.bhi_lock:
            if self.blockchain.height() >= height:
                if self.blockchain.check_headerheader:
                    self.logger.infof"skipping header {height}"
                    return
            _, height = await self.stepheightheader
            if height <= self.tip:
                await self.sync_untilheight
        self.network.trigger_callback'blockchain_updated'

    async def sync_until(self, height, next_height=None):
        if next_height is None:
            next_height = self.tip
        last = None
        while last is None or height <= next_height:
            prev_last, prev_height = last, height
            if next_height > height + 10:
                could_connect, num_headers = await self.request_chunkheightnext_height
                if not could_connect:
                    if height <= constants.net.max_checkpoint():
                        raise GracefulDisconnect('server chain conflicts with checkpoints or genesis')
                    last, height = await self.stepheight
                    continue
                self.network.trigger_callback'network_updated'
                height = height // 2016 * 2016 + num_headers
                assert height <= next_height + 1, (height, self.tip)
                last = 'catchup'
            else:
                last, height = await self.stepheight
            assert (
             prev_last, prev_height) != (last, height), 'had to prevent infinite loop in interface.sync_until'

        return (
         last, height)

    async def step(self, height, header=None):
        if not 0 <= height <= self.tip:
            raise AssertionError((height, self.tip))
        elif header is None:
            header = await self.get_block_headerheight'catchup'
        else:
            chain = blockchain.check_headerheader if 'mock' not in header else header['mock']['check'](header)
            if chain:
                self.blockchain = chain if isinstance(chain, Blockchain) else self.blockchain
                return (
                 'catchup', height + 1)
            can_connect = blockchain.can_connectheader if 'mock' not in header else header['mock']['connect'](height)
            if not can_connect:
                self.logger.infof"can't connect {height}"
                height, header, bad, bad_header = await self._search_headers_backwardsheightheader
                chain = blockchain.check_headerheader if 'mock' not in header else header['mock']['check'](header)
                can_connect = blockchain.can_connectheader if 'mock' not in header else header['mock']['connect'](height)
                if not chain:
                    if not can_connect:
                        raise AssertionError
        if can_connect:
            self.logger.infof"could connect {height}"
            height += 1
            if isinstance(can_connect, Blockchain):
                self.blockchain = can_connect
                self.blockchain.save_headerheader
            return (
             'catchup', height)
        good, bad, bad_header = await self._search_headers_binary(height, bad, bad_header, chain)
        return await self._resolve_potential_chain_fork_given_forkpoint(good, bad, bad_header)

    async def _search_headers_binary(self, height, bad, bad_header, chain):
        assert bad == bad_header['block_height']
        _assert_header_does_not_check_against_any_chain(bad_header)
        self.blockchain = chain if isinstance(chain, Blockchain) else self.blockchain
        good = height
        while 1:
            if not good < bad:
                raise AssertionError((good, bad))
            else:
                height = (good + bad) // 2
                self.logger.infof"binary step. good {good}, bad {bad}, height {height}"
                header = await self.get_block_headerheight'binary'
                chain = blockchain.check_headerheader if 'mock' not in header else header['mock']['check'](header)
                if chain:
                    self.blockchain = chain if isinstance(chain, Blockchain) else self.blockchain
                    good = height
                else:
                    bad = height
                bad_header = header
            if good + 1 == bad:
                break

        mock = 'mock' in bad_header and bad_header['mock']['connect'](height)
        real = not mock and self.blockchain.can_connect(bad_header, check_height=False)
        if not (real or mock):
            raise Exception('unexpected bad header during binary: {}'.formatbad_header)
        _assert_header_does_not_check_against_any_chain(bad_header)
        self.logger.infof"binary search exited. good {good}, bad {bad}"
        return (good, bad, bad_header)

    async def _resolve_potential_chain_fork_given_forkpoint(self, good, bad, bad_header):
        assert good + 1 == bad
        assert bad == bad_header['block_height']
        _assert_header_does_not_check_against_any_chain(bad_header)
        bh = self.blockchain.height()
        assert bh >= good, (bh, good)
        if bh == good:
            height = good + 1
            self.logger.infof"catching up from {height}"
            return ('no_fork', height)
        height = bad + 1
        self.logger.infof"new fork at bad height {bad}"
        forkfun = self.blockchain.fork if 'mock' not in bad_header else bad_header['mock']['fork']
        b = forkfun(bad_header)
        self.blockchain = b
        assert b.forkpoint == bad
        return ('fork', height)

    async def _search_headers_backwards(self, height, header):

        async def iterate():
            nonlocal header
            nonlocal height
            checkp = False
            if height <= constants.net.max_checkpoint():
                height = constants.net.max_checkpoint()
                checkp = True
            header = await self.get_block_headerheight'backward'
            chain = blockchain.check_headerheader if 'mock' not in header else header['mock']['check'](header)
            can_connect = blockchain.can_connectheader if 'mock' not in header else header['mock']['connect'](height)
            if chain or can_connect:
                return False
            if checkp:
                raise GracefulDisconnect('server chain conflicts with checkpoints')
            return True

        bad, bad_header = height, header
        _assert_header_does_not_check_against_any_chain(bad_header)
        with blockchain.blockchains_lock:
            chains = list(blockchain.blockchains.values())
        local_max = max([0] + [x.height() for x in chains]) if 'mock' not in header else float('inf')
        height = min(local_max + 1, height - 1)
        while await iterate():
            bad, bad_header = height, header
            delta = self.tip - height
            height = self.tip - 2 * delta

        _assert_header_does_not_check_against_any_chain(bad_header)
        self.logger.infof"exiting backward mode at {height}"
        return (height, header, bad, bad_header)

    @classmethod
    def client_name(cls) -> str:
        return f"electrum-chi/{version.ELECTRUM_VERSION}"

    def is_tor(self):
        return self.host.endswith'.onion'

    def ip_addr(self) -> Optional[str]:
        session = self.session
        if not session:
            return
        else:
            peer_addr = session.remote_address()
            return peer_addr or None
        return str(peer_addr.host)

    def bucket_based_on_ipaddress(self) -> str:

        def do_bucket():
            if self.is_tor():
                return BUCKET_NAME_OF_ONION_SERVERS
            try:
                ip_addr = ip_address(self.ip_addr())
            except ValueError:
                return ''
            else:
                if not ip_addr:
                    return ''
                if ip_addr.version == 4:
                    slash16 = IPv4Network(ip_addr).supernet(prefixlen_diff=16)
                    return str(slash16)
                if ip_addr.version == 6:
                    slash48 = IPv6Network(ip_addr).supernet(prefixlen_diff=80)
                    return str(slash48)
                return ''

        if not self._ipaddr_bucket:
            self._ipaddr_bucket = do_bucket()
        return self._ipaddr_bucket


def _assert_header_does_not_check_against_any_chain(header: dict) -> None:
    chain_bad = blockchain.check_headerheader if 'mock' not in header else header['mock']['check'](header)
    if chain_bad:
        raise Exception('bad_header must not check!')


def check_cert(host, cert):
    try:
        b = pem.dePemcert'CERTIFICATE'
        x = x509.X509b
    except:
        traceback.print_exc(file=(sys.stdout))
        return
    else:
        try:
            x.check_date()
            expired = False
        except:
            expired = True

        m = 'host: %s\n' % host
        m += 'has_expired: %s\n' % expired
        util.print_msgm


def _match_hostname(name, val):
    if val == name:
        return True
    return val.startswith'*.' and name.endswithval[1:]


def test_certificates():
    from .simple_config import SimpleConfig
    config = SimpleConfig()
    mydir = os.path.joinconfig.path'certs'
    certs = os.listdirmydir
    for c in certs:
        p = os.path.joinmydirc
        with open(p, encoding='utf-8') as (f):
            cert = f.read()
        check_cert(c, cert)


if __name__ == '__main__':
    test_certificates()
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/peng3dnet/net.py
# Compiled at: 2020-04-07 16:15:42
# Size of source mod 2**32: 64499 bytes
__all__ = [
 'STRUCT_HEADER', 'STRUCT_LENGTH32',
 'Server', 'ClientOnServer',
 'Client']
import sys, time, struct, threading, socket, selectors, warnings, collections, zlib
if sys.version_info.major == 2:
    import Queue
else:
    if sys.version_info.major == 3:
        import queue as Queue
    else:
        raise ValueError('Python version %s is not supported' % sys.version)
try:
    import msgpack
    _MSGPACK_TYPE = 'msgpack-python'
except ImportError:
    import umsgpack as msgpack
    _MSGPACK_TYPE = 'umsgpack'

try:
    import ssl
except (ImportError, AttributeError):
    HAVE_SSL = False
else:
    HAVE_SSL = True
import peng3d
from . import version
from . import packet
from . import util
from . import registry
from . import errors
from . import conntypes
from .constants import *
STRUCT_HEADER = struct.Struct(STRUCT_FORMAT_HEADER)
STRUCT_LENGTH32 = struct.Struct(STRUCT_FORMAT_LENGTH32)
try:
    unicode = unicode
except NameError:
    str = str
    unicode = str
    bytes = bytes
    basestring = (str, bytes)
else:
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring

class Server(object):
    __doc__ = '\n    Server class representing the server side of the client-server relationship.\n    \n    Usually, a server will be able to serve many clients simultaneously without problems.\n    This is achieved using the :py:mod:`selectors` standard library module, which\n    internally uses :py:mod:`select` or similiar techniques.\n    \n    If given, ``peng`` should be an instance of :py:class:`peng3d.peng.Peng` and\n    will be used for sending events and the configuration system. Note that without\n    a valid ``peng`` parameter, the event system will not work and a custom config\n    stack will be created.\n    If a ``peng`` parameter is given, its config stack will be adapted and the event system enabled.\n    \n    .. seealso::\n       See :confval:`net.events.enable` and :doc:`/events` for more information on the event system.\n    \n    ``addr``\\ , if given, should be a value parseable by :py:func:`peng3dnet.util.normalize_addr_socketstyle()`\\ .\n    If ``addr`` is not given, first :confval:`net.server.addr` is tried, then :confval:`net.server.addr.host` and :confval:`net.server.addr.port`\\ .\n    If any given address is missing an explicitly specified port, :confval:`net.server.addr.port` is supplemented.\n    \n    ``clientcls`` may be used to override the class used for creating new client-on-server objects.\n    Defaults to :py:class:`ClientOnServer`\\ .\n    \n    ``cfg`` may be used to override initial configuration values and should be a dictionary.\n    '

    def __init__(self, peng=None, addr=None, clientcls=None, cfg=None):
        cfg = cfg if cfg is not None else {}
        if peng is None:
            self.cfg = peng3d.config.Config(cfg, DEFAULT_CONFIG)
        else:
            ncfg = {}
            ncfg.update(DEFAULT_CONFIG)
            ncfg.update(cfg)
            self.cfg = peng3d.config.Config(ncfg, peng.cfg)
        if addr is not None:
            addr = util.normalize_addr_socketstyle(addr, self.cfg['net.server.addr.port'])
            self.cfg['net.server.addr.host'] = addr[0]
            self.cfg['net.server.addr.port'] = addr[1]
        else:
            if self.cfg['net.server.addr'] is None:
                addr = util.normalize_addr_socketstyle(self.cfg['net.server.addr.host'], self.cfg['net.server.addr.port'])
            else:
                addr = util.normalize_addr_socketstyle(self.cfg['net.server.addr'], self.cfg['net.server.addr.port'])
        if self.cfg['net.events.enable'] == 'auto':
            self.cfg['net.events.enable'] = peng is not None
        self.peng = peng
        self.addr = addr
        self.is_client = False
        self.is_server = True
        self.side = SIDE_SERVER
        self.sock = None
        self._sock_lock = threading.Lock()
        self.selector = None
        self._selector_lock = threading.Lock()
        self._next_cid = 1
        self._cid_lock = threading.Lock()
        self._init_lock = threading.Lock()
        self._is_bound = False
        self._is_started = False
        self._is_initialized = False
        self._irqrecv = None
        self._irqsend = None
        self.clientcls = clientcls if clientcls is not None else ClientOnServer
        self._run_thread = None
        self._process_thread = None
        self._process_queue = Queue.Queue()
        self._process_condition = threading.Condition()
        self.run = True
        self.clients = {}
        self.conntypes = {}
        self.registry = registry.PacketRegistry()

    def initialize(self):
        """
        Initializes internal registries used during runtime.
        
        Calling this method repeatedly will be ignored.
        
        Currently, this registers packets and connection types.
        Additionally, the :peng3d:event:`peng3dnet:server.initialize` event is sent.
        
        Subclasses and Mix-ins may hook into this method via definition of methods
        named ``_reg_packets_*`` or ``_reg_conntypes_*`` with the star being an arbitrary string.
        The method may not take any arguments.
        """
        if self._is_initialized:
            return
        with self._init_lock:
            if self._is_initialized:
                return
            from .packet import internal
            self.register_packet('peng3dnet:internal.hello', internal.HelloPacket(self.registry, self), 1)
            self.register_packet('peng3dnet:internal.settype', internal.SetTypePacket(self.registry, self), 2)
            self.register_packet('peng3dnet:internal.handshake', internal.HandshakePacket(self.registry, self), 3)
            self.register_packet('peng3dnet:internal.handshake.accept', internal.HandshakeAcceptPacket(self.registry, self), 4)
            self.register_packet('peng3dnet:internal.closeconn', internal.CloseConnectionPacket(self.registry, self), 16)
            for attr in dir(self):
                if attr.startswith('_reg_packets_') and callable(getattr(self, attr, None)):
                    getattr(self, attr)()

            self.addConnType('classic', conntypes.ClassicConnectionType(self))
            for attr in dir(self):
                if attr.startswith('_reg_conntypes_') and callable(getattr(self, attr, None)):
                    getattr(self, attr)()

            self.sendEvent('peng3dnet:server.initialize', {})

    def bind--- This code section failed: ---

 L. 255         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _is_bound
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 256         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 257        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sock_lock
            14_16  SETUP_WITH          348  'to 348'
               18  POP_TOP          

 L. 258        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _is_bound
               24  POP_JUMP_IF_FALSE    30  'to 30'

 L. 259        26  LOAD_CONST               None
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'

 L. 261        30  LOAD_FAST                'self'
               32  LOAD_ATTR                cfg
               34  LOAD_STR                 'net.ssl.enabled'
               36  BINARY_SUBSCR    
               38  POP_JUMP_IF_FALSE    64  'to 64'
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                cfg
               44  LOAD_STR                 'net.ssl.force'
               46  BINARY_SUBSCR    
               48  POP_JUMP_IF_FALSE    64  'to 64'
               50  LOAD_GLOBAL              HAVE_SSL
               52  POP_JUMP_IF_TRUE     64  'to 64'

 L. 262        54  LOAD_GLOBAL              RuntimeError
               56  LOAD_STR                 'SSL Has not been found, but it is required'
               58  CALL_FUNCTION_1       1  '1 positional argument'
               60  RAISE_VARARGS_1       1  'exception instance'
               62  JUMP_FORWARD        126  'to 126'
             64_0  COME_FROM            52  '52'
             64_1  COME_FROM            48  '48'
             64_2  COME_FROM            38  '38'

 L. 263        64  LOAD_FAST                'self'
               66  LOAD_ATTR                cfg
               68  LOAD_STR                 'net.ssl.enabled'
               70  BINARY_SUBSCR    
               72  POP_JUMP_IF_FALSE    78  'to 78'
               74  LOAD_GLOBAL              HAVE_SSL
               76  POP_JUMP_IF_FALSE   106  'to 106'
             78_0  COME_FROM            72  '72'

 L. 264        78  LOAD_FAST                'self'
               80  LOAD_ATTR                cfg
               82  LOAD_STR                 'net.ssl.server.certfile'
               84  BINARY_SUBSCR    
               86  LOAD_CONST               None
               88  COMPARE_OP               is
               90  POP_JUMP_IF_TRUE    106  'to 106'

 L. 265        92  LOAD_FAST                'self'
               94  LOAD_ATTR                cfg
               96  LOAD_STR                 'net.ssl.server.keyfile'
               98  BINARY_SUBSCR    
              100  LOAD_CONST               None
              102  COMPARE_OP               is
              104  POP_JUMP_IF_FALSE   126  'to 126'
            106_0  COME_FROM            90  '90'
            106_1  COME_FROM            76  '76'

 L. 266       106  LOAD_CONST               False
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                cfg
              112  LOAD_STR                 'net.ssl.enabled'
              114  STORE_SUBSCR     

 L. 267       116  LOAD_GLOBAL              warnings
              118  LOAD_METHOD              warn
              120  LOAD_STR                 'Potential security weakness because ssl had to be disabled'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  POP_TOP          
            126_0  COME_FROM           104  '104'
            126_1  COME_FROM            62  '62'

 L. 269       126  LOAD_GLOBAL              socket
              128  LOAD_METHOD              socketpair
              130  CALL_METHOD_0         0  '0 positional arguments'
              132  UNPACK_SEQUENCE_2     2 
              134  LOAD_FAST                'self'
              136  STORE_ATTR               _irqrecv
              138  LOAD_FAST                'self'
              140  STORE_ATTR               _irqsend

 L. 271       142  LOAD_GLOBAL              socket
              144  LOAD_METHOD              socket
              146  LOAD_GLOBAL              socket
              148  LOAD_ATTR                AF_INET
              150  LOAD_GLOBAL              socket
              152  LOAD_ATTR                SOCK_STREAM
              154  CALL_METHOD_2         2  '2 positional arguments'
              156  LOAD_FAST                'self'
              158  STORE_ATTR               sock

 L. 273       160  LOAD_FAST                'self'
              162  LOAD_ATTR                sock
              164  LOAD_METHOD              setsockopt
              166  LOAD_GLOBAL              socket
              168  LOAD_ATTR                SOL_SOCKET
              170  LOAD_GLOBAL              socket
              172  LOAD_ATTR                SO_REUSEADDR
              174  LOAD_CONST               1
              176  CALL_METHOD_3         3  '3 positional arguments'
              178  POP_TOP          

 L. 274       180  LOAD_FAST                'self'
              182  LOAD_ATTR                sock
              184  LOAD_METHOD              bind
              186  LOAD_GLOBAL              tuple
              188  LOAD_FAST                'self'
              190  LOAD_ATTR                addr
              192  CALL_FUNCTION_1       1  '1 positional argument'
              194  CALL_METHOD_1         1  '1 positional argument'
              196  POP_TOP          

 L. 275       198  LOAD_FAST                'self'
              200  LOAD_ATTR                sock
              202  LOAD_METHOD              listen
              204  LOAD_CONST               100
              206  CALL_METHOD_1         1  '1 positional argument'
              208  POP_TOP          

 L. 276       210  LOAD_FAST                'self'
              212  LOAD_ATTR                sock
              214  LOAD_METHOD              setblocking
              216  LOAD_CONST               False
              218  CALL_METHOD_1         1  '1 positional argument'
              220  POP_TOP          

 L. 278       222  LOAD_FAST                'self'
              224  LOAD_ATTR                cfg
              226  LOAD_STR                 'net.ssl.enabled'
              228  BINARY_SUBSCR    
          230_232  POP_JUMP_IF_FALSE   316  'to 316'

 L. 279       234  LOAD_GLOBAL              ssl
              236  LOAD_ATTR                create_default_context
              238  LOAD_GLOBAL              ssl
              240  LOAD_ATTR                Purpose
              242  LOAD_ATTR                CLIENT_AUTH
              244  LOAD_FAST                'self'
              246  LOAD_ATTR                cfg
              248  LOAD_STR                 'net.ssl.server.certfile'
              250  BINARY_SUBSCR    
              252  LOAD_CONST               ('cafile',)
              254  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              256  LOAD_FAST                'self'
              258  STORE_ATTR               sslcontext

 L. 280       260  LOAD_FAST                'self'
              262  LOAD_ATTR                sslcontext
              264  LOAD_ATTR                load_cert_chain
              266  LOAD_FAST                'self'
              268  LOAD_ATTR                cfg
              270  LOAD_STR                 'net.ssl.server.certfile'
              272  BINARY_SUBSCR    
              274  LOAD_FAST                'self'
              276  LOAD_ATTR                cfg
              278  LOAD_STR                 'net.ssl.server.keyfile'
              280  BINARY_SUBSCR    
              282  LOAD_CONST               ('certfile', 'keyfile')
              284  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              286  POP_TOP          

 L. 283       288  LOAD_FAST                'self'
              290  LOAD_ATTR                cfg
              292  LOAD_STR                 'net.ssl.server.force_verify'
              294  BINARY_SUBSCR    
          296_298  POP_JUMP_IF_FALSE   306  'to 306'
              300  LOAD_GLOBAL              ssl
              302  LOAD_ATTR                CERT_REQUIRED
              304  JUMP_FORWARD        310  'to 310'
            306_0  COME_FROM           296  '296'
              306  LOAD_GLOBAL              ssl
              308  LOAD_ATTR                CERT_OPTIONAL
            310_0  COME_FROM           304  '304'
              310  LOAD_FAST                'self'
              312  LOAD_ATTR                sslcontext
              314  STORE_ATTR               verify_mode
            316_0  COME_FROM           230  '230'

 L. 286       316  LOAD_CONST               True
              318  LOAD_FAST                'self'
              320  STORE_ATTR               _is_bound

 L. 288       322  LOAD_FAST                'self'
              324  LOAD_METHOD              sendEvent
              326  LOAD_STR                 'peng3dnet:server.bind'
              328  LOAD_STR                 'addr'
              330  LOAD_GLOBAL              tuple
              332  LOAD_FAST                'self'
              334  LOAD_ATTR                addr
              336  CALL_FUNCTION_1       1  '1 positional argument'
              338  BUILD_MAP_1           1 
              340  CALL_METHOD_2         2  '2 positional arguments'
              342  POP_TOP          
              344  POP_BLOCK        
              346  LOAD_CONST               None
            348_0  COME_FROM_WITH       14  '14'
              348  WITH_CLEANUP_START
              350  WITH_CLEANUP_FINISH
              352  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 344

    def runBlocking(self, selector=selectors.DefaultSelector):
        """
        Runs the server main loop in a blocking manner.
        
        ``selector`` may be changed to override the selector used for smart waiting.
        
        This method blocks until :py:meth:`stop()` is called.
        """
        if self._is_started:
            return
        self.initialize()
        self.bind()
        with self._selector_lock:
            if self._is_started:
                return
            self.selector = selector()
            self.selector.register(self.sock, selectors.EVENT_READ, [self._accept, self])
            self.selector.register(self._irqrecv, selectors.EVENT_READ, [self._client_ready, None])
            self.selector.register(self._irqsend, selectors.EVENT_READ, [self._client_ready, None])
            self._is_started = True
            self.sendEvent('peng3dnet:server.start', {})
        while self.run:
            events = self.selector.select()
            for key, mask in events:
                callback, data = key.data
                try:
                    callback(key.fileobj, mask, data)
                except Exception:
                    import traceback
                    traceback.print_exc()

    def runAsync(self, selector=selectors.DefaultSelector):
        """
        Runs the server main loop in a seperate thread.
        
        ``selector`` may be changed to override the selector used for smart waiting.
        
        This method does not block and should return immediately.
        
        The newly created thread will be named ``peng3dnet Server Thread`` and is
        a daemon thread, i.e. it will not keep the program alive.
        """
        self._run_thread = threading.Thread(name='peng3dnet Server Thread', target=(self.runBlocking), args=[selector])
        self._run_thread.daemon = True
        self._run_thread.start()

    def stop(self):
        """
        Stops the running server main loop.
        
        Will set an internal flag, then sends the event :peng3d:event:`peng3dnet:server.stop`
        and calls :py:meth:`interrupt()` to force the close.
        
        Note that this will not close open connections properly, use :py:meth:`shutdown()` instead.
        """
        self.run = False
        self.sendEvent('peng3dnet:server.stop', {'reason': 'method'})
        self.interrupt()

    def interrupt(self):
        """
        Wakes up the main loop by sending a special message to an internal socket.
        
        This forces the main loop to iterate once and check that the system is still running.
        
        Also sends the :peng3d:event:`peng3dnet:server.interrupt` event.
        """
        self._irqsend.sendall(b'wake up!')
        self.sendEvent('peng3dnet:server.interrupt', {})

    def shutdown(self, join=True, timeout=0, reason='servershutdown'):
        r"""
        Shuts down the server, disconnecting all clients.
        
        If ``join`` is true, this method will block until all clients are disconnected or ``timeout`` seconds have passed.
        If ``timeout`` is ``0``\ , it will be ignored.
        
        ``reason`` will be used as the closing reason and transmitted to all clients.
        
        After these messages have been sent, :py:meth:`stop()` is called and the :peng3d:event:`peng3dnet:server.shutdown` event is sent.
        """
        for cid in list(self.clients.keys()):
            try:
                self.close_connection(cid, reason)
            except Exception:
                pass

        if join:
            t = time.time()
            while len(self.clients) > 0 and time.time() - t < timeout:
                time.sleep(0.01)

        self.stop()
        self.sendEvent('peng3dnet:server.shutdown', {'reason':reason,  'join':join,  'timeout':timeout})
        if join:
            self.join(timeout - (time.time() - t))

    def join(self, timeout=None):
        """
        Waits for all spawned threads to finish.
        
        If ``timeout`` is given, it indicates the total amount of time spent waiting.
        
        If a thread has not been started yet, it will be skipped and not waited for.
        """
        self.stop()
        ft = time.time() + timeout if timeout is not None else 1
        if self._run_thread is not None:
            if timeout is None:
                self._run_thread.join()
            else:
                self._run_thread.join(max(ft - time.time(), 0))
        elif self._process_thread is not None:
            if timeout is None:
                self._process_thread.join()
            else:
                self._process_thread.join(max(ft - time.time(), 0))

    def _accept(self, sock, mask, data):
        conn, addr = sock.accept()
        if self.cfg['net.ssl.enabled']:
            conn = self.sslcontext.wrap_socket(conn, server_side=True)
        conn.setblocking(False)
        client = self.clientcls(self, conn, addr, self.genCID())
        self.clients[client.cid] = client
        with self._selector_lock:
            self.selector.register(conn, selectors.EVENT_READ, [self._client_ready, client])
        if not self.cfg['net.ssl.enabled']:
            client.state = STATE_HELLOWAIT
            client.on_connect()
            self.send_message('peng3dnet:internal.hello', {'version':version.VERSION,  'protoversion':version.PROTOVERSION}, client.cid)
            self.sendEvent('peng3dnet:server.connection.accept', {'sock':conn,  'addr':addr,  'client':client,  'cid':client.cid})

    def _client_ready(self, conn, mask, data):
        if data is not None and self.cfg['net.ssl.enabled']:
            if data.ssl_state == 'handshake':
                try:
                    conn.do_handshake()
                except ssl.SSLWantWriteError:
                    skey = self.selector.get_key(conn)
                    if not skey & selectors.EVENT_WRITE:
                        self.selector.modify(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, [self._client_ready, data])
                except ssl.SSLWantReadError:
                    pass
                else:
                    data.ssl_state = 'connected'
                    data.state = STATE_HELLOWAIT
                    data.on_connect()
                    self.send_message('peng3dnet:internal.hello', {'version':version.VERSION,  'protoversion':version.PROTOVERSION}, data.cid)
                    self.sendEvent('peng3dnet:server.connection.accept', {'sock':conn,  'addr':data.addr,  'client':data,  'cid':data.cid})
                return
            else:
                if mask & selectors.EVENT_READ:
                    if conn == self._irqrecv:
                        dat = conn.recv(8)
                        if dat != b'wake up!':
                            conn.sendall(b'wrong socket')
                        return
                    if conn == self._irqsend:
                        dat = conn.recv(1024)
                        return
                    if self.cfg['net.ssl.enabled']:
                        try:
                            dat = conn.recv(1024)
                        except ssl.SSLWantWriteError:
                            skey = self.selector.get_key(conn)
                            if not skey & selectors.EVENT_WRITE:
                                self.selector.modify(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, [self._client_ready, data])
                            dat = ''
                        except ssl.SSLWantReadError:
                            dat = ''

                    else:
                        try:
                            dat = conn.recv(1024)
                        except OSError:
                            with self._selector_lock:
                                self.selector.unregister(conn)
                            data.close()
                            return

                        if dat:
                            try:
                                self.receive_data(dat, data.cid)
                            except Exception:
                                import traceback
                                traceback.print_exc()

                        else:
                            with self._selector_lock:
                                self.selector.unregister(conn)
                            data.close()
                if mask & selectors.EVENT_WRITE:
                    if data is None:
                        return
                    try:
                        msg = data.write_queue.popleft()
                    except IndexError:
                        with self._selector_lock:
                            self.selector.modify(conn, selectors.EVENT_READ, [self._client_ready, data])
                    else:
                        if self.cfg['net.ssl.enabled']:
                            try:
                                conn.sendall(msg)
                            except ssl.SSLWantWriteError:
                                pass
                            except ssl.SSLWantReadError:
                                pass
                            else:
                                data.write_queue.appendleft(msg)
                else:
                    conn.sendall(msg)
            if len(data.write_queue) == 0:
                with self._selector_lock:
                    self.selector.modify(conn, selectors.EVENT_READ, [self._client_ready, data])
        elif data._mark_close:
            if len(data.write_queue) == 0:
                with self._selector_lock:
                    self.selector.unregister(conn)
                data.close()

    def genCID(self):
        """
        Generates a client ID number.
        
        These IDs are guaranteed to be unique to the instance that generated them.
        
        Usually, these will be integers that simply count up and are not meant to be cryptographically secure.
        """
        with self._cid_lock:
            cid = self._next_cid
            self._next_cid += 1
            return cid

    def receive_data(self, data, cid):
        """
        Called when new raw data has been read from a socket.
        
        Note that the given ``data`` may contain only parts of a packet or even multiple packets.
        
        ``cid`` is the integer ID number of the client the data was received from.
        
        By default, the received data is stored in a buffer until enough data is available to process a packet, then :py:meth:`process_single_packet()` is called.
        """
        client = self.clients[cid]
        client._buf += data
        while not (client._buflen is None and len(client._buf) > 0):
            if not client._buflen is not None or len(client._buf) >= client._buflen:
                self.process_single_packet(client)

    def process_single_packet(self, client):
        """
        Called when there should be enough data to process a single packet.
        
        ``client`` is an instance of :py:class:`ClientOnServer` representing the client.
        
        Currently parses a single packet including length prefix and calls :py:meth:`receive_packet()` with the packet data.
        """
        if client._buflen is None:
            if len(client._buf) < STRUCT_LENGTH32.size:
                return
            client._buflen = STRUCT_LENGTH32.unpack(client._buf[:STRUCT_LENGTH32.size])[0]
            client._buf = client._buf[STRUCT_LENGTH32.size:]
            if client._buflen > MAX_PACKETLENGTH:
                raise ValueError('Packet too long')
        if len(client._buf) >= client._buflen:
            data = client._buf[:client._buflen]
            client._buf = client._buf[client._buflen:]
            client._buflen = None
            self.receive_packet(data, client.cid)

    def receive_packet(self, data, cid):
        r"""
        Called when a full packet has been received.
        
        ``data`` is the raw packet data without length prefix.
        
        ``cid`` is the integer ID number of the client.
        
        Currently, this puts the data in a queue to be processed further by :py:meth:`process()`\ .
        """
        self._process_queue.put([cid, data])
        with self._process_condition:
            self._process_condition.notify()

    def send_message(self, ptype, data, cid):
        """
        Sends a message to the specified peer.
        
        ``ptype`` should be a valid packet type, e.g. either an ID, name or object.
        
        ``data`` should be the data to send to the peer.
        
        ``cid`` should be the Client ID number to send the message to.
        
        Note that all data encoding will be done synchronously and may cause this method to not return immediately.
        The packet may also be encrypted and compressed, if applicable.
        
        Additionally, the :peng3d:event:`peng3dnet:server.connection.send` event is sent if the connection type allows it.
        """
        if self.cfg['net.debug.print.send']:
            print('SEND %s to %s' % (ptype, cid))
        data = msgpack.dumps(data)
        flags = 0
        if len(data) > self.cfg['net.compress.threshold']:
            if self.cfg['net.compress.enabled']:
                data = zlib.compress(data, self.cfg['net.compress.level'])
                flags = flags | FLAG_COMPRESSED
        header = STRUCT_HEADER.pack(self.registry.getInt(ptype), flags)
        data = header + data
        prefix = STRUCT_LENGTH32.pack(len(data))
        data = prefix + data
        self.clients[cid].write_queue.append(data)
        with self._selector_lock:
            if not self.selector.get_key(self.clients[cid].conn).events & selectors.EVENT_WRITE:
                self.selector.modify(self.clients[cid].conn, selectors.EVENT_READ | selectors.EVENT_WRITE, [self._client_ready, self.clients[cid]])
                self.interrupt()
        if not (isinstance(ptype, int)):
            self.clients[cid].on_send(ptype, data)
            self.sendEvent('peng3dnet:server.connection.send', {'client':self.clients[cid],  'pid':ptype,  'data':data})
            self.registry.getObj(ptype)._send(data, cid)

    def register_packet(self, name, obj, n=None):
        r"""
        Registers a new packet with the internal registry.
        
        ``name`` should be a string of format ``namespace:category.subcategory.name`` where category may be repeated.
        
        ``obj`` should be an instance of a subclass of :py:class:`peng3dnet.packet.Packet()`\ .
        
        ``n`` may be optionally used to force a packet to use a specific packet ID, otherwise one will be generated.
        """
        self.registry.register(obj, name, n)

    def addConnType(self, t, obj):
        r"""
        Adds a connection type to the internal registry.
        
        ``t`` should be the string name of the connection type.
        
        ``obj`` should be an instance of a subclass of :py:class:`peng3dnet.conntypes.ConnectionType()`\ .
        
        Trying to register a name multiple times will cause an :py:exc:`~peng3dnet.errors.AlreadyRegisteredError`\ .
        """
        if t in self.conntypes:
            raise errors.AlreadyRegisteredError('Connection type %s has already been registered' % t)
        self.conntypes[t] = obj

    def close_connection(self, cid, reason=None):
        """
        Closes the connection to the given peer due to the optional reason.
        
        ``cid`` should be the Client ID number.
        
        ``reason`` may be a string describing the reason.
        """
        self.send_message('peng3dnet:internal.closeconn', {'reason': reason}, cid)
        self.clients[cid]._mark_close = True

    def process(self, wait=False, timeout=None):
        """
        Processes all packets awaiting processing.
        
        If ``wait`` is true, this function will wait up to ``timeout`` seconds for new data to arrive.
        
        It will then process all packets in the queue, decoding them and then
        calling the appropriate event handlers.
        This method assumes all messages are packed with msgpack.
        
        If the connection type allows it, event handlers will be called and the
        :peng3d:event:`peng3dnet:server.connection.recv` event is sent.
        
        This method returns the number of packets processed.
        """
        if wait:
            with self._process_condition:
                self._process_condition.wait(timeout)
        n = 0
        while not self._process_queue.empty():
            try:
                cid, data = self._process_queue.get_nowait()
            except Queue.Empty:
                break
            else:
                header, body = data[:STRUCT_HEADER.size], data[STRUCT_HEADER.size:]
                pid, flags = STRUCT_HEADER.unpack(header)
                if self.cfg['net.debug.print.recv']:
                    if pid < 64 or self.clients[cid].conntype == CONNTYPE_CLASSIC:
                        print('RECV %s %s' % (self.registry.getStr(pid), time.time()))
                if flags & FLAG_COMPRESSED:
                    olen = len(body)
                    body = zlib.decompress(body)
                if flags & FLAG_ENCRYPTED_AES:
                    raise NotImplementedError('Encryption not yet implemented')
                msg = msgpack.unpackb(body)
                try:
                    client = self.clients[cid]
                    if not (pid < 64 or self.conntypes[client.conntype].receive(msg, pid, flags, cid)):
                        self.registry.getObj(pid)._receive(msg, cid)
                        client.on_receive(pid, msg)
                        self.sendEvent('peng3dnet:server.connection.recv', {'client':client,  'pid':pid,  'msg':msg})
                except Exception:
                    import traceback
                    traceback.print_exc()

                n += 1

        return n

    def process_forever(self):
        """
        Processes packets in a blocking manner.
        
        Note that this method is currently not interruptable and thus uses short
        timeouts of about 10ms, causing a slight delay in stopping this loop.
        """
        while self.run:
            self.process(wait=True, timeout=0.01)

    def process_async(self):
        r"""
        Processes packets asynchronously.
        
        Internally calls :py:meth:`process_forever` in a separate daemon thread named ``peng3dnet process Thread``\ .
        """
        self._process_thread = threading.Thread(name='peng3dnet process Thread', target=(self.process_forever))
        self._process_thread.daemon = True
        self._process_thread.start()

    def sendEvent(self, event, data=None):
        """
        Helper method used to send events.
        
        Checks if the event system is enabled, adds the ``peng`` and ``server`` data attributes and then sends it.
        """
        data = data if data is not None else {}
        if self.cfg['net.events.enable']:
            if isinstance(data, dict):
                data['peng'] = self.peng
                data['server'] = self.server
            self.peng.sendEvent(event, data)


class ClientOnServer(object):
    __doc__ = '\n    Class representing a client on the server.\n    \n    This serves mainly as a data structure for storing the state of a specific connection.\n    \n    This class is not intended to be created manually.\n    \n    ``server`` is the instance of :py:class:`Server` that created this object.\n    \n    ``conn`` is the socket that should be used for communication with this client.\n    \n    ``addr`` is the address of this client.\n    \n    ``cid`` is the unique Client ID assigned to this client.\n    '

    def __init__(self, server, conn, addr, cid):
        self.server = server
        self.conn = conn
        self.addr = addr
        self.cid = cid
        self.write_queue = collections.deque()
        self.name = None
        self._buf = bytes()
        self._buflen = None
        self._mark_close = False
        self.mode = MODE_NOTSET
        self.conntype = CONNTYPE_NOTSET
        self.state = STATE_INIT
        self.ssl_state = 'handshake'
        self.ssl_seclevel = SSLSEC_NONE

    def close(self, reason=None):
        """
        Called to close the connection to this client.
        
        This method is not an event handler, use :py:meth:`on_close()` instead.
        """
        if self.server.cfg['net.debug.print.close']:
            print('CLOSE %s because of %s' % (self.cid, reason))
        else:
            self.server.sendEvent('peng3dnet:server.connection.close', {'client':self,  'reason':reason})
            if self.state != STATE_CLOSED:
                self.on_close(reason)
            self.state = STATE_CLOSED
            self.mode = MODE_CLOSED
            try:
                self.server.selector.unregister(self.conn)
            except Exception:
                pass

        try:
            self.conn.close()
        except Exception:
            pass

        try:
            del self.server.clients[self.cid]
        except KeyError:
            pass

    def on_handshake_complete(self):
        r"""
        Called when the handshake has been completed.
        
        The default implementation sends the :peng3d:event:`peng3dnet:server.connection.handshakecomplete`
        event and changes the connection state to :py:data:`~peng3dnet.constants.STATE_ACTIVE`\ .
        
        May be overridden by subclasses.
        """
        self.server.sendEvent('peng3dnet:server.connection.handshakecomplete', {'client': self})
        self.state = STATE_ACTIVE

    def on_close(self, reason=None):
        r"""
        Called when the connection has been closed.
        
        ``reason`` is the reason sent either by the peer or passed by the caller of :py:meth:`Server.close_connection()`\ .
        """
        pass

    def on_connect(self):
        """
        Sent once a connection has been established.
        
        Note that at the time this method is called the handshake may not be finished, 
        see :py:meth:`on_handshake_complete()` instead.
        """
        pass

    def on_receive(self, ptype, msg):
        """
        Called when a packet has been received.
        
        ``ptype`` will be an integer or string representing the packet type.
        
        ``msg`` will be a Python object decoded from the raw message via messagepack.
        """
        pass

    def on_send(self, ptype, msg):
        """
        Called when a packet has been sent.
        
        ``ptype`` will be the packet type in either string, integer or object form.
        
        ``msg`` will be the Python object that has been encoded and sent via messagepack.
        """
        pass


class Client(object):
    __doc__ = '\n    Client class representing the client side of the client-server relationship.\n    \n    A client can only be connected to a single server during its lifetime, recycling of client instances is not supported.\n    \n    If given, ``peng`` should be an instance of :py:class:`peng3d.peng.Peng` and\n    will be used for sending events and the configuration system. Note that without\n    a valid ``peng`` parameter, the event system will not work and a custom config\n    stack will be created.\n    If a ``peng`` parameter is given, its config stack will be adapted and the event system enabled.\n    \n    .. seealso::\n       See :confval:`net.events.enable` and :doc:`/events` for more information on the event system.\n    \n    ``addr``\\ , if given, should be a value parseable by :py:func:`peng3dnet.util.normalize_addr_socketstyle()`\\ .\n    If ``addr`` is not given, first :confval:`net.client.addr` is tried, then :confval:`net.client.addr.host` and :confval:`net.client.addr.port`\\ .\n    If any given address is missing an explicitly specified port, :confval:`net.client.addr.port` is supplemented.\n    \n    ``cfg`` may be used to override initial configuration values and should be a dictionary.\n    \n    Optionally, the connection type may be specified via ``conntype``\\ , which\n    may be set to a string identifying the type of the connection.\n    This should usually be :py:data:`~peng3dnet.constants.CONNTYPE_CLASSIC` or one of the other ``CONNTYPE_*`` constants.\n    Note that the connection type specified must also be registered via :py:meth:`addConnType()`\\ , except for the built-in connection types.\n    '

    def __init__(self, peng=None, addr=None, cfg=None, conntype=CONNTYPE_CLASSIC):
        cfg = cfg if cfg is not None else {}
        if peng is None:
            self.cfg = peng3d.config.Config(cfg, DEFAULT_CONFIG)
        else:
            ncfg = {}
            ncfg.update(DEFAULT_CONFIG)
            ncfg.update(cfg)
            self.cfg = peng3d.config.Config(ncfg, peng.cfg)
        if addr is not None:
            addr = util.normalize_addr_socketstyle(addr, self.cfg['net.client.addr.port'])
            self.cfg['net.client.addr.host'] = addr[0]
            self.cfg['net.client.addr.port'] = addr[1]
        else:
            if self.cfg['net.client.addr'] is None:
                addr = util.normalize_addr_socketstyle(self.cfg['net.client.addr.host'], self.cfg['net.client.addr.port'])
            else:
                addr = util.normalize_addr_socketstyle(self.cfg['net.client.addr'], self.cfg['net.client.addr.port'])
        if self.cfg['net.events.enable'] == 'auto':
            self.cfg['net.events.enable'] = peng is not None
        self.peng = peng
        self.addr = addr
        self.is_client = True
        self.is_server = False
        self.side = SIDE_CLIENT
        self.sock = None
        self._sock_lock = threading.Lock()
        self.selector = None
        self._selector_lock = threading.Lock()
        self._init_lock = threading.Lock()
        self._process_lock = threading.Lock()
        self._process_queue = Queue.Queue()
        self._process_condition = threading.Condition()
        self._connected_condition = threading.Condition()
        self._closed_condition = threading.Condition()
        self._is_connected = False
        self._is_started = False
        self._is_initialized = False
        self._irqrecv = None
        self._irqsend = None
        self._mark_close = False
        self._close_reason = None
        self._run_thread = None
        self._process_thread = None
        self.run = True
        self._buf = bytes()
        self._buflen = None
        self._write_buf = b''
        self.target_conntype = conntype
        self.conntype = CONNTYPE_NOTSET
        self.mode = MODE_NOTSET
        self.remote_state = STATE_INIT
        self.ssl_state = 'handshake'
        self.ssl_seclevel = SSLSEC_NONE
        self.conntypes = {}
        self.registry = registry.PacketRegistry()

    def initialize(self):
        """
        Initializes internal registries used during runtime.
        
        Calling this method repeatedly will be ignored.
        
        Currently, this registers packets and connection types.
        Additionally, the :peng3d:event:`peng3dnet:client.initialize` event is sent.
        
        Subclasses and Mix-ins may hook into this method via definition of methods
        named ``_reg_packets_*`` or ``_reg_conntypes_*`` with the star being an arbitrary string.
        The methods may not take any arguments.
        """
        if self._is_initialized:
            return
        with self._init_lock:
            if self._is_initialized:
                return
            from .packet import internal
            self.register_packet('peng3dnet:internal.hello', internal.HelloPacket(self.registry, self), 1)
            self.register_packet('peng3dnet:internal.settype', internal.SetTypePacket(self.registry, self), 2)
            self.register_packet('peng3dnet:internal.handshake', internal.HandshakePacket(self.registry, self), 3)
            self.register_packet('peng3dnet:internal.handshake.accept', internal.HandshakeAcceptPacket(self.registry, self), 4)
            self.register_packet('peng3dnet:internal.closeconn', internal.CloseConnectionPacket(self.registry, self), 16)
            for attr in dir(self):
                if attr.startswith('_reg_packets_') and callable(getattr(self, attr, None)):
                    getattr(self, attr)()

            self.addConnType('classic', conntypes.ClassicConnectionType(self))
            for attr in dir(self):
                if attr.startswith('_reg_conntypes_') and callable(getattr(self, attr, None)):
                    getattr(self, attr)()

            self.sendEvent('peng3dnet:client.initialize', {})

    def connect(self):
        """
        Connects the client with a server.
        
        Note that the server must have been specified before calling this method
        via either the ``addr`` argument to the initializer or any of the
        :confval:`net.client.addr` config values.
        
        Repeated calls of this method will be ignored.
        
        If SSL is enabled, this method will also initialize the SSL Context and load the certificates.
        
        After the connection has been made, the :peng3d:event:`peng3dnet.client.connect` event is sent.
        """
        if self._is_connected:
            return
        with self._sock_lock:
            if self._is_connected:
                return
            if self.cfg['net.ssl.enabled'] and self.cfg['net.ssl.force'] and not HAVE_SSL:
                raise RuntimeError('SSL Has not been found, but it is required')
            else:
                if self.cfg['net.ssl.enabled']:
                    if not HAVE_SSL:
                        self.cfg['net.ssl.enabled'] = False
                        warnings.warn('Potential security weakness because ssl had to be disabled')
                else:
                    self._irqrecv, self._irqsend = socket.socketpair()
                    if self.cfg['net.ssl.enabled']:
                        self.sslcontext = ssl.create_default_context((ssl.Purpose.SERVER_AUTH), cafile=(self.cfg['net.ssl.server.certfile']))
                        self.sslcontext.check_hostname = self.cfg['net.ssl.client.check_hostname']
                        self.sslcontext.verify_mode = ssl.CERT_REQUIRED if self.cfg['net.ssl.client.force_verify'] else ssl.CERT_OPTIONAL
                        self.sock = self.sslcontext.wrap_socket((socket.socket(socket.AF_INET)), server_hostname=(self.addr[0]))
                        self.sock.connect(tuple(self.addr))
                    else:
                        self.sock = socket.create_connection(tuple(self.addr))
                        self.sock.setblocking(True)
                    self.remote_state = STATE_HELLOWAIT
                self._is_connected = True
                self.sendEvent('peng3dnet:client.connect', {'addr':tuple(self.addr),  'sock':self.sock})

    def runBlocking(self, selector=selectors.DefaultSelector):
        """
        Runs the client main loop in a blocking manner.
        
        ``selector`` may be changed to override the selector used for smart waiting.
        
        This method blocks until :py:meth:`stop()` is called.
        """
        if self._is_started:
            return
        self.initialize()
        self.connect()
        with self._selector_lock:
            if self._is_started:
                return
            self.selector = selector()
            self.selector.register(self.sock, selectors.EVENT_READ, [self._sock_ready, self])
            self.selector.register(self._irqrecv, selectors.EVENT_READ, [self._sock_ready, None])
            self.selector.register(self._irqsend, selectors.EVENT_READ, [self._sock_ready, None])
            self._is_started = True
            self.sendEvent('peng3dnet:client.start', {})
        while self.run:
            events = self.selector.select()
            for key, mask in events:
                callback, data = key.data
                try:
                    callback(key.fileobj, mask, data)
                except Exception:
                    import traceback
                    traceback.print_exc()

    def runAsync(self, selector=selectors.DefaultSelector):
        """
        Runs the client main loop in a seperate thread.
        
        ``selector`` may be changed to override the selector used for smart waiting.
        
        This method does not block and should return immediately.
        
        The newly created thread will be named ``peng3dnet Client Thread`` and is
        a daemon thread, i.e. it will not keep the program alive.
        """
        self._run_thread = threading.Thread(name='peng3dnet Client Thread', target=(self.runBlocking), args=[selector])
        self._run_thread.daemon = True
        self._run_thread.start()

    def stop(self):
        """
        Stops the running client main loop.
        
        Will set an internal flag, then sends the event :peng3d:event:`peng3dnet:client.stop`
        and calls :py:meth:`interrupt()` to force the close.
        
        Note that this will not close open connections properly, call :py:meth:`close_connection()` before calling this method.
        """
        self.run = False
        self.sendEvent('peng3dnet:client.stop', {'reason': 'method'})
        self.interrupt()

    def interrupt(self):
        """
        Wakes up the main loop by sending a special message to an internal socket.
        
        This forces the main loop to iterate once and check that the system is still running.
        
        Also sends the :peng3d:event:`peng3dnet:client.interrupt` event.
        """
        self._irqsend.sendall(b'wake up!')
        self.sendEvent('peng3dnet:client.interrupt', {})

    def join(self, timeout=None):
        """
        Waits for all spawned threads to finish.
        
        If ``timeout`` is given, it indicates the total amount of time spent waiting.
        
        If a thread has not been started yet, it will be skipped and not waited for.
        """
        self.stop()
        ft = time.time() + timeout if timeout is not None else 1
        if self._run_thread is not None:
            if timeout is None:
                self._run_thread.join()
            else:
                self._run_thread.join(max(ft - time.time(), 0))
        elif self._process_thread is not None:
            if timeout is None:
                self._process_thread.join()
            else:
                self._process_thread.join(max(ft - time.time(), 0))

    def _sock_ready(self, sock, mask, data):
        if data is not None and self.cfg['net.ssl.enabled'] and self.ssl_state == 'handshake':
            if sock is self.sock:
                try:
                    sock.do_handshake()
                except ssl.SSLWantWriteError:
                    skey = self.selector.get_key(sock)
                    if not skey & selectors.EVENT_WRITE:
                        self.selector.modify(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, [self._sock_ready, None])
                except ssl.SSLWantReadError:
                    pass
                else:
                    self.ssl_state = 'connected'
                return
            elif sock == self._irqrecv:
                dat = sock.recv(8)
                if dat != b'wake up!':
                    sock.sendall(b'wrong socket')
                return
                if sock == self._irqsend:
                    sock.recv(1024)
                    return
                if mask & selectors.EVENT_READ:
                    if self.cfg['net.ssl.enabled']:
                        try:
                            dat = sock.recv(1024)
                        except ssl.SSLWantWriteError:
                            skey = self.selector.get_key(sock)
                            if not skey & selectors.EVENT_WRITE:
                                self.selector.modify(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, [self._sock_ready, None])
                            dat = ''
                        except ssl.SSLWantReadError:
                            dat = ''

            else:
                dat = sock.recv(1024)
            if dat:
                try:
                    self.receive_data(dat)
                except Exception:
                    import traceback
                    traceback.print_exc()

        else:
            self.close('socketclose')
        if mask & selectors.EVENT_WRITE:
            self.pump_write_buffer()

    def send_message(self, ptype, data, cid=None):
        """
        Sends a message to the server.
        
        ``ptype`` should be a valid packet type, e.g. either an ID, name or object.
        
        ``data`` should be the data to send to the server.
        
        ``cid`` will be ignored, available for compatibility with server applications.
        
        Note that all data encoding will be done synchronously and may cause this method to not return immediately.
        The packet may also be encrypted and compressed, if applicable.
        
        Additionally, the :peng3d:event:`peng3dnet:client.send` event is sent if the connection type allows it.
        """
        if self.cfg['net.debug.print.send']:
            print('SEND %s' % ptype)
        if not (isinstance(ptype, int)):
            self.on_send(ptype, data)
            self.sendEvent('peng3dnet:client.send', {'pid':ptype,  'data':data})
            self.registry.getObj(ptype)._send(data)
        data = msgpack.dumps(data)
        flags = 0
        if len(data) > self.cfg['net.compress.threshold']:
            if self.cfg['net.compress.enabled']:
                data = zlib.compress(data, self.cfg['net.compress.level'])
                flags = flags | FLAG_COMPRESSED
        header = STRUCT_HEADER.pack(self.registry.getInt(ptype), flags)
        data = header + data
        prefix = STRUCT_LENGTH32.pack(len(data))
        data = prefix + data
        self._write_buf += bytes(data)
        self.pump_write_buffer()

    def pump_write_buffer(self):
        """
        Tries to send as much of the data in the internal buffer as possible.
        
        Note that depending on various factors, not all data may be sent at once.
        It is possible that sent data will be fragmented at arbitrary points.
        
        If an exception occurs while sending the data, it will be ignored and the error printed to the console.
        """
        if len(self._write_buf) == 0:
            return
        try:
            if self.cfg['net.ssl.enabled']:
                try:
                    bytes_sent = self.sock.send(self._write_buf)
                except ssl.SSLWantWriteError:
                    bytes_sent = 0
                except ssl.SSLWantReadError:
                    bytes_sent = 0

            else:
                bytes_sent = self.sock.send(self._write_buf)
            self._write_buf = self._write_buf[bytes_sent:]
            if len(self._write_buf) == 0:
                if self._mark_close:
                    with self._selector_lock:
                        self.selector.unregister(self.sock)
                    self.on_close(self._close_reason)
                return
            if not self.selector.get_key(self.sock).events & selectors.EVENT_WRITE:
                self.selector.modify(self.sock, selectors.EVENT_READ | selectors.EVENT_WRITE, [self._sock_ready, None])
                self.interrupt()
        except Exception:
            import traceback
            traceback.print_exc()

    def receive_data(self, data, cid=None):
        """
        Called when new raw data has been read from the socket.
        
        Note that the given ``data`` may contain only parts of a packet or even multiple packets.
        
        ``cid`` is a dummy value used for compatibility with server applications.
        
        By default, the received data is stored in a buffer until enough data is available to process a packet, then :py:meth:`process_single_packet()` is called.
        """
        self._buf += data
        while not (self._buflen is None and len(self._buf) > 0):
            if not self._buflen is not None or len(self._buf) >= self._buflen:
                self.process_single_packet()

    def process_single_packet(self, client=None):
        """
        Called when there should be enough data to process a single packet.
        
        ``client`` is a dummy value used for compatibilizy with server applications.
        
        Currently parses a single packet including length prefix and calls :py:meth:`receive_packet()` with the packet data.
        """
        if self._buflen is None:
            if len(self._buf) < STRUCT_LENGTH32.size:
                return
            self._buflen = STRUCT_LENGTH32.unpack(self._buf[:STRUCT_LENGTH32.size])[0]
            self._buf = self._buf[STRUCT_LENGTH32.size:]
            if self._buflen > MAX_PACKETLENGTH:
                raise ValueError('Packet too long')
        if len(self._buf) >= self._buflen:
            data = self._buf[:self._buflen]
            self._buf = self._buf[self._buflen:]
            self._buflen = None
            self.receive_packet(data)

    def receive_packet(self, data, cid=None):
        r"""
        Called when a full packet has been received.
        
        ``data`` is the raw packet data without length prefix.
        
        ``cid`` is a dummy value used for compatibility with server applications.
        
        Currently, this puts the data in a queue to be processed further by :py:meth:`process()`\ .
        """
        self._process_queue.put([None, data])
        with self._process_condition:
            self._process_condition.notify()

    def register_packet(self, name, obj, n=None):
        r"""
        Registers a new packet with the internal registry.
        
        ``name`` should be a string of format ``namespace:category.subcategory.name`` where category may be repeated.
        
        ``obj`` should be an instance of a subclass of :py:class:`peng3dnet.packet.Packet()`\ .
        
        ``n`` may be optionally used to force a packet to use a specific packet ID, otherwise one will be generated.
        """
        self.registry.register(obj, name, n)

    def addConnType(self, t, obj):
        r"""
        Adds a connection type to the internal registry.
        
        ``t`` should be the string name of the connection type.
        
        ``obj`` should be an instance of a subclass of :py:class:`peng3dnet.conntypes.ConnectionType()`\ .
        
        Trying to register a name multiple times will cause an :py:exc:`~peng3dnet.errors.AlreadyRegisteredError`\ .
        """
        if t in self.conntypes:
            raise errors.AlreadyRegisteredError('Connection type %s has already been registered' % t)
        self.conntypes[t] = obj

    def close_connection(self, cid=None, reason=None):
        """
        Closes the connection to the server due to the optional reason.
        
        ``cid`` is a dummy value used for compatibility with server applications.
        
        ``reason`` may be a string describing the reason.
        """
        self.send_message('peng3dnet:internal.closeconn', {'reason': reason})
        self._mark_close = True
        self._close_reason = reason

    def process(self, wait=False, timeout=None):
        """
        Processes all packets awaiting processing.
        
        If ``wait`` is true, this function will wait up to ``timeout`` seconds for new data to arrive.
        
        It will then process all packets in the queue, decoding them and then
        calling the appropriate event handlers.
        This method assumes all messages are packed with msgpack.
        
        If the connection type allows it, event handlers will be called and the
        :peng3d:event:`peng3dnet:client.recv` event is sent.
        
        This method returns the number of packets processed.
        """
        if wait:
            with self._process_condition:
                self._process_condition.wait(timeout)
        n = 0
        while not self._process_queue.empty():
            try:
                _, data = self._process_queue.get_nowait()
            except Queue.Empty:
                break
            else:
                header, body = data[:STRUCT_HEADER.size], data[STRUCT_HEADER.size:]
                pid, flags = STRUCT_HEADER.unpack(header)
                if self.cfg['net.debug.print.recv']:
                    if pid < 64 or self.target_conntype == CONNTYPE_CLASSIC:
                        print('RECV %s' % self.registry.getStr(pid))
                if flags & FLAG_COMPRESSED:
                    body = zlib.decompress(body)
                if flags & FLAG_ENCRYPTED_AES:
                    raise NotImplementedError('Encryption not yet implemented')
                msg = msgpack.unpackb(body)
                with self._process_lock:
                    if not (pid < 64 or self.conntypes[self.target_conntype].receive(msg, pid, flags, None)):
                        self.registry.getObj(pid)._receive(msg)
                        self.on_receive(pid, msg)
                        self.sendEvent('peng3dnet:client.recv', {'pid':pid,  'msg':msg})
                    n += 1

        return n

    def process_forever(self):
        """
        Processes packets in a blocking manner.
        
        Note that this method is currently not interruptable and thus uses short
        timeouts of about 10ms, causing a slight delay in stopping this loop.
        """
        while self.run:
            self.process(wait=True, timeout=0.01)

    def process_async(self):
        r"""
        Processes packets asynchronously.
        
        Internally calls :py:meth:`process_forever()` in a separate daemon thread named ``peng3dnet process Thread``\ .
        """
        self._process_thread = threading.Thread(name='peng3dnet process Thread', target=(self.process_forever))
        self._process_thread.daemon = True
        self._process_thread.start()

    def close(self, reason=None):
        r"""
        Called to close the connection to the server.
        
        This method is not an event handler, use :py:meth:`on_close()` instead.
        
        Also sends the event :peng3d:event:`peng3dnet:client.close`\ .
        """
        if self.cfg['net.debug.print.close']:
            print('CLOSE because %s' % reason)
        self.sendEvent('peng3dnet:client.close', {'reason': reason})
        self.mode = MODE_CLOSED
        with self._closed_condition:
            self._closed_condition.notify_all()
        try:
            self.sock.close()
        except Exception:
            pass

        try:
            with self._selector_lock:
                self.selector.unregister(self.sock)
        except Exception:
            pass

        if self.remote_state != STATE_CLOSED:
            self.on_close(reason)
        self.remote_state = STATE_CLOSED

    def wait_for_connection(self, timeout=None):
        """
        Waits up to ``timeout`` seconds for the connection to be established.
        
        Returns immediately if there is an active connection.
        """
        with self._connected_condition:
            if self.remote_state >= STATE_ACTIVE:
                return
            if not self._connected_condition.wait(timeout):
                raise errors.TimedOutError('Timed out waiting for connection')

    def wait_for_close(self, timeout=None):
        """
        Waits up to ``timeout`` seconds for the connection to close.
        
        Returns immediately if the connection is already closed.
        """
        with self._closed_condition:
            if self.remote_state == STATE_CLOSED:
                return
            if not self._closed_condition.wait(timeout):
                raise errors.TimedOutError('Timed out waiting for closed connection')

    def on_handshake_complete(self):
        r"""
        Callback called once the handshake has been completed.
        
        The default implementation sends the :peng3d:event:`peng3dnet:client.handshakecomplete`
        event and sets the connection state to :py:data:`~peng3dnet.constants.STATE_ACTIVE`\ .
        """
        self.sendEvent('peng3dnet:client.handshakecomplete', {})
        self.remote_state = STATE_ACTIVE

    def on_connect(self):
        """
        Event handler called once a connection has been established.
        
        Note that usually the handshake will still be in progress while this method is called.
        
        .. seealso::
           See the :py:meth:`on_handshake_complete()` event handler for a better indicator when data can be sent.
        """
        pass

    def on_close(self, reason=None):
        """
        Event handler called during connection shutdown.
        
        It may or may not be possible to send data over the connection within this method, depending on various factors.
        """
        pass

    def on_receive(self, ptype, msg):
        """
        Event handler called if data is received from the peer.
        """
        pass

    def on_send(self, ptype, msg):
        """
        Event handler called if data is sent to the peer.
        """
        pass

    def sendEvent(self, event, data):
        """
        Helper method used to send events.
        
        Checks if the event system is enabled, adds the ``peng`` and ``client`` data attributes and then sends it.
        """
        if self.cfg['net.events.enable']:
            if isinstance(data, dict):
                data['peng'] = self.peng
                data['client'] = self
            self.peng.sendEvent(event, data)
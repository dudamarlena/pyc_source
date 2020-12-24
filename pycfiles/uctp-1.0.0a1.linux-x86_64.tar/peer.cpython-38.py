# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.8/dist-packages/uctp/peer.py
# Compiled at: 2020-04-26 16:24:41
# Size of source mod 2**32: 29769 bytes
import errno, hashlib, inspect, json, queue, select, socket, threading, time
from dataclasses import dataclass, field
from typing import Any, Type, Dict, Tuple, Union
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from . import additional
from . import protocol

class PeerError(Exception):
    pass


class AccessError(Exception):
    pass


class ArgumentsError(Exception):
    pass


class CommandError(Exception):
    pass


class _PassException(Exception):
    _e: Exception

    def __init__(self, e: Exception):
        if not isinstance(e, Exception):
            raise TypeError('e must be exception')
        self.e = e

    @property
    def extract(self) -> Exception:
        return self.e


class Annotation:
    type_: Type[Any]

    def __init__(self, annotation: Type[Any]=type(None)):
        if not isinstance(annotation, type):
            if annotation is not Any:
                raise TypeError('annotation must be type')
        self.type_ = annotation

    def __str__(self):
        return self.str(self.type_)

    @staticmethod
    def str(annotation: Type[Any]):
        if isinstance(annotation, type) or annotation is Any:
            if annotation is Any:
                return 'any'
            if isinstance(annotation, type(None)):
                return 'none'
            return annotation.__name__
        else:
            raise TypeError('annotation must be type')


@dataclass
class Parameter:
    name: str
    annotation = Annotation()
    annotation: Annotation
    default = None
    default: Any

    def __post_init__(self):
        if isinstance(self.name, str):
            if self.name.__len__() > 32:
                raise ValueError('Name length must be less than 32')
        else:
            raise TypeError('Name must be str')
        if not isinstance(self.annotation, Annotation):
            raise TypeError('annotation must be Annotation')

    def export(self) -> tuple:
        return (self.name, str(self.annotation), True if self.default else False)


class Aliases(dict):

    def __init__(self, dict_=None):
        if isinstance(dict_, dict):
            for k, v in dict_.items():
                additional.check_hash(k)

            if not isinstance(v, str):
                raise TypeError('value must be str')
        else:
            if dict_ is None:
                dict_ = {}
            else:
                raise TypeError('dict_ must be dict')
        super().__init__(dict_)

    def __setitem__(self, key, value):
        additional.check_hash(key)
        if not isinstance(value, str):
            raise TypeError('value must be str')
        super().__setitem__(key, value)

    def __getitem__(self, item):
        additional.check_hash(item)
        return super().__getitem__(item)


class Trusted(list):

    def __init__(self, *args):
        for i in args:
            additional.check_hash(i)
        else:
            super().__init__(args)

    def __setitem__(self, key, hash_):
        additional.check_hash(hash_)
        super().__setitem__(key, hash_)

    def append(self, hash_):
        additional.check_hash(hash_)
        super().append(hash_)


@dataclass
class Connection:
    name: str
    ip: str
    port: int
    socket: socket.socket
    client: bool
    authorized = field(default=False)
    authorized: bool
    _key = field(init=False, default=None)
    _key: RSA.RsaKey
    _close = field(init=False, default=False)
    _close: bool
    lock = field(init=False)
    lock: threading.Lock
    timestamp = field(init=False)
    timestamp: float
    session = field(init=False)
    session: str
    messages = field(init=False)
    messages: queue.Queue

    def __post_init__(self):
        self.lock = threading.Lock()
        self.timestamp = time.time()
        self.session = hashlib.sha1(Random.new().read(128)).hexdigest()
        self.messages = queue.Queue()

    @property
    def key(self) -> RSA.RsaKey:
        return self._key

    @key.setter
    def key(self, key_: RSA.RsaKey):
        if self._key:
            raise ValueError('key can be set once')
        else:
            if isinstance(key_, RSA.RsaKey):
                self._key = key_.has_private() or key_
            else:
                raise TypeError('key must be public RSA key')

    def key_hash(self) -> str:
        if self.key:
            return hashlib.sha1(self.key.export_key('DER')).hexdigest()
        return ''

    def fileno(self) -> int:
        return self.socket.fileno()

    def close(self):
        self._close = True

    def export(self) -> dict:
        return {'name':self.name, 
         'ip':self.ip, 
         'port':self.port, 
         'key':self.key_hash(), 
         'timestamp':self.timestamp, 
         'session':self.session}


class Commands:
    storage: dict

    def __init__(self):
        self.storage = {}

    def add(self, name: str, return_type: Type[Any]=None, *, protected: bool=True, encrypt: bool=True):
        if isinstance(name, str):
            if len(name.encode()) > 32:
                raise protocol.ProtocolError('Command max length is 32 bytes')
        else:
            raise TypeError('name must be str')
        if return_type:
            if not isinstance(return_type, type):
                if return_type is not Any:
                    raise TypeError('returns must be type')
        if name not in self.storage:

            def decorator(func):
                params = inspect.getfullargspec(func)
                returns = return_type if return_type else params.annotations['return'] if 'return' in params.annotations else type(None)
                if params.defaults:
                    defaults = dict(zip(reversed(params.args), reversed(params.defaults)))
                else:
                    defaults = {}
                param_list = ()
                if inspect.ismethod(func):
                    del params.args[0]
                peer = False
                if len(params.args) > 0:
                    if params.args[0] == 'peer':
                        peer = True
                        del params.args[0]
                for i in params.args:
                    param_list += (
                     Parameter(i, Annotation(params.annotations[i]) if i in params.annotations else type(None), defaults[i] if i in defaults else type(None)),)
                else:
                    self.storage[name] = {'func':func,  'params':{'list':param_list, 
                      'args':True if params.varargs else False, 
                      'kwargs':True if params.varkw else False, 
                      'peer':peer}, 
                     'returns':returns, 
                     'protected':protected, 
                     'encrypt':encrypt}

            return decorator
        raise IndexError('Command with this name already exists')

    def get(self, name: str) -> dict:
        if name in self.storage:
            return self.storage[name]
        raise NameError('Command not found')

    def execute(self, peer: Connection, name: str, *args: tuple, **kwargs: dict) -> Tuple[(bool, Any)]:
        if name in self.storage:
            if self.storage[name]['params']['peer']:
                return (
                 True, (self.storage[name]['func'])(peer, *args, **kwargs))
            return (True, (self.storage[name]['func'])(*args, **kwargs))
        else:
            return (False, None)

    def export(self) -> str:
        snapshot = {}
        for k, v in self.storage.items():
            snapshot[k] = {'params':{'list':tuple((i.export() for i in v['params']['list'])), 
              'args':v['params']['args'], 
              'kwargs':v['params']['kwargs']}, 
             'returns':str(v['returns']), 
             'protected':v['protected'], 
             'encrypt':v['encrypt']}
        else:
            return json.dumps(snapshot)


class Peer:
    _name: str
    _key: RSA.RsaKey
    _buffer: int
    _protocol: protocol.Protocol
    _state: int
    _server: socket.socket
    _connections: Dict[(str, Connection)]
    _increment: int
    aliases: Aliases
    commands: Commands
    listener: threading.Thread
    trusted: Trusted
    IP: str
    PORT: int
    TIMEOUT: float
    AUTH_TIMEOUT: float
    INTERVAL: float
    MAX_CONNECTIONS: int

    def __init__(self, name: str, key: RSA.RsaKey, ip: str, port: int=426, *, trusted: Trusted=None, aliases: Aliases=None, timeout: float=4.0, auth_timeout: float=8.0, max_connections: int=8, interval: float=0.01, buffer: int=4096):
        self._state = 0
        if isinstance(name, str):
            self._name = name
        else:
            raise TypeError('name must be str')
        if isinstance(key, RSA.RsaKey):
            if key.has_private():
                self._key = key
            else:
                raise TypeError('key must be private RSA key')
        else:
            if isinstance(ip, str):
                self.IP = ip
            else:
                raise TypeError('ip must be str')
            if isinstance(port, int):
                self.PORT = port
            else:
                raise TypeError('port must be int')
            if trusted:
                if isinstance(trusted, Trusted):
                    self.trusted = trusted
                else:
                    raise TypeError('trusted must be Trusted')
            else:
                self.trusted = Trusted()
        if aliases:
            if isinstance(aliases, Aliases):
                self.aliases = aliases
            else:
                if not aliases:
                    self.aliases = Aliases()
                else:
                    raise TypeError('aliases must be Aliases')
        else:
            if isinstance(timeout, (float, int)):
                self.TIMEOUT = timeout
            else:
                raise TypeError('timeout must be float or int')
            if isinstance(auth_timeout, (float, int)):
                self.AUTH_TIMEOUT = auth_timeout
            else:
                raise TypeError('auth_timeout must be float or int')
            if isinstance(max_connections, int):
                self.MAX_CONNECTIONS = max_connections
            else:
                raise TypeError('max_connections must be int')
            if isinstance(interval, float):
                self.INTERVAL = interval
            else:
                raise TypeError('interval must be float')
        self._protocol = protocol.Protocol(self._key)
        self.buffer = buffer
        self._increment = 0
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._server.setblocking(False)
        self._connections = {}
        self.commands = Commands()
        self.listener = threading.Thread(target=(self.listener_loop), daemon=True)
        self.commands.add('_handshake', dict, protected=False, encrypt=False)(self._handshake)
        self.commands.add('_auth', int, protected=False)(self._auth)
        self.commands.add('_commands', dict)(self._commands)
        self.commands.add('_ping', str)(self._ping)
        self.commands.add('_echo', Any)(self._echo)
        self.commands.add('_me', dict)(self._me)
        self.commands.add('_peers', list)(self._peers)
        self.commands.add('_close', bool)(self._close)

    @property
    def buffer(self):
        return self._buffer

    @buffer.setter
    def buffer(self, value: int):
        if isinstance(value, int):
            if value < 1024:
                raise ValueError('recv cannot be less than 1024')
            else:
                self._buffer = value
        else:
            raise TypeError('recv must be int')

    @property
    def key(self):
        return self._key

    @property
    def name(self):
        return self._name

    @property
    def increment(self) -> int:
        if self._increment == 1073741823:
            self._increment = 0
        else:
            self._increment += 1
        return self._increment

    def _error(self, peer: Connection, command: Union[(bytes, str)], error: int, description: str='', encrypt: bool=True) -> protocol.Packet:
        if isinstance(command, str):
            command = command.encode()
        if encrypt:
            return self._protocol.pack(command,
              (json.dumps({'error':error,  'description':description})),
              True,
              type_=2,
              key=(peer.key))
        return self._protocol.pack(command,
          (json.dumps({'error':error,  'description':description})),
          False,
          type_=2)

    @staticmethod
    def _raise_error(message: dict):
        if isinstance(message, dict):
            if 'error' in message and isinstance(message['error'], int):
                if message['error'] == 0:
                    raise PeerError('Peer shuts down')
            elif message['error'] == 1:
                raise AccessError('Access denied')
            else:
                if message['error'] == 2:
                    raise RuntimeError('Command tried to return objects that json does not support')
                else:
                    if message['error'] == 3:
                        if 'description' in message:
                            raise NameError(message['description'])
                        else:
                            raise NameError('Peer with this name already connected')
                    elif message['error'] == 4:
                        if 'description' in message:
                            raise CommandError(message['description'])
                        else:
                            raise CommandError('Some exception caught while executing command')
                    elif message['error'] == 5:
                        raise ArgumentsError('Wrong arguments')
                    else:
                        if message['error'] == 6:
                            raise KeyError('Commands not found')
                        else:
                            if message['error'] == 7:
                                raise TypeError('Unexpected packet type')
        else:
            raise PeerError('Unknown error')

    @staticmethod
    def _compile(*args, **kwargs) -> str:
        if args:
            if kwargs:
                return json.dumps(((*args,), {**kwargs}))
        else:
            if not args:
                return json.dumps(({**kwargs},))
            return kwargs or json.dumps(((*args,),))
        return '[]'

    def _clients_count(self) -> int:
        count = 0
        for i in self._connections.values():
            if i.client:
                count += 1
            return count

    def _send--- This code section failed: ---

 L. 504         0  LOAD_FAST                'peer'
                2  LOAD_ATTR                lock
                4  LOAD_METHOD              acquire
                6  CALL_METHOD_0         0  ''
             8_10  POP_JUMP_IF_FALSE   462  'to 462'

 L. 505     12_14  SETUP_FINALLY       438  'to 438'
            16_18  SETUP_FINALLY       394  'to 394'

 L. 506        20  LOAD_FAST                'peer'
               22  LOAD_ATTR                socket
               24  LOAD_METHOD              setblocking
               26  LOAD_CONST               True
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 507        32  LOAD_FAST                'peer'
               34  LOAD_ATTR                socket
               36  LOAD_METHOD              sendall
               38  LOAD_FAST                'packet'
               40  LOAD_METHOD              raw
               42  CALL_METHOD_0         0  ''
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L. 509        48  LOAD_FAST                'peer'
               50  LOAD_ATTR                socket
               52  LOAD_METHOD              recv
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                buffer
               58  CALL_METHOD_1         1  ''
               60  STORE_FAST               'data'

 L. 510        62  LOAD_FAST                'data'
            64_66  POP_JUMP_IF_FALSE   382  'to 382'

 L. 511        68  SETUP_FINALLY       230  'to 230'

 L. 512        70  LOAD_FAST                'self'
               72  LOAD_ATTR                _protocol
               74  LOAD_METHOD              unpack
               76  LOAD_FAST                'data'
               78  CALL_METHOD_1         1  ''
               80  STORE_FAST               'packet_'

 L. 514        82  LOAD_FAST                'packet_'
               84  LOAD_ATTR                flags
               86  LOAD_ATTR                type
               88  LOAD_CONST               0
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_TRUE    106  'to 106'
               94  LOAD_FAST                'packet_'
               96  LOAD_ATTR                flags
               98  LOAD_ATTR                type
              100  LOAD_CONST               2
              102  COMPARE_OP               >
              104  POP_JUMP_IF_FALSE   116  'to 116'
            106_0  COME_FROM            92  '92'

 L. 515       106  LOAD_GLOBAL              TypeError
              108  LOAD_STR                 'Unexpected packet type'
              110  CALL_FUNCTION_1       1  ''
              112  RAISE_VARARGS_1       1  'exception instance'
              114  JUMP_FORWARD        138  'to 138'
            116_0  COME_FROM           104  '104'

 L. 516       116  LOAD_FAST                'packet_'
              118  LOAD_ATTR                command
              120  LOAD_FAST                'packet'
              122  LOAD_ATTR                command
              124  COMPARE_OP               !=
              126  POP_JUMP_IF_FALSE   138  'to 138'

 L. 517       128  LOAD_GLOBAL              protocol
              130  LOAD_METHOD              PacketError
              132  LOAD_STR                 'Unexpected response'
              134  CALL_METHOD_1         1  ''
              136  RAISE_VARARGS_1       1  'exception instance'
            138_0  COME_FROM           126  '126'
            138_1  COME_FROM           114  '114'

 L. 519       138  LOAD_FAST                'packet_'
              140  LOAD_ATTR                flags
              142  LOAD_ATTR                type
              144  STORE_FAST               'type_'

 L. 521       146  LOAD_CONST               None
              148  SETUP_FINALLY       200  'to 200'
              150  SETUP_FINALLY       168  'to 168'

 L. 522       152  LOAD_GLOBAL              json
              154  LOAD_METHOD              loads
              156  LOAD_FAST                'packet_'
              158  LOAD_ATTR                data
              160  CALL_METHOD_1         1  ''
              162  STORE_FAST               'packet_'
              164  POP_BLOCK        
              166  JUMP_FORWARD        196  'to 196'
            168_0  COME_FROM_FINALLY   150  '150'

 L. 523       168  DUP_TOP          
              170  LOAD_GLOBAL              json
              172  LOAD_ATTR                JSONDecodeError
              174  COMPARE_OP               exception-match
              176  POP_JUMP_IF_FALSE   194  'to 194'
              178  POP_TOP          
              180  POP_TOP          
              182  POP_TOP          

 L. 524       184  LOAD_FAST                'packet_'
              186  LOAD_ATTR                data
              188  STORE_FAST               'packet_'
              190  POP_EXCEPT       
              192  JUMP_FORWARD        196  'to 196'
            194_0  COME_FROM           176  '176'
              194  END_FINALLY      
            196_0  COME_FROM           192  '192'
            196_1  COME_FROM           166  '166'
              196  POP_BLOCK        
              198  BEGIN_FINALLY    
            200_0  COME_FROM_FINALLY   148  '148'

 L. 526       200  LOAD_FAST                'type_'
              202  LOAD_FAST                'packet_'
              204  BUILD_TUPLE_2         2 
              206  POP_FINALLY           1  ''
              208  ROT_TWO          
              210  POP_TOP          
              212  POP_BLOCK        
              214  POP_BLOCK        
              216  POP_BLOCK        
              218  CALL_FINALLY        438  'to 438'
              220  RETURN_VALUE     
              222  END_FINALLY      
              224  POP_TOP          
              226  POP_BLOCK        
              228  JUMP_FORWARD        380  'to 380'
            230_0  COME_FROM_FINALLY    68  '68'

 L. 527       230  DUP_TOP          
              232  LOAD_GLOBAL              protocol
              234  LOAD_ATTR                ProtocolError
              236  COMPARE_OP               exception-match
          238_240  POP_JUMP_IF_FALSE   280  'to 280'
              242  POP_TOP          
              244  POP_TOP          
              246  POP_TOP          

 L. 528       248  LOAD_GLOBAL              protocol
              250  LOAD_METHOD              ProtocolError
              252  LOAD_STR                 'peer '
              254  LOAD_FAST                'peer'
              256  LOAD_ATTR                ip
              258  FORMAT_VALUE          0  ''
              260  LOAD_STR                 ':'
              262  LOAD_FAST                'peer'
              264  LOAD_ATTR                port
              266  FORMAT_VALUE          0  ''
              268  LOAD_STR                 " doesn't support uctp protocol"
              270  BUILD_STRING_5        5 
              272  CALL_METHOD_1         1  ''
              274  RAISE_VARARGS_1       1  'exception instance'
              276  POP_EXCEPT       
              278  JUMP_FORWARD        380  'to 380'
            280_0  COME_FROM           238  '238'

 L. 529       280  DUP_TOP          
              282  LOAD_GLOBAL              protocol
              284  LOAD_ATTR                VersionError
              286  COMPARE_OP               exception-match
          288_290  POP_JUMP_IF_FALSE   330  'to 330'
              292  POP_TOP          
              294  POP_TOP          
              296  POP_TOP          

 L. 530       298  LOAD_GLOBAL              protocol
              300  LOAD_METHOD              VersionError

 L. 531       302  LOAD_STR                 'peer '
              304  LOAD_FAST                'peer'
              306  LOAD_ATTR                ip
              308  FORMAT_VALUE          0  ''
              310  LOAD_STR                 ':'
              312  LOAD_FAST                'peer'
              314  LOAD_ATTR                port
              316  FORMAT_VALUE          0  ''
              318  LOAD_STR                 " doesn't support current version of protocol"
              320  BUILD_STRING_5        5 

 L. 530       322  CALL_METHOD_1         1  ''
              324  RAISE_VARARGS_1       1  'exception instance'
              326  POP_EXCEPT       
              328  JUMP_FORWARD        380  'to 380'
            330_0  COME_FROM           288  '288'

 L. 532       330  DUP_TOP          
              332  LOAD_GLOBAL              protocol
              334  LOAD_ATTR                PacketError
              336  COMPARE_OP               exception-match
          338_340  POP_JUMP_IF_FALSE   378  'to 378'
              342  POP_TOP          
              344  POP_TOP          
              346  POP_TOP          

 L. 533       348  LOAD_GLOBAL              protocol
              350  LOAD_METHOD              PacketError
              352  LOAD_STR                 'corrupted data received from peer '
              354  LOAD_FAST                'peer'
              356  LOAD_ATTR                ip
              358  FORMAT_VALUE          0  ''
              360  LOAD_STR                 ':'
              362  LOAD_FAST                'peer'
              364  LOAD_ATTR                port
              366  FORMAT_VALUE          0  ''
              368  BUILD_STRING_4        4 
              370  CALL_METHOD_1         1  ''
              372  RAISE_VARARGS_1       1  'exception instance'
              374  POP_EXCEPT       
              376  JUMP_FORWARD        380  'to 380'
            378_0  COME_FROM           338  '338'
              378  END_FINALLY      
            380_0  COME_FROM           376  '376'
            380_1  COME_FROM           328  '328'
            380_2  COME_FROM           278  '278'
            380_3  COME_FROM           228  '228'
              380  JUMP_FORWARD        390  'to 390'
            382_0  COME_FROM            64  '64'

 L. 535       382  LOAD_GLOBAL              ConnectionError
              384  LOAD_STR                 'connection with peer lost'
              386  CALL_FUNCTION_1       1  ''
              388  RAISE_VARARGS_1       1  'exception instance'
            390_0  COME_FROM           380  '380'
              390  POP_BLOCK        
              392  JUMP_FORWARD        434  'to 434'
            394_0  COME_FROM_FINALLY    16  '16'

 L. 536       394  DUP_TOP          
              396  LOAD_GLOBAL              Exception
              398  COMPARE_OP               exception-match
          400_402  POP_JUMP_IF_FALSE   432  'to 432'
              404  POP_TOP          
              406  STORE_FAST               'e'
              408  POP_TOP          
              410  SETUP_FINALLY       420  'to 420'

 L. 537       412  LOAD_FAST                'e'
              414  RAISE_VARARGS_1       1  'exception instance'
              416  POP_BLOCK        
              418  BEGIN_FINALLY    
            420_0  COME_FROM_FINALLY   410  '410'
              420  LOAD_CONST               None
              422  STORE_FAST               'e'
              424  DELETE_FAST              'e'
              426  END_FINALLY      
              428  POP_EXCEPT       
              430  JUMP_FORWARD        434  'to 434'
            432_0  COME_FROM           400  '400'
              432  END_FINALLY      
            434_0  COME_FROM           430  '430'
            434_1  COME_FROM           392  '392'
              434  POP_BLOCK        
              436  BEGIN_FINALLY    
            438_0  COME_FROM           218  '218'
            438_1  COME_FROM_FINALLY    12  '12'

 L. 539       438  LOAD_FAST                'peer'
              440  LOAD_ATTR                socket
              442  LOAD_METHOD              setblocking
              444  LOAD_CONST               False
              446  CALL_METHOD_1         1  ''
              448  POP_TOP          

 L. 540       450  LOAD_FAST                'peer'
              452  LOAD_ATTR                lock
              454  LOAD_METHOD              release
              456  CALL_METHOD_0         0  ''
              458  POP_TOP          
              460  END_FINALLY      
            462_0  COME_FROM             8  '8'

Parse error at or near `LOAD_FAST' instruction at offset 200

    def listener_loop(self):
        while self._state > 0:
            start = time.time()
            readers = (
             self._server,)
            for i in self._connections.values():
                readers += (i,)
            else:
                writers = tuple((i for i in self._connections.values() if not i.messages.empty()))
                if self._state == 2:
                    if not writers:
                        self._state = 0
                readable, writeable, exceptional = select.select(readers, writers, readers, 0.001)

            for i in readable:
                if i is self._server:
                    peer = self._server.accept()
                    if self.MAX_CONNECTIONS < 0 or self._clients_count() >= self.MAX_CONNECTIONS:
                        peer[0].close()
                    else:
                        peer[0].setblocking(False)
                        increment = self.increment
                        self._connections[f"_{increment}"] = Connection(f"_{increment}", peer[1][0], peer[1][1], peer[0], True)
            else:
                if i.lock.acquire(False):
                    try:
                        data = i.socket.recv(self.buffer)
                    except socket.error as e:
                        try:
                            if e.errno is errno.ECONNRESET:
                                data = None
                            else:
                                raise e
                        finally:
                            e = None
                            del e

                    if data:
                        try:
                            data = self._protocol.unpack(data)
                            if self._state == 1:
                                i.messages.put(data)
                            else:
                                if self._state == 2:
                                    i.messages.put(self._error(i, data.command, 0, 'Peer shuts down', bool(i.key)))
                            i.lock.release()
                        except protocol.ProtocolError:
                            self.disconnect(i.name)
                        except protocol.DamageError:
                            self.disconnect(i.name)

                    else:
                        self.disconnect(i.name)

            for i in writeable:
                if i.lock.acquire(False):
                    packet = i.messages.get_nowait()
                    if packet.flags.type == protocol.TYPE_REQUEST:
                        try:
                            encrypt = self.commands.get(packet.command.decode())['encrypt']
                            if self.commands.get(packet.command.decode())['protected']:
                                packet = i.authorized or self._error(i, packet.command, 1, 'Access denied', encrypt)
                            else:
                                args = []
                            kwargs = {}
                            try:
                                argv = json.loads(packet.data)
                                if not (isinstance(argv, list) and len(argv) > 2 or all((isinstance(i, (list, dict)) for i in argv))):
                                    raise ArgumentsError
                                if len(argv) > 0:
                                    if isinstance(argv[0], list):
                                        args.extend(argv[0])
                                    else:
                                        kwargs.update(argv[0])
                                if len(argv) == 2:
                                    if isinstance(argv[1], list):
                                        args.extend(argv[1])
                                    else:
                                        kwargs.update(argv[1])
                                try:
                                    result = (self.commands.execute)(i, packet.command.decode(), *args, **kwargs)[1]
                                    try:
                                        packet = self._protocol.pack((packet.command),
                                          (json.dumps(result)),
                                          encrypt,
                                          type_=1,
                                          key=(i.key))
                                    except json.JSONDecodeError:
                                        packet = self._error(i, packet.command, 2, "Command tried to return objects that json doesn't support", encrypt)

                                except Exception as e:
                                    try:
                                        if isinstance(e, _PassException):
                                            if isinstance(e.extract, NameError):
                                                packet = self._error(i, packet.command, 3, e.extract.__str__(), encrypt)
                                        else:
                                            packet = self._error(i, packet.command, 4, f"Exception caught while executing command ({e.__class__.__name__}: {e.__str__()})", encrypt)
                                        raise e
                                    finally:
                                        e = None
                                        del e

                            except (json.JSONDecodeError, ArgumentsError):
                                packet = self._error(i, packet.command, 5, 'Wrong arguments', encrypt)

                        except NameError:
                            packet = self._error(i, packet.command, 6, 'Command not found', i.authorized)

                    else:
                        packet = self._error(i, packet.command, 7, 'Unexpected packet type', i.authorized)
                    i.socket.send(packet.raw())
                    i.lock.release()
            else:
                for i in exceptional:
                    self.disconnect(i)
                else:
                    expired = ()
                    for i in self._connections:
                        if not self._connections[i].authorized:
                            if not (self._connections[i].timestamp + self.AUTH_TIMEOUT < time.time() or self._connections[i]._close):
                                if self._connections[i].socket._closed:
                                    pass
                                expired += (i,)
                            for i in expired:
                                self.disconnect(i)
                            else:
                                delta = time.time() - start

                            if self.INTERVAL - delta > 0:
                                time.sleep(self.INTERVAL - delta)

    def connect(self, ip: str, port: int) -> bool:
        if self._state != 1:
            raise RuntimeError('peer must be ran before creating new connections')
        try:
            socket.inet_aton(ip)
        except OSError:
            raise PeerError('illegal ip to connect')
        else:
            if isinstance(port, int):
                if 0 > port > 65535:
                    raise PeerError('illegal port to connect')
                connection = Connection(f"_{self.increment}", ip, port, socket.create_connection((ip, port), 8), False)
                connection.socket.settimeout(self.TIMEOUT)
                type_, result = self._send(connection, self._protocol.pack('_handshake', self._compile(self._name, self._key.publickey().export_key('DER').hex()), False))
                if type_ == protocol.TYPE_RESPONSE:
                    if not result['access']:
                        raise AccessError
                    try:
                        connection.key = RSA.import_key(bytearray.fromhex(result['key']))
                    except ValueError:
                        raise KeyError('Wrong public key received from peer')
                    else:
                        if connection.key_hash() in self.aliases:
                            connection.name = self.aliases[connection.key_hash()]
                        else:
                            connection.name = result['name']
                        if connection.name in self._connections:
                            connection.socket.close()
                            raise NameError('Peer with this name already connected (local)')
            else:
                self._raise_error(result)
            type_, result = self._send(connection, self._protocol.pack('_auth',
              (self._compile(PKCS1_OAEP.new(self._key).decrypt(bytearray.fromhex(result['puzzle'])).decode())),
              True,
              key=(connection.key)))
            if type_ == protocol.TYPE_RESPONSE:
                connection.authorized = True
                connection.socket.setblocking(False)
                self._connections[connection.name] = connection
                return True
            self._raise_error(result)

    def disconnect(self, name: str):
        if name in self._connections:
            self._connections[name].socket.close()
            del self._connections[name]
        else:
            raise NameError(f'No connection named "{name}"')

    def send(self, name: str, command: str, args: Union[(tuple, list)]=(), kwargs: dict=None, *, raise_: bool=True):
        if name not in self._connections:
            raise NameError(f'Peer "{name}" not connected')
        else:
            if not self._connections[name].authorized:
                raise AccessError(f'"{name}" is unauthorized peer')
            else:
                if args:
                    if not isinstance(args, (tuple, list)):
                        raise TypeError('args must be tuple or list')
                else:
                    if kwargs:
                        if not isinstance(kwargs, dict):
                            raise TypeError('kwargs must be dict')
                    kwargs = kwargs or {}
                type_, result = self._send(self._connections[name], self._protocol.pack(command,
                  (self._compile)(*args, **kwargs),
                  True,
                  key=(self._connections[name].key)))
                if raise_ and type_ == protocol.TYPE_ERROR:
                    self._raise_error(result)
            return (
             type_, result)

    def run(self):
        if self._state != 1:
            self._state = 1
            self._server.settimeout(self.TIMEOUT)
            self._server.bind((self.IP, self.PORT))
            self._server.listen()
            self.listener.start()

    def stop(self):
        if self._state == 1:
            self._state = 2
            self.listener.join()
            for i in tuple(self._connections):
                self.disconnect(i)
            else:
                self._server.close()

    def _handshake(self, peer: Connection, name: str, key: str) -> dict:
        try:
            key = RSA.import_key(bytearray.fromhex(key))
        except ValueError:
            raise ValueError('Wrong RSA key')
        else:
            if not self.trusted or hashlib.sha1(key.export_key('DER')).hexdigest() in self.trusted:
                aliased = False
                if hashlib.sha1(key.export_key('DER')).hexdigest() in self.aliases:
                    name = self.aliases[hashlib.sha1(key.export_key('DER')).hexdigest()]
                    aliased = True
                if name in self._connections:
                    raise NameError('Peer with this name already connected{0}'.format(f' (aliased "{name}")' if aliased else ''))
                self._connections[name] = self._connections.pop(peer.name)
                peer.name = name
                peer.key = key
                return {'name':self._name, 
                 'puzzle':PKCS1_OAEP.new(peer.key).encrypt(peer.session.encode()).hex(), 
                 'key':self._key.publickey().export_key('DER').hex(), 
                 'access':True}
            return {'access': False}

    def _auth--- This code section failed: ---

 L. 824         0  LOAD_FAST                'answers'
                2  LOAD_FAST                'peer'
                4  LOAD_ATTR                session
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    16  'to 16'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                trusted
               14  POP_JUMP_IF_FALSE    28  'to 28'
             16_0  COME_FROM             8  '8'
               16  LOAD_FAST                'peer'
               18  LOAD_ATTR                session
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                trusted
               24  COMPARE_OP               in
               26  POP_JUMP_IF_FALSE    38  'to 38'
             28_0  COME_FROM            14  '14'

 L. 825        28  LOAD_CONST               True
               30  LOAD_FAST                'peer'
               32  STORE_ATTR               authorized

 L. 826        34  LOAD_CONST               True
               36  RETURN_VALUE     
             38_0  COME_FROM            26  '26'

 L. 828        38  LOAD_CONST               False
               40  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 38

    def _commands(self):
        return self.commands.export()

    @staticmethod
    def _ping() -> str:
        return 'pong'

    @staticmethod
    def _echo(echo: Any) -> Any:
        return echo

    @staticmethod
    def _me(peer: Connection) -> dict:
        return peer.export()

    def _peers(self) -> list:
        return [i.export() for i in self._connections.values()]

    def _close(self, peer: Connection) -> bool:
        peer.close()
        return True
# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.8/dist-packages/uctp/peer.py
# Compiled at: 2020-05-12 13:38:35
# Size of source mod 2**32: 33761 bytes
import errno, hashlib, inspect, json, math, queue, select, socket, threading, time
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
        if (isinstance(annotation, type) or annotation) is not Any:
            raise TypeError('annotation must be type')
        else:
            if annotation not in (int, float, bool, str, list, dict, Any, type(None)):
                raise TypeError('Only int, float, bool, str, list, dict, NoneType, typing.Any types are supported as annotation')
        self.type_ = annotation

    def __str__(self):
        return self.str(self.type_)

    @staticmethod
    def str(annotation: Type[Any]):
        if isinstance(annotation, type) or annotation is Any:
            if annotation is Any:
                return 'Any'
            if annotation == type(None):
                return 'None'
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
        if not isinstance(self.name, str):
            raise TypeError('name must be str')
        else:
            if not isinstance(self.annotation, Annotation):
                raise TypeError('annotation must be Annotation')
            assert isinstance(self.default, (int, float, bool, str, list, dict, type(None))), 'Only int, float, bool, str, list, dict, NoneType types are supported as default value'

    def export(self) -> list:
        return [self.name, str(self.annotation), self.default]


class Aliases(dict):

    def __init__(self, dict_=None):
        if isinstance(dict_, dict):
            for k, v in dict_.items():
                additional.check_hash(k)
                if not isinstance(v, str):
                    raise TypeError('value must be str')
            else:
                dict_ = {v:k.lower() for k, v in dict_.items()}

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
        super().__setitem__(key.lower(), value)

    def __getitem__(self, item):
        additional.check_hash(item)
        return super().__getitem__(item.lower())


class Trusted(list):

    def __init__(self, *args):
        for i in args:
            additional.check_hash(i)
        else:
            args = [i.lower() for i in args]
            super().__init__(args)

    def __setitem__(self, key, hash_):
        additional.check_hash(hash_)
        super().__setitem__(key, hash_.lower())

    def append(self, hash_):
        additional.check_hash(hash_)
        super().append(hash_.lower())


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
    _to_close = field(init=False, default=False)
    _to_close: bool
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

    @property
    def to_close(self) -> bool:
        return self._to_close

    def key_hash(self) -> str:
        if self.key:
            return hashlib.sha1(self.key.export_key('DER')).hexdigest()
        return ''

    def fileno(self) -> int:
        return self.socket.fileno()

    def close(self):
        self._to_close = True

    def export(self) -> dict:
        return {'name':self.name, 
         'ip':self.ip, 
         'port':self.port, 
         'client':self.client, 
         'key':self.key_hash(), 
         'timestamp':self.timestamp, 
         'session':self.session}


class Commands:
    storage: dict

    def __init__(self):
        self.storage = {}

    def add_(self, func, name: str='', returns: Type[Any]=None, protected: bool=True, encrypt: bool=True):
        if not isinstance(name, str):
            raise TypeError('name must be str')
        else:
            if returns:
                if not isinstance(returns, type):
                    if returns is not Any:
                        raise TypeError('returns must be type')
            else:
                name_ = name if name else func.__name__
                params = inspect.getfullargspec(func)
                returns_ = Annotation(returns) if returns else Annotation(params.annotations['return']) if 'return' in params.annotations else Annotation()
                if name_ in self.storage:
                    raise IndexError('Command with this name already exists')
                if params.defaults:
                    defaults = dict(zip(reversed(params.args), reversed(params.defaults)))
                else:
                    defaults = {}
            args_list = []
            kwargs_list = []
            if inspect.ismethod(func):
                del params.args[0]
            peer = False
            if len(params.args) > 0 and params.args[0] == 'peer':
                peer = True
                del params.args[0]
        for i in params.args:
            args_list.append(Parameter(i, Annotation(params.annotations[i]) if i in params.annotations else Annotation(), defaults[i] if i in defaults else None))
        else:
            for i in params.kwonlyargs:
                kwargs_list.append(Parameter(i, Annotation(params.annotations[i]) if i in params.annotations else Annotation(), params.kwonlydefaults[i] if i in params.kwonlydefaults else None))
            else:
                self.storage[name_] = {'func':func,  'args':args_list, 
                 'kwargs':kwargs_list, 
                 'varargs':params.varargs if params.varargs else '', 
                 'varkw':params.varkw if params.varkw else '', 
                 'peer':peer, 
                 'returns':returns_, 
                 'protected':protected, 
                 'encrypt':encrypt}

    def add(self, name: str='', returns: Type[Any]=None, protected: bool=True, encrypt: bool=True):

        def decorator(func):
            if inspect.ismethod(func):
                raise TypeError('Decorator cannot be used for methods. Use add_() instead')
            self.add_(func, name, returns, protected, encrypt)

        return decorator

    def get(self, name: str) -> dict:
        if name in self.storage:
            return self.storage[name]
        raise NameError('Command not found')

    def execute--- This code section failed: ---

 L. 296         0  LOAD_FAST                'name'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                storage
                6  COMPARE_OP               in
             8_10  POP_JUMP_IF_FALSE   496  'to 496'

 L. 297        12  LOAD_FAST                'self'
               14  LOAD_ATTR                storage
               16  LOAD_FAST                'name'
               18  BINARY_SUBSCR    
               20  STORE_FAST               'command'

 L. 298        22  LOAD_GLOBAL              list
               24  LOAD_FAST                'args'
               26  CALL_FUNCTION_1       1  ''
               28  STORE_FAST               'args'

 L. 300        30  LOAD_GLOBAL              enumerate
               32  LOAD_FAST                'args'
               34  LOAD_CONST               None
               36  LOAD_GLOBAL              len
               38  LOAD_FAST                'command'
               40  LOAD_STR                 'args'
               42  BINARY_SUBSCR    
               44  CALL_FUNCTION_1       1  ''
               46  BUILD_SLICE_2         2 
               48  BINARY_SUBSCR    
               50  CALL_FUNCTION_1       1  ''
               52  GET_ITER         
             54_0  COME_FROM            86  '86'
               54  FOR_ITER            220  'to 220'
               56  UNPACK_SEQUENCE_2     2 
               58  STORE_FAST               'k'
               60  STORE_FAST               'v'

 L. 301        62  LOAD_GLOBAL              isinstance
               64  LOAD_FAST                'v'
               66  LOAD_FAST                'command'
               68  LOAD_STR                 'args'
               70  BINARY_SUBSCR    
               72  LOAD_FAST                'k'
               74  BINARY_SUBSCR    
               76  LOAD_ATTR                annotation
               78  LOAD_ATTR                type_
               80  DUP_TOP          
               82  STORE_FAST               'type_'
               84  CALL_FUNCTION_2       2  ''
               86  POP_JUMP_IF_TRUE     54  'to 54'

 L. 302        88  SETUP_FINALLY       188  'to 188'

 L. 303        90  LOAD_FAST                'type_'
               92  LOAD_GLOBAL              int
               94  LOAD_GLOBAL              float
               96  LOAD_GLOBAL              str
               98  BUILD_TUPLE_3         3 
              100  COMPARE_OP               in
              102  POP_JUMP_IF_FALSE   118  'to 118'

 L. 304       104  LOAD_FAST                'type_'
              106  LOAD_FAST                'v'
              108  CALL_FUNCTION_1       1  ''
              110  LOAD_FAST                'args'
              112  LOAD_FAST                'k'
              114  STORE_SUBSCR     
              116  JUMP_FORWARD        184  'to 184'
            118_0  COME_FROM           102  '102'

 L. 305       118  LOAD_FAST                'type_'
              120  LOAD_GLOBAL              list
              122  LOAD_GLOBAL              dict
              124  BUILD_TUPLE_2         2 
              126  COMPARE_OP               in
              128  POP_JUMP_IF_FALSE   146  'to 146'

 L. 306       130  LOAD_GLOBAL              json
              132  LOAD_METHOD              loads
              134  LOAD_FAST                'v'
              136  CALL_METHOD_1         1  ''
              138  LOAD_FAST                'args'
              140  LOAD_FAST                'k'
              142  STORE_SUBSCR     
              144  JUMP_FORWARD        184  'to 184'
            146_0  COME_FROM           128  '128'

 L. 307       146  LOAD_FAST                'type_'
              148  LOAD_GLOBAL              bool
              150  COMPARE_OP               is
              152  POP_JUMP_IF_FALSE   184  'to 184'

 L. 308       154  LOAD_FAST                'v'
              156  LOAD_CONST               ('false', 'False')
              158  COMPARE_OP               in
              160  POP_JUMP_IF_FALSE   172  'to 172'

 L. 309       162  LOAD_CONST               False
              164  LOAD_FAST                'args'
              166  LOAD_FAST                'k'
              168  STORE_SUBSCR     
              170  JUMP_FORWARD        184  'to 184'
            172_0  COME_FROM           160  '160'

 L. 311       172  LOAD_GLOBAL              bool
              174  LOAD_FAST                'v'
              176  CALL_FUNCTION_1       1  ''
              178  LOAD_FAST                'args'
              180  LOAD_FAST                'k'
              182  STORE_SUBSCR     
            184_0  COME_FROM           170  '170'
            184_1  COME_FROM           152  '152'
            184_2  COME_FROM           144  '144'
            184_3  COME_FROM           116  '116'
              184  POP_BLOCK        
              186  JUMP_BACK            54  'to 54'
            188_0  COME_FROM_FINALLY    88  '88'

 L. 312       188  DUP_TOP          
              190  LOAD_GLOBAL              ValueError
              192  LOAD_GLOBAL              json
              194  LOAD_ATTR                JSONDecodeError
              196  BUILD_TUPLE_2         2 
              198  COMPARE_OP               exception-match
              200  POP_JUMP_IF_FALSE   216  'to 216'
              202  POP_TOP          
              204  POP_TOP          
              206  POP_TOP          

 L. 313       208  POP_EXCEPT       
              210  JUMP_BACK            54  'to 54'
              212  POP_EXCEPT       
              214  JUMP_BACK            54  'to 54'
            216_0  COME_FROM           200  '200'
              216  END_FINALLY      
              218  JUMP_BACK            54  'to 54'

 L. 315       220  LOAD_FAST                'kwargs'
              222  LOAD_METHOD              items
              224  CALL_METHOD_0         0  ''
              226  GET_ITER         
            228_0  COME_FROM           286  '286'
            228_1  COME_FROM           260  '260'
              228  FOR_ITER            442  'to 442'
              230  UNPACK_SEQUENCE_2     2 
              232  STORE_FAST               'k'
              234  STORE_FAST               'v'

 L. 316       236  LOAD_GLOBAL              print
              238  LOAD_FAST                'command'
              240  LOAD_STR                 'kwargs'
              242  BINARY_SUBSCR    
              244  LOAD_FAST                'k'
              246  CALL_FUNCTION_2       2  ''
              248  POP_TOP          

 L. 317       250  LOAD_FAST                'k'
              252  LOAD_FAST                'command'
              254  LOAD_STR                 'kwargs'
              256  BINARY_SUBSCR    
              258  COMPARE_OP               in
              260  POP_JUMP_IF_FALSE   228  'to 228'
              262  LOAD_GLOBAL              isinstance
              264  LOAD_FAST                'v'
              266  LOAD_FAST                'command'
              268  LOAD_STR                 'kwargs'
              270  BINARY_SUBSCR    
              272  LOAD_FAST                'k'
              274  BINARY_SUBSCR    
              276  LOAD_ATTR                annotation
              278  LOAD_ATTR                type_
              280  DUP_TOP          
              282  STORE_FAST               'type_'
              284  CALL_FUNCTION_2       2  ''
              286  POP_JUMP_IF_TRUE    228  'to 228'

 L. 318       288  SETUP_FINALLY       408  'to 408'

 L. 319       290  LOAD_GLOBAL              isinstance
              292  LOAD_FAST                'v'
              294  LOAD_FAST                'type_'
              296  CALL_FUNCTION_2       2  ''
          298_300  POP_JUMP_IF_TRUE    404  'to 404'

 L. 320       302  LOAD_FAST                'type_'
              304  LOAD_GLOBAL              int
              306  LOAD_GLOBAL              float
              308  LOAD_GLOBAL              str
              310  BUILD_TUPLE_3         3 
              312  COMPARE_OP               in
          314_316  POP_JUMP_IF_FALSE   332  'to 332'

 L. 321       318  LOAD_FAST                'type_'
              320  LOAD_FAST                'v'
              322  CALL_FUNCTION_1       1  ''
              324  LOAD_FAST                'kwargs'
              326  LOAD_FAST                'k'
              328  STORE_SUBSCR     
              330  JUMP_FORWARD        404  'to 404'
            332_0  COME_FROM           314  '314'

 L. 322       332  LOAD_FAST                'type_'
              334  LOAD_GLOBAL              list
              336  LOAD_GLOBAL              dict
              338  BUILD_TUPLE_2         2 
              340  COMPARE_OP               in
          342_344  POP_JUMP_IF_FALSE   362  'to 362'

 L. 323       346  LOAD_GLOBAL              json
              348  LOAD_METHOD              loads
              350  LOAD_FAST                'v'
              352  CALL_METHOD_1         1  ''
              354  LOAD_FAST                'kwargs'
              356  LOAD_FAST                'k'
              358  STORE_SUBSCR     
              360  JUMP_FORWARD        404  'to 404'
            362_0  COME_FROM           342  '342'

 L. 324       362  LOAD_FAST                'type_'
              364  LOAD_GLOBAL              bool
              366  COMPARE_OP               is
          368_370  POP_JUMP_IF_FALSE   404  'to 404'

 L. 325       372  LOAD_FAST                'v'
              374  LOAD_CONST               ('false', 'False', 'no', 'No', 'null', 'Null', 'none', 'None')
              376  COMPARE_OP               in
          378_380  POP_JUMP_IF_FALSE   392  'to 392'

 L. 326       382  LOAD_CONST               False
              384  LOAD_FAST                'kwargs'
              386  LOAD_FAST                'k'
              388  STORE_SUBSCR     
              390  JUMP_FORWARD        404  'to 404'
            392_0  COME_FROM           378  '378'

 L. 328       392  LOAD_GLOBAL              bool
              394  LOAD_FAST                'v'
              396  CALL_FUNCTION_1       1  ''
              398  LOAD_FAST                'kwargs'
              400  LOAD_FAST                'k'
              402  STORE_SUBSCR     
            404_0  COME_FROM           390  '390'
            404_1  COME_FROM           368  '368'
            404_2  COME_FROM           360  '360'
            404_3  COME_FROM           330  '330'
            404_4  COME_FROM           298  '298'
              404  POP_BLOCK        
              406  JUMP_BACK           228  'to 228'
            408_0  COME_FROM_FINALLY   288  '288'

 L. 329       408  DUP_TOP          
              410  LOAD_GLOBAL              ValueError
              412  LOAD_GLOBAL              json
              414  LOAD_ATTR                JSONDecodeError
              416  BUILD_TUPLE_2         2 
              418  COMPARE_OP               exception-match
          420_422  POP_JUMP_IF_FALSE   438  'to 438'
              424  POP_TOP          
              426  POP_TOP          
              428  POP_TOP          

 L. 330       430  POP_EXCEPT       
              432  JUMP_BACK           228  'to 228'
              434  POP_EXCEPT       
              436  JUMP_BACK           228  'to 228'
            438_0  COME_FROM           420  '420'
              438  END_FINALLY      
              440  JUMP_BACK           228  'to 228'

 L. 332       442  LOAD_FAST                'command'
              444  LOAD_STR                 'peer'
              446  BINARY_SUBSCR    
          448_450  POP_JUMP_IF_FALSE   476  'to 476'

 L. 333       452  LOAD_CONST               True
              454  LOAD_FAST                'command'
              456  LOAD_STR                 'func'
              458  BINARY_SUBSCR    
              460  LOAD_FAST                'peer'
              462  BUILD_TUPLE_1         1 
              464  LOAD_FAST                'args'
              466  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              468  LOAD_FAST                'kwargs'
              470  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              472  BUILD_TUPLE_2         2 
              474  RETURN_VALUE     
            476_0  COME_FROM           448  '448'

 L. 335       476  LOAD_CONST               True
              478  LOAD_FAST                'command'
              480  LOAD_STR                 'func'
              482  BINARY_SUBSCR    
              484  LOAD_FAST                'args'
              486  LOAD_FAST                'kwargs'
              488  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              490  BUILD_TUPLE_2         2 
              492  RETURN_VALUE     
              494  JUMP_FORWARD        500  'to 500'
            496_0  COME_FROM             8  '8'

 L. 337       496  LOAD_CONST               (False, None)
              498  RETURN_VALUE     
            500_0  COME_FROM           494  '494'

Parse error at or near `POP_EXCEPT' instruction at offset 212

    def export(self) -> dict:
        snapshot = {}
        for k, v in self.storage.items():
            snapshot[k] = {'args':[i.export() for i in v['args']],  'kwargs':[i.export() for i in v['kwargs']], 
             'varargs':v['varargs'], 
             'varkw':v['varkw'], 
             'returns':str(v['returns']), 
             'protected':v['protected'], 
             'encrypt':v['encrypt']}
        else:
            return snapshot


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
    timeout: float
    auth_timeout: float
    interval: float
    max_connections: int
    IP: str
    PORT: int

    def __init__(self, name: str, key: RSA.RsaKey, ip: str, port: int=2604, *, trusted: Trusted=None, aliases: Aliases=None, timeout: float=4.0, auth_timeout: float=8.0, max_connections: int=8, interval: float=0.01, buffer: int=4096):
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
                self.timeout = timeout
            else:
                raise TypeError('timeout must be float or int')
            if isinstance(auth_timeout, (float, int)):
                self.auth_timeout = auth_timeout
            else:
                raise TypeError('auth_timeout must be float or int')
            if isinstance(max_connections, int):
                self.max_connections = max_connections
            else:
                raise TypeError('max_connections must be int')
            if isinstance(interval, float):
                self.interval = interval
            else:
                raise TypeError('interval must be float')
            if isinstance(buffer, int):
                if buffer < 128:
                    raise ValueError('buffer cannot be less than 128')
                self.buffer = buffer
            else:
                raise TypeError('buffer must be int')
        self._protocol = protocol.Protocol(self._key)
        self._increment = 0
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._server.setblocking(False)
        self._connections = {}
        self.commands = Commands()
        self.listener = threading.Thread(target=(self.listener_loop), daemon=True)
        self.commands.add_((self._handshake), protected=False, encrypt=False)
        self.commands.add_((self._auth), protected=False)
        self.commands.add_(self._commands)
        self.commands.add_(self._ping)
        self.commands.add_((self._echo), returns=Any)
        self.commands.add_(self._me)
        self.commands.add_(self._peers)
        self.commands.add_(self._trusted)
        self.commands.add_(self._aliases)
        self.commands.add_(self._close)

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
    def connections(self):
        return self._connections

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

    def _recv(self, socket_: socket.socket) -> bytes:
        try:
            data = socket_.recv(self.buffer)
        except socket.error as e:
            try:
                if e.errno is errno.ECONNRESET:
                    data = None
                else:
                    raise e
            finally:
                e = None
                del e

        else:
            return data

    def _receive--- This code section failed: ---

 L. 584         0  SETUP_FINALLY       124  'to 124'

 L. 585         2  LOAD_GLOBAL              bytearray
                4  LOAD_FAST                'self'
                6  LOAD_METHOD              _recv
                8  LOAD_FAST                'socket_'
               10  CALL_METHOD_1         1  ''
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'data'

 L. 587        16  LOAD_FAST                'data'
               18  POP_JUMP_IF_FALSE   118  'to 118'

 L. 588        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _protocol
               24  LOAD_METHOD              unpack_header
               26  LOAD_FAST                'data'
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'header'

 L. 590        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _protocol
               36  LOAD_METHOD              remained_data_size
               38  LOAD_GLOBAL              len
               40  LOAD_FAST                'data'
               42  CALL_FUNCTION_1       1  ''
               44  LOAD_FAST                'header'
               46  LOAD_ATTR                flags
               48  LOAD_ATTR                size
               50  CALL_METHOD_2         2  ''
               52  LOAD_CONST               0
               54  COMPARE_OP               >
               56  POP_JUMP_IF_FALSE   118  'to 118'

 L. 591        58  LOAD_GLOBAL              range

 L. 592        60  LOAD_GLOBAL              math
               62  LOAD_METHOD              ceil
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                _protocol
               68  LOAD_METHOD              remained_data_size
               70  LOAD_GLOBAL              len
               72  LOAD_FAST                'data'
               74  CALL_FUNCTION_1       1  ''
               76  LOAD_FAST                'header'
               78  LOAD_ATTR                flags
               80  LOAD_ATTR                size
               82  CALL_METHOD_2         2  ''
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                buffer
               88  BINARY_TRUE_DIVIDE
               90  CALL_METHOD_1         1  ''

 L. 591        92  CALL_FUNCTION_1       1  ''
               94  GET_ITER         
               96  FOR_ITER            118  'to 118'
               98  STORE_FAST               'i'

 L. 593       100  LOAD_FAST                'data'
              102  LOAD_METHOD              extend
              104  LOAD_FAST                'self'
              106  LOAD_METHOD              _recv
              108  LOAD_FAST                'socket_'
              110  CALL_METHOD_1         1  ''
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          
              116  JUMP_BACK            96  'to 96'
            118_0  COME_FROM            56  '56'
            118_1  COME_FROM            18  '18'

 L. 594       118  LOAD_FAST                'data'
              120  POP_BLOCK        
              122  RETURN_VALUE     
            124_0  COME_FROM_FINALLY     0  '0'

 L. 595       124  DUP_TOP          
              126  LOAD_GLOBAL              TypeError
              128  COMPARE_OP               exception-match
              130  POP_JUMP_IF_FALSE   148  'to 148'
              132  POP_TOP          
              134  POP_TOP          
              136  POP_TOP          

 L. 596       138  LOAD_GLOBAL              bytearray
              140  CALL_FUNCTION_0       0  ''
              142  ROT_FOUR         
              144  POP_EXCEPT       
              146  RETURN_VALUE     
            148_0  COME_FROM           130  '130'
              148  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 134

    def _send--- This code section failed: ---

 L. 599         0  LOAD_FAST                'peer'
                2  LOAD_ATTR                lock
                4  LOAD_METHOD              acquire
                6  CALL_METHOD_0         0  ''
             8_10  POP_JUMP_IF_FALSE   470  'to 470'

 L. 600     12_14  SETUP_FINALLY       446  'to 446'
            16_18  SETUP_FINALLY       402  'to 402'

 L. 601        20  LOAD_FAST                'peer'
               22  LOAD_ATTR                socket
               24  LOAD_METHOD              setblocking
               26  LOAD_CONST               True
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 602        32  LOAD_FAST                'peer'
               34  LOAD_ATTR                socket
               36  LOAD_METHOD              sendall
               38  LOAD_FAST                'packet'
               40  LOAD_METHOD              raw
               42  CALL_METHOD_0         0  ''
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L. 604        48  LOAD_FAST                'self'
               50  LOAD_METHOD              _receive
               52  LOAD_FAST                'peer'
               54  LOAD_ATTR                socket
               56  CALL_METHOD_1         1  ''
               58  STORE_FAST               'data'

 L. 605        60  LOAD_FAST                'data'
            62_64  POP_JUMP_IF_FALSE   390  'to 390'

 L. 606        66  SETUP_FINALLY       238  'to 238'

 L. 607        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _protocol
               72  LOAD_METHOD              unpack
               74  LOAD_FAST                'data'
               76  CALL_METHOD_1         1  ''
               78  STORE_FAST               'packet_'

 L. 609        80  LOAD_FAST                'packet_'
               82  LOAD_ATTR                header
               84  LOAD_ATTR                flags
               86  LOAD_ATTR                type
               88  LOAD_CONST               0
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_TRUE    108  'to 108'
               94  LOAD_FAST                'packet_'
               96  LOAD_ATTR                header
               98  LOAD_ATTR                flags
              100  LOAD_ATTR                type
              102  LOAD_CONST               2
              104  COMPARE_OP               >
              106  POP_JUMP_IF_FALSE   118  'to 118'
            108_0  COME_FROM            92  '92'

 L. 610       108  LOAD_GLOBAL              TypeError
              110  LOAD_STR                 'Unexpected packet type'
              112  CALL_FUNCTION_1       1  ''
              114  RAISE_VARARGS_1       1  'exception instance'
              116  JUMP_FORWARD        144  'to 144'
            118_0  COME_FROM           106  '106'

 L. 611       118  LOAD_FAST                'packet_'
              120  LOAD_ATTR                header
              122  LOAD_ATTR                command
              124  LOAD_FAST                'packet'
              126  LOAD_ATTR                header
              128  LOAD_ATTR                command
              130  COMPARE_OP               !=
              132  POP_JUMP_IF_FALSE   144  'to 144'

 L. 612       134  LOAD_GLOBAL              protocol
              136  LOAD_METHOD              PacketError
              138  LOAD_STR                 'Unexpected response'
              140  CALL_METHOD_1         1  ''
              142  RAISE_VARARGS_1       1  'exception instance'
            144_0  COME_FROM           132  '132'
            144_1  COME_FROM           116  '116'

 L. 614       144  LOAD_FAST                'packet_'
              146  LOAD_ATTR                header
              148  LOAD_ATTR                flags
              150  LOAD_ATTR                type
              152  STORE_FAST               'type_'

 L. 616       154  LOAD_CONST               None
              156  SETUP_FINALLY       208  'to 208'
              158  SETUP_FINALLY       176  'to 176'

 L. 617       160  LOAD_GLOBAL              json
              162  LOAD_METHOD              loads
              164  LOAD_FAST                'packet_'
              166  LOAD_ATTR                data
              168  CALL_METHOD_1         1  ''
              170  STORE_FAST               'packet_'
              172  POP_BLOCK        
              174  JUMP_FORWARD        204  'to 204'
            176_0  COME_FROM_FINALLY   158  '158'

 L. 618       176  DUP_TOP          
              178  LOAD_GLOBAL              json
              180  LOAD_ATTR                JSONDecodeError
              182  COMPARE_OP               exception-match
              184  POP_JUMP_IF_FALSE   202  'to 202'
              186  POP_TOP          
              188  POP_TOP          
              190  POP_TOP          

 L. 619       192  LOAD_FAST                'packet_'
              194  LOAD_ATTR                data
              196  STORE_FAST               'packet_'
              198  POP_EXCEPT       
              200  JUMP_FORWARD        204  'to 204'
            202_0  COME_FROM           184  '184'
              202  END_FINALLY      
            204_0  COME_FROM           200  '200'
            204_1  COME_FROM           174  '174'
              204  POP_BLOCK        
              206  BEGIN_FINALLY    
            208_0  COME_FROM_FINALLY   156  '156'

 L. 621       208  LOAD_FAST                'type_'
              210  LOAD_FAST                'packet_'
              212  BUILD_TUPLE_2         2 
              214  POP_FINALLY           1  ''
              216  ROT_TWO          
              218  POP_TOP          
              220  POP_BLOCK        
              222  POP_BLOCK        
              224  POP_BLOCK        
              226  CALL_FINALLY        446  'to 446'
              228  RETURN_VALUE     
              230  END_FINALLY      
              232  POP_TOP          
              234  POP_BLOCK        
              236  JUMP_FORWARD        388  'to 388'
            238_0  COME_FROM_FINALLY    66  '66'

 L. 622       238  DUP_TOP          
              240  LOAD_GLOBAL              protocol
              242  LOAD_ATTR                ProtocolError
              244  COMPARE_OP               exception-match
          246_248  POP_JUMP_IF_FALSE   288  'to 288'
              250  POP_TOP          
              252  POP_TOP          
              254  POP_TOP          

 L. 623       256  LOAD_GLOBAL              protocol
              258  LOAD_METHOD              ProtocolError
              260  LOAD_STR                 'peer '
              262  LOAD_FAST                'peer'
              264  LOAD_ATTR                ip
              266  FORMAT_VALUE          0  ''
              268  LOAD_STR                 ':'
              270  LOAD_FAST                'peer'
              272  LOAD_ATTR                port
              274  FORMAT_VALUE          0  ''
              276  LOAD_STR                 ' does not support uctp protocol'
              278  BUILD_STRING_5        5 
              280  CALL_METHOD_1         1  ''
              282  RAISE_VARARGS_1       1  'exception instance'
              284  POP_EXCEPT       
              286  JUMP_FORWARD        388  'to 388'
            288_0  COME_FROM           246  '246'

 L. 624       288  DUP_TOP          
              290  LOAD_GLOBAL              protocol
              292  LOAD_ATTR                VersionError
              294  COMPARE_OP               exception-match
          296_298  POP_JUMP_IF_FALSE   338  'to 338'
              300  POP_TOP          
              302  POP_TOP          
              304  POP_TOP          

 L. 625       306  LOAD_GLOBAL              protocol
              308  LOAD_METHOD              VersionError

 L. 626       310  LOAD_STR                 'peer '
              312  LOAD_FAST                'peer'
              314  LOAD_ATTR                ip
              316  FORMAT_VALUE          0  ''
              318  LOAD_STR                 ':'
              320  LOAD_FAST                'peer'
              322  LOAD_ATTR                port
              324  FORMAT_VALUE          0  ''
              326  LOAD_STR                 ' does not support current version of protocol'
              328  BUILD_STRING_5        5 

 L. 625       330  CALL_METHOD_1         1  ''
              332  RAISE_VARARGS_1       1  'exception instance'
              334  POP_EXCEPT       
              336  JUMP_FORWARD        388  'to 388'
            338_0  COME_FROM           296  '296'

 L. 627       338  DUP_TOP          
              340  LOAD_GLOBAL              protocol
              342  LOAD_ATTR                PacketError
              344  COMPARE_OP               exception-match
          346_348  POP_JUMP_IF_FALSE   386  'to 386'
              350  POP_TOP          
              352  POP_TOP          
              354  POP_TOP          

 L. 628       356  LOAD_GLOBAL              protocol
              358  LOAD_METHOD              PacketError
              360  LOAD_STR                 'corrupted data received from peer '
              362  LOAD_FAST                'peer'
              364  LOAD_ATTR                ip
              366  FORMAT_VALUE          0  ''
              368  LOAD_STR                 ':'
              370  LOAD_FAST                'peer'
              372  LOAD_ATTR                port
              374  FORMAT_VALUE          0  ''
              376  BUILD_STRING_4        4 
              378  CALL_METHOD_1         1  ''
              380  RAISE_VARARGS_1       1  'exception instance'
              382  POP_EXCEPT       
              384  JUMP_FORWARD        388  'to 388'
            386_0  COME_FROM           346  '346'
              386  END_FINALLY      
            388_0  COME_FROM           384  '384'
            388_1  COME_FROM           336  '336'
            388_2  COME_FROM           286  '286'
            388_3  COME_FROM           236  '236'
              388  JUMP_FORWARD        398  'to 398'
            390_0  COME_FROM            62  '62'

 L. 630       390  LOAD_GLOBAL              ConnectionError
              392  LOAD_STR                 'connection with peer lost'
              394  CALL_FUNCTION_1       1  ''
              396  RAISE_VARARGS_1       1  'exception instance'
            398_0  COME_FROM           388  '388'
              398  POP_BLOCK        
              400  JUMP_FORWARD        442  'to 442'
            402_0  COME_FROM_FINALLY    16  '16'

 L. 631       402  DUP_TOP          
              404  LOAD_GLOBAL              Exception
              406  COMPARE_OP               exception-match
          408_410  POP_JUMP_IF_FALSE   440  'to 440'
              412  POP_TOP          
              414  STORE_FAST               'e'
              416  POP_TOP          
              418  SETUP_FINALLY       428  'to 428'

 L. 632       420  LOAD_FAST                'e'
              422  RAISE_VARARGS_1       1  'exception instance'
              424  POP_BLOCK        
              426  BEGIN_FINALLY    
            428_0  COME_FROM_FINALLY   418  '418'
              428  LOAD_CONST               None
              430  STORE_FAST               'e'
              432  DELETE_FAST              'e'
              434  END_FINALLY      
              436  POP_EXCEPT       
              438  JUMP_FORWARD        442  'to 442'
            440_0  COME_FROM           408  '408'
              440  END_FINALLY      
            442_0  COME_FROM           438  '438'
            442_1  COME_FROM           400  '400'
              442  POP_BLOCK        
              444  BEGIN_FINALLY    
            446_0  COME_FROM           226  '226'
            446_1  COME_FROM_FINALLY    12  '12'

 L. 634       446  LOAD_FAST                'peer'
              448  LOAD_ATTR                socket
              450  LOAD_METHOD              setblocking
              452  LOAD_CONST               False
              454  CALL_METHOD_1         1  ''
              456  POP_TOP          

 L. 635       458  LOAD_FAST                'peer'
              460  LOAD_ATTR                lock
              462  LOAD_METHOD              release
              464  CALL_METHOD_0         0  ''
              466  POP_TOP          
              468  END_FINALLY      
            470_0  COME_FROM             8  '8'

Parse error at or near `LOAD_FAST' instruction at offset 208

    def listener_loop(self):
        while self._state > 0:
            start = time.time()
            readers = [
             self._server]
            for i in self._connections.values():
                readers.append(i)
            else:
                writers = [i for i in self._connections.values() if not i.messages.empty()]
                if self._state == 2:
                    if not writers:
                        self._state = 0
                readable, writeable, exceptional = select.select(readers, writers, readers, 0.001)

            for i in readable:
                if i is self._server:
                    peer = self._server.accept()
                    if self.max_connections < 0 or self._clients_count() >= self.max_connections:
                        peer[0].close()
                    else:
                        peer[0].setblocking(False)
                        increment = self.increment
                        self._connections[f"_{increment}"] = Connection(f"_{increment}", peer[1][0], peer[1][1], peer[0], True)
            else:
                if i.lock.acquire(False):
                    data = self._receive(i.socket)
                    if data:
                        try:
                            data = self._protocol.unpack(data)
                            if self._state == 1:
                                i.messages.put(data)
                            else:
                                if self._state == 2:
                                    i.messages.put(self._error(i, data.header.command, 0, 'Peer shuts down', bool(i.key)))
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
                    if packet.header.flags.type == protocol.TYPE_REQUEST:
                        try:
                            encrypt = self.commands.get(packet.header.command.decode())['encrypt']
                            if self.commands.get(packet.header.command.decode())['protected']:
                                packet = i.authorized or self._error(i, packet.header.command, 1, 'Access denied', encrypt)
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
                                    result = (self.commands.execute)(
 i,
 packet.header.command.decode(), *args, **kwargs)[1]
                                    try:
                                        packet = self._protocol.pack((packet.header.command),
                                          (json.dumps(result)),
                                          encrypt,
                                          type_=1,
                                          key=(i.key))
                                    except json.JSONDecodeError:
                                        packet = self._error(i, packet.header.command, 2, 'Command tried to return objects that json does not support', encrypt)

                                except Exception as e:
                                    try:
                                        if isinstance(e, _PassException):
                                            if isinstance(e.extract, NameError):
                                                packet = self._error(i, packet.header.command, 3, e.extract.__str__(), encrypt)
                                        else:
                                            packet = self._error(i, packet.header.command, 4, f"Exception caught while executing command ({e.__class__.__name__}: {e.__str__()})", encrypt)
                                    finally:
                                        e = None
                                        del e

                            except (json.JSONDecodeError, ArgumentsError):
                                packet = self._error(i, packet.header.command, 5, 'Wrong arguments', encrypt)

                        except NameError:
                            packet = self._error(i, packet.header.command, 6, 'Command not found', i.authorized)

                    else:
                        packet = self._error(i, packet.header.command, 7, 'Unexpected packet type', i.authorized)
                    i.socket.send(packet.raw())
                    i.lock.release()
            else:
                for i in exceptional:
                    self.disconnect(i)
                else:
                    expired = []
                    for i in self._connections:
                        if not self._connections[i].authorized:
                            if not (self._connections[i].timestamp + self.auth_timeout < time.time() or self._connections[i].to_close):
                                if self._connections[i].socket._closed:
                                    pass
                                expired.append(i)
                            for i in expired:
                                self.disconnect(i)
                            else:
                                delta = time.time() - start

                            if self.interval - delta > 0:
                                time.sleep(self.interval - delta)

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
                connection.socket.settimeout(self.timeout)
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

    def send(self, name: str, command: str, args: Union[(list, tuple)]=(), kwargs: dict=None, *, raise_: bool=True):
        if name not in self._connections:
            raise NameError(f'Peer "{name}" not connected')
        else:
            if not self._connections[name].authorized:
                raise AccessError(f'"{name}" is unauthorized peer')
            else:
                if args:
                    if not isinstance(args, (list, tuple)):
                        raise TypeError('args must be list or tuple')
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
            self._server.settimeout(self.timeout)
            self._server.bind((self.IP, self.PORT))
            self._server.listen()
            self.listener.start()

    def stop(self):
        if self._state == 1:
            self._state = 2
            self.listener.join()
            for i in list(self._connections):
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

 L. 923         0  LOAD_FAST                'answer'
                2  LOAD_FAST                'peer'
                4  LOAD_ATTR                session
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    16  'to 16'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                trusted
               14  POP_JUMP_IF_FALSE    30  'to 30'
             16_0  COME_FROM             8  '8'
               16  LOAD_FAST                'peer'
               18  LOAD_METHOD              key_hash
               20  CALL_METHOD_0         0  ''
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                trusted
               26  COMPARE_OP               in
               28  POP_JUMP_IF_FALSE    40  'to 40'
             30_0  COME_FROM            14  '14'

 L. 924        30  LOAD_CONST               True
               32  LOAD_FAST                'peer'
               34  STORE_ATTR               authorized

 L. 925        36  LOAD_CONST               True
               38  RETURN_VALUE     
             40_0  COME_FROM            28  '28'

 L. 927        40  LOAD_CONST               False
               42  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 40

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

    def _trusted(self) -> list:
        return self.trusted

    def _aliases(self) -> dict:
        return self.aliases

    @staticmethod
    def _close(peer: Connection) -> bool:
        peer.close()
        return True
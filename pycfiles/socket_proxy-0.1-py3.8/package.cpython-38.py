# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/socket_proxy/package.py
# Compiled at: 2020-05-03 10:24:35
# Size of source mod 2**32: 6248 bytes
import ipaddress, logging, struct
from .base import CLIENT_NAME_SIZE, DuplicatePackageType, InvalidPackage, InvalidPackageType, TransportType
_logger = logging.getLogger(__name__)
_package_registry = {}

class MetaPackage(type):

    def __new__(metacls, name, bases, attrs):
        ptype = attrs['_type']
        if ptype in _package_registry:
            raise DuplicatePackageType()
        cls = super().__new__(metacls, name, bases, attrs)
        if ptype is not None:
            _package_registry[ptype] = cls
        return cls


class PackageStruct(struct.Struct):

    async def read(self, reader):
        return self.unpack(await reader.readexactly(self.size))


class Package(metaclass=MetaPackage):
    _name = None
    _type = None
    __slots__ = ()
    HEADER = PackageStruct('!B')

    def to_bytes(self):
        return self.HEADER.pack(self._type)

    @classmethod
    async def recv(cls, reader):
        return ()

    @classmethod
    async def from_reader--- This code section failed: ---

 L.  58         0  SETUP_FINALLY        66  'to 66'

 L.  59         2  LOAD_FAST                'cls'
                4  LOAD_ATTR                HEADER
                6  LOAD_METHOD              read
                8  LOAD_FAST                'reader'
               10  CALL_METHOD_1         1  ''
               12  GET_AWAITABLE    
               14  LOAD_CONST               None
               16  YIELD_FROM       
               18  UNPACK_SEQUENCE_1     1 
               20  STORE_FAST               'ptype'

 L.  61        22  LOAD_FAST                'ptype'
               24  LOAD_GLOBAL              _package_registry
               26  COMPARE_OP               not-in
               28  POP_JUMP_IF_FALSE    36  'to 36'

 L.  62        30  LOAD_GLOBAL              InvalidPackageType
               32  CALL_FUNCTION_0       0  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            28  '28'

 L.  64        36  LOAD_GLOBAL              _package_registry
               38  LOAD_FAST                'ptype'
               40  BINARY_SUBSCR    
               42  STORE_FAST               'pcls'

 L.  65        44  LOAD_FAST                'pcls'
               46  LOAD_FAST                'pcls'
               48  LOAD_METHOD              recv
               50  LOAD_FAST                'reader'
               52  CALL_METHOD_1         1  ''
               54  GET_AWAITABLE    
               56  LOAD_CONST               None
               58  YIELD_FROM       
               60  CALL_FUNCTION_EX      0  'positional arguments only'
               62  POP_BLOCK        
               64  RETURN_VALUE     
             66_0  COME_FROM_FINALLY     0  '0'

 L.  66        66  DUP_TOP          
               68  LOAD_GLOBAL              Exception
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE    86  'to 86'
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L.  67        80  POP_EXCEPT       
               82  LOAD_CONST               None
               84  RETURN_VALUE     
             86_0  COME_FROM            72  '72'
               86  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 76


class InitPackage(Package):
    _name = 'init'
    _type = 16
    __slots__ = ('token', 'addresses')
    INIT = PackageStruct(f"!{CLIENT_NAME_SIZE}sB")
    ADDRESS = PackageStruct('!BH')

    def __init__(self, token, addresses, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.token = token
        self.addresses = addresses[:255]

    def to_bytes(self):
        data = super().to_bytes() + self.INIT.pack(self.token, len(self.addresses))
        for ip_type, port in self.addresses:
            data += self.ADDRESS.pack(ip_type, port)
        else:
            return data

    @classmethod
    async def recv(cls, reader):
        res = await super().recv(reader)
        token, length = await cls.INIT.read(reader)
        addresses = []
        for _ in range(length):
            ip_type, port = await cls.ADDRESS.read(reader)
            addresses.append((TransportType(ip_type), port))
        else:
            return (
             token, addresses) + res


class ConfigPackage(Package):
    _name = 'client>config'
    _type = 17
    __slots__ = ('bantime', 'clients', 'connects')
    CONFIG = PackageStruct('!III')

    def __init__(self, bantime, clients, connects, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.bantime = bantime
        self.clients = clients
        self.connects = connects

    def to_bytes(self):
        return super().to_bytes() + self.CONFIG.pack(self.bantime, self.clients, self.connects)

    @classmethod
    async def recv(cls, reader):
        res = await super().recv(reader)
        return await cls.CONFIG.read(reader) + res


class ClientPackage(Package):
    _name = 'client'
    _type = 48
    __slots__ = ('token', )
    TOKEN = PackageStruct(f"!{CLIENT_NAME_SIZE}s")

    def __init__(self, token, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.token = token

    def to_bytes(self):
        return super().to_bytes() + self.TOKEN.pack(self.token)

    @classmethod
    async def recv(cls, reader):
        res = await super().recv(reader)
        return await cls.TOKEN.read(reader) + res


class ClientInitPackage(ClientPackage):
    _name = 'client>init'
    _type = 49
    __slots__ = ('ip', 'port')
    IP = PackageStruct('!BH')

    def __init__(self, ip, port, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.ip, self.port = ip, port

    def to_bytes(self):
        ip_type = TransportType.from_ip(self.ip)
        return super().to_bytes() + self.IP.pack(ip_type, self.port) + self.ip.packed

    @classmethod
    async def recv(cls, reader):
        res = await super().recv(reader)
        ip_type, port = await cls.IP.read(reader)
        if ip_type == TransportType.IPv4:
            ip = ipaddress.IPv4Address(await reader.readexactly(4))
        else:
            if ip_type == TransportType.IPv6:
                ip = ipaddress.IPv6Address(await reader.readexactly(16))
            else:
                raise InvalidPackageType()
        return (
         ip, port) + res


class ClientClosePackage(ClientPackage):
    _name = 'client>close'
    _type = 50
    __slots__ = ()


class ClientDataPackage(ClientPackage):
    _name = 'client>data'
    _type = 51
    __slots__ = ('data', )
    MAX_SIZE = 65536
    DATA = PackageStruct('!I')

    def __init__(self, data, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.data = data

    def to_bytes(self):
        data = b''
        header = super().to_bytes()
        for i in range(0, len(self.data), self.MAX_SIZE):
            chunk = self.data[i:][:self.MAX_SIZE]
            data += header + self.DATA.pack(len(chunk)) + chunk
        else:
            return data

    @classmethod
    async def recv(cls, reader):
        res = await super().recv(reader)
        length, = await cls.DATA.read(reader)
        if length > cls.MAX_SIZE:
            raise InvalidPackage()
        data = await reader.read(length)
        return (data,) + res
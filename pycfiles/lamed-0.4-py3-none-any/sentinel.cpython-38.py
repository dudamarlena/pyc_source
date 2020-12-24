# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-03p63p8r/redis/redis/sentinel.py
# Compiled at: 2020-04-05 04:25:10
# Size of source mod 2**32: 11358 bytes
import random, weakref
from redis.client import Redis
from redis.connection import ConnectionPool, Connection
from redis.exceptions import ConnectionError, ResponseError, ReadOnlyError, TimeoutError
from redis._compat import iteritems, nativestr, xrange

class MasterNotFoundError(ConnectionError):
    pass


class SlaveNotFoundError(ConnectionError):
    pass


class SentinelManagedConnection(Connection):

    def __init__(self, **kwargs):
        self.connection_pool = kwargs.pop('connection_pool')
        (super(SentinelManagedConnection, self).__init__)(**kwargs)

    def __repr__(self):
        pool = self.connection_pool
        s = '%s<service=%s%%s>' % (type(self).__name__, pool.service_name)
        if self.host:
            host_info = ',host=%s,port=%s' % (self.host, self.port)
            s = s % host_info
        return s

    def connect_to(self, address):
        self.host, self.port = address
        super(SentinelManagedConnection, self).connect()
        if self.connection_pool.check_connection:
            self.send_command('PING')
            if nativestr(self.read_response()) != 'PONG':
                raise ConnectionError('PING failed')

    def connect--- This code section failed: ---

 L.  41         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _sock
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L.  42         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L.  43        10  LOAD_FAST                'self'
               12  LOAD_ATTR                connection_pool
               14  LOAD_ATTR                is_master
               16  POP_JUMP_IF_FALSE    36  'to 36'

 L.  44        18  LOAD_FAST                'self'
               20  LOAD_METHOD              connect_to
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                connection_pool
               26  LOAD_METHOD              get_master_address
               28  CALL_METHOD_0         0  ''
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          
               34  JUMP_FORWARD         98  'to 98'
             36_0  COME_FROM            16  '16'

 L.  46        36  LOAD_FAST                'self'
               38  LOAD_ATTR                connection_pool
               40  LOAD_METHOD              rotate_slaves
               42  CALL_METHOD_0         0  ''
               44  GET_ITER         
               46  FOR_ITER             94  'to 94'
               48  STORE_FAST               'slave'

 L.  47        50  SETUP_FINALLY        68  'to 68'

 L.  48        52  LOAD_FAST                'self'
               54  LOAD_METHOD              connect_to
               56  LOAD_FAST                'slave'
               58  CALL_METHOD_1         1  ''
               60  POP_BLOCK        
               62  ROT_TWO          
               64  POP_TOP          
               66  RETURN_VALUE     
             68_0  COME_FROM_FINALLY    50  '50'

 L.  49        68  DUP_TOP          
               70  LOAD_GLOBAL              ConnectionError
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE    90  'to 90'
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L.  50        82  POP_EXCEPT       
               84  JUMP_BACK            46  'to 46'
               86  POP_EXCEPT       
               88  JUMP_BACK            46  'to 46'
             90_0  COME_FROM            74  '74'
               90  END_FINALLY      
               92  JUMP_BACK            46  'to 46'

 L.  51        94  LOAD_GLOBAL              SlaveNotFoundError
               96  RAISE_VARARGS_1       1  'exception instance'
             98_0  COME_FROM            34  '34'

Parse error at or near `ROT_TWO' instruction at offset 62

    def read_response--- This code section failed: ---

 L.  54         0  SETUP_FINALLY        18  'to 18'

 L.  55         2  LOAD_GLOBAL              super
                4  LOAD_GLOBAL              SentinelManagedConnection
                6  LOAD_FAST                'self'
                8  CALL_FUNCTION_2       2  ''
               10  LOAD_METHOD              read_response
               12  CALL_METHOD_0         0  ''
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L.  56        18  DUP_TOP          
               20  LOAD_GLOBAL              ReadOnlyError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    62  'to 62'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L.  57        32  LOAD_FAST                'self'
               34  LOAD_ATTR                connection_pool
               36  LOAD_ATTR                is_master
               38  POP_JUMP_IF_FALSE    56  'to 56'

 L.  63        40  LOAD_FAST                'self'
               42  LOAD_METHOD              disconnect
               44  CALL_METHOD_0         0  ''
               46  POP_TOP          

 L.  64        48  LOAD_GLOBAL              ConnectionError
               50  LOAD_STR                 'The previous master is now a slave'
               52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            38  '38'

 L.  65        56  RAISE_VARARGS_0       0  'reraise'
               58  POP_EXCEPT       
               60  JUMP_FORWARD         64  'to 64'
             62_0  COME_FROM            24  '24'
               62  END_FINALLY      
             64_0  COME_FROM            60  '60'

Parse error at or near `POP_TOP' instruction at offset 28


class SentinelConnectionPool(ConnectionPool):
    __doc__ = '\n    Sentinel backed connection pool.\n\n    If ``check_connection`` flag is set to True, SentinelManagedConnection\n    sends a PING command right after establishing the connection.\n    '

    def __init__(self, service_name, sentinel_manager, **kwargs):
        kwargs['connection_class'] = kwargs.get('connection_class', SentinelManagedConnection)
        self.is_master = kwargs.pop('is_master', True)
        self.check_connection = kwargs.pop('check_connection', False)
        (super(SentinelConnectionPool, self).__init__)(**kwargs)
        self.connection_kwargs['connection_pool'] = weakref.proxy(self)
        self.service_name = service_name
        self.sentinel_manager = sentinel_manager

    def __repr__(self):
        return '%s<service=%s(%s)' % (
         type(self).__name__,
         self.service_name,
         self.is_master and 'master' or 'slave')

    def reset(self):
        super(SentinelConnectionPool, self).reset()
        self.master_address = None
        self.slave_rr_counter = None

    def get_master_address(self):
        master_address = self.sentinel_manager.discover_master(self.service_name)
        if self.is_master:
            if self.master_address is None:
                self.master_address = master_address
            else:
                if master_address != self.master_address:
                    self.disconnect()
        return master_address

    def rotate_slaves(self):
        """Round-robin slave balancer"""
        slaves = self.sentinel_manager.discover_slaves(self.service_name)
        if slaves:
            if self.slave_rr_counter is None:
                self.slave_rr_counter = random.randint(0, len(slaves) - 1)
            for _ in xrange(len(slaves)):
                self.slave_rr_counter = (self.slave_rr_counter + 1) % len(slaves)
                slave = slaves[self.slave_rr_counter]
                (yield slave)

        try:
            (yield self.get_master_address())
        except MasterNotFoundError:
            pass
        else:
            raise SlaveNotFoundError('No slave found for %r' % self.service_name)


class Sentinel(object):
    __doc__ = "\n    Redis Sentinel cluster client\n\n    >>> from redis.sentinel import Sentinel\n    >>> sentinel = Sentinel([('localhost', 26379)], socket_timeout=0.1)\n    >>> master = sentinel.master_for('mymaster', socket_timeout=0.1)\n    >>> master.set('foo', 'bar')\n    >>> slave = sentinel.slave_for('mymaster', socket_timeout=0.1)\n    >>> slave.get('foo')\n    'bar'\n\n    ``sentinels`` is a list of sentinel nodes. Each node is represented by\n    a pair (hostname, port).\n\n    ``min_other_sentinels`` defined a minimum number of peers for a sentinel.\n    When querying a sentinel, if it doesn't meet this threshold, responses\n    from that sentinel won't be considered valid.\n\n    ``sentinel_kwargs`` is a dictionary of connection arguments used when\n    connecting to sentinel instances. Any argument that can be passed to\n    a normal Redis connection can be specified here. If ``sentinel_kwargs`` is\n    not specified, any socket_timeout and socket_keepalive options specified\n    in ``connection_kwargs`` will be used.\n\n    ``connection_kwargs`` are keyword arguments that will be used when\n    establishing a connection to a Redis server.\n    "

    def __init__(self, sentinels, min_other_sentinels=0, sentinel_kwargs=None, **connection_kwargs):
        if sentinel_kwargs is None:
            sentinel_kwargs = {v:k for k, v in iteritems(connection_kwargs) if k.startswith('socket_') if k.startswith('socket_')}
        self.sentinel_kwargs = sentinel_kwargs
        self.sentinels = [Redis(hostname, port, **self.sentinel_kwargs) for hostname, port in sentinels]
        self.min_other_sentinels = min_other_sentinels
        self.connection_kwargs = connection_kwargs

    def __repr__(self):
        sentinel_addresses = []
        for sentinel in self.sentinels:
            sentinel_addresses.append('%s:%s' % (
             sentinel.connection_pool.connection_kwargs['host'],
             sentinel.connection_pool.connection_kwargs['port']))
        else:
            return '%s<sentinels=[%s]>' % (
             type(self).__name__,
             ','.join(sentinel_addresses))

    def check_master_state(self, state, service_name):
        if not state['is_master'] or state['is_sdown'] or state['is_odown']:
            return False
            if state['num-other-sentinels'] < self.min_other_sentinels:
                return False
        return True

    def discover_master--- This code section failed: ---

 L. 201         0  LOAD_GLOBAL              enumerate
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                sentinels
                6  CALL_FUNCTION_1       1  ''
                8  GET_ITER         
             10_0  COME_FROM            84  '84'
             10_1  COME_FROM            72  '72'
               10  FOR_ITER            136  'to 136'
               12  UNPACK_SEQUENCE_2     2 
               14  STORE_FAST               'sentinel_no'
               16  STORE_FAST               'sentinel'

 L. 202        18  SETUP_FINALLY        32  'to 32'

 L. 203        20  LOAD_FAST                'sentinel'
               22  LOAD_METHOD              sentinel_masters
               24  CALL_METHOD_0         0  ''
               26  STORE_FAST               'masters'
               28  POP_BLOCK        
               30  JUMP_FORWARD         60  'to 60'
             32_0  COME_FROM_FINALLY    18  '18'

 L. 204        32  DUP_TOP          
               34  LOAD_GLOBAL              ConnectionError
               36  LOAD_GLOBAL              TimeoutError
               38  BUILD_TUPLE_2         2 
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    58  'to 58'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 205        50  POP_EXCEPT       
               52  JUMP_BACK            10  'to 10'
               54  POP_EXCEPT       
               56  JUMP_FORWARD         60  'to 60'
             58_0  COME_FROM            42  '42'
               58  END_FINALLY      
             60_0  COME_FROM            56  '56'
             60_1  COME_FROM            30  '30'

 L. 206        60  LOAD_FAST                'masters'
               62  LOAD_METHOD              get
               64  LOAD_FAST                'service_name'
               66  CALL_METHOD_1         1  ''
               68  STORE_FAST               'state'

 L. 207        70  LOAD_FAST                'state'
               72  POP_JUMP_IF_FALSE    10  'to 10'
               74  LOAD_FAST                'self'
               76  LOAD_METHOD              check_master_state
               78  LOAD_FAST                'state'
               80  LOAD_FAST                'service_name'
               82  CALL_METHOD_2         2  ''
               84  POP_JUMP_IF_FALSE    10  'to 10'

 L. 210        86  LOAD_FAST                'sentinel'

 L. 210        88  LOAD_FAST                'self'
               90  LOAD_ATTR                sentinels
               92  LOAD_CONST               0
               94  BINARY_SUBSCR    

 L. 209        96  ROT_TWO          
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                sentinels
              102  LOAD_CONST               0
              104  STORE_SUBSCR     
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                sentinels
              110  LOAD_FAST                'sentinel_no'
              112  STORE_SUBSCR     

 L. 211       114  LOAD_FAST                'state'
              116  LOAD_STR                 'ip'
              118  BINARY_SUBSCR    
              120  LOAD_FAST                'state'
              122  LOAD_STR                 'port'
              124  BINARY_SUBSCR    
              126  BUILD_TUPLE_2         2 
              128  ROT_TWO          
              130  POP_TOP          
              132  RETURN_VALUE     
              134  JUMP_BACK            10  'to 10'

 L. 212       136  LOAD_GLOBAL              MasterNotFoundError
              138  LOAD_STR                 'No master found for %r'
              140  LOAD_FAST                'service_name'
              142  BUILD_TUPLE_1         1 
              144  BINARY_MODULO    
              146  CALL_FUNCTION_1       1  ''
              148  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_EXCEPT' instruction at offset 54

    def filter_slaves(self, slaves):
        """Remove slaves that are in an ODOWN or SDOWN state"""
        slaves_alive = []
        for slave in slaves:
            if not slave['is_odown']:
                if slave['is_sdown']:
                    pass
                else:
                    slaves_alive.append((slave['ip'], slave['port']))
            return slaves_alive

    def discover_slaves--- This code section failed: ---

 L. 225         0  LOAD_FAST                'self'
                2  LOAD_ATTR                sentinels
                4  GET_ITER         
              6_0  COME_FROM            68  '68'
                6  FOR_ITER             80  'to 80'
                8  STORE_FAST               'sentinel'

 L. 226        10  SETUP_FINALLY        26  'to 26'

 L. 227        12  LOAD_FAST                'sentinel'
               14  LOAD_METHOD              sentinel_slaves
               16  LOAD_FAST                'service_name'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'slaves'
               22  POP_BLOCK        
               24  JUMP_FORWARD         56  'to 56'
             26_0  COME_FROM_FINALLY    10  '10'

 L. 228        26  DUP_TOP          
               28  LOAD_GLOBAL              ConnectionError
               30  LOAD_GLOBAL              ResponseError
               32  LOAD_GLOBAL              TimeoutError
               34  BUILD_TUPLE_3         3 
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    54  'to 54'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 229        46  POP_EXCEPT       
               48  JUMP_BACK             6  'to 6'
               50  POP_EXCEPT       
               52  JUMP_FORWARD         56  'to 56'
             54_0  COME_FROM            38  '38'
               54  END_FINALLY      
             56_0  COME_FROM            52  '52'
             56_1  COME_FROM            24  '24'

 L. 230        56  LOAD_FAST                'self'
               58  LOAD_METHOD              filter_slaves
               60  LOAD_FAST                'slaves'
               62  CALL_METHOD_1         1  ''
               64  STORE_FAST               'slaves'

 L. 231        66  LOAD_FAST                'slaves'
               68  POP_JUMP_IF_FALSE     6  'to 6'

 L. 232        70  LOAD_FAST                'slaves'
               72  ROT_TWO          
               74  POP_TOP          
               76  RETURN_VALUE     
               78  JUMP_BACK             6  'to 6'

 L. 233        80  BUILD_LIST_0          0 
               82  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 50

    def master_for(self, service_name, redis_class=Redis, connection_pool_class=SentinelConnectionPool, **kwargs):
        """
        Returns a redis client instance for the ``service_name`` master.

        A SentinelConnectionPool class is used to retrive the master's
        address before establishing a new connection.

        NOTE: If the master's address has changed, any cached connections to
        the old master are closed.

        By default clients will be a redis.Redis instance. Specify a
        different class to the ``redis_class`` argument if you desire
        something different.

        The ``connection_pool_class`` specifies the connection pool to use.
        The SentinelConnectionPool will be used by default.

        All other keyword arguments are merged with any connection_kwargs
        passed to this class and passed to the connection pool as keyword
        arguments to be used to initialize Redis connections.
        """
        kwargs['is_master'] = True
        connection_kwargs = dict(self.connection_kwargs)
        connection_kwargs.update(kwargs)
        return redis_class(connection_pool=connection_pool_class(
         service_name, self, **connection_kwargs))

    def slave_for(self, service_name, redis_class=Redis, connection_pool_class=SentinelConnectionPool, **kwargs):
        """
        Returns redis client instance for the ``service_name`` slave(s).

        A SentinelConnectionPool class is used to retrive the slave's
        address before establishing a new connection.

        By default clients will be a redis.Redis instance. Specify a
        different class to the ``redis_class`` argument if you desire
        something different.

        The ``connection_pool_class`` specifies the connection pool to use.
        The SentinelConnectionPool will be used by default.

        All other keyword arguments are merged with any connection_kwargs
        passed to this class and passed to the connection pool as keyword
        arguments to be used to initialize Redis connections.
        """
        kwargs['is_master'] = False
        connection_kwargs = dict(self.connection_kwargs)
        connection_kwargs.update(kwargs)
        return redis_class(connection_pool=connection_pool_class(
         service_name, self, **connection_kwargs))
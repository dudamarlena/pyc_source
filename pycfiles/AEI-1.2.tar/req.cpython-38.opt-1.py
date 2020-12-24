# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aehostd/req.py
# Compiled at: 2020-05-12 07:06:59
# Size of source mod 2**32: 4728 bytes
__doc__ = '\naehostd.req - base stuff for processing requests\n'
import logging, inspect, sys
from importlib import import_module
PROTO_VERSION = 2
RES_BEGIN = 1
RES_END = 2

class Request:
    """Request"""
    __slots__ = ('tios', 'server', 'peer', '_log_prefix', '_params')
    rtype = None

    def __init__(self, tios, server, peer):
        self.tios = tios
        self.server = server
        self.peer = peer
        self._log_prefix = self._get_log_prefix()
        self._params = self._read_params()

    def _get_log_prefix(self):
        pid, uid, gid = self.peer
        return 'pid=%d uid=%d gid=%d %s' % (pid, uid, gid, self.__class__.__name__)

    def _get_peer_env--- This code section failed: ---

 L.  59         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                platform
                4  LOAD_STR                 'linux'
                6  COMPARE_OP               !=
                8  POP_JUMP_IF_FALSE    32  'to 32'

 L.  60        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _log

 L.  61        14  LOAD_GLOBAL              logging
               16  LOAD_ATTR                DEBUG

 L.  62        18  LOAD_STR                 'Platform is %r => skip reading peer env'

 L.  63        20  LOAD_GLOBAL              sys
               22  LOAD_ATTR                platform

 L.  60        24  CALL_METHOD_3         3  ''
               26  POP_TOP          

 L.  65        28  BUILD_MAP_0           0 
               30  RETURN_VALUE     
             32_0  COME_FROM             8  '8'

 L.  66        32  LOAD_GLOBAL              set
               34  LOAD_FAST                'names'
               36  JUMP_IF_TRUE_OR_POP    40  'to 40'
               38  BUILD_LIST_0          0 
             40_0  COME_FROM            36  '36'
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'names'

 L.  67        44  LOAD_FAST                'self'
               46  LOAD_ATTR                peer
               48  LOAD_CONST               0
               50  BINARY_SUBSCR    
               52  STORE_FAST               'pid'

 L.  68        54  LOAD_STR                 '/proc/%d/environ'
               56  LOAD_FAST                'pid'
               58  BUILD_TUPLE_1         1 
               60  BINARY_MODULO    
               62  STORE_FAST               'peer_env_filename'

 L.  69        64  SETUP_FINALLY       100  'to 100'

 L.  70        66  LOAD_GLOBAL              open
               68  LOAD_FAST                'peer_env_filename'
               70  LOAD_STR                 'r'
               72  CALL_FUNCTION_2       2  ''
               74  SETUP_WITH           90  'to 90'
               76  STORE_FAST               'env_file'

 L.  71        78  LOAD_FAST                'env_file'
               80  LOAD_METHOD              read
               82  CALL_METHOD_0         0  ''
               84  STORE_FAST               'env_str'
               86  POP_BLOCK        
               88  BEGIN_FINALLY    
             90_0  COME_FROM_WITH       74  '74'
               90  WITH_CLEANUP_START
               92  WITH_CLEANUP_FINISH
               94  END_FINALLY      
               96  POP_BLOCK        
               98  JUMP_FORWARD        160  'to 160'
            100_0  COME_FROM_FINALLY    64  '64'

 L.  72       100  DUP_TOP          
              102  LOAD_GLOBAL              IOError
              104  COMPARE_OP               exception-match
              106  POP_JUMP_IF_FALSE   158  'to 158'
              108  POP_TOP          
              110  STORE_FAST               'err'
              112  POP_TOP          
              114  SETUP_FINALLY       146  'to 146'

 L.  73       116  LOAD_FAST                'self'
              118  LOAD_METHOD              _log

 L.  74       120  LOAD_GLOBAL              logging
              122  LOAD_ATTR                DEBUG

 L.  75       124  LOAD_STR                 'Error reading peer env from %s: %s'

 L.  76       126  LOAD_FAST                'peer_env_filename'

 L.  77       128  LOAD_FAST                'err'

 L.  73       130  CALL_METHOD_4         4  ''
              132  POP_TOP          

 L.  79       134  BUILD_MAP_0           0 
              136  ROT_FOUR         
              138  POP_BLOCK        
              140  POP_EXCEPT       
              142  CALL_FINALLY        146  'to 146'
              144  RETURN_VALUE     
            146_0  COME_FROM           142  '142'
            146_1  COME_FROM_FINALLY   114  '114'
              146  LOAD_CONST               None
              148  STORE_FAST               'err'
              150  DELETE_FAST              'err'
              152  END_FINALLY      
              154  POP_EXCEPT       
              156  JUMP_FORWARD        160  'to 160'
            158_0  COME_FROM           106  '106'
              158  END_FINALLY      
            160_0  COME_FROM           156  '156'
            160_1  COME_FROM            98  '98'

 L.  80       160  BUILD_MAP_0           0 
              162  STORE_FAST               'env'

 L.  81       164  LOAD_FAST                'env_str'
              166  LOAD_METHOD              split
              168  LOAD_STR                 '\x00'
              170  CALL_METHOD_1         1  ''
              172  GET_ITER         
            174_0  COME_FROM           234  '234'
              174  FOR_ITER            246  'to 246'
              176  STORE_FAST               'line'

 L.  82       178  SETUP_FINALLY       200  'to 200'

 L.  83       180  LOAD_FAST                'line'
              182  LOAD_METHOD              split
              184  LOAD_STR                 '='
              186  LOAD_CONST               1
              188  CALL_METHOD_2         2  ''
              190  UNPACK_SEQUENCE_2     2 
              192  STORE_FAST               'name'
              194  STORE_FAST               'val'
              196  POP_BLOCK        
              198  JUMP_FORWARD        224  'to 224'
            200_0  COME_FROM_FINALLY   178  '178'

 L.  84       200  DUP_TOP          
              202  LOAD_GLOBAL              ValueError
              204  COMPARE_OP               exception-match
              206  POP_JUMP_IF_FALSE   222  'to 222'
              208  POP_TOP          
              210  POP_TOP          
              212  POP_TOP          

 L.  85       214  POP_EXCEPT       
              216  JUMP_BACK           174  'to 174'
              218  POP_EXCEPT       
              220  JUMP_FORWARD        224  'to 224'
            222_0  COME_FROM           206  '206'
              222  END_FINALLY      
            224_0  COME_FROM           220  '220'
            224_1  COME_FROM           198  '198'

 L.  86       224  LOAD_FAST                'names'
              226  POP_JUMP_IF_FALSE   236  'to 236'
              228  LOAD_FAST                'name'
              230  LOAD_FAST                'names'
              232  COMPARE_OP               in
              234  POP_JUMP_IF_FALSE   174  'to 174'
            236_0  COME_FROM           226  '226'

 L.  87       236  LOAD_FAST                'val'
              238  LOAD_FAST                'env'
              240  LOAD_FAST                'name'
              242  STORE_SUBSCR     
              244  JUMP_BACK           174  'to 174'

 L.  88       246  LOAD_FAST                'self'
              248  LOAD_METHOD              _log
              250  LOAD_GLOBAL              logging
              252  LOAD_ATTR                DEBUG
              254  LOAD_STR                 'Retrieved peer env vars: %r'
              256  LOAD_FAST                'env'
              258  CALL_METHOD_3         3  ''
              260  POP_TOP          

 L.  89       262  LOAD_FAST                'env'
              264  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 88

    def _log(self, log_level, msg, *args, **kwargs):
        msg = ' '.join(self._log_prefix, msg)
        (logging.log)(log_level, msg, *args, **kwargs)

    def _read_params(self) -> dict:
        """
        Read and return the input params from the input stream
        """
        return dict()

    def get_results(self, params):
        """
        get results for params
        """
        return []

    def write(self, result):
        """
        send result to client
        just a place holder must be over-written by derived classes
        """
        raise RuntimeError('%s.write() must not be directly used!' % (self.__class__.__name__,))

    def process(self):
        """
        This method handles the request based on the params read
        with read_params().
        """
        res_count = 0
        for res in self.get_resultsself._params:
            res_count += 1
            self._loglogging.DEBUG'res#%d: %r'res_countres
            self.tios.write_int32RES_BEGIN
            self.writeres

        if not res_count:
            self._loglogging.DEBUG'no result'
        self.tios.write_int32RES_END

    def log_params(self, log_level):
        if self._params is not None:
            params = dict(self._params)
            for param in ('password', 'oldpassword', 'newpassword'):
                if params.getparam:
                    params[param] = '***'

        self._loglog_level'(%r)'params


def get_handlers(module_name):
    """
    Return a dictionary mapping request types to Request handler classes.
    """
    res = {}
    module = import_module(module_name)
    logging.debug'Inspecting module %s: %s'module_namemodule
    for _, cls in inspect.getmembersmoduleinspect.isclass:
        if issubclass(cls, Request) and hasattr(cls, 'rtype') and cls.rtype is not None:
            res[cls.rtype] = cls
        logging.debug'Registered %d request classes in module %s: %s'len(res)module_name', '.join[cls.__name__ for cls in res.values()]
        return res
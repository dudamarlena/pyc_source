# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /aehostd/req.py
# Compiled at: 2020-03-29 09:12:30
# Size of source mod 2**32: 4272 bytes
"""
aehostd.req - base stuff for processing requests
"""
from __future__ import absolute_import
import logging, inspect, sys
from importlib import import_module
PROTO_VERSION = 2
RES_BEGIN = 1
RES_END = 2

class Request:
    __doc__ = '\n    Request handler class. Subclasses are expected to handle actual requests\n    and should implement the following members:\n\n      rtype - the request type handled by a class\n\n      read_params() - a function that reads the request params of the\n                          request stream\n      write() - function that writes a single LDAP entry to the result stream\n\n    '
    rtype = None

    def __init__(self, tios, server, peer):
        self.tios = tios
        self.server = server
        self.peer = peer
        self._log_prefix = self._get_log_prefix()
        self.search = getattr(sys.modules[self.__module__], 'Search', None)
        self._params = self._read_params()

    def _get_log_prefix(self):
        pid, uid, gid = self.peer
        return 'pid=%d uid=%d gid=%d %s' % (pid, uid, gid, self.__class__.__name__)

    def _get_peer_env--- This code section failed: ---

 L.  55         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                platform
                4  LOAD_STR                 'linux'
                6  COMPARE_OP               !=
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L.  56        10  BUILD_MAP_0           0 
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L.  57        14  LOAD_GLOBAL              set
               16  LOAD_FAST                'names'
               18  JUMP_IF_TRUE_OR_POP    22  'to 22'
               20  BUILD_LIST_0          0 
             22_0  COME_FROM            18  '18'
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'names'

 L.  58        26  LOAD_FAST                'self'
               28  LOAD_ATTR                peer
               30  LOAD_CONST               0
               32  BINARY_SUBSCR    
               34  STORE_FAST               'pid'

 L.  59        36  SETUP_FINALLY        78  'to 78'

 L.  60        38  LOAD_GLOBAL              open
               40  LOAD_STR                 '/proc/%d/environ'
               42  LOAD_FAST                'pid'
               44  BUILD_TUPLE_1         1 
               46  BINARY_MODULO    
               48  LOAD_STR                 'r'
               50  CALL_FUNCTION_2       2  ''
               52  SETUP_WITH           68  'to 68'
               54  STORE_FAST               'env_file'

 L.  61        56  LOAD_FAST                'env_file'
               58  LOAD_METHOD              read
               60  CALL_METHOD_0         0  ''
               62  STORE_FAST               'env_str'
               64  POP_BLOCK        
               66  BEGIN_FINALLY    
             68_0  COME_FROM_WITH       52  '52'
               68  WITH_CLEANUP_START
               70  WITH_CLEANUP_FINISH
               72  END_FINALLY      
               74  POP_BLOCK        
               76  JUMP_FORWARD        102  'to 102'
             78_0  COME_FROM_FINALLY    36  '36'

 L.  62        78  DUP_TOP          
               80  LOAD_GLOBAL              IOError
               82  COMPARE_OP               exception-match
               84  POP_JUMP_IF_FALSE   100  'to 100'
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L.  63        92  BUILD_MAP_0           0 
               94  ROT_FOUR         
               96  POP_EXCEPT       
               98  RETURN_VALUE     
            100_0  COME_FROM            84  '84'
              100  END_FINALLY      
            102_0  COME_FROM            76  '76'

 L.  64       102  BUILD_MAP_0           0 
              104  STORE_FAST               'env'

 L.  65       106  LOAD_FAST                'env_str'
              108  LOAD_METHOD              split
              110  LOAD_STR                 '\x00'
              112  CALL_METHOD_1         1  ''
              114  GET_ITER         
            116_0  COME_FROM           176  '176'
              116  FOR_ITER            188  'to 188'
              118  STORE_FAST               'line'

 L.  66       120  SETUP_FINALLY       142  'to 142'

 L.  67       122  LOAD_FAST                'line'
              124  LOAD_METHOD              split
              126  LOAD_STR                 '='
              128  LOAD_CONST               1
              130  CALL_METHOD_2         2  ''
              132  UNPACK_SEQUENCE_2     2 
              134  STORE_FAST               'name'
              136  STORE_FAST               'val'
              138  POP_BLOCK        
              140  JUMP_FORWARD        166  'to 166'
            142_0  COME_FROM_FINALLY   120  '120'

 L.  68       142  DUP_TOP          
              144  LOAD_GLOBAL              ValueError
              146  COMPARE_OP               exception-match
              148  POP_JUMP_IF_FALSE   164  'to 164'
              150  POP_TOP          
              152  POP_TOP          
              154  POP_TOP          

 L.  69       156  POP_EXCEPT       
              158  JUMP_BACK           116  'to 116'
              160  POP_EXCEPT       
              162  JUMP_FORWARD        166  'to 166'
            164_0  COME_FROM           148  '148'
              164  END_FINALLY      
            166_0  COME_FROM           162  '162'
            166_1  COME_FROM           140  '140'

 L.  70       166  LOAD_FAST                'names'
              168  POP_JUMP_IF_FALSE   178  'to 178'
              170  LOAD_FAST                'name'
              172  LOAD_FAST                'names'
              174  COMPARE_OP               in
              176  POP_JUMP_IF_FALSE   116  'to 116'
            178_0  COME_FROM           168  '168'

 L.  71       178  LOAD_FAST                'val'
              180  LOAD_FAST                'env'
              182  LOAD_FAST                'name'
              184  STORE_SUBSCR     
              186  JUMP_BACK           116  'to 116'

 L.  72       188  LOAD_FAST                'env'
              190  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 160

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
            self._log(logging.DEBUG, 'res#%d: %r', res_count, res)
            self.tios.write_int32RES_BEGIN
            self.writeres
        else:
            if not res_count:
                self._loglogging.DEBUG'no result'
            self.tios.write_int32RES_END

    def log_params(self, log_level):
        if self._params is not None:
            params = dict(self._params)
            for param in ('password', 'oldpassword', 'newpassword'):
                if params.getparam:
                    params[param] = '***'

        self._log(log_level, '(%r)', params)


def get_handlers(module_name):
    """
    Return a dictionary mapping request types to Request handler classes.
    """
    res = {}
    module = import_module(module_name)
    logging.debug('Inspecting module %s: %s', module_name, module)
    for _, cls in inspect.getmembersmoduleinspect.isclass:
        if issubclass(cls, Request) and hasattr(cls, 'rtype') and cls.rtype is not None:
            res[cls.rtype] = cls
        logging.debug('Registered %d request classes in module %s: %s', len(res), module_name, ', '.join[cls.__name__ for cls in res.values()])
        return res
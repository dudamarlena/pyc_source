# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\utils\update_checker.py
# Compiled at: 2020-03-23 16:33:38
# Size of source mod 2**32: 1088 bytes
import logging
from distutils.version import StrictVersion
import requests
from assets.version import get_value
from core.display import new_version_news
logger = logging.Logger('UPDATE_CHECK')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'

def check_updates--- This code section failed: ---

 L.  16         0  SETUP_EXCEPT        118  'to 118'

 L.  17         2  LOAD_GLOBAL              logger
                4  LOAD_METHOD              info
                6  LOAD_STR                 'Checking latest version'
                8  CALL_METHOD_1         1  '1 positional argument'
               10  POP_TOP          

 L.  19        12  LOAD_GLOBAL              StrictVersion
               14  LOAD_GLOBAL              get_value
               16  CALL_FUNCTION_0       0  '0 positional arguments'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  STORE_FAST               'current_version'

 L.  21        22  LOAD_STR                 'http://bit.ly/2yYyFGd'
               24  STORE_FAST               'pypi_short_url'

 L.  22        26  LOAD_STR                 'User-Agent'
               28  LOAD_GLOBAL              user_agent
               30  BUILD_MAP_1           1 
               32  STORE_FAST               'headers'

 L.  23        34  LOAD_GLOBAL              requests
               36  LOAD_ATTR                get
               38  LOAD_FAST                'pypi_short_url'
               40  LOAD_FAST                'headers'
               42  LOAD_CONST               3
               44  LOAD_CONST               ('headers', 'timeout')
               46  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               48  STORE_FAST               'res'

 L.  24        50  LOAD_GLOBAL              StrictVersion
               52  LOAD_FAST                'res'
               54  LOAD_METHOD              json
               56  CALL_METHOD_0         0  '0 positional arguments'
               58  LOAD_STR                 'info'
               60  BINARY_SUBSCR    
               62  LOAD_STR                 'version'
               64  BINARY_SUBSCR    
               66  CALL_FUNCTION_1       1  '1 positional argument'
               68  STORE_FAST               'latest_version'

 L.  26        70  LOAD_FAST                'current_version'
               72  LOAD_FAST                'latest_version'
               74  COMPARE_OP               <
               76  POP_JUMP_IF_FALSE    92  'to 92'

 L.  27        78  LOAD_GLOBAL              new_version_news
               80  LOAD_GLOBAL              str
               82  LOAD_FAST                'latest_version'
               84  CALL_FUNCTION_1       1  '1 positional argument'
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  POP_TOP          
               90  JUMP_FORWARD        114  'to 114'
             92_0  COME_FROM            76  '76'

 L.  28        92  LOAD_FAST                'current_version'
               94  LOAD_FAST                'latest_version'
               96  COMPARE_OP               >
               98  POP_JUMP_IF_FALSE   114  'to 114'

 L.  29       100  LOAD_GLOBAL              new_version_news
              102  LOAD_GLOBAL              str
              104  LOAD_FAST                'latest_version'
              106  CALL_FUNCTION_1       1  '1 positional argument'
              108  CALL_FUNCTION_1       1  '1 positional argument'
              110  POP_TOP          
              112  JUMP_FORWARD        114  'to 114'
            114_0  COME_FROM           112  '112'
            114_1  COME_FROM            98  '98'
            114_2  COME_FROM            90  '90'

 L.  31       114  POP_BLOCK        
              116  JUMP_FORWARD        162  'to 162'
            118_0  COME_FROM_EXCEPT      0  '0'

 L.  33       118  DUP_TOP          
              120  LOAD_GLOBAL              Exception
              122  COMPARE_OP               exception-match
              124  POP_JUMP_IF_FALSE   160  'to 160'
              126  POP_TOP          
              128  STORE_FAST               'ex'
              130  POP_TOP          
              132  SETUP_FINALLY       148  'to 148'

 L.  34       134  LOAD_GLOBAL              logger
              136  LOAD_METHOD              exception
              138  LOAD_STR                 'Failed to check for update'
              140  CALL_METHOD_1         1  '1 positional argument'
              142  POP_TOP          
              144  POP_BLOCK        
              146  LOAD_CONST               None
            148_0  COME_FROM_FINALLY   132  '132'
              148  LOAD_CONST               None
              150  STORE_FAST               'ex'
              152  DELETE_FAST              'ex'
              154  END_FINALLY      
              156  POP_EXCEPT       
              158  JUMP_FORWARD        162  'to 162'
            160_0  COME_FROM           124  '124'
              160  END_FINALLY      
            162_0  COME_FROM           158  '158'
            162_1  COME_FROM           116  '116'

Parse error at or near `POP_BLOCK' instruction at offset 114
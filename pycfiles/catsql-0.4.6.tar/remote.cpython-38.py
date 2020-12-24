# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__QTYPES__/pythoncode/__SANDBOXES__/remote.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 1560 bytes
import json, urllib.request, urllib.parse, urllib.error
SANDBOX_URL = 'https://catsoop.org/python_sandbox_v2019.9/'

def run_code--- This code section failed: ---

 L.  31         0  LOAD_FAST                'code'
                2  LOAD_METHOD              replace
                4  LOAD_STR                 '\r\n'
                6  LOAD_STR                 '\n'
                8  CALL_METHOD_2         2  ''
               10  STORE_FAST               'code'

 L.  32        12  LOAD_GLOBAL              urllib
               14  LOAD_ATTR                parse
               16  LOAD_METHOD              urlencode

 L.  33        18  LOAD_FAST                'code'
               20  LOAD_FAST                'result_as_string'
               22  LOAD_CONST               ('code', 'result_as_string')
               24  BUILD_CONST_KEY_MAP_2     2 

 L.  32        26  CALL_METHOD_1         1  ''
               28  LOAD_METHOD              encode
               30  CALL_METHOD_0         0  ''
               32  STORE_FAST               'data'

 L.  35        34  LOAD_GLOBAL              urllib
               36  LOAD_ATTR                request
               38  LOAD_METHOD              Request
               40  LOAD_FAST                'context'
               42  LOAD_METHOD              get
               44  LOAD_STR                 'csq_sandbox_url'
               46  LOAD_GLOBAL              SANDBOX_URL
               48  CALL_METHOD_2         2  ''
               50  LOAD_FAST                'data'
               52  CALL_METHOD_2         2  ''
               54  STORE_FAST               'request'

 L.  36        56  SETUP_FINALLY        92  'to 92'

 L.  37        58  LOAD_GLOBAL              urllib
               60  LOAD_ATTR                request
               62  LOAD_METHOD              urlopen
               64  LOAD_FAST                'request'
               66  LOAD_FAST                'data'
               68  CALL_METHOD_2         2  ''
               70  LOAD_METHOD              read
               72  CALL_METHOD_0         0  ''
               74  STORE_FAST               'resp'

 L.  38        76  LOAD_GLOBAL              json
               78  LOAD_METHOD              loads
               80  LOAD_FAST                'resp'
               82  LOAD_METHOD              decode
               84  CALL_METHOD_0         0  ''
               86  CALL_METHOD_1         1  ''
               88  POP_BLOCK        
               90  RETURN_VALUE     
             92_0  COME_FROM_FINALLY    56  '56'

 L.  39        92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L.  40        98  LOAD_STR                 'CAT-SOOP: Could not connect to %s'
              100  LOAD_FAST                'context'
              102  LOAD_METHOD              get

 L.  41       104  LOAD_STR                 'csq_sandbox_url'

 L.  41       106  LOAD_GLOBAL              SANDBOX_URL

 L.  40       108  CALL_METHOD_2         2  ''
              110  BINARY_MODULO    
              112  STORE_FAST               'err'

 L.  43       114  LOAD_STR                 ''
              116  LOAD_STR                 ''
              118  LOAD_FAST                'err'
              120  BUILD_MAP_0           0 
              122  LOAD_CONST               ('fname', 'out', 'err', 'info')
              124  BUILD_CONST_KEY_MAP_4     4 
              126  ROT_FOUR         
              128  POP_EXCEPT       
              130  RETURN_VALUE     
              132  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 90
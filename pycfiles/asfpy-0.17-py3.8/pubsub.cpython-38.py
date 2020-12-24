# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asfpy/pubsub.py
# Compiled at: 2020-05-02 20:23:05
# Size of source mod 2**32: 2798 bytes
""" PyPubSub listener class. """
import urllib.request, json, time, sys

class Listener:
    __doc__ = ' Generic listener for pubsubs. Grabs each payload and runs process() on them. '

    def __init__(self, url):
        self.url = url

    def attach--- This code section failed: ---
              0_0  COME_FROM           228  '228'

 L.  31         0  LOAD_FAST                'debug'
                2  POP_JUMP_IF_FALSE    18  'to 18'

 L.  32         4  LOAD_GLOBAL              print
                6  LOAD_STR                 '[INFO] Subscribing to stream at %s'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                url
               12  BINARY_MODULO    
               14  CALL_FUNCTION_1       1  ''
               16  POP_TOP          
             18_0  COME_FROM             2  '2'

 L.  33        18  LOAD_CONST               None
               20  LOAD_FAST                'self'
               22  STORE_ATTR               connection

 L.  34        24  LOAD_FAST                'self'
               26  LOAD_ATTR                connection
               28  POP_JUMP_IF_TRUE    114  'to 114'

 L.  35        30  SETUP_FINALLY        68  'to 68'

 L.  36        32  LOAD_GLOBAL              urllib
               34  LOAD_ATTR                request
               36  LOAD_METHOD              urlopen
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                url
               42  LOAD_CONST               None
               44  LOAD_CONST               30
               46  CALL_METHOD_3         3  ''
               48  LOAD_FAST                'self'
               50  STORE_ATTR               connection

 L.  37        52  LOAD_FAST                'debug'
               54  POP_JUMP_IF_FALSE    64  'to 64'

 L.  38        56  LOAD_GLOBAL              print
               58  LOAD_STR                 '[INFO] Subscribed, reading stream'
               60  CALL_FUNCTION_1       1  ''
               62  POP_TOP          
             64_0  COME_FROM            54  '54'
               64  POP_BLOCK        
               66  JUMP_BACK            24  'to 24'
             68_0  COME_FROM_FINALLY    30  '30'

 L.  39        68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L.  40        74  LOAD_GLOBAL              sys
               76  LOAD_ATTR                stderr
               78  LOAD_METHOD              write
               80  LOAD_STR                 '[WARNING] Could not connect to pubsub service at %s, retrying in 10s...\n'
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                url
               86  BINARY_MODULO    
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          

 L.  41        92  LOAD_GLOBAL              time
               94  LOAD_METHOD              sleep
               96  LOAD_CONST               10
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          

 L.  42       102  POP_EXCEPT       
              104  JUMP_BACK            24  'to 24'
              106  POP_EXCEPT       
              108  JUMP_BACK            24  'to 24'
              110  END_FINALLY      
              112  JUMP_BACK            24  'to 24'
            114_0  COME_FROM            28  '28'

 L.  43       114  LOAD_FAST                'self'
              116  LOAD_METHOD              read_payload
              118  CALL_METHOD_0         0  ''
              120  GET_ITER         
              122  FOR_ITER            226  'to 226'
              124  STORE_FAST               'payload'

 L.  44       126  SETUP_FINALLY       162  'to 162'

 L.  45       128  LOAD_FAST                'raw'
              130  LOAD_CONST               False
              132  COMPARE_OP               ==
              134  POP_JUMP_IF_FALSE   146  'to 146'

 L.  46       136  LOAD_FAST                'payload'
              138  LOAD_METHOD              get
              140  LOAD_STR                 'payload'
              142  CALL_METHOD_1         1  ''
              144  STORE_FAST               'payload'
            146_0  COME_FROM           134  '134'

 L.  47       146  LOAD_FAST                'payload'
              148  POP_JUMP_IF_FALSE   158  'to 158'

 L.  48       150  LOAD_FAST                'func'
              152  LOAD_FAST                'payload'
              154  CALL_FUNCTION_1       1  ''
              156  POP_TOP          
            158_0  COME_FROM           148  '148'
              158  POP_BLOCK        
              160  JUMP_BACK           122  'to 122'
            162_0  COME_FROM_FINALLY   126  '126'

 L.  49       162  DUP_TOP          
              164  LOAD_GLOBAL              ValueError
              166  COMPARE_OP               exception-match
              168  POP_JUMP_IF_FALSE   222  'to 222'
              170  POP_TOP          
              172  STORE_FAST               'detail'
              174  POP_TOP          
              176  SETUP_FINALLY       210  'to 210'

 L.  50       178  LOAD_FAST                'debug'
              180  POP_JUMP_IF_FALSE   198  'to 198'

 L.  51       182  LOAD_GLOBAL              sys
              184  LOAD_ATTR                stderr
              186  LOAD_METHOD              write
              188  LOAD_STR                 '[WARNING] Bad JSON or something: %s\n'
              190  LOAD_FAST                'detail'
              192  BINARY_MODULO    
              194  CALL_METHOD_1         1  ''
              196  POP_TOP          
            198_0  COME_FROM           180  '180'

 L.  52       198  POP_BLOCK        
              200  POP_EXCEPT       
              202  CALL_FINALLY        210  'to 210'
              204  JUMP_BACK           122  'to 122'
              206  POP_BLOCK        
              208  BEGIN_FINALLY    
            210_0  COME_FROM           202  '202'
            210_1  COME_FROM_FINALLY   176  '176'
              210  LOAD_CONST               None
              212  STORE_FAST               'detail'
              214  DELETE_FAST              'detail'
              216  END_FINALLY      
              218  POP_EXCEPT       
              220  JUMP_BACK           122  'to 122'
            222_0  COME_FROM           168  '168'
              222  END_FINALLY      
              224  JUMP_BACK           122  'to 122'

 L.  53       226  LOAD_FAST                'debug'
              228  POP_JUMP_IF_FALSE     0  'to 0'

 L.  54       230  LOAD_GLOBAL              sys
              232  LOAD_ATTR                stderr
              234  LOAD_METHOD              write
              236  LOAD_STR                 '[WARNING] Disconnected from %s, reconnecting\n'
              238  LOAD_FAST                'self'
              240  LOAD_ATTR                url
              242  BINARY_MODULO    
              244  CALL_METHOD_1         1  ''
              246  POP_TOP          
              248  JUMP_BACK             0  'to 0'

Parse error at or near `POP_EXCEPT' instruction at offset 106

    def read_payload--- This code section failed: ---

 L.  59         0  SETUP_FINALLY        66  'to 66'

 L.  60         2  LOAD_FAST                'self'
                4  LOAD_ATTR                connection
                6  LOAD_METHOD              readline
                8  CALL_METHOD_0         0  ''
               10  LOAD_METHOD              strip
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'line'

 L.  61        16  LOAD_FAST                'line'
               18  POP_JUMP_IF_FALSE    58  'to 58'

 L.  62        20  LOAD_GLOBAL              json
               22  LOAD_METHOD              loads
               24  LOAD_FAST                'line'
               26  LOAD_ATTR                decode
               28  LOAD_STR                 'utf-8'
               30  LOAD_STR                 'ignore'
               32  LOAD_CONST               ('errors',)
               34  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               36  LOAD_METHOD              rstrip
               38  LOAD_STR                 '\r\n,'
               40  CALL_METHOD_1         1  ''
               42  LOAD_METHOD              replace
               44  LOAD_STR                 '\x00'
               46  LOAD_STR                 ''
               48  CALL_METHOD_2         2  ''
               50  CALL_METHOD_1         1  ''
               52  YIELD_VALUE      
               54  POP_TOP          
               56  JUMP_FORWARD         62  'to 62'
             58_0  COME_FROM            18  '18'

 L.  64        58  POP_BLOCK        
               60  BREAK_LOOP          122  'to 122'
             62_0  COME_FROM            56  '56'
               62  POP_BLOCK        
               64  JUMP_BACK             0  'to 0'
             66_0  COME_FROM_FINALLY     0  '0'

 L.  65        66  DUP_TOP          
               68  LOAD_GLOBAL              Exception
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE   118  'to 118'
               74  POP_TOP          
               76  STORE_FAST               'info'
               78  POP_TOP          
               80  SETUP_FINALLY       106  'to 106'

 L.  66        82  LOAD_GLOBAL              print
               84  LOAD_STR                 '[ERROR] Error reading from stream: %s'
               86  LOAD_FAST                'info'
               88  BINARY_MODULO    
               90  CALL_FUNCTION_1       1  ''
               92  POP_TOP          

 L.  67        94  POP_BLOCK        
               96  POP_EXCEPT       
               98  CALL_FINALLY        106  'to 106'
              100  BREAK_LOOP          122  'to 122'
              102  POP_BLOCK        
              104  BEGIN_FINALLY    
            106_0  COME_FROM            98  '98'
            106_1  COME_FROM_FINALLY    80  '80'
              106  LOAD_CONST               None
              108  STORE_FAST               'info'
              110  DELETE_FAST              'info'
              112  END_FINALLY      
              114  POP_EXCEPT       
              116  JUMP_BACK             0  'to 0'
            118_0  COME_FROM            72  '72'
              118  END_FINALLY      
              120  JUMP_BACK             0  'to 0'

Parse error at or near `CALL_FINALLY' instruction at offset 98
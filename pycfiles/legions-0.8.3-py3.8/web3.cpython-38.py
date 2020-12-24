# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/legions/network/web3.py
# Compiled at: 2020-05-07 10:49:55
# Size of source mod 2**32: 1032 bytes
import os
from web3 import Web3 as _web3
from web3 import IPCProvider, HTTPProvider, WebsocketProvider

class Web3(_web3):
    __doc__ = '\n    Web3 class\n    '

    def __init__(self):
        self.node_uri = None
        super().__init__(HTTPProvider('null'))

    def connect--- This code section failed: ---

 L.  18         0  LOAD_FAST                'node'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               node_uri

 L.  20         6  SETUP_FINALLY        40  'to 40'

 L.  21         8  LOAD_GLOBAL              os
               10  LOAD_ATTR                path
               12  LOAD_METHOD              exists
               14  LOAD_FAST                'node'
               16  CALL_METHOD_1         1  ''
               18  POP_JUMP_IF_FALSE    36  'to 36'

 L.  22        20  LOAD_GLOBAL              IPCProvider
               22  LOAD_FAST                'node'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_FAST                'self'
               28  STORE_ATTR               provider

 L.  23        30  POP_BLOCK        
               32  LOAD_CONST               None
               34  RETURN_VALUE     
             36_0  COME_FROM            18  '18'
               36  POP_BLOCK        
               38  JUMP_FORWARD         60  'to 60'
             40_0  COME_FROM_FINALLY     6  '6'

 L.  24        40  DUP_TOP          
               42  LOAD_GLOBAL              OSError
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    58  'to 58'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L.  25        54  POP_EXCEPT       
               56  JUMP_FORWARD         60  'to 60'
             58_0  COME_FROM            46  '46'
               58  END_FINALLY      
             60_0  COME_FROM            56  '56'
             60_1  COME_FROM            38  '38'

 L.  27        60  LOAD_FAST                'node'
               62  LOAD_METHOD              startswith
               64  LOAD_STR                 'https://'
               66  CALL_METHOD_1         1  ''
               68  POP_JUMP_IF_TRUE     80  'to 80'
               70  LOAD_FAST                'node'
               72  LOAD_METHOD              startswith
               74  LOAD_STR                 'http://'
               76  CALL_METHOD_1         1  ''
               78  POP_JUMP_IF_FALSE   100  'to 100'
             80_0  COME_FROM            68  '68'

 L.  28        80  LOAD_GLOBAL              HTTPProvider
               82  LOAD_FAST                'node'
               84  LOAD_STR                 'timeout'
               86  LOAD_FAST                'timeout'
               88  BUILD_MAP_1           1 
               90  LOAD_CONST               ('request_kwargs',)
               92  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               94  LOAD_FAST                'self'
               96  STORE_ATTR               provider
               98  JUMP_FORWARD        138  'to 138'
            100_0  COME_FROM            78  '78'

 L.  29       100  LOAD_FAST                'node'
              102  LOAD_METHOD              startswith
              104  LOAD_STR                 'ws://'
              106  CALL_METHOD_1         1  ''
              108  POP_JUMP_IF_FALSE   130  'to 130'

 L.  30       110  LOAD_GLOBAL              WebsocketProvider

 L.  31       112  LOAD_FAST                'node'

 L.  31       114  LOAD_STR                 'timeout'
              116  LOAD_FAST                'timeout'
              118  BUILD_MAP_1           1 

 L.  30       120  LOAD_CONST               ('websocket_kwargs',)
              122  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              124  LOAD_FAST                'self'
              126  STORE_ATTR               provider
              128  JUMP_FORWARD        138  'to 138'
            130_0  COME_FROM           108  '108'

 L.  34       130  LOAD_GLOBAL              ValueError

 L.  35       132  LOAD_STR                 "The provided node is not valid. It must start with 'http://' or 'https://' or 'ws://' or a path to an IPC socket file."

 L.  34       134  CALL_FUNCTION_1       1  ''
              136  RAISE_VARARGS_1       1  'exception instance'
            138_0  COME_FROM           128  '128'
            138_1  COME_FROM            98  '98'

Parse error at or near `LOAD_CONST' instruction at offset 32
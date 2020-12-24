# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/legions/utils/helper_functions.py
# Compiled at: 2020-05-07 10:49:55
# Size of source mod 2**32: 935 bytes
import requests, json, os
from termcolor import cprint
ChainID_JSON = 'chains.json'

def checkConnection(url, verbose=None):
    r = requests.get(url, timeout=5)
    if verbose:
        cprint('Status Code: {}'.format(r.status_code), 'grey')
        cprint('Response: {}'.format(r.text), 'grey')
    if r.status_code not in (400, 404, 503):
        return True
    return False


def getChainName--- This code section failed: ---

 L.  25         0  SETUP_FINALLY       102  'to 102'

 L.  26         2  LOAD_GLOBAL              open
                4  LOAD_GLOBAL              os
                6  LOAD_ATTR                path
                8  LOAD_METHOD              join
               10  LOAD_GLOBAL              os
               12  LOAD_ATTR                path
               14  LOAD_METHOD              dirname
               16  LOAD_GLOBAL              __file__
               18  CALL_METHOD_1         1  ''
               20  LOAD_FAST                'json_file'
               22  CALL_METHOD_2         2  ''
               24  LOAD_STR                 'r'
               26  CALL_FUNCTION_2       2  ''
               28  SETUP_WITH           46  'to 46'
               30  STORE_FAST               'f'

 L.  27        32  LOAD_GLOBAL              json
               34  LOAD_METHOD              load
               36  LOAD_FAST                'f'
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'chains_dict'
               42  POP_BLOCK        
               44  BEGIN_FINALLY    
             46_0  COME_FROM_WITH       28  '28'
               46  WITH_CLEANUP_START
               48  WITH_CLEANUP_FINISH
               50  END_FINALLY      

 L.  28        52  LOAD_FAST                'chains_dict'
               54  GET_ITER         
             56_0  COME_FROM            78  '78'
               56  FOR_ITER             98  'to 98'
               58  STORE_FAST               'chain'

 L.  29        60  LOAD_GLOBAL              print
               62  POP_TOP          

 L.  30        64  LOAD_FAST                'chain'
               66  LOAD_METHOD              get
               68  LOAD_STR                 'chainId'
               70  LOAD_CONST               None
               72  CALL_METHOD_2         2  ''
               74  LOAD_FAST                'ChainID'
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE    56  'to 56'

 L.  31        80  LOAD_FAST                'chain'
               82  LOAD_METHOD              get
               84  LOAD_STR                 'name'
               86  CALL_METHOD_1         1  ''
               88  ROT_TWO          
               90  POP_TOP          
               92  POP_BLOCK        
               94  RETURN_VALUE     
               96  JUMP_BACK            56  'to 56'
               98  POP_BLOCK        
              100  JUMP_FORWARD        158  'to 158'
            102_0  COME_FROM_FINALLY     0  '0'

 L.  32       102  DUP_TOP          
              104  LOAD_GLOBAL              Exception
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   156  'to 156'
              110  POP_TOP          
              112  STORE_FAST               'e'
              114  POP_TOP          
              116  SETUP_FINALLY       144  'to 144'

 L.  33       118  LOAD_GLOBAL              print
              120  LOAD_STR                 'Failed to find the chainID for {} - {}'
              122  LOAD_METHOD              format
              124  LOAD_FAST                'ChainID'
              126  LOAD_FAST                'e'
              128  CALL_METHOD_2         2  ''
              130  CALL_FUNCTION_1       1  ''
              132  POP_TOP          

 L.  34       134  POP_BLOCK        
              136  POP_EXCEPT       
              138  CALL_FINALLY        144  'to 144'
              140  LOAD_STR                 ''
              142  RETURN_VALUE     
            144_0  COME_FROM           138  '138'
            144_1  COME_FROM_FINALLY   116  '116'
              144  LOAD_CONST               None
              146  STORE_FAST               'e'
              148  DELETE_FAST              'e'
              150  END_FINALLY      
              152  POP_EXCEPT       
              154  JUMP_FORWARD        158  'to 158'
            156_0  COME_FROM           108  '108'
              156  END_FINALLY      
            158_0  COME_FROM           154  '154'
            158_1  COME_FROM           100  '100'

Parse error at or near `POP_BLOCK' instruction at offset 92
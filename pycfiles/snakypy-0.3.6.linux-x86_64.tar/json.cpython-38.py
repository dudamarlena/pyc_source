# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wc4nin/.cache/pypoetry/virtualenvs/snakypy-Jn9yRLD4-py3.8/lib/python3.8/site-packages/snakypy/json.py
# Compiled at: 2020-04-02 13:03:18
# Size of source mod 2**32: 3167 bytes
import json
from os.path import exists

def read--- This code section failed: ---

 L.  20         0  SETUP_FINALLY        38  'to 38'

 L.  21         2  LOAD_GLOBAL              open
                4  LOAD_FAST                'file_path'
                6  CALL_FUNCTION_1       1  ''
                8  SETUP_WITH           26  'to 26'
               10  STORE_FAST               'f'

 L.  22        12  LOAD_GLOBAL              json
               14  LOAD_METHOD              load
               16  LOAD_FAST                'f'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'data'
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH        8  '8'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      

 L.  23        32  LOAD_FAST                'data'
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY     0  '0'

 L.  24        38  DUP_TOP          
               40  LOAD_GLOBAL              FileNotFoundError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    84  'to 84'
               46  POP_TOP          
               48  STORE_FAST               'err'
               50  POP_TOP          
               52  SETUP_FINALLY        72  'to 72'

 L.  25        54  LOAD_GLOBAL              FileNotFoundError
               56  LOAD_STR                 '>>> File not found '
               58  LOAD_FAST                'err'
               60  FORMAT_VALUE          0  ''
               62  BUILD_STRING_2        2 
               64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
               68  POP_BLOCK        
               70  BEGIN_FINALLY    
             72_0  COME_FROM_FINALLY    52  '52'
               72  LOAD_CONST               None
               74  STORE_FAST               'err'
               76  DELETE_FAST              'err'
               78  END_FINALLY      
               80  POP_EXCEPT       
               82  JUMP_FORWARD        168  'to 168'
             84_0  COME_FROM            44  '44'

 L.  26        84  DUP_TOP          
               86  LOAD_GLOBAL              json
               88  LOAD_ATTR                decoder
               90  LOAD_ATTR                JSONDecodeError
               92  COMPARE_OP               exception-match
               94  POP_JUMP_IF_FALSE   134  'to 134'
               96  POP_TOP          
               98  STORE_FAST               'err_j'
              100  POP_TOP          
              102  SETUP_FINALLY       122  'to 122'

 L.  27       104  LOAD_GLOBAL              Exception
              106  LOAD_STR                 '>>> Incorrect Json file structure: '
              108  LOAD_FAST                'file_path'
              110  FORMAT_VALUE          0  ''
              112  BUILD_STRING_2        2 
              114  CALL_FUNCTION_1       1  ''
              116  RAISE_VARARGS_1       1  'exception instance'
              118  POP_BLOCK        
              120  BEGIN_FINALLY    
            122_0  COME_FROM_FINALLY   102  '102'
              122  LOAD_CONST               None
              124  STORE_FAST               'err_j'
              126  DELETE_FAST              'err_j'
              128  END_FINALLY      
              130  POP_EXCEPT       
              132  JUMP_FORWARD        168  'to 168'
            134_0  COME_FROM            94  '94'

 L.  28       134  DUP_TOP          
              136  LOAD_GLOBAL              Exception
              138  COMPARE_OP               exception-match
              140  POP_JUMP_IF_FALSE   166  'to 166'
              142  POP_TOP          
              144  POP_TOP          
              146  POP_TOP          

 L.  29       148  LOAD_GLOBAL              Exception
              150  LOAD_STR                 '>>> There was an error reading the file: '
              152  LOAD_FAST                'file_path'
              154  FORMAT_VALUE          0  ''
              156  BUILD_STRING_2        2 
              158  CALL_FUNCTION_1       1  ''
              160  RAISE_VARARGS_1       1  'exception instance'
              162  POP_EXCEPT       
              164  JUMP_FORWARD        168  'to 168'
            166_0  COME_FROM           140  '140'
              166  END_FINALLY      
            168_0  COME_FROM           164  '164'
            168_1  COME_FROM           132  '132'
            168_2  COME_FROM            82  '82'

Parse error at or near `DUP_TOP' instruction at offset 84


def create--- This code section failed: ---

 L.  53         0  LOAD_CONST               0
                2  LOAD_CONST               ('splitext',)
                4  IMPORT_NAME_ATTR         os.path
                6  IMPORT_FROM              splitext
                8  STORE_FAST               'splitext'
               10  POP_TOP          

 L.  55        12  LOAD_FAST                'splitext'
               14  LOAD_FAST                'file_path'
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_CONST               1
               20  BINARY_SUBSCR    
               22  LOAD_STR                 '.json'
               24  COMPARE_OP               !=
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L.  56        28  LOAD_GLOBAL              Exception
               30  LOAD_STR                 'The JSON file extension was not explicit.'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L.  57        36  LOAD_FAST                'force'
               38  POP_JUMP_IF_TRUE     66  'to 66'
               40  LOAD_GLOBAL              exists
               42  LOAD_FAST                'file_path'
               44  CALL_FUNCTION_1       1  ''
               46  POP_JUMP_IF_FALSE    66  'to 66'

 L.  58        48  LOAD_GLOBAL              FileExistsError

 L.  59        50  LOAD_STR                 '>>> The file '
               52  LOAD_FAST                'file_path'
               54  FORMAT_VALUE          0  ''
               56  LOAD_STR                 ' already exists, use force=True.'
               58  BUILD_STRING_3        3 

 L.  58        60  CALL_FUNCTION_1       1  ''
               62  RAISE_VARARGS_1       1  'exception instance'
               64  JUMP_FORWARD        186  'to 186'
             66_0  COME_FROM            46  '46'
             66_1  COME_FROM            38  '38'

 L.  62        66  SETUP_FINALLY       138  'to 138'

 L.  63        68  LOAD_GLOBAL              type
               70  LOAD_FAST                'dictionary'
               72  CALL_FUNCTION_1       1  ''
               74  LOAD_GLOBAL              dict
               76  COMPARE_OP               is
               78  POP_JUMP_IF_FALSE   132  'to 132'

 L.  64        80  LOAD_GLOBAL              open
               82  LOAD_FAST                'file_path'
               84  LOAD_STR                 'w'
               86  CALL_FUNCTION_2       2  ''
               88  SETUP_WITH          126  'to 126'
               90  STORE_FAST               'f'

 L.  65        92  LOAD_GLOBAL              json
               94  LOAD_ATTR                dump
               96  LOAD_FAST                'dictionary'
               98  LOAD_FAST                'f'
              100  LOAD_CONST               4
              102  LOAD_CONST               (',', ': ')
              104  LOAD_CONST               ('indent', 'separators')
              106  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              108  POP_TOP          

 L.  66       110  POP_BLOCK        
              112  BEGIN_FINALLY    
              114  WITH_CLEANUP_START
              116  WITH_CLEANUP_FINISH
              118  POP_FINALLY           0  ''
              120  POP_BLOCK        
              122  LOAD_CONST               True
              124  RETURN_VALUE     
            126_0  COME_FROM_WITH       88  '88'
              126  WITH_CLEANUP_START
              128  WITH_CLEANUP_FINISH
              130  END_FINALLY      
            132_0  COME_FROM            78  '78'

 L.  67       132  POP_BLOCK        
              134  LOAD_CONST               False
              136  RETURN_VALUE     
            138_0  COME_FROM_FINALLY    66  '66'

 L.  68       138  DUP_TOP          
              140  LOAD_GLOBAL              Exception
              142  COMPARE_OP               exception-match
              144  POP_JUMP_IF_FALSE   184  'to 184'
              146  POP_TOP          
              148  STORE_FAST               'err'
              150  POP_TOP          
              152  SETUP_FINALLY       172  'to 172'

 L.  69       154  LOAD_GLOBAL              Exception
              156  LOAD_STR                 '>>> There was an error creating the file. '
              158  LOAD_FAST                'err'
              160  FORMAT_VALUE          0  ''
              162  BUILD_STRING_2        2 
              164  CALL_FUNCTION_1       1  ''
              166  RAISE_VARARGS_1       1  'exception instance'
              168  POP_BLOCK        
              170  BEGIN_FINALLY    
            172_0  COME_FROM_FINALLY   152  '152'
              172  LOAD_CONST               None
              174  STORE_FAST               'err'
              176  DELETE_FAST              'err'
              178  END_FINALLY      
              180  POP_EXCEPT       
              182  JUMP_FORWARD        186  'to 186'
            184_0  COME_FROM           144  '144'
              184  END_FINALLY      
            186_0  COME_FROM           182  '182'
            186_1  COME_FROM            64  '64'

Parse error at or near `WITH_CLEANUP_START' instruction at offset 114


def update--- This code section failed: ---

 L.  90         0  SETUP_FINALLY        66  'to 66'

 L.  91         2  LOAD_GLOBAL              type
                4  LOAD_FAST                'content'
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_GLOBAL              dict
               10  COMPARE_OP               is
               12  POP_JUMP_IF_FALSE    60  'to 60'

 L.  92        14  LOAD_GLOBAL              open
               16  LOAD_FAST                'file_path'
               18  LOAD_STR                 'w'
               20  CALL_FUNCTION_2       2  ''
               22  SETUP_WITH           48  'to 48'
               24  STORE_FAST               'f'

 L.  93        26  LOAD_GLOBAL              json
               28  LOAD_ATTR                dump
               30  LOAD_FAST                'content'
               32  LOAD_FAST                'f'
               34  LOAD_CONST               2
               36  LOAD_CONST               (',', ': ')
               38  LOAD_CONST               ('indent', 'separators')
               40  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               42  POP_TOP          
               44  POP_BLOCK        
               46  BEGIN_FINALLY    
             48_0  COME_FROM_WITH       22  '22'
               48  WITH_CLEANUP_START
               50  WITH_CLEANUP_FINISH
               52  END_FINALLY      

 L.  94        54  POP_BLOCK        
               56  LOAD_CONST               True
               58  RETURN_VALUE     
             60_0  COME_FROM            12  '12'

 L.  95        60  POP_BLOCK        
               62  LOAD_CONST               False
               64  RETURN_VALUE     
             66_0  COME_FROM_FINALLY     0  '0'

 L.  96        66  DUP_TOP          
               68  LOAD_GLOBAL              Exception
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE   118  'to 118'
               74  POP_TOP          
               76  STORE_FAST               'err'
               78  POP_TOP          
               80  SETUP_FINALLY       106  'to 106'

 L.  97        82  LOAD_STR                 '>>> Something unexpected happened while updating '
               84  LOAD_FAST                'file_path'
               86  FORMAT_VALUE          0  ''
               88  BUILD_STRING_2        2 
               90  STORE_FAST               'msg'

 L.  98        92  LOAD_GLOBAL              Exception
               94  LOAD_FAST                'msg'
               96  LOAD_FAST                'err'
               98  CALL_FUNCTION_2       2  ''
              100  RAISE_VARARGS_1       1  'exception instance'
              102  POP_BLOCK        
              104  BEGIN_FINALLY    
            106_0  COME_FROM_FINALLY    80  '80'
              106  LOAD_CONST               None
              108  STORE_FAST               'err'
              110  DELETE_FAST              'err'
              112  END_FINALLY      
              114  POP_EXCEPT       
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM            72  '72'
              118  END_FINALLY      
            120_0  COME_FROM           116  '116'

Parse error at or near `LOAD_CONST' instruction at offset 56


__all__ = [
 'read', 'create']
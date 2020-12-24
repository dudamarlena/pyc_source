# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wc4nin/.cache/pypoetry/virtualenvs/snakypy-Jn9yRLD4-py3.8/lib/python3.8/site-packages/snakypy/file.py
# Compiled at: 2020-03-21 13:30:36
# Size of source mod 2**32: 1935 bytes
from os.path import exists

def read--- This code section failed: ---

 L.  22         0  SETUP_FINALLY        76  'to 76'

 L.  23         2  LOAD_GLOBAL              open
                4  LOAD_FAST                'file_path'
                6  CALL_FUNCTION_1       1  ''
                8  SETUP_WITH           66  'to 66'
               10  STORE_FAST               'f'

 L.  24        12  LOAD_FAST                'split'
               14  POP_JUMP_IF_FALSE    44  'to 44'

 L.  25        16  LOAD_FAST                'f'
               18  LOAD_METHOD              read
               20  CALL_METHOD_0         0  ''
               22  LOAD_METHOD              split
               24  LOAD_STR                 '\n'
               26  CALL_METHOD_1         1  ''
               28  POP_BLOCK        
               30  ROT_TWO          
               32  BEGIN_FINALLY    
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  POP_FINALLY           0  ''
               40  POP_BLOCK        
               42  RETURN_VALUE     
             44_0  COME_FROM            14  '14'

 L.  26        44  LOAD_FAST                'f'
               46  LOAD_METHOD              read
               48  CALL_METHOD_0         0  ''
               50  POP_BLOCK        
               52  ROT_TWO          
               54  BEGIN_FINALLY    
               56  WITH_CLEANUP_START
               58  WITH_CLEANUP_FINISH
               60  POP_FINALLY           0  ''
               62  POP_BLOCK        
               64  RETURN_VALUE     
             66_0  COME_FROM_WITH        8  '8'
               66  WITH_CLEANUP_START
               68  WITH_CLEANUP_FINISH
               70  END_FINALLY      
               72  POP_BLOCK        
               74  JUMP_FORWARD        130  'to 130'
             76_0  COME_FROM_FINALLY     0  '0'

 L.  27        76  DUP_TOP          
               78  LOAD_GLOBAL              FileNotFoundError
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE   128  'to 128'
               84  POP_TOP          
               86  STORE_FAST               'err'
               88  POP_TOP          
               90  SETUP_FINALLY       116  'to 116'

 L.  28        92  LOAD_GLOBAL              FileNotFoundError
               94  LOAD_STR                 '>>> File "'
               96  LOAD_FAST                'file_path'
               98  FORMAT_VALUE          0  ''
              100  LOAD_STR                 '" does not exist. '
              102  LOAD_FAST                'err'
              104  FORMAT_VALUE          0  ''
              106  BUILD_STRING_4        4 
              108  CALL_FUNCTION_1       1  ''
              110  RAISE_VARARGS_1       1  'exception instance'
              112  POP_BLOCK        
              114  BEGIN_FINALLY    
            116_0  COME_FROM_FINALLY    90  '90'
              116  LOAD_CONST               None
              118  STORE_FAST               'err'
              120  DELETE_FAST              'err'
              122  END_FINALLY      
              124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
            128_0  COME_FROM            82  '82'
              128  END_FINALLY      
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM            74  '74'

Parse error at or near `ROT_TWO' instruction at offset 30


def create--- This code section failed: ---

 L.  52         0  LOAD_FAST                'force'
                2  POP_JUMP_IF_TRUE     30  'to 30'
                4  LOAD_GLOBAL              exists
                6  LOAD_FAST                'file_path'
                8  CALL_FUNCTION_1       1  ''
               10  POP_JUMP_IF_FALSE    30  'to 30'

 L.  53        12  LOAD_GLOBAL              FileExistsError

 L.  54        14  LOAD_STR                 '>>> The file '
               16  LOAD_FAST                'file_path'
               18  FORMAT_VALUE          0  ''
               20  LOAD_STR                 ' already exists, use force=True.'
               22  BUILD_STRING_3        3 

 L.  53        24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
               28  JUMP_FORWARD        128  'to 128'
             30_0  COME_FROM            10  '10'
             30_1  COME_FROM             2  '2'

 L.  57        30  SETUP_FINALLY        80  'to 80'

 L.  58        32  LOAD_GLOBAL              open
               34  LOAD_FAST                'file_path'
               36  LOAD_STR                 'w'
               38  CALL_FUNCTION_2       2  ''
               40  SETUP_WITH           70  'to 70'
               42  STORE_FAST               'f'

 L.  59        44  LOAD_FAST                'f'
               46  LOAD_METHOD              write
               48  LOAD_FAST                'content'
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L.  60        54  POP_BLOCK        
               56  BEGIN_FINALLY    
               58  WITH_CLEANUP_START
               60  WITH_CLEANUP_FINISH
               62  POP_FINALLY           0  ''
               64  POP_BLOCK        
               66  LOAD_CONST               True
               68  RETURN_VALUE     
             70_0  COME_FROM_WITH       40  '40'
               70  WITH_CLEANUP_START
               72  WITH_CLEANUP_FINISH
               74  END_FINALLY      
               76  POP_BLOCK        
               78  JUMP_FORWARD        128  'to 128'
             80_0  COME_FROM_FINALLY    30  '30'

 L.  61        80  DUP_TOP          
               82  LOAD_GLOBAL              Exception
               84  COMPARE_OP               exception-match
               86  POP_JUMP_IF_FALSE   126  'to 126'
               88  POP_TOP          
               90  STORE_FAST               'err'
               92  POP_TOP          
               94  SETUP_FINALLY       114  'to 114'

 L.  62        96  LOAD_GLOBAL              Exception
               98  LOAD_STR                 '>>> There was an error creating the file: '
              100  LOAD_FAST                'err'
              102  FORMAT_VALUE          0  ''
              104  BUILD_STRING_2        2 
              106  CALL_FUNCTION_1       1  ''
              108  RAISE_VARARGS_1       1  'exception instance'
              110  POP_BLOCK        
              112  BEGIN_FINALLY    
            114_0  COME_FROM_FINALLY    94  '94'
              114  LOAD_CONST               None
              116  STORE_FAST               'err'
              118  DELETE_FAST              'err'
              120  END_FINALLY      
              122  POP_EXCEPT       
              124  JUMP_FORWARD        128  'to 128'
            126_0  COME_FROM            86  '86'
              126  END_FINALLY      
            128_0  COME_FROM           124  '124'
            128_1  COME_FROM            78  '78'
            128_2  COME_FROM            28  '28'

Parse error at or near `WITH_CLEANUP_START' instruction at offset 58


__all__ = [
 'read', 'create']
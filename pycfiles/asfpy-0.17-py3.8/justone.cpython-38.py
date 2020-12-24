# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asfpy/justone.py
# Compiled at: 2020-04-17 18:57:47
# Size of source mod 2**32: 4067 bytes
import os, errno, time, contextlib
STALE = 3600
DID_NOT_RUN = object()

def maybe_run--- This code section failed: ---

 L.  51         0  SETUP_FINALLY        16  'to 16'

 L.  52         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              stat
                6  LOAD_FAST                'fifo_fname'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'info'
               12  POP_BLOCK        
               14  JUMP_FORWARD         46  'to 46'
             16_0  COME_FROM_FINALLY     0  '0'

 L.  53        16  DUP_TOP          
               18  LOAD_GLOBAL              OSError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    44  'to 44'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  55        30  LOAD_GLOBAL              _run_func
               32  LOAD_FAST                'fifo_fname'
               34  LOAD_FAST                'func'
               36  CALL_FUNCTION_2       2  ''
               38  ROT_FOUR         
               40  POP_EXCEPT       
               42  RETURN_VALUE     
             44_0  COME_FROM            22  '22'
               44  END_FINALLY      
             46_0  COME_FROM            14  '14'

 L.  59        46  SETUP_FINALLY        84  'to 84'

 L.  60        48  LOAD_GLOBAL              os
               50  LOAD_METHOD              open
               52  LOAD_FAST                'fifo_fname'
               54  LOAD_GLOBAL              os
               56  LOAD_ATTR                O_WRONLY
               58  LOAD_GLOBAL              os
               60  LOAD_ATTR                O_NONBLOCK
               62  BINARY_OR        
               64  CALL_METHOD_2         2  ''
               66  STORE_FAST               'fd'

 L.  63        68  LOAD_GLOBAL              os
               70  LOAD_METHOD              close
               72  LOAD_FAST                'fd'
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          

 L.  64        78  LOAD_GLOBAL              DID_NOT_RUN
               80  POP_BLOCK        
               82  RETURN_VALUE     
             84_0  COME_FROM_FINALLY    46  '46'

 L.  66        84  DUP_TOP          
               86  LOAD_GLOBAL              OSError
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   214  'to 214'
               92  POP_TOP          
               94  STORE_FAST               'e'
               96  POP_TOP          
               98  SETUP_FINALLY       202  'to 202'

 L.  67       100  LOAD_FAST                'e'
              102  LOAD_ATTR                errno
              104  LOAD_GLOBAL              errno
              106  LOAD_ATTR                ENOENT
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_FALSE   130  'to 130'

 L.  70       112  LOAD_GLOBAL              _run_func
              114  LOAD_FAST                'fifo_fname'
              116  LOAD_FAST                'func'
              118  CALL_FUNCTION_2       2  ''
              120  ROT_FOUR         
              122  POP_BLOCK        
              124  POP_EXCEPT       
              126  CALL_FINALLY        202  'to 202'
              128  RETURN_VALUE     
            130_0  COME_FROM           110  '110'

 L.  74       130  LOAD_FAST                'e'
              132  LOAD_ATTR                errno
              134  LOAD_GLOBAL              errno
              136  LOAD_ATTR                ENXIO
              138  COMPARE_OP               !=
              140  POP_JUMP_IF_FALSE   144  'to 144'

 L.  75       142  RAISE_VARARGS_0       0  'reraise'
            144_0  COME_FROM           140  '140'

 L.  82       144  LOAD_GLOBAL              time
              146  LOAD_METHOD              time
              148  CALL_METHOD_0         0  ''
              150  LOAD_FAST                'info'
              152  LOAD_ATTR                st_mtime
              154  BINARY_SUBTRACT  
              156  LOAD_FAST                'stale'
              158  COMPARE_OP               >
              160  POP_JUMP_IF_FALSE   190  'to 190'

 L.  84       162  LOAD_GLOBAL              os
              164  LOAD_METHOD              unlink
              166  LOAD_FAST                'fifo_fname'
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          

 L.  85       172  LOAD_GLOBAL              _run_func
              174  LOAD_FAST                'fifo_fname'
              176  LOAD_FAST                'func'
              178  CALL_FUNCTION_2       2  ''
              180  ROT_FOUR         
              182  POP_BLOCK        
              184  POP_EXCEPT       
              186  CALL_FINALLY        202  'to 202'
              188  RETURN_VALUE     
            190_0  COME_FROM           160  '160'

 L.  88       190  LOAD_GLOBAL              DID_NOT_RUN
              192  ROT_FOUR         
              194  POP_BLOCK        
              196  POP_EXCEPT       
              198  CALL_FINALLY        202  'to 202'
              200  RETURN_VALUE     
            202_0  COME_FROM           198  '198'
            202_1  COME_FROM           186  '186'
            202_2  COME_FROM           126  '126'
            202_3  COME_FROM_FINALLY    98  '98'
              202  LOAD_CONST               None
              204  STORE_FAST               'e'
              206  DELETE_FAST              'e'
              208  END_FINALLY      
              210  POP_EXCEPT       
              212  JUMP_FORWARD        216  'to 216'
            214_0  COME_FROM            90  '90'
              214  END_FINALLY      
            216_0  COME_FROM           212  '212'

Parse error at or near `POP_BLOCK' instruction at offset 122


def _run_func--- This code section failed: ---

 L.  92         0  LOAD_GLOBAL              _temp_fifo
                2  LOAD_FAST                'fifo_fname'
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH           36  'to 36'
                8  STORE_FAST               'okay'

 L.  93        10  LOAD_FAST                'okay'
               12  POP_JUMP_IF_FALSE    32  'to 32'

 L.  94        14  LOAD_FAST                'func'
               16  CALL_FUNCTION_0       0  ''
               18  POP_BLOCK        
               20  ROT_TWO          
               22  BEGIN_FINALLY    
               24  WITH_CLEANUP_START
               26  WITH_CLEANUP_FINISH
               28  POP_FINALLY           0  ''
               30  RETURN_VALUE     
             32_0  COME_FROM            12  '12'
               32  POP_BLOCK        
               34  BEGIN_FINALLY    
             36_0  COME_FROM_WITH        6  '6'
               36  WITH_CLEANUP_START
               38  WITH_CLEANUP_FINISH
               40  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 20


@contextlib.contextmanager
def _temp_fifo--- This code section failed: ---

 L. 100         0  SETUP_FINALLY        16  'to 16'

 L. 101         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              mkfifo
                6  LOAD_FAST                'fifo_fname'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          
               12  POP_BLOCK        
               14  JUMP_FORWARD         44  'to 44'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 102        16  DUP_TOP          
               18  LOAD_GLOBAL              OSError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    42  'to 42'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 105        30  LOAD_CONST               False
               32  YIELD_VALUE      
               34  POP_TOP          

 L. 106        36  POP_EXCEPT       
               38  LOAD_CONST               None
               40  RETURN_VALUE     
             42_0  COME_FROM            22  '22'
               42  END_FINALLY      
             44_0  COME_FROM            14  '14'

 L. 108        44  SETUP_FINALLY        94  'to 94'

 L. 110        46  LOAD_GLOBAL              os
               48  LOAD_METHOD              open
               50  LOAD_FAST                'fifo_fname'
               52  LOAD_GLOBAL              os
               54  LOAD_ATTR                O_RDONLY
               56  LOAD_GLOBAL              os
               58  LOAD_ATTR                O_NONBLOCK
               60  BINARY_OR        
               62  CALL_METHOD_2         2  ''
               64  STORE_FAST               'fd'

 L. 112        66  SETUP_FINALLY        78  'to 78'

 L. 114        68  LOAD_CONST               True
               70  YIELD_VALUE      
               72  POP_TOP          
               74  POP_BLOCK        
               76  BEGIN_FINALLY    
             78_0  COME_FROM_FINALLY    66  '66'

 L. 116        78  LOAD_GLOBAL              os
               80  LOAD_METHOD              close
               82  LOAD_FAST                'fd'
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          
               88  END_FINALLY      
               90  POP_BLOCK        
               92  BEGIN_FINALLY    
             94_0  COME_FROM_FINALLY    44  '44'

 L. 123        94  SETUP_FINALLY       110  'to 110'

 L. 124        96  LOAD_GLOBAL              os
               98  LOAD_METHOD              unlink
              100  LOAD_FAST                'fifo_fname'
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          
              106  POP_BLOCK        
              108  JUMP_FORWARD        130  'to 130'
            110_0  COME_FROM_FINALLY    94  '94'

 L. 125       110  DUP_TOP          
              112  LOAD_GLOBAL              OSError
              114  COMPARE_OP               exception-match
              116  POP_JUMP_IF_FALSE   128  'to 128'
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L. 127       124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
            128_0  COME_FROM           116  '116'
              128  END_FINALLY      
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM           108  '108'
              130  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 38
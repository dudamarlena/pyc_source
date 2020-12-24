# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/nemo/miniconda3/envs/cli/lib/python3.8/site-packages/cli_passthrough/_passthrough.py
# Compiled at: 2019-11-05 20:39:15
# Size of source mod 2**32: 1530 bytes
import errno, os, pty, sys
from select import select
from subprocess import Popen
from .utils import echo

def cli_passthrough--- This code section failed: ---

 L.  13         0  LOAD_GLOBAL              zip
                2  LOAD_GLOBAL              pty
                4  LOAD_METHOD              openpty
                6  CALL_METHOD_0         0  ''
                8  LOAD_GLOBAL              pty
               10  LOAD_METHOD              openpty
               12  CALL_METHOD_0         0  ''
               14  CALL_FUNCTION_2       2  ''
               16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'masters'
               20  STORE_FAST               'slaves'

 L.  14        22  LOAD_FAST                'interactive'
               24  POP_JUMP_IF_FALSE    46  'to 46'

 L.  15        26  LOAD_STR                 '/bin/bash'
               28  LOAD_STR                 '-i'
               30  LOAD_STR                 '-c'
               32  BUILD_LIST_3          3 
               34  LOAD_FAST                'cmd'
               36  LOAD_METHOD              split
               38  CALL_METHOD_0         0  ''
               40  BINARY_ADD       
               42  STORE_FAST               'cmd'
               44  JUMP_FORWARD         54  'to 54'
             46_0  COME_FROM            24  '24'

 L.  17        46  LOAD_FAST                'cmd'
               48  LOAD_METHOD              split
               50  CALL_METHOD_0         0  ''
               52  STORE_FAST               'cmd'
             54_0  COME_FROM            44  '44'

 L.  19        54  LOAD_GLOBAL              Popen
               56  LOAD_FAST                'cmd'
               58  LOAD_FAST                'slaves'
               60  LOAD_CONST               0
               62  BINARY_SUBSCR    
               64  LOAD_FAST                'slaves'
               66  LOAD_CONST               0
               68  BINARY_SUBSCR    
               70  LOAD_FAST                'slaves'
               72  LOAD_CONST               1
               74  BINARY_SUBSCR    
               76  LOAD_CONST               ('stdin', 'stdout', 'stderr')
               78  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               80  SETUP_WITH          306  'to 306'
               82  STORE_FAST               'p'

 L.  20        84  LOAD_FAST                'slaves'
               86  GET_ITER         
               88  FOR_ITER            132  'to 132'
               90  STORE_FAST               'fd'

 L.  21        92  LOAD_GLOBAL              os
               94  LOAD_METHOD              close
               96  LOAD_FAST                'fd'
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          

 L.  23       102  LOAD_FAST                'masters'
              104  LOAD_CONST               0
              106  BINARY_SUBSCR    

 L.  23       108  LOAD_GLOBAL              sys
              110  LOAD_ATTR                stdout
              112  LOAD_ATTR                buffer

 L.  24       114  LOAD_FAST                'masters'
              116  LOAD_CONST               1
              118  BINARY_SUBSCR    

 L.  24       120  LOAD_GLOBAL              sys
              122  LOAD_ATTR                stderr
              124  LOAD_ATTR                buffer

 L.  22       126  BUILD_MAP_2           2 
              128  STORE_FAST               'readable'
              130  JUMP_BACK            88  'to 88'

 L.  26       132  LOAD_FAST                'readable'
          134_136  POP_JUMP_IF_FALSE   302  'to 302'

 L.  27       138  LOAD_GLOBAL              select
              140  LOAD_FAST                'readable'
              142  BUILD_LIST_0          0 
              144  BUILD_LIST_0          0 
              146  CALL_FUNCTION_3       3  ''
              148  LOAD_CONST               0
              150  BINARY_SUBSCR    
              152  GET_ITER         
              154  FOR_ITER            300  'to 300'
              156  STORE_FAST               'fd'

 L.  28       158  SETUP_FINALLY       176  'to 176'

 L.  29       160  LOAD_GLOBAL              os
              162  LOAD_METHOD              read
              164  LOAD_FAST                'fd'
              166  LOAD_CONST               1024
              168  CALL_METHOD_2         2  ''
              170  STORE_FAST               'data'
              172  POP_BLOCK        
              174  JUMP_FORWARD        230  'to 230'
            176_0  COME_FROM_FINALLY   158  '158'

 L.  30       176  DUP_TOP          
              178  LOAD_GLOBAL              OSError
              180  COMPARE_OP               exception-match
              182  POP_JUMP_IF_FALSE   228  'to 228'
              184  POP_TOP          
              186  STORE_FAST               'e'
              188  POP_TOP          
              190  SETUP_FINALLY       216  'to 216'

 L.  31       192  LOAD_FAST                'e'
              194  LOAD_ATTR                errno
              196  LOAD_GLOBAL              errno
              198  LOAD_ATTR                EIO
              200  COMPARE_OP               !=
              202  POP_JUMP_IF_FALSE   206  'to 206'

 L.  32       204  RAISE_VARARGS_0       0  ''
            206_0  COME_FROM           202  '202'

 L.  33       206  LOAD_FAST                'readable'
              208  LOAD_FAST                'fd'
              210  DELETE_SUBSCR    
              212  POP_BLOCK        
              214  BEGIN_FINALLY    
            216_0  COME_FROM_FINALLY   190  '190'
              216  LOAD_CONST               None
              218  STORE_FAST               'e'
              220  DELETE_FAST              'e'
              222  END_FINALLY      
              224  POP_EXCEPT       
              226  JUMP_BACK           154  'to 154'
            228_0  COME_FROM           182  '182'
              228  END_FINALLY      
            230_0  COME_FROM           174  '174'

 L.  35       230  LOAD_FAST                'data'
              232  POP_JUMP_IF_TRUE    242  'to 242'

 L.  36       234  LOAD_FAST                'readable'
              236  LOAD_FAST                'fd'
              238  DELETE_SUBSCR    
              240  JUMP_BACK           154  'to 154'
            242_0  COME_FROM           232  '232'

 L.  38       242  LOAD_FAST                'fd'
              244  LOAD_FAST                'masters'
              246  LOAD_CONST               0
              248  BINARY_SUBSCR    
              250  COMPARE_OP               ==
          252_254  POP_JUMP_IF_FALSE   270  'to 270'

 L.  39       256  LOAD_GLOBAL              echo
              258  LOAD_FAST                'data'
              260  LOAD_METHOD              rstrip
              262  CALL_METHOD_0         0  ''
              264  CALL_FUNCTION_1       1  ''
              266  POP_TOP          
              268  JUMP_FORWARD        286  'to 286'
            270_0  COME_FROM           252  '252'

 L.  41       270  LOAD_GLOBAL              echo
              272  LOAD_FAST                'data'
              274  LOAD_METHOD              rstrip
              276  CALL_METHOD_0         0  ''
              278  LOAD_CONST               True
              280  LOAD_CONST               ('err',)
              282  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              284  POP_TOP          
            286_0  COME_FROM           268  '268'

 L.  42       286  LOAD_FAST                'readable'
              288  LOAD_FAST                'fd'
              290  BINARY_SUBSCR    
              292  LOAD_METHOD              flush
              294  CALL_METHOD_0         0  ''
              296  POP_TOP          
              298  JUMP_BACK           154  'to 154'
              300  JUMP_BACK           132  'to 132'
            302_0  COME_FROM           134  '134'
              302  POP_BLOCK        
              304  BEGIN_FINALLY    
            306_0  COME_FROM_WITH       80  '80'
              306  WITH_CLEANUP_START
              308  WITH_CLEANUP_FINISH
              310  END_FINALLY      

 L.  43       312  LOAD_FAST                'masters'
              314  GET_ITER         
              316  FOR_ITER            334  'to 334'
              318  STORE_FAST               'fd'

 L.  44       320  LOAD_GLOBAL              os
              322  LOAD_METHOD              close
              324  LOAD_FAST                'fd'
              326  CALL_METHOD_1         1  ''
              328  POP_TOP          
          330_332  JUMP_BACK           316  'to 316'

 L.  45       334  LOAD_FAST                'p'
              336  LOAD_ATTR                returncode
              338  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 304
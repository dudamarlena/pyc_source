# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\brython\make_file_system.py
# Compiled at: 2019-11-06 03:43:45
# Size of source mod 2**32: 2172 bytes
import json, os, stat, sys, binascii

def make--- This code section failed: ---

 L.  30         0  BUILD_MAP_0           0 
                2  STORE_FAST               'files'

 L.  32         4  LOAD_GLOBAL              os
                6  LOAD_METHOD              getcwd
                8  CALL_METHOD_0         0  ''
               10  STORE_FAST               'this_dir'

 L.  33        12  LOAD_FAST                'vfs_name'
               14  FORMAT_VALUE          0  ''
               16  LOAD_STR                 '.vfs.js'
               18  BUILD_STRING_2        2 
               20  STORE_FAST               'dest_file'

 L.  34        22  LOAD_FAST                'prefix'
               24  POP_JUMP_IF_FALSE    36  'to 36'
               26  LOAD_FAST                'prefix'
               28  LOAD_METHOD              split
               30  LOAD_STR                 '/'
               32  CALL_METHOD_1         1  ''
               34  JUMP_FORWARD         38  'to 38'
             36_0  COME_FROM            24  '24'
               36  BUILD_LIST_0          0 
             38_0  COME_FROM            34  '34'
               38  STORE_FAST               'virtual_dir'

 L.  35        40  LOAD_GLOBAL              print
               42  LOAD_STR                 'virtual dir'
               44  LOAD_FAST                'virtual_dir'
               46  CALL_FUNCTION_2       2  ''
               48  POP_TOP          

 L.  37        50  LOAD_GLOBAL              os
               52  LOAD_METHOD              walk
               54  LOAD_FAST                'this_dir'
               56  CALL_METHOD_1         1  ''
               58  GET_ITER         
               60  FOR_ITER            248  'to 248'
               62  UNPACK_SEQUENCE_3     3 
               64  STORE_FAST               'dirpath'
               66  STORE_FAST               'dirnames'
               68  STORE_FAST               'filenames'

 L.  38        70  LOAD_FAST                'dirpath'
               72  LOAD_FAST                'this_dir'
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE    84  'to 84'

 L.  39        78  BUILD_LIST_0          0 
               80  STORE_FAST               'path'
               82  JUMP_FORWARD        118  'to 118'
             84_0  COME_FROM            76  '76'

 L.  41        84  LOAD_FAST                'dirpath'
               86  LOAD_GLOBAL              len
               88  LOAD_FAST                'this_dir'
               90  CALL_FUNCTION_1       1  ''
               92  LOAD_GLOBAL              len
               94  LOAD_GLOBAL              os
               96  LOAD_ATTR                sep
               98  CALL_FUNCTION_1       1  ''
              100  BINARY_ADD       
              102  LOAD_CONST               None
              104  BUILD_SLICE_2         2 
              106  BINARY_SUBSCR    
              108  LOAD_METHOD              split
              110  LOAD_GLOBAL              os
              112  LOAD_ATTR                sep
              114  CALL_METHOD_1         1  ''
              116  STORE_FAST               'path'
            118_0  COME_FROM            82  '82'

 L.  42       118  LOAD_FAST                'filenames'
              120  GET_ITER         
              122  FOR_ITER            246  'to 246'
              124  STORE_FAST               'filename'

 L.  43       126  LOAD_FAST                'filename'
              128  LOAD_METHOD              endswith
              130  LOAD_STR                 '.vfs.js'
              132  CALL_METHOD_1         1  ''
              134  POP_JUMP_IF_FALSE   138  'to 138'

 L.  44       136  JUMP_BACK           122  'to 122'
            138_0  COME_FROM           134  '134'

 L.  45       138  LOAD_STR                 '/'
              140  LOAD_METHOD              join
              142  LOAD_FAST                'virtual_dir'
              144  LOAD_FAST                'path'
              146  BINARY_ADD       
              148  LOAD_FAST                'filename'
              150  BUILD_LIST_1          1 
              152  BINARY_ADD       
              154  CALL_METHOD_1         1  ''
              156  STORE_FAST               'rel_path'

 L.  46       158  LOAD_GLOBAL              open
              160  LOAD_GLOBAL              os
              162  LOAD_ATTR                path
              164  LOAD_METHOD              join
              166  LOAD_FAST                'dirpath'
              168  LOAD_FAST                'filename'
              170  CALL_METHOD_2         2  ''
              172  LOAD_STR                 'rb'
              174  CALL_FUNCTION_2       2  ''
              176  SETUP_WITH          238  'to 238'
              178  STORE_FAST               'f'

 L.  48       180  LOAD_GLOBAL              binascii
              182  LOAD_METHOD              b2a_base64
              184  LOAD_FAST                'f'
              186  LOAD_METHOD              read
              188  CALL_METHOD_0         0  ''
              190  CALL_METHOD_1         1  ''
              192  LOAD_METHOD              decode
              194  LOAD_STR                 'ascii'
              196  CALL_METHOD_1         1  ''
              198  STORE_FAST               'content'

 L.  49       200  LOAD_GLOBAL              os
              202  LOAD_METHOD              fstat
              204  LOAD_FAST                'f'
              206  LOAD_METHOD              fileno
              208  CALL_METHOD_0         0  ''
              210  CALL_METHOD_1         1  ''
              212  STORE_FAST               'file_stat'

 L.  51       214  LOAD_FAST                'content'

 L.  52       216  LOAD_FAST                'file_stat'
              218  LOAD_ATTR                st_ctime

 L.  53       220  LOAD_FAST                'file_stat'
              222  LOAD_ATTR                st_mtime

 L.  50       224  LOAD_CONST               ('content', 'ctime', 'mtime')
              226  BUILD_CONST_KEY_MAP_3     3 
              228  LOAD_FAST                'files'
              230  LOAD_FAST                'rel_path'
              232  STORE_SUBSCR     
              234  POP_BLOCK        
              236  BEGIN_FINALLY    
            238_0  COME_FROM_WITH      176  '176'
              238  WITH_CLEANUP_START
              240  WITH_CLEANUP_FINISH
              242  END_FINALLY      
              244  JUMP_BACK           122  'to 122'
              246  JUMP_BACK            60  'to 60'

 L.  56       248  LOAD_GLOBAL              print
              250  LOAD_GLOBAL              list
              252  LOAD_FAST                'files'
              254  CALL_FUNCTION_1       1  ''
              256  CALL_FUNCTION_1       1  ''
              258  POP_TOP          

 L.  57       260  LOAD_GLOBAL              open
              262  LOAD_FAST                'dest_file'
              264  LOAD_STR                 'w'
              266  LOAD_STR                 'utf-8'
              268  LOAD_CONST               ('encoding',)
              270  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              272  SETUP_WITH          316  'to 316'
              274  STORE_FAST               'out'

 L.  58       276  LOAD_FAST                'out'
              278  LOAD_METHOD              write
              280  LOAD_STR                 '__BRYTHON__.add_files('
              282  CALL_METHOD_1         1  ''
              284  POP_TOP          

 L.  59       286  LOAD_GLOBAL              json
              288  LOAD_ATTR                dump
              290  LOAD_FAST                'files'
              292  LOAD_FAST                'out'
              294  LOAD_CONST               4
              296  LOAD_CONST               ('indent',)
              298  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              300  POP_TOP          

 L.  60       302  LOAD_FAST                'out'
              304  LOAD_METHOD              write
              306  LOAD_STR                 ')'
              308  CALL_METHOD_1         1  ''
              310  POP_TOP          
              312  POP_BLOCK        
              314  BEGIN_FINALLY    
            316_0  COME_FROM_WITH      272  '272'
              316  WITH_CLEANUP_START
              318  WITH_CLEANUP_FINISH
              320  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 236
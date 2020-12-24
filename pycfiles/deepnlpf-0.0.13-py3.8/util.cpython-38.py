# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deepnlpf/core/util.py
# Compiled at: 2020-04-15 23:48:55
# Size of source mod 2**32: 1459 bytes
"""
    Date: 07/03/2019
"""
import os, json, datetime

class Util(object):

    def __init__(self):
        pass

    def openfile_json--- This code section failed: ---

 L.  15         0  SETUP_FINALLY        48  'to 48'

 L.  16         2  LOAD_GLOBAL              open
                4  LOAD_FAST                'path_file'
                6  LOAD_STR                 'r'
                8  CALL_FUNCTION_2       2  ''
               10  SETUP_WITH           38  'to 38'
               12  STORE_FAST               'file'

 L.  17        14  LOAD_GLOBAL              json
               16  LOAD_METHOD              load
               18  LOAD_FAST                'file'
               20  CALL_METHOD_1         1  ''
               22  POP_BLOCK        
               24  ROT_TWO          
               26  BEGIN_FINALLY    
               28  WITH_CLEANUP_START
               30  WITH_CLEANUP_FINISH
               32  POP_FINALLY           0  ''
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_WITH       10  '10'
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  END_FINALLY      
               44  POP_BLOCK        
               46  JUMP_FORWARD         94  'to 94'
             48_0  COME_FROM_FINALLY     0  '0'

 L.  18        48  DUP_TOP          
               50  LOAD_GLOBAL              Exception
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    92  'to 92'
               56  POP_TOP          
               58  STORE_FAST               'err'
               60  POP_TOP          
               62  SETUP_FINALLY        80  'to 80'

 L.  19        64  LOAD_STR                 'Error loading file!'
               66  LOAD_FAST                'err'
               68  BINARY_ADD       
               70  ROT_FOUR         
               72  POP_BLOCK        
               74  POP_EXCEPT       
               76  CALL_FINALLY         80  'to 80'
               78  RETURN_VALUE     
             80_0  COME_FROM            76  '76'
             80_1  COME_FROM_FINALLY    62  '62'
               80  LOAD_CONST               None
               82  STORE_FAST               'err'
               84  DELETE_FAST              'err'
               86  END_FINALLY      
               88  POP_EXCEPT       
               90  JUMP_FORWARD         94  'to 94'
             92_0  COME_FROM            54  '54'
               92  END_FINALLY      
             94_0  COME_FROM            90  '90'
             94_1  COME_FROM            46  '46'

Parse error at or near `ROT_TWO' instruction at offset 24

    def open_txt--- This code section failed: ---

 L.  22         0  BUILD_LIST_0          0 
                2  STORE_FAST               'data_temp'

 L.  24         4  SETUP_FINALLY        68  'to 68'

 L.  25         6  LOAD_GLOBAL              open
                8  LOAD_FAST                'path_file'
               10  CALL_FUNCTION_1       1  ''
               12  SETUP_WITH           58  'to 58'
               14  STORE_FAST               'file'

 L.  26        16  LOAD_FAST                'file'
               18  GET_ITER         
               20  FOR_ITER             40  'to 40'
               22  STORE_FAST               'line'

 L.  27        24  LOAD_FAST                'data_temp'
               26  LOAD_METHOD              append
               28  LOAD_FAST                'line'
               30  LOAD_METHOD              strip
               32  CALL_METHOD_0         0  ''
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          
               38  JUMP_BACK            20  'to 20'

 L.  28        40  LOAD_FAST                'data_temp'
               42  POP_BLOCK        
               44  ROT_TWO          
               46  BEGIN_FINALLY    
               48  WITH_CLEANUP_START
               50  WITH_CLEANUP_FINISH
               52  POP_FINALLY           0  ''
               54  POP_BLOCK        
               56  RETURN_VALUE     
             58_0  COME_FROM_WITH       12  '12'
               58  WITH_CLEANUP_START
               60  WITH_CLEANUP_FINISH
               62  END_FINALLY      
               64  POP_BLOCK        
               66  JUMP_FORWARD        118  'to 118'
             68_0  COME_FROM_FINALLY     4  '4'

 L.  29        68  DUP_TOP          
               70  LOAD_GLOBAL              Exception
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE   116  'to 116'
               76  POP_TOP          
               78  STORE_FAST               'err'
               80  POP_TOP          
               82  SETUP_FINALLY       104  'to 104'

 L.  30        84  LOAD_STR                 'Error loading file!'
               86  LOAD_GLOBAL              str
               88  LOAD_FAST                'err'
               90  CALL_FUNCTION_1       1  ''
               92  BINARY_ADD       
               94  ROT_FOUR         
               96  POP_BLOCK        
               98  POP_EXCEPT       
              100  CALL_FINALLY        104  'to 104'
              102  RETURN_VALUE     
            104_0  COME_FROM           100  '100'
            104_1  COME_FROM_FINALLY    82  '82'
              104  LOAD_CONST               None
              106  STORE_FAST               'err'
              108  DELETE_FAST              'err'
              110  END_FINALLY      
              112  POP_EXCEPT       
              114  JUMP_FORWARD        118  'to 118'
            116_0  COME_FROM            74  '74'
              116  END_FINALLY      
            118_0  COME_FROM           114  '114'
            118_1  COME_FROM            66  '66'

Parse error at or near `ROT_TWO' instruction at offset 44

    def save_txt(self, path_file, corpus):
        try:
            temp_file = openpath_file'w'
            for line in corpus:
                temp_file.write(line + '\n')
            else:
                temp_file.close

        except Exception as err:
            try:
                print(err)
            finally:
                err = None
                del err

    def save_json(self, path_file, corpus):
        try:
            temp_file = openpath_file'w'
            for line in corpus:
                temp_file.write(line + '\n')
            else:
                temp_file.close

        except Exception as err:
            try:
                print(err)
            finally:
                err = None
                del err

    def save_file(self, path_file_output, data):
        try:
            with openpath_file_output'w' as (file):
                file.writedata
        except Exception as err:
            try:
                print(err)
            finally:
                err = None
                del err
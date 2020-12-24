# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\aigpy\fileHelper.py
# Compiled at: 2020-02-14 02:12:37
# Size of source mod 2**32: 849 bytes
"""
@File    :   fileHelper.py
@Time    :   2019/03/11
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
"""
import os

def getFileSize--- This code section failed: ---

 L.  16         0  SETUP_FINALLY        38  'to 38'

 L.  17         2  LOAD_GLOBAL              os
                4  LOAD_ATTR                path
                6  LOAD_METHOD              isfile
                8  LOAD_FAST                'path'
               10  CALL_METHOD_1         1  ''
               12  LOAD_CONST               False
               14  COMPARE_OP               is
               16  POP_JUMP_IF_FALSE    24  'to 24'

 L.  18        18  POP_BLOCK        
               20  LOAD_CONST               0
               22  RETURN_VALUE     
             24_0  COME_FROM            16  '16'

 L.  19        24  LOAD_GLOBAL              os
               26  LOAD_ATTR                path
               28  LOAD_METHOD              getsize
               30  LOAD_FAST                'path'
               32  CALL_METHOD_1         1  ''
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY     0  '0'

 L.  20        38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L.  21        44  POP_EXCEPT       
               46  LOAD_CONST               0
               48  RETURN_VALUE     
               50  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 20


def getFileContent--- This code section failed: ---

 L.  25         0  LOAD_STR                 'r'
                2  STORE_FAST               'mode'

 L.  26         4  LOAD_FAST                'isBin'
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  27         8  LOAD_STR                 'rb'
               10  STORE_FAST               'mode'
             12_0  COME_FROM             6  '6'

 L.  28        12  SETUP_FINALLY        74  'to 74'

 L.  29        14  LOAD_GLOBAL              getFileSize
               16  LOAD_FAST                'path'
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'size'

 L.  30        22  LOAD_FAST                'size'
               24  LOAD_CONST               0
               26  COMPARE_OP               <=
               28  POP_JUMP_IF_FALSE    36  'to 36'

 L.  31        30  POP_BLOCK        
               32  LOAD_STR                 ''
               34  RETURN_VALUE     
             36_0  COME_FROM            28  '28'

 L.  32        36  LOAD_GLOBAL              open
               38  LOAD_FAST                'path'
               40  LOAD_FAST                'mode'
               42  CALL_FUNCTION_2       2  ''
               44  SETUP_WITH           62  'to 62'
               46  STORE_FAST               'fd'

 L.  33        48  LOAD_FAST                'fd'
               50  LOAD_METHOD              read
               52  LOAD_FAST                'size'
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'content'
               58  POP_BLOCK        
               60  BEGIN_FINALLY    
             62_0  COME_FROM_WITH       44  '44'
               62  WITH_CLEANUP_START
               64  WITH_CLEANUP_FINISH
               66  END_FINALLY      

 L.  34        68  LOAD_FAST                'content'
               70  POP_BLOCK        
               72  RETURN_VALUE     
             74_0  COME_FROM_FINALLY    12  '12'

 L.  35        74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L.  36        80  POP_EXCEPT       
               82  LOAD_STR                 ''
               84  RETURN_VALUE     
               86  END_FINALLY      

Parse error at or near `LOAD_STR' instruction at offset 32


def write--- This code section failed: ---

 L.  40         0  SETUP_FINALLY        40  'to 40'

 L.  41         2  LOAD_GLOBAL              open
                4  LOAD_FAST                'path'
                6  LOAD_FAST                'mode'
                8  CALL_FUNCTION_2       2  ''
               10  SETUP_WITH           28  'to 28'
               12  STORE_FAST               'fd'

 L.  42        14  LOAD_FAST                'fd'
               16  LOAD_METHOD              write
               18  LOAD_FAST                'content'
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          
               24  POP_BLOCK        
               26  BEGIN_FINALLY    
             28_0  COME_FROM_WITH       10  '10'
               28  WITH_CLEANUP_START
               30  WITH_CLEANUP_FINISH
               32  END_FINALLY      

 L.  43        34  POP_BLOCK        
               36  LOAD_CONST               True
               38  RETURN_VALUE     
             40_0  COME_FROM_FINALLY     0  '0'

 L.  44        40  DUP_TOP          
               42  LOAD_GLOBAL              Exception
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    78  'to 78'
               48  POP_TOP          
               50  STORE_FAST               'e'
               52  POP_TOP          
               54  SETUP_FINALLY        66  'to 66'

 L.  45        56  POP_BLOCK        
               58  POP_EXCEPT       
               60  CALL_FINALLY         66  'to 66'
               62  LOAD_CONST               False
               64  RETURN_VALUE     
             66_0  COME_FROM            60  '60'
             66_1  COME_FROM_FINALLY    54  '54'
               66  LOAD_CONST               None
               68  STORE_FAST               'e'
               70  DELETE_FAST              'e'
               72  END_FINALLY      
               74  POP_EXCEPT       
               76  JUMP_FORWARD         80  'to 80'
             78_0  COME_FROM            46  '46'
               78  END_FINALLY      
             80_0  COME_FROM            76  '76'

Parse error at or near `RETURN_VALUE' instruction at offset 38
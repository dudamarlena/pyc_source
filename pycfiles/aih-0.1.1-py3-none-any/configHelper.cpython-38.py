# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\aigpy\configHelper.py
# Compiled at: 2020-02-14 02:12:36
# Size of source mod 2**32: 2373 bytes
__doc__ = '\n@File    :   configHelper.py\n@Time    :   2018/12/17\n@Author  :   Yaron Huang \n@Version :   1.0\n@Contact :   yaronhuang@qq.com\n@Desc    :   Config Tool\n'
import os, configparser

def Count--- This code section failed: ---

 L.  16         0  SETUP_FINALLY       102  'to 102'

 L.  17         2  LOAD_CONST               0
                4  STORE_FAST               'ret'

 L.  18         6  LOAD_GLOBAL              configparser
                8  LOAD_METHOD              ConfigParser
               10  CALL_METHOD_0         0  ''
               12  STORE_FAST               'cf'

 L.  19        14  LOAD_FAST                'cf'
               16  LOAD_METHOD              read
               18  LOAD_FAST                'fileName'
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          

 L.  20        24  LOAD_FAST                'section'
               26  LOAD_CONST               None
               28  COMPARE_OP               is
               30  POP_JUMP_IF_FALSE    74  'to 74'

 L.  21        32  LOAD_FAST                'cf'
               34  LOAD_METHOD              sections
               36  CALL_METHOD_0         0  ''
               38  STORE_FAST               'seclist'

 L.  22        40  LOAD_FAST                'seclist'
               42  GET_ITER         
               44  FOR_ITER             72  'to 72'
               46  STORE_FAST               'sec'

 L.  23        48  LOAD_FAST                'cf'
               50  LOAD_METHOD              options
               52  LOAD_FAST                'sec'
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'oplist'

 L.  24        58  LOAD_FAST                'ret'
               60  LOAD_GLOBAL              len
               62  LOAD_FAST                'oplist'
               64  CALL_FUNCTION_1       1  ''
               66  BINARY_ADD       
               68  STORE_FAST               'ret'
               70  JUMP_BACK            44  'to 44'
               72  JUMP_FORWARD         96  'to 96'
             74_0  COME_FROM            30  '30'

 L.  25        74  LOAD_FAST                'cf'
               76  LOAD_METHOD              has_section
               78  LOAD_FAST                'section'
               80  CALL_METHOD_1         1  ''
               82  POP_JUMP_IF_FALSE    96  'to 96'

 L.  26        84  LOAD_GLOBAL              len
               86  LOAD_FAST                'cf'
               88  LOAD_FAST                'section'
               90  BINARY_SUBSCR    
               92  CALL_FUNCTION_1       1  ''
               94  STORE_FAST               'ret'
             96_0  COME_FROM            82  '82'
             96_1  COME_FROM            72  '72'

 L.  27        96  LOAD_FAST                'ret'
               98  POP_BLOCK        
              100  RETURN_VALUE     
            102_0  COME_FROM_FINALLY     0  '0'

 L.  28       102  POP_TOP          
              104  POP_TOP          
              106  POP_TOP          

 L.  29       108  POP_EXCEPT       
              110  LOAD_CONST               0
              112  RETURN_VALUE     
              114  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 98


def Sections--- This code section failed: ---

 L.  33         0  SETUP_FINALLY        30  'to 30'

 L.  34         2  LOAD_GLOBAL              configparser
                4  LOAD_METHOD              ConfigParser
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'cf'

 L.  35        10  LOAD_FAST                'cf'
               12  LOAD_METHOD              read
               14  LOAD_FAST                'fileName'
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          

 L.  36        20  LOAD_FAST                'cf'
               22  LOAD_METHOD              sections
               24  CALL_METHOD_0         0  ''
               26  POP_BLOCK        
               28  RETURN_VALUE     
             30_0  COME_FROM_FINALLY     0  '0'

 L.  37        30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L.  38        36  POP_EXCEPT       
               38  LOAD_CONST               None
               40  RETURN_VALUE     
               42  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 28


def GetValue--- This code section failed: ---

 L.  42         0  SETUP_FINALLY        66  'to 66'

 L.  43         2  LOAD_GLOBAL              configparser
                4  LOAD_METHOD              ConfigParser
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'cf'

 L.  44        10  LOAD_FAST                'cf'
               12  LOAD_METHOD              read
               14  LOAD_FAST                'fileName'
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          

 L.  45        20  LOAD_FAST                'cf'
               22  LOAD_METHOD              has_section
               24  LOAD_FAST                'section'
               26  CALL_METHOD_1         1  ''
               28  POP_JUMP_IF_TRUE     36  'to 36'

 L.  46        30  LOAD_FAST                'default'
               32  POP_BLOCK        
               34  RETURN_VALUE     
             36_0  COME_FROM            28  '28'

 L.  48        36  LOAD_FAST                'key'
               38  LOAD_FAST                'cf'
               40  LOAD_FAST                'section'
               42  BINARY_SUBSCR    
               44  COMPARE_OP               in
               46  POP_JUMP_IF_FALSE    60  'to 60'

 L.  49        48  LOAD_FAST                'cf'
               50  LOAD_METHOD              get
               52  LOAD_FAST                'section'
               54  LOAD_FAST                'key'
               56  CALL_METHOD_2         2  ''
               58  STORE_FAST               'default'
             60_0  COME_FROM            46  '46'

 L.  50        60  LOAD_FAST                'default'
               62  POP_BLOCK        
               64  RETURN_VALUE     
             66_0  COME_FROM_FINALLY     0  '0'

 L.  51        66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L.  52        72  LOAD_FAST                'default'
               74  ROT_FOUR         
               76  POP_EXCEPT       
               78  RETURN_VALUE     
               80  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 32


def SetValue--- This code section failed: ---

 L.  55         0  SETUP_FINALLY       126  'to 126'

 L.  56         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              access
                6  LOAD_FAST                'fileName'
                8  LOAD_CONST               0
               10  CALL_METHOD_2         2  ''
               12  LOAD_CONST               False
               14  COMPARE_OP               is
               16  POP_JUMP_IF_FALSE    36  'to 36'

 L.  57        18  LOAD_GLOBAL              open
               20  LOAD_FAST                'fileName'
               22  LOAD_STR                 'w'
               24  CALL_FUNCTION_2       2  ''
               26  STORE_FAST               'fp'

 L.  58        28  LOAD_FAST                'fp'
               30  LOAD_METHOD              close
               32  CALL_METHOD_0         0  ''
               34  POP_TOP          
             36_0  COME_FROM            16  '16'

 L.  60        36  LOAD_GLOBAL              configparser
               38  LOAD_METHOD              ConfigParser
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               'cf'

 L.  61        44  LOAD_FAST                'cf'
               46  LOAD_METHOD              read
               48  LOAD_FAST                'fileName'
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L.  62        54  LOAD_FAST                'cf'
               56  LOAD_METHOD              has_section
               58  LOAD_FAST                'section'
               60  CALL_METHOD_1         1  ''
               62  LOAD_CONST               False
               64  COMPARE_OP               is
               66  POP_JUMP_IF_FALSE    76  'to 76'

 L.  63        68  BUILD_MAP_0           0 
               70  LOAD_FAST                'cf'
               72  LOAD_FAST                'section'
               74  STORE_SUBSCR     
             76_0  COME_FROM            66  '66'

 L.  65        76  LOAD_FAST                'value'
               78  LOAD_FAST                'cf'
               80  LOAD_FAST                'section'
               82  BINARY_SUBSCR    
               84  LOAD_FAST                'key'
               86  STORE_SUBSCR     

 L.  66        88  LOAD_GLOBAL              open
               90  LOAD_FAST                'fileName'
               92  LOAD_STR                 'w'
               94  CALL_FUNCTION_2       2  ''
               96  SETUP_WITH          114  'to 114'
               98  STORE_FAST               'f'

 L.  67       100  LOAD_FAST                'cf'
              102  LOAD_METHOD              write
              104  LOAD_FAST                'f'
              106  CALL_METHOD_1         1  ''
              108  POP_TOP          
              110  POP_BLOCK        
              112  BEGIN_FINALLY    
            114_0  COME_FROM_WITH       96  '96'
              114  WITH_CLEANUP_START
              116  WITH_CLEANUP_FINISH
              118  END_FINALLY      

 L.  68       120  POP_BLOCK        
              122  LOAD_CONST               True
              124  RETURN_VALUE     
            126_0  COME_FROM_FINALLY     0  '0'

 L.  69       126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          

 L.  70       132  POP_EXCEPT       
              134  LOAD_CONST               False
              136  RETURN_VALUE     
              138  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 112


def ParseNoEqual--- This code section failed: ---

 L.  74         0  BUILD_MAP_0           0 
                2  STORE_FAST               'ret'

 L.  75         4  SETUP_FINALLY       170  'to 170'

 L.  76         6  LOAD_GLOBAL              open
                8  LOAD_FAST                'fileName'
               10  LOAD_STR                 'r'
               12  CALL_FUNCTION_2       2  ''
               14  STORE_FAST               'fd'

 L.  77        16  LOAD_FAST                'fd'
               18  LOAD_METHOD              readlines
               20  CALL_METHOD_0         0  ''
               22  STORE_FAST               'arr'

 L.  78        24  LOAD_CONST               None
               26  STORE_FAST               'group'

 L.  79        28  LOAD_FAST                'arr'
               30  GET_ITER         
               32  FOR_ITER            164  'to 164'
               34  STORE_FAST               'item'

 L.  80        36  LOAD_FAST                'item'
               38  LOAD_METHOD              strip
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               'item'

 L.  81        44  LOAD_GLOBAL              len
               46  LOAD_FAST                'item'
               48  CALL_FUNCTION_1       1  ''
               50  LOAD_CONST               0
               52  COMPARE_OP               <=
               54  POP_JUMP_IF_FALSE    58  'to 58'

 L.  82        56  JUMP_BACK            32  'to 32'
             58_0  COME_FROM            54  '54'

 L.  83        58  LOAD_FAST                'item'
               60  LOAD_CONST               0
               62  BINARY_SUBSCR    
               64  LOAD_STR                 '#'
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    74  'to 74'

 L.  84        70  CONTINUE             32  'to 32'
               72  JUMP_BACK            32  'to 32'
             74_0  COME_FROM            68  '68'

 L.  85        74  LOAD_FAST                'item'
               76  LOAD_CONST               0
               78  BINARY_SUBSCR    
               80  LOAD_STR                 '['
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE   136  'to 136'
               86  LOAD_FAST                'item'
               88  LOAD_GLOBAL              len
               90  LOAD_FAST                'item'
               92  CALL_FUNCTION_1       1  ''
               94  LOAD_CONST               1
               96  BINARY_SUBTRACT  
               98  BINARY_SUBSCR    
              100  LOAD_STR                 ']'
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   136  'to 136'

 L.  86       106  LOAD_FAST                'item'
              108  LOAD_CONST               1
              110  LOAD_GLOBAL              len
              112  LOAD_FAST                'item'
              114  CALL_FUNCTION_1       1  ''
              116  LOAD_CONST               1
              118  BINARY_SUBTRACT  
              120  BUILD_SLICE_2         2 
              122  BINARY_SUBSCR    
              124  STORE_FAST               'group'

 L.  87       126  BUILD_LIST_0          0 
              128  LOAD_FAST                'ret'
              130  LOAD_FAST                'group'
              132  STORE_SUBSCR     
              134  JUMP_BACK            32  'to 32'
            136_0  COME_FROM           104  '104'
            136_1  COME_FROM            84  '84'

 L.  88       136  LOAD_FAST                'group'
              138  LOAD_CONST               None
              140  COMPARE_OP               is
              142  POP_JUMP_IF_FALSE   148  'to 148'

 L.  89       144  CONTINUE             32  'to 32'
              146  JUMP_BACK            32  'to 32'
            148_0  COME_FROM           142  '142'

 L.  91       148  LOAD_FAST                'ret'
              150  LOAD_FAST                'group'
              152  BINARY_SUBSCR    
              154  LOAD_METHOD              append
              156  LOAD_FAST                'item'
              158  CALL_METHOD_1         1  ''
              160  POP_TOP          
              162  JUMP_BACK            32  'to 32'

 L.  92       164  LOAD_FAST                'ret'
              166  POP_BLOCK        
              168  RETURN_VALUE     
            170_0  COME_FROM_FINALLY     4  '4'

 L.  93       170  POP_TOP          
              172  POP_TOP          
              174  POP_TOP          

 L.  94       176  LOAD_FAST                'ret'
              178  ROT_FOUR         
              180  POP_EXCEPT       
              182  RETURN_VALUE     
              184  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 166
# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\aigpy\convertHelper.py
# Compiled at: 2020-02-14 02:12:37
# Size of source mod 2**32: 1574 bytes


def convertStorageUnit--- This code section failed: ---

 L.   9         0  SETUP_FINALLY       168  'to 168'

 L.  10         2  LOAD_STR                 'gb'
                4  LOAD_STR                 'mb'
                6  LOAD_STR                 'kb'
                8  LOAD_STR                 'byte'
               10  BUILD_LIST_4          4 
               12  STORE_FAST               'units'

 L.  11        14  LOAD_FAST                'srcUnit'
               16  LOAD_FAST                'units'
               18  COMPARE_OP               not-in
               20  POP_JUMP_IF_TRUE     30  'to 30'
               22  LOAD_FAST                'desUnit'
               24  LOAD_FAST                'units'
               26  COMPARE_OP               not-in
               28  POP_JUMP_IF_FALSE    36  'to 36'
             30_0  COME_FROM            20  '20'

 L.  12        30  POP_BLOCK        
               32  LOAD_CONST               None
               34  RETURN_VALUE     
             36_0  COME_FROM            28  '28'

 L.  13        36  LOAD_FAST                'srcUnit'
               38  LOAD_FAST                'desUnit'
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    50  'to 50'

 L.  14        44  LOAD_FAST                'num'
               46  POP_BLOCK        
               48  RETURN_VALUE     
             50_0  COME_FROM            42  '42'

 L.  15        50  LOAD_GLOBAL              float
               52  LOAD_FAST                'num'
               54  CALL_FUNCTION_1       1  ''
               56  STORE_FAST               'num'

 L.  16        58  LOAD_FAST                'num'
               60  LOAD_CONST               0
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    72  'to 72'

 L.  17        66  POP_BLOCK        
               68  LOAD_CONST               0
               70  RETURN_VALUE     
             72_0  COME_FROM            64  '64'

 L.  18        72  LOAD_FAST                'units'
               74  LOAD_METHOD              index
               76  LOAD_FAST                'srcUnit'
               78  CALL_METHOD_1         1  ''
               80  STORE_FAST               'srcIndex'

 L.  19        82  LOAD_FAST                'units'
               84  LOAD_METHOD              index
               86  LOAD_FAST                'desUnit'
               88  CALL_METHOD_1         1  ''
               90  STORE_FAST               'desIndex'

 L.  20        92  LOAD_FAST                'desIndex'
               94  LOAD_FAST                'srcIndex'
               96  BINARY_SUBTRACT  
               98  STORE_FAST               'tmp'

 L.  21       100  LOAD_FAST                'tmp'
              102  LOAD_CONST               0
              104  COMPARE_OP               !=
              106  POP_JUMP_IF_FALSE   162  'to 162'

 L.  22       108  LOAD_FAST                'srcIndex'
              110  LOAD_FAST                'desIndex'
              112  COMPARE_OP               <
              114  POP_JUMP_IF_FALSE   126  'to 126'

 L.  23       116  LOAD_FAST                'num'
              118  LOAD_CONST               1024
              120  BINARY_MULTIPLY  
              122  STORE_FAST               'num'
              124  JUMP_FORWARD        134  'to 134'
            126_0  COME_FROM           114  '114'

 L.  25       126  LOAD_FAST                'num'
              128  LOAD_CONST               1024
              130  BINARY_TRUE_DIVIDE
              132  STORE_FAST               'num'
            134_0  COME_FROM           124  '124'

 L.  26       134  LOAD_FAST                'tmp'
              136  LOAD_CONST               0
              138  COMPARE_OP               >
              140  POP_JUMP_IF_FALSE   152  'to 152'

 L.  27       142  LOAD_FAST                'tmp'
              144  LOAD_CONST               1
              146  BINARY_SUBTRACT  
              148  STORE_FAST               'tmp'
              150  JUMP_BACK           100  'to 100'
            152_0  COME_FROM           140  '140'

 L.  29       152  LOAD_FAST                'tmp'
              154  LOAD_CONST               1
              156  BINARY_ADD       
              158  STORE_FAST               'tmp'
              160  JUMP_BACK           100  'to 100'
            162_0  COME_FROM           106  '106'

 L.  30       162  LOAD_FAST                'num'
              164  POP_BLOCK        
              166  RETURN_VALUE     
            168_0  COME_FROM_FINALLY     0  '0'

 L.  31       168  POP_TOP          
              170  POP_TOP          
              172  POP_TOP          

 L.  32       174  POP_EXCEPT       
              176  LOAD_CONST               None
              178  RETURN_VALUE     
              180  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 32


def convertStorageUnitToString--- This code section failed: ---

 L.  39         0  SETUP_FINALLY       192  'to 192'

 L.  40         2  LOAD_STR                 'gb'
                4  LOAD_STR                 'mb'
                6  LOAD_STR                 'kb'
                8  LOAD_STR                 'byte'
               10  BUILD_LIST_4          4 
               12  STORE_FAST               'units'

 L.  41        14  LOAD_FAST                'srcUnit'
               16  LOAD_FAST                'units'
               18  COMPARE_OP               not-in
               20  POP_JUMP_IF_FALSE    28  'to 28'

 L.  42        22  POP_BLOCK        
               24  LOAD_STR                 '0 KB'
               26  RETURN_VALUE     
             28_0  COME_FROM            20  '20'

 L.  43        28  LOAD_GLOBAL              float
               30  LOAD_FAST                'num'
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'num'

 L.  44        36  LOAD_FAST                'units'
               38  LOAD_METHOD              index
               40  LOAD_FAST                'srcUnit'
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'srcIndex'

 L.  45        46  LOAD_FAST                'srcIndex'
               48  LOAD_CONST               0
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    86  'to 86'

 L.  46        54  LOAD_GLOBAL              str
               56  LOAD_GLOBAL              round
               58  LOAD_FAST                'num'
               60  LOAD_CONST               2
               62  CALL_FUNCTION_2       2  ''
               64  CALL_FUNCTION_1       1  ''
               66  LOAD_STR                 ' '
               68  BINARY_ADD       
               70  LOAD_FAST                'units'
               72  LOAD_CONST               0
               74  BINARY_SUBSCR    
               76  LOAD_METHOD              upper
               78  CALL_METHOD_0         0  ''
               80  BINARY_ADD       
               82  POP_BLOCK        
               84  RETURN_VALUE     
             86_0  COME_FROM            52  '52'

 L.  48        86  LOAD_FAST                'num'
               88  STORE_FAST               'tmp'

 L.  49        90  LOAD_FAST                'srcIndex'
               92  LOAD_CONST               0
               94  COMPARE_OP               !=
               96  POP_JUMP_IF_FALSE   160  'to 160'

 L.  50        98  LOAD_FAST                'num'
              100  LOAD_CONST               1024
              102  BINARY_TRUE_DIVIDE
              104  STORE_FAST               'num'

 L.  51       106  LOAD_FAST                'num'
              108  LOAD_CONST               1
              110  COMPARE_OP               <
              112  POP_JUMP_IF_FALSE   146  'to 146'

 L.  52       114  LOAD_GLOBAL              str
              116  LOAD_GLOBAL              round
              118  LOAD_FAST                'tmp'
              120  LOAD_CONST               2
              122  CALL_FUNCTION_2       2  ''
              124  CALL_FUNCTION_1       1  ''
              126  LOAD_STR                 ' '
              128  BINARY_ADD       
              130  LOAD_FAST                'units'
              132  LOAD_FAST                'srcIndex'
              134  BINARY_SUBSCR    
              136  LOAD_METHOD              upper
              138  CALL_METHOD_0         0  ''
              140  BINARY_ADD       
              142  POP_BLOCK        
              144  RETURN_VALUE     
            146_0  COME_FROM           112  '112'

 L.  53       146  LOAD_FAST                'num'
              148  STORE_FAST               'tmp'

 L.  54       150  LOAD_FAST                'srcIndex'
              152  LOAD_CONST               1
              154  BINARY_SUBTRACT  
              156  STORE_FAST               'srcIndex'
              158  JUMP_BACK            90  'to 90'
            160_0  COME_FROM            96  '96'

 L.  55       160  LOAD_GLOBAL              str
              162  LOAD_GLOBAL              round
              164  LOAD_FAST                'tmp'
              166  LOAD_CONST               2
              168  CALL_FUNCTION_2       2  ''
              170  CALL_FUNCTION_1       1  ''
              172  LOAD_STR                 ' '
              174  BINARY_ADD       
              176  LOAD_FAST                'units'
              178  LOAD_FAST                'srcIndex'
              180  BINARY_SUBSCR    
              182  LOAD_METHOD              upper
              184  CALL_METHOD_0         0  ''
              186  BINARY_ADD       
              188  POP_BLOCK        
              190  RETURN_VALUE     
            192_0  COME_FROM_FINALLY     0  '0'

 L.  56       192  POP_TOP          
              194  POP_TOP          
              196  POP_TOP          

 L.  57       198  POP_EXCEPT       
              200  LOAD_STR                 '0 KB'
              202  RETURN_VALUE     
              204  END_FINALLY      

Parse error at or near `LOAD_STR' instruction at offset 24
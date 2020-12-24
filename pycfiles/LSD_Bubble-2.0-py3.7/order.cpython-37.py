# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/LSD/dfs_tree/order.py
# Compiled at: 2019-01-31 04:58:01
# Size of source mod 2**32: 1330 bytes
from LSD.hashed_list import HashedList
from LSD.colors import GREY, BLACK

def create_dfs_order_cycle--- This code section failed: ---

 L.   6         0  LOAD_GLOBAL              HashedList
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  STORE_FAST               'order'

 L.   7         6  LOAD_FAST                'v'
                8  BUILD_LIST_1          1 
               10  STORE_FAST               'stack'

 L.   8        12  LOAD_CONST               True
               14  STORE_FAST               'cycle'

 L.   9        16  LOAD_CONST               None
               18  STORE_FAST               'v2'

 L.  10        20  SETUP_LOOP          210  'to 210'
             22_0  COME_FROM           182  '182'
               22  LOAD_FAST                'stack'
               24  POP_JUMP_IF_FALSE   208  'to 208'

 L.  11        26  LOAD_FAST                'stack'
               28  LOAD_CONST               -1
               30  BINARY_SUBSCR    
               32  STORE_FAST               'u'

 L.  12        34  LOAD_FAST                'g'
               36  LOAD_METHOD              get_color
               38  LOAD_FAST                'u'
               40  CALL_METHOD_1         1  '1 positional argument'
               42  STORE_FAST               'c'

 L.  13        44  LOAD_FAST                'c'
               46  LOAD_GLOBAL              GREY
               48  COMPARE_OP               !=
               50  POP_JUMP_IF_FALSE   168  'to 168'
               52  LOAD_FAST                'c'
               54  LOAD_GLOBAL              BLACK
               56  COMPARE_OP               !=
               58  POP_JUMP_IF_FALSE   168  'to 168'

 L.  14        60  LOAD_FAST                'g'
               62  LOAD_METHOD              set_color
               64  LOAD_FAST                'u'
               66  LOAD_GLOBAL              GREY
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  POP_TOP          

 L.  15        72  SETUP_LOOP          206  'to 206'
               74  LOAD_FAST                'g'
               76  LOAD_METHOD              successors
               78  LOAD_FAST                'u'
               80  CALL_METHOD_1         1  '1 positional argument'
               82  GET_ITER         
             84_0  COME_FROM           150  '150'
             84_1  COME_FROM           142  '142'
               84  FOR_ITER            164  'to 164'
               86  STORE_FAST               'w'

 L.  16        88  LOAD_FAST                'cycle'
               90  POP_JUMP_IF_FALSE   126  'to 126'
               92  LOAD_FAST                'w'
               94  LOAD_FAST                'v'
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE   126  'to 126'

 L.  17       100  LOAD_STR                 '{v}_split_duplicate'
              102  LOAD_ATTR                format
              104  LOAD_FAST                'v'
              106  LOAD_CONST               ('v',)
              108  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              110  STORE_FAST               'v2'

 L.  18       112  LOAD_FAST                'order'
              114  LOAD_METHOD              append
              116  LOAD_FAST                'v2'
              118  CALL_METHOD_1         1  '1 positional argument'
              120  POP_TOP          

 L.  19       122  LOAD_CONST               False
              124  STORE_FAST               'cycle'
            126_0  COME_FROM            98  '98'
            126_1  COME_FROM            90  '90'

 L.  20       126  LOAD_FAST                'g'
              128  LOAD_METHOD              get_color
              130  LOAD_FAST                'w'
              132  CALL_METHOD_1         1  '1 positional argument'
              134  STORE_FAST               'color'

 L.  21       136  LOAD_FAST                'color'
              138  LOAD_GLOBAL              GREY
              140  COMPARE_OP               !=
              142  POP_JUMP_IF_FALSE    84  'to 84'
              144  LOAD_FAST                'color'
              146  LOAD_GLOBAL              BLACK
              148  COMPARE_OP               !=
              150  POP_JUMP_IF_FALSE    84  'to 84'

 L.  22       152  LOAD_FAST                'stack'
              154  LOAD_METHOD              append
              156  LOAD_FAST                'w'
              158  CALL_METHOD_1         1  '1 positional argument'
              160  POP_TOP          
              162  JUMP_BACK            84  'to 84'
              164  POP_BLOCK        
              166  JUMP_BACK            22  'to 22'
            168_0  COME_FROM            58  '58'
            168_1  COME_FROM            50  '50'

 L.  24       168  LOAD_FAST                'stack'
              170  LOAD_METHOD              pop
              172  CALL_METHOD_0         0  '0 positional arguments'
              174  POP_TOP          

 L.  25       176  LOAD_FAST                'c'
              178  LOAD_GLOBAL              GREY
              180  COMPARE_OP               ==
              182  POP_JUMP_IF_FALSE    22  'to 22'

 L.  26       184  LOAD_FAST                'order'
              186  LOAD_METHOD              append
              188  LOAD_FAST                'u'
              190  CALL_METHOD_1         1  '1 positional argument'
              192  POP_TOP          

 L.  27       194  LOAD_FAST                'g'
              196  LOAD_METHOD              set_color
              198  LOAD_FAST                'u'
              200  LOAD_GLOBAL              BLACK
              202  CALL_METHOD_2         2  '2 positional arguments'
              204  POP_TOP          
            206_0  COME_FROM_LOOP       72  '72'
              206  JUMP_BACK            22  'to 22'
            208_0  COME_FROM            24  '24'
              208  POP_BLOCK        
            210_0  COME_FROM_LOOP       20  '20'

 L.  28       210  LOAD_FAST                'order'
              212  LOAD_FAST                'v2'
              214  BUILD_TUPLE_2         2 
              216  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 208_0


def create_dfs_order--- This code section failed: ---

 L.  32         0  LOAD_GLOBAL              HashedList
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  STORE_FAST               'order'

 L.  33         6  LOAD_FAST                'v'
                8  BUILD_LIST_1          1 
               10  STORE_FAST               'stack'

 L.  34        12  SETUP_LOOP          164  'to 164'
             14_0  COME_FROM           136  '136'
               14  LOAD_FAST                'stack'
               16  POP_JUMP_IF_FALSE   162  'to 162'

 L.  35        18  LOAD_FAST                'stack'
               20  LOAD_CONST               -1
               22  BINARY_SUBSCR    
               24  STORE_FAST               'u'

 L.  36        26  LOAD_FAST                'g'
               28  LOAD_METHOD              get_color
               30  LOAD_FAST                'u'
               32  CALL_METHOD_1         1  '1 positional argument'
               34  STORE_FAST               'c'

 L.  37        36  LOAD_FAST                'c'
               38  LOAD_GLOBAL              GREY
               40  COMPARE_OP               !=
               42  POP_JUMP_IF_FALSE   122  'to 122'
               44  LOAD_FAST                'c'
               46  LOAD_GLOBAL              BLACK
               48  COMPARE_OP               !=
               50  POP_JUMP_IF_FALSE   122  'to 122'

 L.  38        52  LOAD_FAST                'g'
               54  LOAD_METHOD              set_color
               56  LOAD_FAST                'u'
               58  LOAD_GLOBAL              GREY
               60  CALL_METHOD_2         2  '2 positional arguments'
               62  POP_TOP          

 L.  39        64  SETUP_LOOP          160  'to 160'
               66  LOAD_FAST                'g'
               68  LOAD_METHOD              successors
               70  LOAD_FAST                'u'
               72  CALL_METHOD_1         1  '1 positional argument'
               74  GET_ITER         
             76_0  COME_FROM           104  '104'
             76_1  COME_FROM            96  '96'
               76  FOR_ITER            118  'to 118'
               78  STORE_FAST               'w'

 L.  40        80  LOAD_FAST                'g'
               82  LOAD_METHOD              get_color
               84  LOAD_FAST                'w'
               86  CALL_METHOD_1         1  '1 positional argument'
               88  STORE_FAST               'color'

 L.  41        90  LOAD_FAST                'color'
               92  LOAD_GLOBAL              GREY
               94  COMPARE_OP               !=
               96  POP_JUMP_IF_FALSE    76  'to 76'
               98  LOAD_FAST                'color'
              100  LOAD_GLOBAL              BLACK
              102  COMPARE_OP               !=
              104  POP_JUMP_IF_FALSE    76  'to 76'

 L.  42       106  LOAD_FAST                'stack'
              108  LOAD_METHOD              append
              110  LOAD_FAST                'w'
              112  CALL_METHOD_1         1  '1 positional argument'
              114  POP_TOP          
              116  JUMP_BACK            76  'to 76'
              118  POP_BLOCK        
              120  JUMP_BACK            14  'to 14'
            122_0  COME_FROM            50  '50'
            122_1  COME_FROM            42  '42'

 L.  44       122  LOAD_FAST                'stack'
              124  LOAD_METHOD              pop
              126  CALL_METHOD_0         0  '0 positional arguments'
              128  POP_TOP          

 L.  45       130  LOAD_FAST                'c'
              132  LOAD_GLOBAL              GREY
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE    14  'to 14'

 L.  46       138  LOAD_FAST                'order'
              140  LOAD_METHOD              append
              142  LOAD_FAST                'u'
              144  CALL_METHOD_1         1  '1 positional argument'
              146  POP_TOP          

 L.  47       148  LOAD_FAST                'g'
              150  LOAD_METHOD              set_color
              152  LOAD_FAST                'u'
              154  LOAD_GLOBAL              BLACK
              156  CALL_METHOD_2         2  '2 positional arguments'
              158  POP_TOP          
            160_0  COME_FROM_LOOP       64  '64'
              160  JUMP_BACK            14  'to 14'
            162_0  COME_FROM            16  '16'
              162  POP_BLOCK        
            164_0  COME_FROM_LOOP       12  '12'

 L.  48       164  LOAD_FAST                'order'
              166  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 162_0
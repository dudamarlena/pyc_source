# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/plugins/fastclean.py
# Compiled at: 2018-03-06 06:50:33
# Size of source mod 2**32: 1434 bytes
"""A utility to set to zero all points below a ratio

"""
from __future__ import print_function
from spike import NPKError
from spike.NPKData import NPKData_plugin
from spike.util.signal_tools import findnoiselevel

def fastclean--- This code section failed: ---

 L.  26         0  LOAD_FAST                'npkd'
                2  LOAD_METHOD              test_axis
                4  LOAD_FAST                'axis'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'todo'

 L.  27        10  LOAD_FAST                'npkd'
               12  LOAD_ATTR                dim
               14  LOAD_CONST               1
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    52  'to 52'

 L.  28        20  LOAD_GLOBAL              findnoiselevel
               22  LOAD_FAST                'npkd'
               24  LOAD_METHOD              get_buffer
               26  CALL_METHOD_0         0  '0 positional arguments'
               28  LOAD_FAST                'nbseg'
               30  LOAD_CONST               ('nbseg',)
               32  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               34  STORE_FAST               'noise'

 L.  29        36  LOAD_FAST                'npkd'
               38  LOAD_METHOD              zeroing
               40  LOAD_FAST                'nsigma'
               42  LOAD_FAST                'noise'
               44  BINARY_MULTIPLY  
               46  CALL_METHOD_1         1  '1 positional argument'
               48  POP_TOP          
               50  JUMP_FORWARD        186  'to 186'
             52_0  COME_FROM            18  '18'

 L.  30        52  LOAD_FAST                'npkd'
               54  LOAD_ATTR                dim
               56  LOAD_CONST               2
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE   178  'to 178'

 L.  31        62  LOAD_FAST                'todo'
               64  LOAD_CONST               2
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE   120  'to 120'

 L.  32        70  SETUP_LOOP          176  'to 176'
               72  LOAD_GLOBAL              xrange
               74  LOAD_FAST                'npkd'
               76  LOAD_ATTR                size1
               78  CALL_FUNCTION_1       1  '1 positional argument'
               80  GET_ITER         
               82  FOR_ITER            116  'to 116'
               84  STORE_FAST               'i'

 L.  33        86  LOAD_FAST                'npkd'
               88  LOAD_METHOD              set_row
               90  LOAD_FAST                'i'
               92  LOAD_FAST                'npkd'
               94  LOAD_METHOD              row
               96  LOAD_FAST                'i'
               98  CALL_METHOD_1         1  '1 positional argument'
              100  LOAD_ATTR                fastclean
              102  LOAD_FAST                'nsigma'
              104  LOAD_FAST                'nbseg'
              106  LOAD_CONST               ('nsigma', 'nbseg')
              108  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              110  CALL_METHOD_2         2  '2 positional arguments'
              112  POP_TOP          
              114  JUMP_BACK            82  'to 82'
              116  POP_BLOCK        
              118  JUMP_ABSOLUTE       186  'to 186'
            120_0  COME_FROM            68  '68'

 L.  34       120  LOAD_FAST                'todo'
              122  LOAD_CONST               1
              124  COMPARE_OP               ==
              126  POP_JUMP_IF_FALSE   186  'to 186'

 L.  35       128  SETUP_LOOP          186  'to 186'
              130  LOAD_GLOBAL              xrange
              132  LOAD_FAST                'npkd'
              134  LOAD_ATTR                size2
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  GET_ITER         
              140  FOR_ITER            174  'to 174'
              142  STORE_FAST               'i'

 L.  36       144  LOAD_FAST                'npkd'
              146  LOAD_METHOD              set_col
              148  LOAD_FAST                'i'
              150  LOAD_FAST                'npkd'
              152  LOAD_METHOD              col
              154  LOAD_FAST                'i'
              156  CALL_METHOD_1         1  '1 positional argument'
              158  LOAD_ATTR                fastclean
              160  LOAD_FAST                'nsigma'
              162  LOAD_FAST                'nbseg'
              164  LOAD_CONST               ('nsigma', 'nbseg')
              166  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              168  CALL_METHOD_2         2  '2 positional arguments'
              170  POP_TOP          
              172  JUMP_BACK           140  'to 140'
              174  POP_BLOCK        
            176_0  COME_FROM_LOOP      128  '128'
            176_1  COME_FROM_LOOP       70  '70'
              176  JUMP_FORWARD        186  'to 186'
            178_0  COME_FROM            60  '60'

 L.  38       178  LOAD_GLOBAL              NPKError
              180  LOAD_STR                 'a faire'
              182  CALL_FUNCTION_1       1  '1 positional argument'
              184  RAISE_VARARGS_1       1  'exception instance'
            186_0  COME_FROM           176  '176'
            186_1  COME_FROM           126  '126'
            186_2  COME_FROM            50  '50'

 L.  39       186  LOAD_FAST                'npkd'
              188  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 176_1


NPKData_plugin('fastclean', fastclean)
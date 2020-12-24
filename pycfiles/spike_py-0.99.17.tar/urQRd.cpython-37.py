# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/plugins/urQRd.py
# Compiled at: 2018-03-06 06:50:33
# Size of source mod 2**32: 1931 bytes
"""plugin for the urQRd denoising method"""
from __future__ import print_function
import unittest
from spike.NPKData import NPKData_plugin, as_cpx, as_float, _base_fft, _base_ifft, _base_rfft, _base_irfft
import spike.Algo.urQRd as urQRd
from spike.util.signal_tools import filtering
import sys
if sys.version_info[0] < 3:
    pass
else:
    xrange = range

def urqrd--- This code section failed: ---

 L.  27         0  LOAD_FAST                'npkd'
                2  LOAD_ATTR                dim
                4  LOAD_CONST               1
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE   118  'to 118'

 L.  28        10  LOAD_FAST                'npkd'
               12  LOAD_ATTR                axis1
               14  LOAD_ATTR                itype
               16  LOAD_CONST               0
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    42  'to 42'

 L.  29        22  LOAD_GLOBAL              as_cpx
               24  LOAD_GLOBAL              _base_ifft
               26  LOAD_GLOBAL              _base_rfft
               28  LOAD_FAST                'npkd'
               30  LOAD_ATTR                buffer
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  CALL_FUNCTION_1       1  '1 positional argument'
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  STORE_FAST               'buff'
               40  JUMP_FORWARD         50  'to 50'
             42_0  COME_FROM            20  '20'

 L.  31        42  LOAD_FAST                'npkd'
               44  LOAD_METHOD              get_buffer
               46  CALL_METHOD_0         0  '0 positional arguments'
               48  STORE_FAST               'buff'
             50_0  COME_FROM            40  '40'

 L.  32        50  LOAD_GLOBAL              urQRd
               52  LOAD_FAST                'buff'
               54  LOAD_FAST                'k'
               56  LOAD_FAST                'orda'
               58  LOAD_FAST                'iterations'
               60  LOAD_CONST               ('orda', 'iterations')
               62  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               64  STORE_FAST               'urqrd_result'

 L.  33        66  LOAD_FAST                'npkd'
               68  LOAD_ATTR                axis1
               70  LOAD_ATTR                itype
               72  LOAD_CONST               0
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE   106  'to 106'

 L.  34        78  LOAD_GLOBAL              _base_irfft
               80  LOAD_GLOBAL              _base_fft
               82  LOAD_GLOBAL              as_float
               84  LOAD_FAST                'urqrd_result'
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  CALL_FUNCTION_1       1  '1 positional argument'
               90  CALL_FUNCTION_1       1  '1 positional argument'
               92  STORE_FAST               'buff'

 L.  35        94  LOAD_FAST                'npkd'
               96  LOAD_METHOD              set_buffer
               98  LOAD_FAST                'buff'
              100  CALL_METHOD_1         1  '1 positional argument'
              102  POP_TOP          
              104  JUMP_FORWARD        116  'to 116'
            106_0  COME_FROM            76  '76'

 L.  37       106  LOAD_GLOBAL              as_float
              108  LOAD_FAST                'urqrd_result'
              110  CALL_FUNCTION_1       1  '1 positional argument'
              112  LOAD_FAST                'npkd'
              114  STORE_ATTR               buffer
            116_0  COME_FROM           104  '104'
              116  JUMP_FORWARD        290  'to 290'
            118_0  COME_FROM             8  '8'

 L.  38       118  LOAD_FAST                'npkd'
              120  LOAD_ATTR                dim
              122  LOAD_CONST               2
              124  COMPARE_OP               ==
          126_128  POP_JUMP_IF_FALSE   270  'to 270'

 L.  39       130  LOAD_FAST                'npkd'
              132  LOAD_METHOD              test_axis
              134  LOAD_FAST                'axis'
              136  CALL_METHOD_1         1  '1 positional argument'
              138  STORE_FAST               'todo'

 L.  40       140  LOAD_FAST                'todo'
              142  LOAD_CONST               2
              144  COMPARE_OP               ==
              146  POP_JUMP_IF_FALSE   204  'to 204'

 L.  41       148  SETUP_LOOP          268  'to 268'
              150  LOAD_GLOBAL              xrange
              152  LOAD_FAST                'npkd'
              154  LOAD_ATTR                size1
              156  CALL_FUNCTION_1       1  '1 positional argument'
              158  GET_ITER         
              160  FOR_ITER            200  'to 200'
              162  STORE_FAST               'i'

 L.  42       164  LOAD_FAST                'npkd'
              166  LOAD_METHOD              row
              168  LOAD_FAST                'i'
              170  CALL_METHOD_1         1  '1 positional argument'
              172  LOAD_ATTR                urqrd
              174  LOAD_FAST                'k'
              176  LOAD_FAST                'orda'
              178  LOAD_FAST                'iterations'
              180  LOAD_CONST               ('k', 'orda', 'iterations')
              182  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              184  STORE_FAST               'r'

 L.  43       186  LOAD_FAST                'npkd'
              188  LOAD_METHOD              set_row
              190  LOAD_FAST                'i'
              192  LOAD_FAST                'r'
              194  CALL_METHOD_2         2  '2 positional arguments'
              196  POP_TOP          
              198  JUMP_BACK           160  'to 160'
              200  POP_BLOCK        
              202  JUMP_FORWARD        268  'to 268'
            204_0  COME_FROM           146  '146'

 L.  44       204  LOAD_FAST                'todo'
              206  LOAD_CONST               1
              208  COMPARE_OP               ==
          210_212  POP_JUMP_IF_FALSE   290  'to 290'

 L.  45       214  SETUP_LOOP          290  'to 290'
              216  LOAD_GLOBAL              xrange
              218  LOAD_FAST                'npkd'
              220  LOAD_ATTR                size2
              222  CALL_FUNCTION_1       1  '1 positional argument'
              224  GET_ITER         
              226  FOR_ITER            266  'to 266'
              228  STORE_FAST               'i'

 L.  46       230  LOAD_FAST                'npkd'
              232  LOAD_METHOD              col
              234  LOAD_FAST                'i'
              236  CALL_METHOD_1         1  '1 positional argument'
              238  LOAD_ATTR                urqrd
              240  LOAD_FAST                'k'
              242  LOAD_FAST                'orda'
              244  LOAD_FAST                'iterations'
              246  LOAD_CONST               ('k', 'orda', 'iterations')
              248  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              250  STORE_FAST               'r'

 L.  47       252  LOAD_FAST                'npkd'
              254  LOAD_METHOD              set_col
              256  LOAD_FAST                'i'
              258  LOAD_FAST                'r'
              260  CALL_METHOD_2         2  '2 positional arguments'
              262  POP_TOP          
              264  JUMP_BACK           226  'to 226'
              266  POP_BLOCK        
            268_0  COME_FROM_LOOP      214  '214'
            268_1  COME_FROM           202  '202'
            268_2  COME_FROM_LOOP      148  '148'
              268  JUMP_FORWARD        290  'to 290'
            270_0  COME_FROM           126  '126'

 L.  48       270  LOAD_FAST                'npkd'
              272  LOAD_ATTR                dim
              274  LOAD_CONST               3
              276  COMPARE_OP               ==
          278_280  POP_JUMP_IF_FALSE   290  'to 290'

 L.  49       282  LOAD_GLOBAL              Exception
              284  LOAD_STR                 'not implemented yet'
              286  CALL_FUNCTION_1       1  '1 positional argument'
              288  RAISE_VARARGS_1       1  'exception instance'
            290_0  COME_FROM           278  '278'
            290_1  COME_FROM           268  '268'
            290_2  COME_FROM           210  '210'
            290_3  COME_FROM           116  '116'

 L.  50       290  LOAD_FAST                'npkd'
              292  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 268_2


class urQRdTests(unittest.TestCase):
    pass


NPKData_plugin('urqrd', urqrd)
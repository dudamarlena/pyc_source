# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/plugins/sg.py
# Compiled at: 2018-03-06 06:50:33
# Size of source mod 2**32: 2286 bytes
"""set of function Savitsky-Golay smoothing

"""
from __future__ import print_function
from spike import NPKError
from spike.NPKData import NPKData_plugin
from spike.util.signal_tools import findnoiselevel

def sg--- This code section failed: ---

 L.  26         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME_ATTR         spike.Algo.savitzky_golay
                6  IMPORT_FROM              Algo
                8  ROT_TWO          
               10  POP_TOP          
               12  IMPORT_FROM              savitzky_golay
               14  STORE_FAST               'sgm'
               16  POP_TOP          

 L.  27        18  LOAD_FAST                'npkd'
               20  LOAD_METHOD              test_axis
               22  LOAD_FAST                'axis'
               24  CALL_METHOD_1         1  '1 positional argument'
               26  STORE_FAST               'todo'

 L.  28        28  LOAD_FAST                'sgm'
               30  LOAD_ATTR                sgolay_coef
               32  LOAD_FAST                'window_size'
               34  LOAD_FAST                'order'
               36  LOAD_CONST               0
               38  LOAD_CONST               ('deriv',)
               40  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               42  STORE_FAST               'm'

 L.  29        44  LOAD_FAST                'npkd'
               46  LOAD_ATTR                dim
               48  LOAD_CONST               1
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    80  'to 80'

 L.  30        54  LOAD_FAST                'npkd'
               56  LOAD_METHOD              set_buffer
               58  LOAD_FAST                'sgm'
               60  LOAD_METHOD              sgolay_comp
               62  LOAD_FAST                'npkd'
               64  LOAD_METHOD              get_buffer
               66  CALL_METHOD_0         0  '0 positional arguments'
               68  LOAD_FAST                'm'
               70  LOAD_FAST                'window_size'
               72  CALL_METHOD_3         3  '3 positional arguments'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  POP_TOP          
               78  JUMP_FORWARD        244  'to 244'
             80_0  COME_FROM            52  '52'

 L.  31        80  LOAD_FAST                'npkd'
               82  LOAD_ATTR                dim
               84  LOAD_CONST               2
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE   236  'to 236'

 L.  32        90  LOAD_FAST                'todo'
               92  LOAD_CONST               2
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   162  'to 162'

 L.  33        98  SETUP_LOOP          234  'to 234'
              100  LOAD_GLOBAL              xrange
              102  LOAD_FAST                'npkd'
              104  LOAD_ATTR                size1
              106  CALL_FUNCTION_1       1  '1 positional argument'
              108  GET_ITER         
              110  FOR_ITER            158  'to 158'
              112  STORE_FAST               'i'

 L.  34       114  LOAD_FAST                'sgm'
              116  LOAD_METHOD              sgolay_comp
              118  LOAD_FAST                'npkd'
              120  LOAD_ATTR                buffer
              122  LOAD_FAST                'i'
              124  LOAD_CONST               None
              126  LOAD_CONST               None
              128  BUILD_SLICE_2         2 
              130  BUILD_TUPLE_2         2 
              132  BINARY_SUBSCR    
              134  LOAD_FAST                'm'
              136  LOAD_FAST                'window_size'
              138  CALL_METHOD_3         3  '3 positional arguments'
              140  LOAD_FAST                'npkd'
              142  LOAD_ATTR                buffer
              144  LOAD_FAST                'i'
              146  LOAD_CONST               None
              148  LOAD_CONST               None
              150  BUILD_SLICE_2         2 
              152  BUILD_TUPLE_2         2 
              154  STORE_SUBSCR     
              156  JUMP_BACK           110  'to 110'
              158  POP_BLOCK        
              160  JUMP_ABSOLUTE       244  'to 244'
            162_0  COME_FROM            96  '96'

 L.  35       162  LOAD_FAST                'todo'
              164  LOAD_CONST               1
              166  COMPARE_OP               ==
              168  POP_JUMP_IF_FALSE   244  'to 244'

 L.  36       170  SETUP_LOOP          244  'to 244'
              172  LOAD_GLOBAL              xrange
              174  LOAD_CONST               1
              176  LOAD_FAST                'npkd'
              178  LOAD_ATTR                size2
              180  CALL_FUNCTION_2       2  '2 positional arguments'
              182  GET_ITER         
              184  FOR_ITER            232  'to 232'
              186  STORE_FAST               'i'

 L.  37       188  LOAD_FAST                'sgm'
              190  LOAD_METHOD              sgolay_comp
              192  LOAD_FAST                'npkd'
              194  LOAD_ATTR                buffer
              196  LOAD_CONST               None
              198  LOAD_CONST               None
              200  BUILD_SLICE_2         2 
              202  LOAD_FAST                'i'
              204  BUILD_TUPLE_2         2 
              206  BINARY_SUBSCR    
              208  LOAD_FAST                'm'
              210  LOAD_FAST                'window_size'
              212  CALL_METHOD_3         3  '3 positional arguments'
              214  LOAD_FAST                'npkd'
              216  LOAD_ATTR                buffer
              218  LOAD_CONST               None
              220  LOAD_CONST               None
              222  BUILD_SLICE_2         2 
              224  LOAD_FAST                'i'
              226  BUILD_TUPLE_2         2 
              228  STORE_SUBSCR     
              230  JUMP_BACK           184  'to 184'
              232  POP_BLOCK        
            234_0  COME_FROM_LOOP      170  '170'
            234_1  COME_FROM_LOOP       98  '98'
              234  JUMP_FORWARD        244  'to 244'
            236_0  COME_FROM            88  '88'

 L.  39       236  LOAD_GLOBAL              NPKError
              238  LOAD_STR                 'a faire'
              240  CALL_FUNCTION_1       1  '1 positional argument'
              242  RAISE_VARARGS_1       1  'exception instance'
            244_0  COME_FROM           234  '234'
            244_1  COME_FROM           168  '168'
            244_2  COME_FROM            78  '78'

 L.  40       244  LOAD_FAST                'npkd'
              246  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 234_1


def sg2D(npkd, window_size, order, deriv=None):
    """applies a 2D Savitzky-Golay of order filter to data
    window_size : int
        the length of the square window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less than `window_size` - 1.
    deriv: None, 'col', or 'row'.   'both' mode does not work.
        the direction of the derivative to compute (default = None means only smoothing)
    can be applied to a 2D only.
    """
    import spike.Algo.savitzky_golay as sgm
    npkd.check2D
    npkd.set_buffersgm.savitzky_golay2D((npkd.get_buffer), window_size, order, derivative=deriv)
    return npkd


NPKData_plugin('sg', sg)
NPKData_plugin('sg2D', sg2D)
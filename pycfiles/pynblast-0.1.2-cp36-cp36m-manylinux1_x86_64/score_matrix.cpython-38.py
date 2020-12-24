# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/barnesc/work/code/nblast-rs/nblast-py/pynblast/score_matrix.py
# Compiled at: 2020-04-20 07:50:20
# Size of source mod 2**32: 1913 bytes
from typing import List, NamedTuple
import csv, numpy as np

def parse_interval(s):
    no_brackets = s.strip('([]) ')
    if not no_brackets:
        return
    low_high = no_brackets.split(',')
    if len(low_high) == 1:
        return float(low_high)
    return float(low_high[(-1)])


class ScoreMatrix(NamedTuple):
    dist_thresholds: List[float]
    dot_thresholds: List[float]
    values: np.ndarray

    def to_df(self):
        import pandas as pd
        return pd.DataFrame(self.values, self.dist_thresholds, self.dot_thresholds)

    @classmethod
    def read--- This code section failed: ---

 L.  43         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'fpath'
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH          182  'to 182'
                8  STORE_FAST               'f'

 L.  44        10  LOAD_GLOBAL              csv
               12  LOAD_ATTR                reader
               14  LOAD_FAST                'f'
               16  BUILD_TUPLE_1         1 
               18  LOAD_FAST                'csv_kwargs'
               20  CALL_FUNCTION_EX_KW     1  'keyword args'
               22  STORE_FAST               'reader'

 L.  45        24  LOAD_LISTCOMP            '<code_object <listcomp>>'
               26  LOAD_STR                 'ScoreMatrix.read.<locals>.<listcomp>'
               28  MAKE_FUNCTION_0          ''
               30  LOAD_GLOBAL              next
               32  LOAD_FAST                'reader'
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_CONST               1
               38  LOAD_CONST               None
               40  BUILD_SLICE_2         2 
               42  BINARY_SUBSCR    
               44  GET_ITER         
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'dot_bins'

 L.  47        50  BUILD_LIST_0          0 
               52  STORE_FAST               'dist_bins'

 L.  48        54  BUILD_LIST_0          0 
               56  STORE_FAST               'data'

 L.  49        58  LOAD_GLOBAL              enumerate
               60  LOAD_FAST                'reader'
               62  LOAD_CONST               1
               64  CALL_FUNCTION_2       2  ''
               66  GET_ITER         
               68  FOR_ITER            178  'to 178'
               70  UNPACK_SEQUENCE_2     2 
               72  STORE_FAST               'idx'
               74  STORE_FAST               'row'

 L.  50        76  LOAD_FAST                'dist_bins'
               78  LOAD_METHOD              append
               80  LOAD_GLOBAL              parse_interval
               82  LOAD_FAST                'row'
               84  LOAD_CONST               0
               86  BINARY_SUBSCR    
               88  CALL_FUNCTION_1       1  ''
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          

 L.  51        94  LOAD_LISTCOMP            '<code_object <listcomp>>'
               96  LOAD_STR                 'ScoreMatrix.read.<locals>.<listcomp>'
               98  MAKE_FUNCTION_0          ''
              100  LOAD_FAST                'row'
              102  LOAD_CONST               1
              104  LOAD_CONST               None
              106  BUILD_SLICE_2         2 
              108  BINARY_SUBSCR    
              110  GET_ITER         
              112  CALL_FUNCTION_1       1  ''
              114  STORE_FAST               'row_data'

 L.  52       116  LOAD_GLOBAL              len
              118  LOAD_FAST                'row_data'
              120  CALL_FUNCTION_1       1  ''
              122  LOAD_GLOBAL              len
              124  LOAD_FAST                'dot_bins'
              126  CALL_FUNCTION_1       1  ''
              128  COMPARE_OP               !=
              130  POP_JUMP_IF_FALSE   166  'to 166'

 L.  53       132  LOAD_GLOBAL              ValueError

 L.  54       134  LOAD_STR                 'Line '
              136  LOAD_FAST                'idx'
              138  FORMAT_VALUE          0  ''
              140  LOAD_STR                 ' has '
              142  LOAD_GLOBAL              len
              144  LOAD_FAST                'row_data'
              146  CALL_FUNCTION_1       1  ''
              148  FORMAT_VALUE          0  ''
              150  LOAD_STR                 ' values; expected '
              152  LOAD_GLOBAL              len
              154  LOAD_FAST                'dot_bins'
              156  CALL_FUNCTION_1       1  ''
              158  FORMAT_VALUE          0  ''
              160  BUILD_STRING_6        6 

 L.  53       162  CALL_FUNCTION_1       1  ''
              164  RAISE_VARARGS_1       1  ''
            166_0  COME_FROM           130  '130'

 L.  57       166  LOAD_FAST                'data'
              168  LOAD_METHOD              append
              170  LOAD_FAST                'row_data'
              172  CALL_METHOD_1         1  ''
              174  POP_TOP          
              176  JUMP_BACK            68  'to 68'
              178  POP_BLOCK        
              180  BEGIN_FINALLY    
            182_0  COME_FROM_WITH        6  '6'
              182  WITH_CLEANUP_START
              184  WITH_CLEANUP_FINISH
              186  END_FINALLY      

 L.  59       188  LOAD_FAST                'cls'
              190  LOAD_FAST                'dist_bins'
              192  LOAD_FAST                'dot_bins'
              194  LOAD_GLOBAL              np
              196  LOAD_METHOD              array
              198  LOAD_FAST                'data'
              200  CALL_METHOD_1         1  ''
              202  CALL_FUNCTION_3       3  ''
              204  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 180
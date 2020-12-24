# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/myroi2roi.py
# Compiled at: 2018-06-25 07:11:00
# Size of source mod 2**32: 1465 bytes
from __future__ import print_function
import numpy as np
from skimage.measure import grid_points_in_poly
import dicom_tools.roiFileHandler as roiFileHandler

def convert1roi(myroi, layershape, verbose=False):
    points = np.array(myroi['points'])
    shift = np.array(myroi['pos'])
    shift -= np.array([0.5, 0.5])
    if verbose:
        print(type(shift))
        print(myroi)
        print(points + shift)
    return grid_points_in_poly(layershape, points + shift)


def myroi2roi--- This code section failed: ---

 L.  18         0  LOAD_FAST                'verbose'
                2  POP_JUMP_IF_FALSE    22  'to 22'

 L.  19         4  LOAD_GLOBAL              print
                6  LOAD_STR                 'myroi2roi: called'
                8  CALL_FUNCTION_1       1  ''
               10  POP_TOP          

 L.  20        12  LOAD_GLOBAL              print
               14  LOAD_STR                 'myroi2roi: shape'
               16  LOAD_FAST                'shape'
               18  CALL_FUNCTION_2       2  ''
               20  POP_TOP          
             22_0  COME_FROM             2  '2'

 L.  21        22  LOAD_GLOBAL              np
               24  LOAD_ATTR                full
               26  LOAD_FAST                'shape'
               28  LOAD_CONST               False
               30  LOAD_GLOBAL              bool
               32  LOAD_CONST               ('dtype',)
               34  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               36  STORE_FAST               'outroi'

 L.  24        38  LOAD_FAST                'outroi'
               40  LOAD_ATTR                ndim
               42  LOAD_CONST               2
               44  COMPARE_OP               >
               46  POP_JUMP_IF_FALSE   184  'to 184'

 L.  25        48  LOAD_GLOBAL              len
               50  LOAD_FAST                'myrois'
               52  CALL_FUNCTION_1       1  ''
               54  LOAD_GLOBAL              len
               56  LOAD_FAST                'outroi'
               58  CALL_FUNCTION_1       1  ''
               60  COMPARE_OP               !=
               62  POP_JUMP_IF_FALSE    86  'to 86'

 L.  26        64  LOAD_GLOBAL              print
               66  LOAD_STR                 'error: len rois = '
               68  LOAD_GLOBAL              len
               70  LOAD_FAST                'myrois'
               72  CALL_FUNCTION_1       1  ''
               74  LOAD_STR                 ' but len dicom='
               76  LOAD_GLOBAL              len
               78  LOAD_FAST                'outroi'
               80  CALL_FUNCTION_1       1  ''
               82  CALL_FUNCTION_4       4  ''
               84  POP_TOP          
             86_0  COME_FROM            62  '62'

 L.  27        86  SETUP_LOOP          228  'to 228'
               88  LOAD_GLOBAL              enumerate
               90  LOAD_FAST                'myrois'
               92  CALL_FUNCTION_1       1  ''
               94  GET_ITER         
             96_0  COME_FROM           164  '164'
               96  FOR_ITER            180  'to 180'
               98  UNPACK_SEQUENCE_2     2 
              100  STORE_FAST               'n'
              102  STORE_FAST               'myroi'

 L.  28       104  LOAD_FAST                'myroi'
              106  LOAD_CONST               None
              108  COMPARE_OP               is-not
              110  POP_JUMP_IF_FALSE   162  'to 162'

 L.  29       112  LOAD_GLOBAL              convert1roi
              114  LOAD_FAST                'myroi'
              116  LOAD_FAST                'outroi'
              118  LOAD_FAST                'n'
              120  BINARY_SUBSCR    
              122  LOAD_ATTR                shape
              124  LOAD_FAST                'verbose'
              126  CALL_FUNCTION_3       3  ''
              128  LOAD_FAST                'outroi'
              130  LOAD_FAST                'n'
              132  STORE_SUBSCR     

 L.  30       134  LOAD_FAST                'verbose'
              136  POP_JUMP_IF_FALSE   178  'to 178'

 L.  31       138  LOAD_GLOBAL              print
              140  LOAD_STR                 'myroi2roi: layer'
              142  LOAD_FAST                'n'
              144  LOAD_STR                 'tot true pixels'
              146  LOAD_FAST                'outroi'
              148  LOAD_FAST                'n'
              150  BINARY_SUBSCR    
              152  LOAD_METHOD              sum
              154  CALL_METHOD_0         0  ''
              156  CALL_FUNCTION_4       4  ''
              158  POP_TOP          
              160  JUMP_BACK            96  'to 96'
            162_0  COME_FROM           110  '110'

 L.  32       162  LOAD_FAST                'verbose'
              164  POP_JUMP_IF_FALSE    96  'to 96'

 L.  33       166  LOAD_GLOBAL              print
              168  LOAD_STR                 'myroi2roi: layer'
              170  LOAD_FAST                'n'
              172  LOAD_STR                 'myroi is None'
              174  CALL_FUNCTION_3       3  ''
              176  POP_TOP          
            178_0  COME_FROM           136  '136'
              178  JUMP_BACK            96  'to 96'
              180  POP_BLOCK        
              182  JUMP_FORWARD        228  'to 228'
            184_0  COME_FROM            46  '46'

 L.  35       184  LOAD_FAST                'verbose'
              186  POP_JUMP_IF_FALSE   196  'to 196'

 L.  36       188  LOAD_GLOBAL              print
              190  LOAD_STR                 'myroi2roi: only one layer'
              192  CALL_FUNCTION_1       1  ''
              194  POP_TOP          
            196_0  COME_FROM           186  '186'

 L.  37       196  LOAD_GLOBAL              convert1roi
              198  LOAD_FAST                'myrois'
              200  LOAD_FAST                'outroi'
              202  LOAD_ATTR                shape
              204  LOAD_FAST                'verbose'
              206  CALL_FUNCTION_3       3  ''
              208  STORE_FAST               'outroi'

 L.  38       210  LOAD_FAST                'verbose'
              212  POP_JUMP_IF_FALSE   228  'to 228'

 L.  39       214  LOAD_GLOBAL              print
              216  LOAD_STR                 'myroi2roi: tot true pixels'
              218  LOAD_FAST                'outroi'
              220  LOAD_METHOD              sum
              222  CALL_METHOD_0         0  ''
              224  CALL_FUNCTION_2       2  ''
              226  POP_TOP          
            228_0  COME_FROM           212  '212'
            228_1  COME_FROM           182  '182'
            228_2  COME_FROM_LOOP       86  '86'

 L.  41       228  LOAD_FAST                'verbose'
              230  POP_JUMP_IF_FALSE   240  'to 240'

 L.  42       232  LOAD_GLOBAL              print
              234  LOAD_STR                 'myroi2roi: returning \n'
              236  CALL_FUNCTION_1       1  ''
              238  POP_TOP          
            240_0  COME_FROM           230  '230'

 L.  43       240  LOAD_FAST                'outroi'
              242  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 228_2
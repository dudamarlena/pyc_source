# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wehrle/opt/DesOptPy/DesOptPy/Normalize.py
# Compiled at: 2019-04-12 20:18:51
# Size of source mod 2**32: 3154 bytes
"""
Title:    Normalize.py
Units:    -
Author:   E. J. Wehrle
Date:     July 9, 2016
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
Description:

Normalization and denormalization for design optimiazation

TODOs:
-------------------------------------------------------------------------------
"""
from __future__ import absolute_import, division, print_function
import numpy as np

def normalize--- This code section failed: ---

 L.  23         0  LOAD_FAST                'DesVarNorm'
                2  LOAD_STR                 'xLxU'
                4  COMPARE_OP               is
                6  POP_JUMP_IF_TRUE      8  'to 8'
              8_0  COME_FROM             6  '6'

 L.  24         8  LOAD_FAST                'x'
               10  LOAD_FAST                'xL'
               12  BINARY_SUBTRACT  
               14  LOAD_FAST                'xU'
               16  LOAD_FAST                'xL'
               18  BINARY_SUBTRACT  
               20  BINARY_TRUE_DIVIDE
               22  STORE_FAST               'xNorm'

 L.  25        24  LOAD_GLOBAL              np
               26  LOAD_METHOD              zeros
               28  LOAD_GLOBAL              np
               30  LOAD_METHOD              size
               32  LOAD_FAST                'x'
               34  CALL_METHOD_1         1  '1 positional argument'
               36  CALL_METHOD_1         1  '1 positional argument'
               38  STORE_FAST               'xLnorm'

 L.  26        40  LOAD_GLOBAL              np
               42  LOAD_METHOD              ones
               44  LOAD_GLOBAL              np
               46  LOAD_METHOD              size
               48  LOAD_FAST                'x'
               50  CALL_METHOD_1         1  '1 positional argument'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  STORE_FAST               'xUnorm'
               56  JUMP_FORWARD        226  'to 226'

 L.  27        58  LOAD_FAST                'DesVarNorm'
               60  LOAD_STR                 'xLx0'
               62  COMPARE_OP               is
               64  POP_JUMP_IF_FALSE   116  'to 116'

 L.  28        66  LOAD_FAST                'x'
               68  LOAD_FAST                'xL'
               70  BINARY_SUBTRACT  
               72  LOAD_FAST                'x0'
               74  LOAD_FAST                'xL'
               76  BINARY_SUBTRACT  
               78  BINARY_TRUE_DIVIDE
               80  STORE_FAST               'xNorm'

 L.  29        82  LOAD_GLOBAL              np
               84  LOAD_METHOD              zeros
               86  LOAD_GLOBAL              np
               88  LOAD_METHOD              size
               90  LOAD_FAST                'x'
               92  CALL_METHOD_1         1  '1 positional argument'
               94  CALL_METHOD_1         1  '1 positional argument'
               96  STORE_FAST               'xLnorm'

 L.  30        98  LOAD_FAST                'xU'
              100  LOAD_FAST                'xL'
              102  BINARY_SUBTRACT  
              104  LOAD_FAST                'x0'
              106  LOAD_FAST                'xL'
              108  BINARY_SUBTRACT  
              110  BINARY_TRUE_DIVIDE
              112  STORE_FAST               'xUnorm'
              114  JUMP_FORWARD        226  'to 226'
            116_0  COME_FROM            64  '64'

 L.  31       116  LOAD_FAST                'DesVarNorm'
              118  LOAD_STR                 'x0'
              120  COMPARE_OP               is
              122  POP_JUMP_IF_FALSE   150  'to 150'

 L.  32       124  LOAD_FAST                'x'
              126  LOAD_FAST                'x0'
              128  BINARY_TRUE_DIVIDE
              130  STORE_FAST               'xNorm'

 L.  33       132  LOAD_FAST                'xL'
              134  LOAD_FAST                'x0'
              136  BINARY_TRUE_DIVIDE
              138  STORE_FAST               'xLnorm'

 L.  34       140  LOAD_FAST                'xU'
              142  LOAD_FAST                'x0'
              144  BINARY_TRUE_DIVIDE
              146  STORE_FAST               'xUnorm'
              148  JUMP_FORWARD        226  'to 226'
            150_0  COME_FROM           122  '122'

 L.  35       150  LOAD_FAST                'DesVarNorm'
              152  LOAD_STR                 'xU'
              154  COMPARE_OP               is
              156  POP_JUMP_IF_FALSE   184  'to 184'

 L.  36       158  LOAD_FAST                'x'
              160  LOAD_FAST                'xU'
              162  BINARY_TRUE_DIVIDE
              164  STORE_FAST               'xNorm'

 L.  37       166  LOAD_FAST                'xL'
              168  LOAD_FAST                'xU'
              170  BINARY_TRUE_DIVIDE
              172  STORE_FAST               'xLnorm'

 L.  38       174  LOAD_FAST                'xU'
              176  LOAD_FAST                'xU'
              178  BINARY_TRUE_DIVIDE
              180  STORE_FAST               'xUnorm'
              182  JUMP_FORWARD        226  'to 226'
            184_0  COME_FROM           156  '156'

 L.  39       184  LOAD_FAST                'DesVarNorm'
              186  LOAD_STR                 'None'
              188  COMPARE_OP               is
              190  POP_JUMP_IF_TRUE    200  'to 200'
              192  LOAD_CONST               None
              194  POP_JUMP_IF_TRUE    200  'to 200'
              196  LOAD_CONST               False
              198  POP_JUMP_IF_FALSE   214  'to 214'
            200_0  COME_FROM           194  '194'
            200_1  COME_FROM           190  '190'

 L.  40       200  LOAD_FAST                'x'
              202  STORE_FAST               'xNorm'

 L.  41       204  LOAD_FAST                'xL'
              206  STORE_FAST               'xLnorm'

 L.  42       208  LOAD_FAST                'xU'
              210  STORE_FAST               'xUnorm'
              212  JUMP_FORWARD        226  'to 226'
            214_0  COME_FROM           198  '198'

 L.  44       214  LOAD_GLOBAL              print
              216  LOAD_STR                 'Error: Normalization type not found: '
              218  LOAD_FAST                'DesVarNorm'
              220  BINARY_ADD       
              222  CALL_FUNCTION_1       1  '1 positional argument'
              224  POP_TOP          
            226_0  COME_FROM           212  '212'
            226_1  COME_FROM           182  '182'
            226_2  COME_FROM           148  '148'
            226_3  COME_FROM           114  '114'
            226_4  COME_FROM            56  '56'

 L.  45       226  LOAD_FAST                'xNorm'
              228  LOAD_FAST                'xLnorm'
              230  LOAD_FAST                'xUnorm'
              232  BUILD_TUPLE_3         3 
              234  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 58


def denormalize--- This code section failed: ---

 L.  49         0  LOAD_FAST                'DesVarNorm'
                2  LOAD_STR                 'xLxU'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_TRUE      8  'to 8'
              8_0  COME_FROM             6  '6'

 L.  50         8  LOAD_FAST                'xNorm'
               10  LOAD_CONST               0
               12  LOAD_GLOBAL              np
               14  LOAD_METHOD              size
               16  LOAD_FAST                'xL'
               18  CALL_METHOD_1         1  '1 positional argument'
               20  BUILD_SLICE_2         2 
               22  BUILD_TUPLE_1         1 
               24  BINARY_SUBSCR    
               26  LOAD_FAST                'xU'
               28  LOAD_FAST                'xL'
               30  BINARY_SUBTRACT  
               32  BINARY_MULTIPLY  
               34  LOAD_FAST                'xL'
               36  BINARY_ADD       
               38  STORE_FAST               'x'
               40  JUMP_FORWARD        186  'to 186'

 L.  51        42  LOAD_FAST                'DesVarNorm'
               44  LOAD_STR                 'xLx0'
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    84  'to 84'

 L.  52        50  LOAD_FAST                'xNorm'
               52  LOAD_CONST               0
               54  LOAD_GLOBAL              np
               56  LOAD_METHOD              size
               58  LOAD_FAST                'xL'
               60  CALL_METHOD_1         1  '1 positional argument'
               62  BUILD_SLICE_2         2 
               64  BUILD_TUPLE_1         1 
               66  BINARY_SUBSCR    
               68  LOAD_FAST                'x0'
               70  LOAD_FAST                'xL'
               72  BINARY_SUBTRACT  
               74  BINARY_MULTIPLY  
               76  LOAD_FAST                'xL'
               78  BINARY_ADD       
               80  STORE_FAST               'x'
               82  JUMP_FORWARD        186  'to 186'
             84_0  COME_FROM            48  '48'

 L.  53        84  LOAD_FAST                'DesVarNorm'
               86  LOAD_STR                 'x0'
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE   118  'to 118'

 L.  54        92  LOAD_FAST                'xNorm'
               94  LOAD_CONST               0
               96  LOAD_GLOBAL              np
               98  LOAD_METHOD              size
              100  LOAD_FAST                'xL'
              102  CALL_METHOD_1         1  '1 positional argument'
              104  BUILD_SLICE_2         2 
              106  BUILD_TUPLE_1         1 
              108  BINARY_SUBSCR    
              110  LOAD_FAST                'x0'
              112  BINARY_MULTIPLY  
              114  STORE_FAST               'x'
              116  JUMP_FORWARD        186  'to 186'
            118_0  COME_FROM            90  '90'

 L.  55       118  LOAD_FAST                'DesVarNorm'
              120  LOAD_STR                 'xU'
              122  COMPARE_OP               ==
              124  POP_JUMP_IF_FALSE   152  'to 152'

 L.  56       126  LOAD_FAST                'xNorm'
              128  LOAD_CONST               0
              130  LOAD_GLOBAL              np
              132  LOAD_METHOD              size
              134  LOAD_FAST                'xL'
              136  CALL_METHOD_1         1  '1 positional argument'
              138  BUILD_SLICE_2         2 
              140  BUILD_TUPLE_1         1 
              142  BINARY_SUBSCR    
              144  LOAD_FAST                'xU'
              146  BINARY_MULTIPLY  
              148  STORE_FAST               'x'
              150  JUMP_FORWARD        186  'to 186'
            152_0  COME_FROM           124  '124'

 L.  57       152  LOAD_FAST                'DesVarNorm'
              154  LOAD_STR                 'None'
              156  COMPARE_OP               is
              158  POP_JUMP_IF_TRUE    168  'to 168'
              160  LOAD_CONST               None
              162  POP_JUMP_IF_TRUE    168  'to 168'
              164  LOAD_CONST               False
              166  POP_JUMP_IF_FALSE   174  'to 174'
            168_0  COME_FROM           162  '162'
            168_1  COME_FROM           158  '158'

 L.  58       168  LOAD_FAST                'xNorm'
              170  STORE_FAST               'x'
              172  JUMP_FORWARD        186  'to 186'
            174_0  COME_FROM           166  '166'

 L.  60       174  LOAD_GLOBAL              print
              176  LOAD_STR                 'Error: Normalization type not found: '
              178  LOAD_FAST                'DesVarNorm'
              180  BINARY_ADD       
              182  CALL_FUNCTION_1       1  '1 positional argument'
              184  POP_TOP          
            186_0  COME_FROM           172  '172'
            186_1  COME_FROM           150  '150'
            186_2  COME_FROM           116  '116'
            186_3  COME_FROM            82  '82'
            186_4  COME_FROM            40  '40'

 L.  61       186  LOAD_FAST                'x'
              188  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 42


def normalizeSens--- This code section failed: ---

 L.  65         0  LOAD_FAST                'drdx'
                2  BUILD_LIST_0          0 
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  66         8  LOAD_FAST                'drdx'
               10  LOAD_METHOD              copy
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  STORE_FAST               'drdxNorm'
             16_0  COME_FROM             6  '6'

 L.  67        16  LOAD_FAST                'DesVarNorm'
               18  LOAD_STR                 'xLxU'
               20  COMPARE_OP               is
               22  POP_JUMP_IF_TRUE     24  'to 24'
             24_0  COME_FROM            22  '22'

 L.  68        24  LOAD_FAST                'drdx'
               26  LOAD_GLOBAL              np
               28  LOAD_METHOD              tile
               30  LOAD_FAST                'xU'
               32  LOAD_FAST                'xL'
               34  BINARY_SUBTRACT  
               36  LOAD_GLOBAL              np
               38  LOAD_METHOD              shape
               40  LOAD_FAST                'drdx'
               42  CALL_METHOD_1         1  '1 positional argument'
               44  LOAD_CONST               0
               46  BINARY_SUBSCR    
               48  LOAD_CONST               1
               50  BUILD_LIST_2          2 
               52  CALL_METHOD_2         2  '2 positional arguments'
               54  BINARY_MULTIPLY  
               56  STORE_FAST               'drdxNorm'
               58  JUMP_FORWARD        222  'to 222'

 L.  69        60  LOAD_FAST                'DesVarNorm'
               62  LOAD_STR                 'xLx0'
               64  COMPARE_OP               is
               66  POP_JUMP_IF_FALSE   104  'to 104'

 L.  70        68  LOAD_FAST                'drdx'
               70  LOAD_GLOBAL              np
               72  LOAD_METHOD              tile
               74  LOAD_FAST                'xL'
               76  LOAD_FAST                'x0'
               78  BINARY_SUBTRACT  
               80  LOAD_GLOBAL              np
               82  LOAD_METHOD              shape
               84  LOAD_FAST                'drdx'
               86  CALL_METHOD_1         1  '1 positional argument'
               88  LOAD_CONST               0
               90  BINARY_SUBSCR    
               92  LOAD_CONST               1
               94  BUILD_LIST_2          2 
               96  CALL_METHOD_2         2  '2 positional arguments'
               98  BINARY_MULTIPLY  
              100  STORE_FAST               'drdxNorm'
              102  JUMP_FORWARD        222  'to 222'
            104_0  COME_FROM            66  '66'

 L.  71       104  LOAD_FAST                'DesVarNorm'
              106  LOAD_STR                 'x0'
              108  COMPARE_OP               is
              110  POP_JUMP_IF_FALSE   144  'to 144'

 L.  72       112  LOAD_FAST                'drdx'
              114  LOAD_GLOBAL              np
              116  LOAD_METHOD              tile
              118  LOAD_FAST                'x0'
              120  LOAD_GLOBAL              np
              122  LOAD_METHOD              shape
              124  LOAD_FAST                'drdx'
              126  CALL_METHOD_1         1  '1 positional argument'
              128  LOAD_CONST               0
              130  BINARY_SUBSCR    
              132  LOAD_CONST               1
              134  BUILD_LIST_2          2 
              136  CALL_METHOD_2         2  '2 positional arguments'
              138  BINARY_TRUE_DIVIDE
              140  STORE_FAST               'drdxNorm'
              142  JUMP_FORWARD        222  'to 222'
            144_0  COME_FROM           110  '110'

 L.  73       144  LOAD_FAST                'DesVarNorm'
              146  LOAD_STR                 'xU'
              148  COMPARE_OP               is
              150  POP_JUMP_IF_FALSE   184  'to 184'

 L.  74       152  LOAD_FAST                'drdx'
              154  LOAD_GLOBAL              np
              156  LOAD_METHOD              tile
              158  LOAD_FAST                'xU'
              160  LOAD_GLOBAL              np
              162  LOAD_METHOD              shape
              164  LOAD_FAST                'drdx'
              166  CALL_METHOD_1         1  '1 positional argument'
              168  LOAD_CONST               0
              170  BINARY_SUBSCR    
              172  LOAD_CONST               1
              174  BUILD_LIST_2          2 
              176  CALL_METHOD_2         2  '2 positional arguments'
              178  BINARY_TRUE_DIVIDE
              180  STORE_FAST               'drdxNorm'
              182  JUMP_FORWARD        222  'to 222'
            184_0  COME_FROM           150  '150'

 L.  75       184  LOAD_FAST                'DesVarNorm'
              186  LOAD_STR                 'None'
              188  COMPARE_OP               is
              190  POP_JUMP_IF_TRUE    200  'to 200'
              192  LOAD_CONST               None
              194  POP_JUMP_IF_TRUE    200  'to 200'
              196  LOAD_CONST               False
              198  POP_JUMP_IF_FALSE   210  'to 210'
            200_0  COME_FROM           194  '194'
            200_1  COME_FROM           190  '190'

 L.  76       200  LOAD_FAST                'drdx'
              202  LOAD_METHOD              copy
              204  CALL_METHOD_0         0  '0 positional arguments'
              206  STORE_FAST               'drdxNorm'
              208  JUMP_FORWARD        222  'to 222'
            210_0  COME_FROM           198  '198'

 L.  78       210  LOAD_GLOBAL              print
              212  LOAD_STR                 'Error: Normalization type not found: '
              214  LOAD_FAST                'DesVarNorm'
              216  BINARY_ADD       
              218  CALL_FUNCTION_1       1  '1 positional argument'
              220  POP_TOP          
            222_0  COME_FROM           208  '208'
            222_1  COME_FROM           182  '182'
            222_2  COME_FROM           142  '142'
            222_3  COME_FROM           102  '102'
            222_4  COME_FROM            58  '58'

 L.  79       222  LOAD_FAST                'drdxNorm'
              224  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 60


def denormalizeSens--- This code section failed: ---

 L.  82         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'x0'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               'nx'

 L.  83         8  LOAD_GLOBAL              int
               10  LOAD_GLOBAL              np
               12  LOAD_METHOD              size
               14  LOAD_FAST                'drdx'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  LOAD_FAST                'nx'
               20  BINARY_TRUE_DIVIDE
               22  CALL_FUNCTION_1       1  '1 positional argument'
               24  STORE_FAST               'nr'

 L.  84        26  LOAD_FAST                'drdx'
               28  BUILD_LIST_0          0 
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    42  'to 42'

 L.  85        34  LOAD_FAST                'drdx'
               36  LOAD_METHOD              copy
               38  CALL_METHOD_0         0  '0 positional arguments'
               40  STORE_FAST               'drdxDenorm'
             42_0  COME_FROM            32  '32'

 L.  86        42  LOAD_FAST                'DesVarNorm'
               44  LOAD_STR                 'xLxU'
               46  COMPARE_OP               is
               48  POP_JUMP_IF_TRUE     50  'to 50'
             50_0  COME_FROM            48  '48'

 L.  87        50  LOAD_FAST                'drdx'
               52  LOAD_METHOD              reshape
               54  LOAD_FAST                'nx'
               56  LOAD_FAST                'nr'
               58  CALL_METHOD_2         2  '2 positional arguments'
               60  LOAD_GLOBAL              np
               62  LOAD_METHOD              tile
               64  LOAD_FAST                'xU'
               66  LOAD_FAST                'xL'
               68  BINARY_SUBTRACT  
               70  LOAD_METHOD              reshape
               72  LOAD_FAST                'nx'
               74  LOAD_CONST               1
               76  BUILD_TUPLE_2         2 
               78  CALL_METHOD_1         1  '1 positional argument'
               80  LOAD_CONST               1
               82  LOAD_FAST                'nr'
               84  BUILD_TUPLE_2         2 
               86  CALL_METHOD_2         2  '2 positional arguments'
               88  BINARY_TRUE_DIVIDE
               90  STORE_FAST               'drdxDenorm'
               92  JUMP_FORWARD        298  'to 298'

 L.  88        94  LOAD_FAST                'DesVarNorm'
               96  LOAD_STR                 'xLx0'
               98  COMPARE_OP               is
              100  POP_JUMP_IF_FALSE   146  'to 146'

 L.  89       102  LOAD_FAST                'drdx'
              104  LOAD_METHOD              reshape
              106  LOAD_FAST                'nx'
              108  LOAD_FAST                'nr'
              110  CALL_METHOD_2         2  '2 positional arguments'
              112  LOAD_GLOBAL              np
              114  LOAD_METHOD              tile
              116  LOAD_FAST                'xL'
              118  LOAD_FAST                'x0'
              120  BINARY_SUBTRACT  
              122  LOAD_METHOD              reshape
              124  LOAD_FAST                'nx'
              126  LOAD_CONST               1
              128  BUILD_TUPLE_2         2 
              130  CALL_METHOD_1         1  '1 positional argument'
              132  LOAD_CONST               1
              134  LOAD_FAST                'nr'
              136  BUILD_TUPLE_2         2 
              138  CALL_METHOD_2         2  '2 positional arguments'
              140  BINARY_TRUE_DIVIDE
              142  STORE_FAST               'drdxDenorm'
              144  JUMP_FORWARD        298  'to 298'
            146_0  COME_FROM           100  '100'

 L.  90       146  LOAD_FAST                'DesVarNorm'
              148  LOAD_STR                 'x0'
              150  COMPARE_OP               is
              152  POP_JUMP_IF_FALSE   194  'to 194'

 L.  91       154  LOAD_FAST                'drdx'
              156  LOAD_METHOD              reshape
              158  LOAD_FAST                'nx'
              160  LOAD_FAST                'nr'
              162  CALL_METHOD_2         2  '2 positional arguments'
              164  LOAD_GLOBAL              np
              166  LOAD_METHOD              tile
              168  LOAD_FAST                'x0'
              170  LOAD_METHOD              reshape
              172  LOAD_FAST                'nx'
              174  LOAD_CONST               1
              176  BUILD_TUPLE_2         2 
              178  CALL_METHOD_1         1  '1 positional argument'
              180  LOAD_CONST               1
              182  LOAD_FAST                'nr'
              184  BUILD_TUPLE_2         2 
              186  CALL_METHOD_2         2  '2 positional arguments'
              188  BINARY_TRUE_DIVIDE
              190  STORE_FAST               'drdxDenorm'
              192  JUMP_FORWARD        298  'to 298'
            194_0  COME_FROM           152  '152'

 L.  92       194  LOAD_FAST                'DesVarNorm'
              196  LOAD_STR                 'xU'
              198  COMPARE_OP               is
              200  POP_JUMP_IF_FALSE   242  'to 242'

 L.  93       202  LOAD_FAST                'drdx'
              204  LOAD_METHOD              reshape
              206  LOAD_FAST                'nx'
              208  LOAD_FAST                'nr'
              210  CALL_METHOD_2         2  '2 positional arguments'
              212  LOAD_GLOBAL              np
              214  LOAD_METHOD              tile
              216  LOAD_FAST                'xU'
              218  LOAD_METHOD              reshape
              220  LOAD_FAST                'nx'
              222  LOAD_CONST               1
              224  BUILD_TUPLE_2         2 
              226  CALL_METHOD_1         1  '1 positional argument'
              228  LOAD_CONST               1
              230  LOAD_FAST                'nr'
              232  BUILD_TUPLE_2         2 
              234  CALL_METHOD_2         2  '2 positional arguments'
              236  BINARY_TRUE_DIVIDE
              238  STORE_FAST               'drdxDenorm'
              240  JUMP_FORWARD        298  'to 298'
            242_0  COME_FROM           200  '200'

 L.  94       242  LOAD_FAST                'DesVarNorm'
              244  LOAD_STR                 'None'
              246  COMPARE_OP               is
          248_250  POP_JUMP_IF_TRUE    264  'to 264'
              252  LOAD_CONST               None
          254_256  POP_JUMP_IF_TRUE    264  'to 264'
              258  LOAD_CONST               False
          260_262  POP_JUMP_IF_FALSE   298  'to 298'
            264_0  COME_FROM           254  '254'
            264_1  COME_FROM           248  '248'

 L.  95       264  LOAD_FAST                'drdx'
              266  LOAD_GLOBAL              np
              268  LOAD_METHOD              tile
              270  LOAD_FAST                'xU'
              272  LOAD_FAST                'xL'
              274  BINARY_SUBTRACT  
              276  LOAD_GLOBAL              np
              278  LOAD_METHOD              shape
              280  LOAD_FAST                'drdx'
              282  CALL_METHOD_1         1  '1 positional argument'
              284  LOAD_CONST               0
              286  BINARY_SUBSCR    
              288  LOAD_CONST               1
              290  BUILD_LIST_2          2 
              292  CALL_METHOD_2         2  '2 positional arguments'
              294  BINARY_TRUE_DIVIDE
              296  STORE_FAST               'drdxDenorm'
            298_0  COME_FROM           260  '260'
            298_1  COME_FROM           240  '240'
            298_2  COME_FROM           192  '192'
            298_3  COME_FROM           144  '144'
            298_4  COME_FROM            92  '92'

 L.  96       298  LOAD_FAST                'drdxDenorm'
              300  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 94
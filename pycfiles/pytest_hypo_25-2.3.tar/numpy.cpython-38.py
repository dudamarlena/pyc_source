# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\extra\numpy.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 56785 bytes
import math, re
from collections import namedtuple
from typing import Any, NamedTuple, Sequence, Tuple, Union
import numpy as np
import hypothesis.internal.conjecture.utils as cu
import hypothesis.strategies._internal.core as st
from hypothesis import assume
from hypothesis.errors import InvalidArgument
from hypothesis.internal.coverage import check_function
from hypothesis.internal.reflection import proxies
from hypothesis.internal.validation import check_type, check_valid_interval
from hypothesis.strategies._internal import SearchStrategy
from hypothesis.strategies._internal.strategies import T
from hypothesis.utils.conventions import UniqueIdentifier, not_set
Shape = Tuple[(int, ...)]
BasicIndex = Tuple[(Union[(int, slice, 'ellipsis', np.newaxis)], ...)]
BroadcastableShapes = NamedTuple('BroadcastableShapes', [
 (
  'input_shapes', Tuple[(Shape, ...)]), ('result_shape', Shape)])
TIME_RESOLUTIONS = tuple('Y  M  D  h  m  s  ms  us  ns  ps  fs  as'.split())

@st.defines_strategy_with_reusable_values
def from_dtype--- This code section failed: ---

 L.  47         0  LOAD_GLOBAL              check_type
                2  LOAD_GLOBAL              np
                4  LOAD_ATTR                dtype
                6  LOAD_DEREF               'dtype'
                8  LOAD_STR                 'dtype'
               10  CALL_FUNCTION_3       3  ''
               12  POP_TOP          

 L.  49        14  LOAD_DEREF               'dtype'
               16  LOAD_ATTR                names
               18  LOAD_CONST               None
               20  COMPARE_OP               is-not
               22  POP_JUMP_IF_FALSE    50  'to 50'

 L.  51        24  LOAD_GLOBAL              st
               26  LOAD_ATTR                tuples
               28  LOAD_CLOSURE             'dtype'
               30  BUILD_TUPLE_1         1 
               32  LOAD_LISTCOMP            '<code_object <listcomp>>'
               34  LOAD_STR                 'from_dtype.<locals>.<listcomp>'
               36  MAKE_FUNCTION_8          'closure'
               38  LOAD_DEREF               'dtype'
               40  LOAD_ATTR                names
               42  GET_ITER         
               44  CALL_FUNCTION_1       1  ''
               46  CALL_FUNCTION_EX      0  'positional arguments only'
               48  RETURN_VALUE     
             50_0  COME_FROM            22  '22'

 L.  54        50  LOAD_DEREF               'dtype'
               52  LOAD_ATTR                subdtype
               54  LOAD_CONST               None
               56  COMPARE_OP               is-not
               58  POP_JUMP_IF_FALSE    80  'to 80'

 L.  55        60  LOAD_DEREF               'dtype'
               62  LOAD_ATTR                subdtype
               64  UNPACK_SEQUENCE_2     2 
               66  STORE_FAST               'subtype'
               68  STORE_FAST               'shape'

 L.  56        70  LOAD_GLOBAL              arrays
               72  LOAD_FAST                'subtype'
               74  LOAD_FAST                'shape'
               76  CALL_FUNCTION_2       2  ''
               78  RETURN_VALUE     
             80_0  COME_FROM            58  '58'

 L.  59        80  LOAD_DEREF               'dtype'
               82  LOAD_ATTR                kind
               84  LOAD_STR                 'b'
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE   102  'to 102'

 L.  60        90  LOAD_GLOBAL              st
               92  LOAD_METHOD              booleans
               94  CALL_METHOD_0         0  ''
               96  STORE_FAST               'result'
           98_100  JUMP_FORWARD        530  'to 530'
            102_0  COME_FROM            88  '88'

 L.  61       102  LOAD_DEREF               'dtype'
              104  LOAD_ATTR                kind
              106  LOAD_STR                 'f'
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_FALSE   172  'to 172'

 L.  62       112  LOAD_DEREF               'dtype'
              114  LOAD_ATTR                itemsize
              116  LOAD_CONST               2
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   136  'to 136'

 L.  63       122  LOAD_GLOBAL              st
              124  LOAD_ATTR                floats
              126  LOAD_CONST               16
              128  LOAD_CONST               ('width',)
              130  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              132  STORE_FAST               'result'
              134  JUMP_FORWARD        530  'to 530'
            136_0  COME_FROM           120  '120'

 L.  64       136  LOAD_DEREF               'dtype'
              138  LOAD_ATTR                itemsize
              140  LOAD_CONST               4
              142  COMPARE_OP               ==
              144  POP_JUMP_IF_FALSE   160  'to 160'

 L.  65       146  LOAD_GLOBAL              st
              148  LOAD_ATTR                floats
              150  LOAD_CONST               32
              152  LOAD_CONST               ('width',)
              154  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              156  STORE_FAST               'result'
              158  JUMP_FORWARD        530  'to 530'
            160_0  COME_FROM           144  '144'

 L.  67       160  LOAD_GLOBAL              st
              162  LOAD_METHOD              floats
              164  CALL_METHOD_0         0  ''
              166  STORE_FAST               'result'
          168_170  JUMP_FORWARD        530  'to 530'
            172_0  COME_FROM           110  '110'

 L.  68       172  LOAD_DEREF               'dtype'
              174  LOAD_ATTR                kind
              176  LOAD_STR                 'c'
              178  COMPARE_OP               ==
              180  POP_JUMP_IF_FALSE   232  'to 232'

 L.  69       182  LOAD_DEREF               'dtype'
              184  LOAD_ATTR                itemsize
              186  LOAD_CONST               8
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_FALSE   220  'to 220'

 L.  70       192  LOAD_GLOBAL              st
              194  LOAD_ATTR                floats
              196  LOAD_CONST               32
              198  LOAD_CONST               ('width',)
              200  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              202  STORE_FAST               'float32'

 L.  71       204  LOAD_GLOBAL              st
              206  LOAD_METHOD              builds
              208  LOAD_GLOBAL              complex
              210  LOAD_FAST                'float32'
              212  LOAD_FAST                'float32'
              214  CALL_METHOD_3         3  ''
              216  STORE_FAST               'result'
              218  JUMP_FORWARD        530  'to 530'
            220_0  COME_FROM           190  '190'

 L.  73       220  LOAD_GLOBAL              st
              222  LOAD_METHOD              complex_numbers
              224  CALL_METHOD_0         0  ''
              226  STORE_FAST               'result'
          228_230  JUMP_FORWARD        530  'to 530'
            232_0  COME_FROM           180  '180'

 L.  74       232  LOAD_DEREF               'dtype'
              234  LOAD_ATTR                kind
              236  LOAD_CONST               ('S', 'a')
              238  COMPARE_OP               in
          240_242  POP_JUMP_IF_FALSE   276  'to 276'

 L.  77       244  LOAD_GLOBAL              st
              246  LOAD_ATTR                binary
              248  LOAD_DEREF               'dtype'
              250  LOAD_ATTR                itemsize
          252_254  JUMP_IF_TRUE_OR_POP   258  'to 258'
              256  LOAD_CONST               None
            258_0  COME_FROM           252  '252'
              258  LOAD_CONST               ('max_size',)
              260  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              262  LOAD_METHOD              filter

 L.  78       264  LOAD_LAMBDA              '<code_object <lambda>>'
              266  LOAD_STR                 'from_dtype.<locals>.<lambda>'
              268  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  77       270  CALL_METHOD_1         1  ''
              272  STORE_FAST               'result'
              274  JUMP_FORWARD        530  'to 530'
            276_0  COME_FROM           240  '240'

 L.  80       276  LOAD_DEREF               'dtype'
              278  LOAD_ATTR                kind
              280  LOAD_STR                 'u'
              282  COMPARE_OP               ==
          284_286  POP_JUMP_IF_FALSE   318  'to 318'

 L.  81       288  LOAD_GLOBAL              st
              290  LOAD_ATTR                integers
              292  LOAD_CONST               0
              294  LOAD_CONST               2
              296  LOAD_CONST               8
              298  LOAD_DEREF               'dtype'
              300  LOAD_ATTR                itemsize
              302  BINARY_MULTIPLY  
              304  BINARY_POWER     
              306  LOAD_CONST               1
              308  BINARY_SUBTRACT  
              310  LOAD_CONST               ('min_value', 'max_value')
              312  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              314  STORE_FAST               'result'
              316  JUMP_FORWARD        530  'to 530'
            318_0  COME_FROM           284  '284'

 L.  82       318  LOAD_DEREF               'dtype'
              320  LOAD_ATTR                kind
              322  LOAD_STR                 'i'
              324  COMPARE_OP               ==
          326_328  POP_JUMP_IF_FALSE   370  'to 370'

 L.  83       330  LOAD_CONST               2
              332  LOAD_CONST               8
              334  LOAD_DEREF               'dtype'
              336  LOAD_ATTR                itemsize
              338  BINARY_MULTIPLY  
              340  LOAD_CONST               1
              342  BINARY_SUBTRACT  
              344  BINARY_POWER     
              346  STORE_FAST               'overflow'

 L.  84       348  LOAD_GLOBAL              st
              350  LOAD_ATTR                integers
              352  LOAD_FAST                'overflow'
              354  UNARY_NEGATIVE   
              356  LOAD_FAST                'overflow'
              358  LOAD_CONST               1
              360  BINARY_SUBTRACT  
              362  LOAD_CONST               ('min_value', 'max_value')
              364  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              366  STORE_FAST               'result'
              368  JUMP_FORWARD        530  'to 530'
            370_0  COME_FROM           326  '326'

 L.  85       370  LOAD_DEREF               'dtype'
              372  LOAD_ATTR                kind
              374  LOAD_STR                 'U'
              376  COMPARE_OP               ==
          378_380  POP_JUMP_IF_FALSE   424  'to 424'

 L.  87       382  LOAD_GLOBAL              st
              384  LOAD_ATTR                text
              386  LOAD_DEREF               'dtype'
              388  LOAD_ATTR                itemsize
          390_392  JUMP_IF_TRUE_OR_POP   396  'to 396'
              394  LOAD_CONST               0
            396_0  COME_FROM           390  '390'
              396  LOAD_CONST               4
              398  BINARY_FLOOR_DIVIDE
          400_402  JUMP_IF_TRUE_OR_POP   406  'to 406'
              404  LOAD_CONST               None
            406_0  COME_FROM           400  '400'
              406  LOAD_CONST               ('max_size',)
              408  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              410  LOAD_METHOD              filter

 L.  88       412  LOAD_LAMBDA              '<code_object <lambda>>'
              414  LOAD_STR                 'from_dtype.<locals>.<lambda>'
              416  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  87       418  CALL_METHOD_1         1  ''
              420  STORE_FAST               'result'
              422  JUMP_FORWARD        530  'to 530'
            424_0  COME_FROM           378  '378'

 L.  90       424  LOAD_DEREF               'dtype'
              426  LOAD_ATTR                kind
              428  LOAD_CONST               ('m', 'M')
              430  COMPARE_OP               in
          432_434  POP_JUMP_IF_FALSE   516  'to 516'

 L.  91       436  LOAD_STR                 '['
              438  LOAD_DEREF               'dtype'
              440  LOAD_ATTR                str
              442  COMPARE_OP               in
          444_446  POP_JUMP_IF_FALSE   480  'to 480'

 L.  92       448  LOAD_GLOBAL              st
              450  LOAD_METHOD              just
              452  LOAD_DEREF               'dtype'
              454  LOAD_ATTR                str
              456  LOAD_METHOD              split
              458  LOAD_STR                 '['
              460  CALL_METHOD_1         1  ''
              462  LOAD_CONST               -1
              464  BINARY_SUBSCR    
              466  LOAD_CONST               None
              468  LOAD_CONST               -1
              470  BUILD_SLICE_2         2 
              472  BINARY_SUBSCR    
              474  CALL_METHOD_1         1  ''
              476  STORE_FAST               'res'
              478  JUMP_FORWARD        490  'to 490'
            480_0  COME_FROM           444  '444'

 L.  94       480  LOAD_GLOBAL              st
              482  LOAD_METHOD              sampled_from
              484  LOAD_GLOBAL              TIME_RESOLUTIONS
              486  CALL_METHOD_1         1  ''
              488  STORE_FAST               'res'
            490_0  COME_FROM           478  '478'

 L.  95       490  LOAD_GLOBAL              st
              492  LOAD_METHOD              builds
            494_0  COME_FROM           134  '134'
              494  LOAD_DEREF               'dtype'
              496  LOAD_ATTR                type
              498  LOAD_GLOBAL              st
              500  LOAD_METHOD              integers
              502  LOAD_CONST               -9223372036854775808
              504  LOAD_CONST               9223372036854775807
              506  CALL_METHOD_2         2  ''
              508  LOAD_FAST                'res'
              510  CALL_METHOD_3         3  ''
              512  STORE_FAST               'result'
              514  JUMP_FORWARD        530  'to 530'
            516_0  COME_FROM           432  '432'

 L.  97       516  LOAD_GLOBAL              InvalidArgument
            518_0  COME_FROM           218  '218'
            518_1  COME_FROM           158  '158'
              518  LOAD_STR                 'No strategy inference for {}'
              520  LOAD_METHOD              format
              522  LOAD_DEREF               'dtype'
              524  CALL_METHOD_1         1  ''
              526  CALL_FUNCTION_1       1  ''
              528  RAISE_VARARGS_1       1  'exception instance'
            530_0  COME_FROM           514  '514'
            530_1  COME_FROM           422  '422'
            530_2  COME_FROM           368  '368'
            530_3  COME_FROM           316  '316'
            530_4  COME_FROM           274  '274'
            530_5  COME_FROM           228  '228'
            530_6  COME_FROM           168  '168'
            530_7  COME_FROM            98  '98'

 L.  98       530  LOAD_FAST                'result'
              532  LOAD_METHOD              map
              534  LOAD_DEREF               'dtype'
              536  LOAD_ATTR                type
              538  CALL_METHOD_1         1  ''
              540  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 494_0


@check_function
def check_argument(condition, fail_message, *f_args, **f_kwargs):
    if not condition:
        raise InvalidArgument((fail_message.format)(*f_args, **f_kwargs))


@check_function
def order_check(name, floor, small, large):
    check_argument((floor <= small),
      'min_{name} must be at least {} but was {}',
      floor,
      small,
      name=name)
    check_argument((small <= large),
      'min_{name}={} is larger than max_{name}={}',
      small,
      large,
      name=name)


class ArrayStrategy(SearchStrategy):

    def __init__(self, element_strategy, shape, dtype, fill, unique):
        self.shape = tuple(shape)
        self.fill = fill
        self.array_size = int(np.prod(shape))
        self.dtype = dtype
        self.element_strategy = element_strategy
        self.unique = unique
        self._check_elements = dtype.kind not in ('O', 'V')

    def set_element(self, data, result, idx, strategy=None):
        strategy = strategy or self.element_strategy
        val = data.draw(strategy)
        result[idx] = val
        if self._check_elements:
            if val != result[idx]:
                if val == val:
                    raise InvalidArgument('Generated array element %r from %r cannot be represented as dtype %r - instead it becomes %r (type %r).  Consider using a more precise strategy, for example passing the `width` argument to `floats()`.' % (
                     val, strategy, self.dtype, result[idx], type(result[idx])))

    def do_draw--- This code section failed: ---

 L. 149         0  LOAD_CONST               0
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                shape
                6  COMPARE_OP               in
                8  POP_JUMP_IF_FALSE    28  'to 28'

 L. 150        10  LOAD_GLOBAL              np
               12  LOAD_ATTR                zeros
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                dtype
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                shape
               22  LOAD_CONST               ('dtype', 'shape')
               24  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               26  RETURN_VALUE     
             28_0  COME_FROM             8  '8'

 L. 155        28  LOAD_FAST                'self'
               30  LOAD_ATTR                dtype
               32  LOAD_ATTR                kind
               34  LOAD_CONST               ('S', 'a', 'U')
               36  COMPARE_OP               in
               38  JUMP_IF_FALSE_OR_POP    50  'to 50'
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                dtype
               44  LOAD_ATTR                itemsize
               46  LOAD_CONST               0
               48  COMPARE_OP               ==
             50_0  COME_FROM            38  '38'

 L. 154        50  STORE_FAST               'unsized_string_dtype'

 L. 161        52  LOAD_GLOBAL              np
               54  LOAD_ATTR                zeros

 L. 162        56  LOAD_FAST                'self'
               58  LOAD_ATTR                array_size

 L. 162        60  LOAD_FAST                'unsized_string_dtype'
               62  POP_JUMP_IF_FALSE    68  'to 68'
               64  LOAD_GLOBAL              object
               66  JUMP_FORWARD         72  'to 72'
             68_0  COME_FROM            62  '62'
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                dtype
             72_0  COME_FROM            66  '66'

 L. 161        72  LOAD_CONST               ('shape', 'dtype')
               74  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               76  STORE_FAST               'result'

 L. 165        78  LOAD_FAST                'self'
               80  LOAD_ATTR                fill
               82  LOAD_ATTR                is_empty
               84  POP_JUMP_IF_FALSE   232  'to 232'

 L. 171        86  LOAD_FAST                'self'
               88  LOAD_ATTR                unique
               90  POP_JUMP_IF_FALSE   196  'to 196'

 L. 172        92  LOAD_GLOBAL              set
               94  CALL_FUNCTION_0       0  ''
               96  STORE_FAST               'seen'

 L. 173        98  LOAD_GLOBAL              cu
              100  LOAD_ATTR                many

 L. 174       102  LOAD_FAST                'data'

 L. 175       104  LOAD_FAST                'self'
              106  LOAD_ATTR                array_size

 L. 176       108  LOAD_FAST                'self'
              110  LOAD_ATTR                array_size

 L. 177       112  LOAD_FAST                'self'
              114  LOAD_ATTR                array_size

 L. 173       116  LOAD_CONST               ('min_size', 'max_size', 'average_size')
              118  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              120  STORE_FAST               'elements'

 L. 179       122  LOAD_CONST               0
              124  STORE_FAST               'i'

 L. 180       126  LOAD_FAST                'elements'
              128  LOAD_METHOD              more
              130  CALL_METHOD_0         0  ''
              132  POP_JUMP_IF_FALSE   228  'to 228'

 L. 185       134  LOAD_FAST                'self'
              136  LOAD_METHOD              set_element
              138  LOAD_FAST                'data'
              140  LOAD_FAST                'result'
              142  LOAD_FAST                'i'
              144  CALL_METHOD_3         3  ''
              146  POP_TOP          

 L. 186       148  LOAD_FAST                'result'
              150  LOAD_FAST                'i'
              152  BINARY_SUBSCR    
              154  LOAD_FAST                'seen'
              156  COMPARE_OP               not-in
              158  POP_JUMP_IF_FALSE   184  'to 184'

 L. 187       160  LOAD_FAST                'seen'
              162  LOAD_METHOD              add
              164  LOAD_FAST                'result'
              166  LOAD_FAST                'i'
              168  BINARY_SUBSCR    
              170  CALL_METHOD_1         1  ''
              172  POP_TOP          

 L. 188       174  LOAD_FAST                'i'
              176  LOAD_CONST               1
              178  INPLACE_ADD      
              180  STORE_FAST               'i'
              182  JUMP_BACK           126  'to 126'
            184_0  COME_FROM           158  '158'

 L. 190       184  LOAD_FAST                'elements'
              186  LOAD_METHOD              reject
              188  CALL_METHOD_0         0  ''
              190  POP_TOP          
              192  JUMP_BACK           126  'to 126'
              194  JUMP_FORWARD        572  'to 572'
            196_0  COME_FROM            90  '90'

 L. 192       196  LOAD_GLOBAL              range
              198  LOAD_GLOBAL              len
              200  LOAD_FAST                'result'
              202  CALL_FUNCTION_1       1  ''
              204  CALL_FUNCTION_1       1  ''
              206  GET_ITER         
              208  FOR_ITER            228  'to 228'
              210  STORE_FAST               'i'

 L. 193       212  LOAD_FAST                'self'
              214  LOAD_METHOD              set_element
              216  LOAD_FAST                'data'
              218  LOAD_FAST                'result'
              220  LOAD_FAST                'i'
              222  CALL_METHOD_3         3  ''
              224  POP_TOP          
              226  JUMP_BACK           208  'to 208'
            228_0  COME_FROM           132  '132'
          228_230  JUMP_FORWARD        572  'to 572'
            232_0  COME_FROM            84  '84'

 L. 202       232  LOAD_GLOBAL              cu
              234  LOAD_ATTR                many

 L. 203       236  LOAD_FAST                'data'

 L. 204       238  LOAD_CONST               0

 L. 205       240  LOAD_FAST                'self'
              242  LOAD_ATTR                array_size

 L. 209       244  LOAD_GLOBAL              math
              246  LOAD_METHOD              sqrt
              248  LOAD_FAST                'self'
              250  LOAD_ATTR                array_size
              252  CALL_METHOD_1         1  ''

 L. 202       254  LOAD_CONST               ('min_size', 'max_size', 'average_size')
              256  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              258  STORE_FAST               'elements'

 L. 212       260  LOAD_GLOBAL              np
              262  LOAD_METHOD              full
              264  LOAD_FAST                'self'
              266  LOAD_ATTR                array_size
              268  LOAD_CONST               True
              270  CALL_METHOD_2         2  ''
              272  STORE_FAST               'needs_fill'

 L. 213       274  LOAD_GLOBAL              set
              276  CALL_FUNCTION_0       0  ''
              278  STORE_FAST               'seen'

 L. 215       280  LOAD_FAST                'elements'
              282  LOAD_METHOD              more
              284  CALL_METHOD_0         0  ''
          286_288  POP_JUMP_IF_FALSE   408  'to 408'

 L. 216       290  LOAD_GLOBAL              cu
              292  LOAD_METHOD              integer_range
              294  LOAD_FAST                'data'
              296  LOAD_CONST               0
              298  LOAD_FAST                'self'
              300  LOAD_ATTR                array_size
              302  LOAD_CONST               1
              304  BINARY_SUBTRACT  
              306  CALL_METHOD_3         3  ''
              308  STORE_FAST               'i'

 L. 217       310  LOAD_FAST                'needs_fill'
              312  LOAD_FAST                'i'
              314  BINARY_SUBSCR    
          316_318  POP_JUMP_IF_TRUE    332  'to 332'

 L. 218       320  LOAD_FAST                'elements'
              322  LOAD_METHOD              reject
              324  CALL_METHOD_0         0  ''
              326  POP_TOP          

 L. 219   328_330  JUMP_BACK           280  'to 280'
            332_0  COME_FROM           316  '316'

 L. 220       332  LOAD_FAST                'self'
              334  LOAD_METHOD              set_element
              336  LOAD_FAST                'data'
              338  LOAD_FAST                'result'
              340  LOAD_FAST                'i'
              342  CALL_METHOD_3         3  ''
              344  POP_TOP          

 L. 221       346  LOAD_FAST                'self'
              348  LOAD_ATTR                unique
          350_352  POP_JUMP_IF_FALSE   396  'to 396'

 L. 222       354  LOAD_FAST                'result'
              356  LOAD_FAST                'i'
              358  BINARY_SUBSCR    
              360  LOAD_FAST                'seen'
              362  COMPARE_OP               in
          364_366  POP_JUMP_IF_FALSE   382  'to 382'

 L. 223       368  LOAD_FAST                'elements'
              370  LOAD_METHOD              reject
              372  CALL_METHOD_0         0  ''
              374  POP_TOP          

 L. 224   376_378  JUMP_BACK           280  'to 280'
              380  JUMP_FORWARD        396  'to 396'
            382_0  COME_FROM           364  '364'

 L. 226       382  LOAD_FAST                'seen'
              384  LOAD_METHOD              add
              386  LOAD_FAST                'result'
              388  LOAD_FAST                'i'
              390  BINARY_SUBSCR    
              392  CALL_METHOD_1         1  ''
              394  POP_TOP          
            396_0  COME_FROM           380  '380'
            396_1  COME_FROM           350  '350'

 L. 227       396  LOAD_CONST               False
              398  LOAD_FAST                'needs_fill'
              400  LOAD_FAST                'i'
              402  STORE_SUBSCR     
          404_406  JUMP_BACK           280  'to 280'
            408_0  COME_FROM           286  '286'

 L. 228       408  LOAD_FAST                'needs_fill'
              410  LOAD_METHOD              any
              412  CALL_METHOD_0         0  ''
          414_416  POP_JUMP_IF_FALSE   572  'to 572'

 L. 240       418  LOAD_GLOBAL              np
              420  LOAD_ATTR                zeros

 L. 241       422  LOAD_CONST               1

 L. 241       424  LOAD_FAST                'unsized_string_dtype'
          426_428  POP_JUMP_IF_FALSE   434  'to 434'
              430  LOAD_GLOBAL              object
              432  JUMP_FORWARD        438  'to 438'
            434_0  COME_FROM           426  '426'
              434  LOAD_FAST                'self'
              436  LOAD_ATTR                dtype
            438_0  COME_FROM           432  '432'

 L. 240       438  LOAD_CONST               ('shape', 'dtype')
              440  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              442  STORE_FAST               'one_element'

 L. 243       444  LOAD_FAST                'self'
              446  LOAD_METHOD              set_element
              448  LOAD_FAST                'data'
              450  LOAD_FAST                'one_element'
              452  LOAD_CONST               0
              454  LOAD_FAST                'self'
              456  LOAD_ATTR                fill
              458  CALL_METHOD_4         4  ''
              460  POP_TOP          

 L. 244       462  LOAD_FAST                'unsized_string_dtype'
          464_466  POP_JUMP_IF_FALSE   480  'to 480'

 L. 245       468  LOAD_FAST                'one_element'
              470  LOAD_METHOD              astype
              472  LOAD_FAST                'self'
              474  LOAD_ATTR                dtype
              476  CALL_METHOD_1         1  ''
              478  STORE_FAST               'one_element'
            480_0  COME_FROM           464  '464'

 L. 246       480  LOAD_FAST                'one_element'
              482  LOAD_CONST               0
              484  BINARY_SUBSCR    
              486  STORE_FAST               'fill_value'

 L. 247       488  LOAD_FAST                'self'
              490  LOAD_ATTR                unique
          492_494  POP_JUMP_IF_FALSE   558  'to 558'

 L. 248       496  SETUP_FINALLY       512  'to 512'

 L. 249       498  LOAD_GLOBAL              np
              500  LOAD_METHOD              isnan
              502  LOAD_FAST                'fill_value'
              504  CALL_METHOD_1         1  ''
              506  STORE_FAST               'is_nan'
              508  POP_BLOCK        
              510  JUMP_FORWARD        538  'to 538'
            512_0  COME_FROM_FINALLY   496  '496'

 L. 250       512  DUP_TOP          
              514  LOAD_GLOBAL              TypeError
              516  COMPARE_OP               exception-match
          518_520  POP_JUMP_IF_FALSE   536  'to 536'
              522  POP_TOP          
              524  POP_TOP          
              526  POP_TOP          

 L. 251       528  LOAD_CONST               False
              530  STORE_FAST               'is_nan'
              532  POP_EXCEPT       
              534  JUMP_FORWARD        538  'to 538'
            536_0  COME_FROM           518  '518'
            536_1  COME_FROM           194  '194'
              536  END_FINALLY      
            538_0  COME_FROM           534  '534'
            538_1  COME_FROM           510  '510'

 L. 253       538  LOAD_FAST                'is_nan'
          540_542  POP_JUMP_IF_TRUE    558  'to 558'

 L. 254       544  LOAD_GLOBAL              InvalidArgument

 L. 255       546  LOAD_STR                 'Cannot fill unique array with non-NaN value %r'

 L. 256       548  LOAD_FAST                'fill_value'
              550  BUILD_TUPLE_1         1 

 L. 255       552  BINARY_MODULO    

 L. 254       554  CALL_FUNCTION_1       1  ''
              556  RAISE_VARARGS_1       1  'exception instance'
            558_0  COME_FROM           540  '540'
            558_1  COME_FROM           492  '492'

 L. 259       558  LOAD_GLOBAL              np
              560  LOAD_METHOD              putmask
              562  LOAD_FAST                'result'
              564  LOAD_FAST                'needs_fill'
              566  LOAD_FAST                'one_element'
              568  CALL_METHOD_3         3  ''
              570  POP_TOP          
            572_0  COME_FROM           414  '414'
            572_1  COME_FROM           228  '228'

 L. 261       572  LOAD_FAST                'unsized_string_dtype'
          574_576  POP_JUMP_IF_FALSE   640  'to 640'

 L. 262       578  LOAD_FAST                'result'
              580  LOAD_METHOD              astype
              582  LOAD_FAST                'self'
              584  LOAD_ATTR                dtype
              586  CALL_METHOD_1         1  ''
              588  STORE_FAST               'out'

 L. 263       590  LOAD_FAST                'out'
              592  LOAD_FAST                'result'
              594  COMPARE_OP               !=
              596  STORE_FAST               'mismatch'

 L. 264       598  LOAD_FAST                'mismatch'
              600  LOAD_METHOD              any
              602  CALL_METHOD_0         0  ''
          604_606  POP_JUMP_IF_FALSE   636  'to 636'

 L. 265       608  LOAD_GLOBAL              InvalidArgument

 L. 266       610  LOAD_STR                 'Array elements %r cannot be represented as dtype %r - instead they becomes %r.  Use a more precise strategy, e.g. without trailing null bytes, as this will be an error future versions.'

 L. 269       612  LOAD_FAST                'result'
              614  LOAD_FAST                'mismatch'
              616  BINARY_SUBSCR    
              618  LOAD_FAST                'self'
              620  LOAD_ATTR                dtype
              622  LOAD_FAST                'out'
              624  LOAD_FAST                'mismatch'
              626  BINARY_SUBSCR    
              628  BUILD_TUPLE_3         3 

 L. 266       630  BINARY_MODULO    

 L. 265       632  CALL_FUNCTION_1       1  ''
              634  RAISE_VARARGS_1       1  'exception instance'
            636_0  COME_FROM           604  '604'

 L. 271       636  LOAD_FAST                'out'
              638  STORE_FAST               'result'
            640_0  COME_FROM           574  '574'

 L. 273       640  LOAD_FAST                'result'
              642  LOAD_METHOD              reshape
              644  LOAD_FAST                'self'
              646  LOAD_ATTR                shape
              648  CALL_METHOD_1         1  ''
              650  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 536_1


@check_function
def fill_for(elements, unique, fill, name=''):
    if fill is None:
        if not unique:
            fill = elements.has_reusable_values or st.nothing()
        else:
            fill = elements
    else:
        st.check_strategy(fill, '%s.fill' % (name,) if name else 'fill')
    return fill


@st.defines_strategy
def arrays(dtype: Any, shape: Union[(int, Shape, st.SearchStrategy[Shape])], elements: st.SearchStrategy[Any]=None, fill: st.SearchStrategy[Any]=None, unique: bool=False) -> st.SearchStrategy[np.ndarray]:
    r"""Returns a strategy for generating :class:`numpy:numpy.ndarray`\ s.

    * ``dtype`` may be any valid input to :class:`~numpy:numpy.dtype`
      (this includes :class:`~numpy:numpy.dtype` objects), or a strategy that
      generates such values.
    * ``shape`` may be an integer >= 0, a tuple of such integers, or a
      strategy that generates such values.
    * ``elements`` is a strategy for generating values to put in the array.
      If it is None a suitable value will be inferred based on the dtype,
      which may give any legal value (including eg ``NaN`` for floats).
      If you have more specific requirements, you should supply your own
      elements strategy.
    * ``fill`` is a strategy that may be used to generate a single background
      value for the array. If None, a suitable default will be inferred
      based on the other arguments. If set to
      :func:`~hypothesis.strategies.nothing` then filling
      behaviour will be disabled entirely and every element will be generated
      independently.
    * ``unique`` specifies if the elements of the array should all be
      distinct from one another. Note that in this case multiple NaN values
      may still be allowed. If fill is also set, the only valid values for
      it to return are NaN values (anything for which :obj:`numpy:numpy.isnan`
      returns True. So e.g. for complex numbers (nan+1j) is also a valid fill).
      Note that if unique is set to True the generated values must be hashable.

    Arrays of specified ``dtype`` and ``shape`` are generated for example
    like this:

    .. code-block:: pycon

      >>> import numpy as np
      >>> arrays(np.int8, (2, 3)).example()
      array([[-8,  6,  3],
             [-6,  4,  6]], dtype=int8)

    - See :doc:`What you can generate and how <data>`.

    .. code-block:: pycon

      >>> import numpy as np
      >>> from hypothesis.strategies import floats
      >>> arrays(np.float, 3, elements=floats(0, 1)).example()
      array([ 0.88974794,  0.77387938,  0.1977879 ])

    Array values are generated in two parts:

    1. Some subset of the coordinates of the array are populated with a value
       drawn from the elements strategy (or its inferred form).
    2. If any coordinates were not assigned in the previous step, a single
       value is drawn from the fill strategy and is assigned to all remaining
       places.

    You can set fill to :func:`~hypothesis.strategies.nothing` if you want to
    disable this behaviour and draw a value for every element.

    If fill is set to None then it will attempt to infer the correct behaviour
    automatically: If unique is True, no filling will occur by default.
    Otherwise, if it looks safe to reuse the values of elements across
    multiple coordinates (this will be the case for any inferred strategy, and
    for most of the builtins, but is not the case for mutable values or
    strategies built with flatmap, map, composite, etc) then it will use the
    elements strategy as the fill, else it will default to having no fill.

    Having a fill helps Hypothesis craft high quality examples, but its
    main importance is when the array generated is large: Hypothesis is
    primarily designed around testing small examples. If you have arrays with
    hundreds or more elements, having a fill value is essential if you want
    your tests to run in reasonable time.
    """
    if isinstance(dtype, SearchStrategy):
        return dtype.flatmap(lambda d: arrays(d, shape, elements=elements, fill=fill, unique=unique))
    if isinstance(shape, SearchStrategy):
        return shape.flatmap(lambda s: arrays(dtype, s, elements=elements, fill=fill, unique=unique))
    dtype = np.dtype(dtype)
    if elements is None:
        elements = from_dtype(dtype)
    if isinstance(shape, int):
        shape = (
         shape,)
    shape = tuple(shape)
    check_argument(all((isinstance(s, int) for s in shape)), 'Array shape must be integer in each dimension, provided shape was {}', shape)
    fill = fill_for(elements=elements, unique=unique, fill=fill)
    return ArrayStrategy(elements, shape, dtype, fill, unique)


@st.defines_strategy
def array_shapes(min_dims: int=1, max_dims: int=None, min_side: int=1, max_side: int=None) -> st.SearchStrategy[Shape]:
    """Return a strategy for array shapes (tuples of int >= 1)."""
    check_type(int, min_dims, 'min_dims')
    check_type(int, min_side, 'min_side')
    if min_dims > 32:
        raise InvalidArgument('Got min_dims=%r, but numpy does not support arrays greater than 32 dimensions' % min_dims)
    if max_dims is None:
        max_dims = min(min_dims + 2, 32)
    check_type(int, max_dims, 'max_dims')
    if max_dims > 32:
        raise InvalidArgument('Got max_dims=%r, but numpy does not support arrays greater than 32 dimensions' % max_dims)
    if max_side is None:
        max_side = min_side + 5
    check_type(int, max_side, 'max_side')
    order_check('dims', 0, min_dims, max_dims)
    order_check('side', 0, min_side, max_side)
    return st.lists((st.integers(min_side, max_side)),
      min_size=min_dims, max_size=max_dims).map(tuple)


@st.defines_strategy
def scalar_dtypes() -> st.SearchStrategy[np.dtype]:
    """Return a strategy that can return any non-flexible scalar dtype."""
    return st.one_of(boolean_dtypes(), integer_dtypes(), unsigned_integer_dtypes(), floating_dtypes(), complex_number_dtypes(), datetime64_dtypes(), timedelta64_dtypes())


def defines_dtype_strategy(strat: T) -> T:

    @st.defines_strategy
    @proxies(strat)
    def inner(*args, **kwargs):
        return strat(*args, **kwargs).map(np.dtype)

    return inner


@defines_dtype_strategy
def boolean_dtypes() -> st.SearchStrategy[np.dtype]:
    return st.just('?')


def dtype_factory(kind, sizes, valid_sizes, endianness):
    valid_endian = ('?', '<', '=', '>')
    check_argument(endianness in valid_endian, 'Unknown endianness: was {}, must be in {}', endianness, valid_endian)
    if valid_sizes is not None:
        if isinstance(sizes, int):
            sizes = (
             sizes,)
        check_argument(sizes, 'Dtype must have at least one possible size.')
        check_argument(all((s in valid_sizes for s in sizes)), 'Invalid sizes: was {} must be an item or sequence in {}', sizes, valid_sizes)
        if all((isinstance(s, int) for s in sizes)):
            sizes = sorted({s // 8 for s in sizes})
    strat = st.sampled_from(sizes)
    if '{}' not in kind:
        kind += '{}'
    if endianness == '?':
        return strat.map(('<' + kind).format) | strat.map(('>' + kind).format)
    return strat.map((endianness + kind).format)


@defines_dtype_strategy
def unsigned_integer_dtypes(endianness: str='?', sizes: Sequence[int]=(8, 16, 32, 64)) -> st.SearchStrategy[np.dtype]:
    """Return a strategy for unsigned integer dtypes.

    endianness may be ``<`` for little-endian, ``>`` for big-endian,
    ``=`` for native byte order, or ``?`` to allow either byte order.
    This argument only applies to dtypes of more than one byte.

    sizes must be a collection of integer sizes in bits.  The default
    (8, 16, 32, 64) covers the full range of sizes.
    """
    return dtype_factory('u', sizes, (8, 16, 32, 64), endianness)


@defines_dtype_strategy
def integer_dtypes(endianness: str='?', sizes: Sequence[int]=(8, 16, 32, 64)) -> st.SearchStrategy[np.dtype]:
    """Return a strategy for signed integer dtypes.

    endianness and sizes are treated as for
    :func:`unsigned_integer_dtypes`.
    """
    return dtype_factory('i', sizes, (8, 16, 32, 64), endianness)


@defines_dtype_strategy
def floating_dtypes(endianness: str='?', sizes: Sequence[int]=(16, 32, 64)) -> st.SearchStrategy[np.dtype]:
    """Return a strategy for floating-point dtypes.

    sizes is the size in bits of floating-point number.  Some machines support
    96- or 128-bit floats, but these are not generated by default.

    Larger floats (96 and 128 bit real parts) are not supported on all
    platforms and therefore disabled by default.  To generate these dtypes,
    include these values in the sizes argument.
    """
    return dtype_factory('f', sizes, (16, 32, 64, 96, 128), endianness)


@defines_dtype_strategy
def complex_number_dtypes(endianness: str='?', sizes: Sequence[int]=(64, 128)) -> st.SearchStrategy[np.dtype]:
    """Return a strategy for complex-number dtypes.

    sizes is the total size in bits of a complex number, which consists
    of two floats.  Complex halfs (a 16-bit real part) are not supported
    by numpy and will not be generated by this strategy.
    """
    return dtype_factory('c', sizes, (64, 128, 192, 256), endianness)


@check_function
def validate_time_slice(max_period, min_period):
    check_argument(max_period in TIME_RESOLUTIONS, 'max_period {} must be a valid resolution in {}', max_period, TIME_RESOLUTIONS)
    check_argument(min_period in TIME_RESOLUTIONS, 'min_period {} must be a valid resolution in {}', min_period, TIME_RESOLUTIONS)
    start = TIME_RESOLUTIONS.index(max_period)
    end = TIME_RESOLUTIONS.index(min_period) + 1
    check_argument(start < end, 'max_period {} must be earlier in sequence {} than min_period {}', max_period, TIME_RESOLUTIONS, min_period)
    return TIME_RESOLUTIONS[start:end]


@defines_dtype_strategy
def datetime64_dtypes(max_period: str='Y', min_period: str='ns', endianness: str='?') -> st.SearchStrategy[np.dtype]:
    """Return a strategy for datetime64 dtypes, with various precisions from
    year to attosecond."""
    return dtype_factory('datetime64[{}]', validate_time_slice(max_period, min_period), TIME_RESOLUTIONS, endianness)


@defines_dtype_strategy
def timedelta64_dtypes(max_period: str='Y', min_period: str='ns', endianness: str='?') -> st.SearchStrategy[np.dtype]:
    """Return a strategy for timedelta64 dtypes, with various precisions from
    year to attosecond."""
    return dtype_factory('timedelta64[{}]', validate_time_slice(max_period, min_period), TIME_RESOLUTIONS, endianness)


@defines_dtype_strategy
def byte_string_dtypes(endianness: str='?', min_len: int=1, max_len: int=16) -> st.SearchStrategy[np.dtype]:
    """Return a strategy for generating bytestring dtypes, of various lengths
    and byteorder.

    While Hypothesis' string strategies can generate empty strings, string
    dtypes with length 0 indicate that size is still to be determined, so
    the minimum length for string dtypes is 1.
    """
    order_check('len', 1, min_len, max_len)
    return dtype_factory('S', list(range(min_len, max_len + 1)), None, endianness)


@defines_dtype_strategy
def unicode_string_dtypes(endianness: str='?', min_len: int=1, max_len: int=16) -> st.SearchStrategy[np.dtype]:
    """Return a strategy for generating unicode string dtypes, of various
    lengths and byteorder.

    While Hypothesis' string strategies can generate empty strings, string
    dtypes with length 0 indicate that size is still to be determined, so
    the minimum length for string dtypes is 1.
    """
    order_check('len', 1, min_len, max_len)
    return dtype_factory('U', list(range(min_len, max_len + 1)), None, endianness)


@defines_dtype_strategy
def array_dtypes(subtype_strategy: st.SearchStrategy[np.dtype]=scalar_dtypes(), min_size: int=1, max_size: int=5, allow_subarrays: bool=False) -> st.SearchStrategy[np.dtype]:
    """Return a strategy for generating array (compound) dtypes, with members
    drawn from the given subtype strategy."""
    order_check('size', 0, min_size, max_size)
    field_names = st.text(min_size=1)
    elements = st.tuples(field_names, subtype_strategy)
    if allow_subarrays:
        elements |= st.tuplesfield_namessubtype_strategyarray_shapes(max_dims=2, max_side=2)
    return st.lists(elements=elements,
      min_size=min_size,
      max_size=max_size,
      unique_by=(lambda d: d[0]))


@st.defines_strategy
def nested_dtypes(subtype_strategy: st.SearchStrategy[np.dtype]=scalar_dtypes(), max_leaves: int=10, max_itemsize: int=None) -> st.SearchStrategy[np.dtype]:
    """Return the most-general dtype strategy.

    Elements drawn from this strategy may be simple (from the
    subtype_strategy), or several such values drawn from
    :func:`array_dtypes` with ``allow_subarrays=True``. Subdtypes in an
    array dtype may be nested to any depth, subject to the max_leaves
    argument.
    """
    return st.recursivesubtype_strategy(lambda x: array_dtypes(x, allow_subarrays=True))max_leaves.filter(lambda d: max_itemsize is None or d.itemsize <= max_itemsize)


@st.defines_strategy
def valid_tuple_axes(ndim: int, min_size: int=0, max_size: int=None) -> st.SearchStrategy[Shape]:
    """Return a strategy for generating permissible tuple-values for the
    ``axis`` argument for a numpy sequential function (e.g.
    :func:`numpy:numpy.sum`), given an array of the specified
    dimensionality.

    All tuples will have an length >= min_size and <= max_size. The default
    value for max_size is ``ndim``.

    Examples from this strategy shrink towards an empty tuple, which render
    most sequential functions as no-ops.

    The following are some examples drawn from this strategy.

    .. code-block:: pycon

        >>> [valid_tuple_axes(3).example() for i in range(4)]
        [(-3, 1), (0, 1, -1), (0, 2), (0, -2, 2)]

    ``valid_tuple_axes`` can be joined with other strategies to generate
    any type of valid axis object, i.e. integers, tuples, and ``None``:

    .. code-block:: pycon

        any_axis_strategy = none() | integers(-ndim, ndim - 1) | valid_tuple_axes(ndim)

    """
    if max_size is None:
        max_size = ndim
    check_type(int, ndim, 'ndim')
    check_type(int, min_size, 'min_size')
    check_type(int, max_size, 'max_size')
    order_check('size', 0, min_size, max_size)
    check_valid_interval(max_size, ndim, 'max_size', 'ndim')
    axes = st.integers(0, max(0, 2 * ndim - 1)).map(lambda x:     if x < ndim:
x # Avoid dead code: x - 2 * ndim)
    return st.lists(axes, min_size, max_size, unique_by=(lambda x: x % ndim)).map(tuple)


@st.defines_strategy
def broadcastable_shapes(shape: Shape, min_dims: int=0, max_dims: int=None, min_side: int=1, max_side: int=None) -> st.SearchStrategy[Shape]:
    """Return a strategy for generating shapes that are broadcast-compatible
    with the provided shape.

    Examples from this strategy shrink towards a shape with length ``min_dims``.
    The size of an aligned dimension shrinks towards size ``1``. The
    size of an unaligned dimension shrink towards ``min_side``.

    * ``shape`` a tuple of integers
    * ``min_dims`` The smallest length that the generated shape can possess.
    * ``max_dims`` The largest length that the generated shape can possess.
      The default-value for ``max_dims`` is ``min(32, max(len(shape), min_dims) + 2)``.
    * ``min_side`` The smallest size that an unaligned dimension can possess.
    * ``max_side`` The largest size that an unaligned dimension can possess.
      The default value is 2 + 'size-of-largest-aligned-dimension'.

    The following are some examples drawn from this strategy.

    .. code-block:: pycon

        >>> [broadcastable_shapes(shape=(2, 3)).example() for i in range(5)]
        [(1, 3), (), (2, 3), (2, 1), (4, 1, 3), (3, )]

    """
    check_type(tuple, shape, 'shape')
    strict_check = max_side is None or max_dims is None
    check_type(int, min_side, 'min_side')
    check_type(int, min_dims, 'min_dims')
    if max_dims is None:
        max_dims = min(32, max(len(shape), min_dims) + 2)
    else:
        check_type(int, max_dims, 'max_dims')
    if max_side is None:
        max_side = max(tuple(shape[-max_dims:]) + (min_side,)) + 2
    else:
        check_type(int, max_side, 'max_side')
    order_check('dims', 0, min_dims, max_dims)
    order_check('side', 0, min_side, max_side)
    if 32 < max_dims:
        raise InvalidArgument('max_dims cannot exceed 32')
    dims, bnd_name = (max_dims, 'max_dims') if strict_check else (min_dims, 'min_dims')
    if not all((min_side <= s for s in shape[::-1][:dims] if s != 1)):
        raise InvalidArgument('Given shape=%r, there are no broadcast-compatible shapes that satisfy: %s=%s and min_side=%s' % (
         shape, bnd_name, dims, min_side))
    if not min_side <= 1 <= max_side:
        if not all((s <= max_side for s in shape[::-1][:dims])):
            raise InvalidArgument('Given shape=%r, there are no broadcast-compatible shapes that satisfy: %s=%s and [min_side=%s, max_side=%s]' % (
             shape, bnd_name, dims, min_side, max_side))
    for n, s in strict_check or zip(range(max_dims), reversed(shape)):
        if s < min_side and s != 1:
            max_dims = n
            break
        elif not min_side <= 1 <= max_side:
            if not s <= max_side:
                max_dims = n
                break
            else:
                return MutuallyBroadcastableShapesStrategy(num_shapes=1,
                  base_shape=shape,
                  min_dims=min_dims,
                  max_dims=max_dims,
                  min_side=min_side,
                  max_side=max_side).map(lambda x: x.input_shapes[0])


class MutuallyBroadcastableShapesStrategy(SearchStrategy):

    def __init__--- This code section failed: ---

 L. 816         0  LOAD_CONST               0
                2  LOAD_FAST                'min_side'
                4  DUP_TOP          
                6  ROT_THREE        
                8  COMPARE_OP               <=
               10  POP_JUMP_IF_FALSE    20  'to 20'
               12  LOAD_FAST                'max_side'
               14  COMPARE_OP               <=
               16  POP_JUMP_IF_TRUE     26  'to 26'
               18  JUMP_FORWARD         22  'to 22'
             20_0  COME_FROM            10  '10'
               20  POP_TOP          
             22_0  COME_FROM            18  '18'
               22  LOAD_GLOBAL              AssertionError
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L. 817        26  LOAD_CONST               0
               28  LOAD_FAST                'min_dims'
               30  DUP_TOP          
               32  ROT_THREE        
               34  COMPARE_OP               <=
               36  POP_JUMP_IF_FALSE    56  'to 56'
               38  LOAD_FAST                'max_dims'
               40  DUP_TOP          
               42  ROT_THREE        
               44  COMPARE_OP               <=
               46  POP_JUMP_IF_FALSE    56  'to 56'
               48  LOAD_CONST               32
               50  COMPARE_OP               <=
               52  POP_JUMP_IF_TRUE     62  'to 62'
               54  JUMP_FORWARD         58  'to 58'
             56_0  COME_FROM            46  '46'
             56_1  COME_FROM            36  '36'
               56  POP_TOP          
             58_0  COME_FROM            54  '54'
               58  LOAD_GLOBAL              AssertionError
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'

 L. 818        62  LOAD_GLOBAL              SearchStrategy
               64  LOAD_METHOD              __init__
               66  LOAD_FAST                'self'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L. 819        72  LOAD_FAST                'base_shape'
               74  LOAD_FAST                'self'
               76  STORE_ATTR               base_shape

 L. 820        78  LOAD_GLOBAL              st
               80  LOAD_METHOD              integers
               82  LOAD_FAST                'min_side'
               84  LOAD_FAST                'max_side'
               86  CALL_METHOD_2         2  ''
               88  LOAD_FAST                'self'
               90  STORE_ATTR               side_strat

 L. 821        92  LOAD_FAST                'num_shapes'
               94  LOAD_FAST                'self'
               96  STORE_ATTR               num_shapes

 L. 822        98  LOAD_FAST                'signature'
              100  LOAD_FAST                'self'
              102  STORE_ATTR               signature

 L. 823       104  LOAD_FAST                'min_dims'
              106  LOAD_FAST                'self'
              108  STORE_ATTR               min_dims

 L. 824       110  LOAD_FAST                'max_dims'
              112  LOAD_FAST                'self'
              114  STORE_ATTR               max_dims

 L. 825       116  LOAD_FAST                'min_side'
              118  LOAD_FAST                'self'
              120  STORE_ATTR               min_side

 L. 826       122  LOAD_FAST                'max_side'
              124  LOAD_FAST                'self'
              126  STORE_ATTR               max_side

 L. 828       128  LOAD_FAST                'self'
              130  LOAD_ATTR                min_side
              132  LOAD_CONST               1
              134  DUP_TOP          
              136  ROT_THREE        
              138  COMPARE_OP               <=
              140  JUMP_IF_FALSE_OR_POP   150  'to 150'
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                max_side
              146  COMPARE_OP               <=
              148  JUMP_FORWARD        154  'to 154'
            150_0  COME_FROM           140  '140'
              150  ROT_TWO          
              152  POP_TOP          
            154_0  COME_FROM           148  '148'
              154  LOAD_FAST                'self'
              156  STORE_ATTR               size_one_allowed

Parse error at or near `COME_FROM' instruction at offset 58_0

    def do_draw(self, data):
        if self.signature is None:
            return self._draw_loop_dimensions(data)
        core_in, core_res = self._draw_core_dimensions(data)
        use = [None not in shp for shp in core_in]
        loop_in, loop_res = self._draw_loop_dimensions(data, use=use)

        def add_shape(loop, core):
            return tuple((x for x in (loop + core)[-32:] if x is not None))

        return BroadcastableShapes(input_shapes=(tuple((add_shape(l, c) for l, c in zip(loop_in, core_in)))),
          result_shape=(add_shape(loop_res, core_res)))

    def _draw_core_dimensions(self, data):
        dims = {}
        shapes = []
        for shape in self.signature.input_shapes + (self.signature.result_shape,):
            shapes.append([])
            for name in shape:
                if name.isdigit():
                    shapes[(-1)].append(int(name))
                else:
                    if name not in dims:
                        dim = name.strip('?')
                        dims[dim] = data.draw(self.side_strat)
                        if self.min_dims == 0:
                            dims[dim + '?'] = data.draw_bits(3) or None
                        else:
                            dims[dim + '?'] = dims[dim]
                    shapes[(-1)].append(dims[name])
            else:
                return (
                 tuple((tuple(s) for s in shapes[:-1])), tuple(shapes[(-1)]))

    def _draw_loop_dimensions--- This code section failed: ---

 L. 879         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                base_shape
                4  LOAD_CONST               None
                6  LOAD_CONST               None
                8  LOAD_CONST               -1
               10  BUILD_SLICE_3         3 
               12  BINARY_SUBSCR    
               14  STORE_FAST               'base_shape'

 L. 880        16  LOAD_GLOBAL              list
               18  LOAD_FAST                'base_shape'
               20  CALL_FUNCTION_1       1  ''
               22  STORE_FAST               'result_shape'

 L. 881        24  LOAD_LISTCOMP            '<code_object <listcomp>>'
               26  LOAD_STR                 'MutuallyBroadcastableShapesStrategy._draw_loop_dimensions.<locals>.<listcomp>'
               28  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               30  LOAD_GLOBAL              range
               32  LOAD_DEREF               'self'
               34  LOAD_ATTR                num_shapes
               36  CALL_FUNCTION_1       1  ''
               38  GET_ITER         
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'shapes'

 L. 882        44  LOAD_FAST                'use'
               46  LOAD_CONST               None
               48  COMPARE_OP               is
               50  POP_JUMP_IF_FALSE    74  'to 74'

 L. 883        52  LOAD_LISTCOMP            '<code_object <listcomp>>'
               54  LOAD_STR                 'MutuallyBroadcastableShapesStrategy._draw_loop_dimensions.<locals>.<listcomp>'
               56  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               58  LOAD_GLOBAL              range
               60  LOAD_DEREF               'self'
               62  LOAD_ATTR                num_shapes
               64  CALL_FUNCTION_1       1  ''
               66  GET_ITER         
               68  CALL_FUNCTION_1       1  ''
               70  STORE_FAST               'use'
               72  JUMP_FORWARD        114  'to 114'
             74_0  COME_FROM            50  '50'

 L. 885        74  LOAD_GLOBAL              len
               76  LOAD_FAST                'use'
               78  CALL_FUNCTION_1       1  ''
               80  LOAD_DEREF               'self'
               82  LOAD_ATTR                num_shapes
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_TRUE     92  'to 92'
               88  LOAD_ASSERT              AssertionError
               90  RAISE_VARARGS_1       1  'exception instance'
             92_0  COME_FROM            86  '86'

 L. 886        92  LOAD_GLOBAL              all
               94  LOAD_GENEXPR             '<code_object <genexpr>>'
               96  LOAD_STR                 'MutuallyBroadcastableShapesStrategy._draw_loop_dimensions.<locals>.<genexpr>'
               98  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              100  LOAD_FAST                'use'
              102  GET_ITER         
              104  CALL_FUNCTION_1       1  ''
              106  CALL_FUNCTION_1       1  ''
              108  POP_JUMP_IF_TRUE    114  'to 114'
              110  LOAD_ASSERT              AssertionError
              112  RAISE_VARARGS_1       1  'exception instance'
            114_0  COME_FROM           108  '108'
            114_1  COME_FROM            72  '72'

 L. 888       114  LOAD_GLOBAL              range
              116  LOAD_CONST               1
              118  LOAD_DEREF               'self'
              120  LOAD_ATTR                max_dims
              122  LOAD_CONST               1
              124  BINARY_ADD       
              126  CALL_FUNCTION_2       2  ''
              128  GET_ITER         
            130_0  COME_FROM           424  '424'
          130_132  FOR_ITER            434  'to 434'
              134  STORE_FAST               'dim_count'

 L. 889       136  LOAD_FAST                'dim_count'
              138  LOAD_CONST               1
              140  BINARY_SUBTRACT  
              142  STORE_FAST               'dim'

 L. 895       144  LOAD_GLOBAL              len
              146  LOAD_FAST                'base_shape'
              148  CALL_FUNCTION_1       1  ''
              150  LOAD_FAST                'dim_count'
              152  COMPARE_OP               <
              154  POP_JUMP_IF_TRUE    168  'to 168'
              156  LOAD_FAST                'base_shape'
              158  LOAD_FAST                'dim'
              160  BINARY_SUBSCR    
              162  LOAD_CONST               1
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_FALSE   182  'to 182'
            168_0  COME_FROM           154  '154'

 L. 897       168  LOAD_FAST                'data'
              170  LOAD_METHOD              draw
              172  LOAD_DEREF               'self'
              174  LOAD_ATTR                side_strat
              176  CALL_METHOD_1         1  ''
              178  STORE_FAST               'dim_side'
              180  JUMP_FORWARD        210  'to 210'
            182_0  COME_FROM           166  '166'

 L. 898       182  LOAD_FAST                'base_shape'
              184  LOAD_FAST                'dim'
              186  BINARY_SUBSCR    
              188  LOAD_DEREF               'self'
              190  LOAD_ATTR                max_side
              192  COMPARE_OP               <=
              194  POP_JUMP_IF_FALSE   206  'to 206'

 L. 900       196  LOAD_FAST                'base_shape'
              198  LOAD_FAST                'dim'
              200  BINARY_SUBSCR    
              202  STORE_FAST               'dim_side'
              204  JUMP_FORWARD        210  'to 210'
            206_0  COME_FROM           194  '194'

 L. 903       206  LOAD_CONST               1
              208  STORE_FAST               'dim_side'
            210_0  COME_FROM           204  '204'
            210_1  COME_FROM           180  '180'

 L. 905       210  LOAD_GLOBAL              enumerate
              212  LOAD_FAST                'shapes'
              214  CALL_FUNCTION_1       1  ''
              216  GET_ITER         
            218_0  COME_FROM           402  '402'
            218_1  COME_FROM           390  '390'
            218_2  COME_FROM           334  '334'
              218  FOR_ITER            418  'to 418'
              220  UNPACK_SEQUENCE_2     2 
              222  STORE_FAST               'shape_id'
              224  STORE_FAST               'shape'

 L. 909       226  LOAD_FAST                'dim_count'
              228  LOAD_GLOBAL              len
              230  LOAD_FAST                'base_shape'
              232  CALL_FUNCTION_1       1  ''
              234  COMPARE_OP               <=
          236_238  POP_JUMP_IF_FALSE   270  'to 270'
              240  LOAD_DEREF               'self'
              242  LOAD_ATTR                size_one_allowed
          244_246  POP_JUMP_IF_FALSE   270  'to 270'

 L. 911       248  LOAD_FAST                'data'
              250  LOAD_METHOD              draw
              252  LOAD_GLOBAL              st
              254  LOAD_METHOD              sampled_from
              256  LOAD_CONST               1
              258  LOAD_FAST                'dim_side'
              260  BUILD_LIST_2          2 
              262  CALL_METHOD_1         1  ''
              264  CALL_METHOD_1         1  ''
              266  STORE_FAST               'side'
              268  JUMP_FORWARD        274  'to 274'
            270_0  COME_FROM           244  '244'
            270_1  COME_FROM           236  '236'

 L. 913       270  LOAD_FAST                'dim_side'
              272  STORE_FAST               'side'
            274_0  COME_FROM           268  '268'

 L. 920       274  LOAD_DEREF               'self'
              276  LOAD_ATTR                min_dims
              278  LOAD_FAST                'dim_count'
              280  COMPARE_OP               <
          282_284  POP_JUMP_IF_FALSE   328  'to 328'

 L. 921       286  LOAD_FAST                'use'
              288  LOAD_FAST                'shape_id'
              290  DUP_TOP_TWO      
              292  BINARY_SUBSCR    
              294  LOAD_GLOBAL              cu
              296  LOAD_METHOD              biased_coin

 L. 922       298  LOAD_FAST                'data'

 L. 922       300  LOAD_CONST               1
              302  LOAD_CONST               1
              304  LOAD_CONST               1
              306  LOAD_DEREF               'self'
              308  LOAD_ATTR                max_dims
              310  BINARY_ADD       
              312  LOAD_FAST                'dim'
              314  BINARY_SUBTRACT  
              316  BINARY_TRUE_DIVIDE
              318  BINARY_SUBTRACT  

 L. 921       320  CALL_METHOD_2         2  ''
              322  INPLACE_AND      
              324  ROT_THREE        
              326  STORE_SUBSCR     
            328_0  COME_FROM           282  '282'

 L. 925       328  LOAD_FAST                'use'
              330  LOAD_FAST                'shape_id'
              332  BINARY_SUBSCR    
              334  POP_JUMP_IF_FALSE   218  'to 218'

 L. 926       336  LOAD_FAST                'shape'
              338  LOAD_METHOD              append
              340  LOAD_FAST                'side'
              342  CALL_METHOD_1         1  ''
              344  POP_TOP          

 L. 927       346  LOAD_GLOBAL              len
              348  LOAD_FAST                'result_shape'
              350  CALL_FUNCTION_1       1  ''
              352  LOAD_GLOBAL              len
              354  LOAD_FAST                'shape'
              356  CALL_FUNCTION_1       1  ''
              358  COMPARE_OP               <
          360_362  POP_JUMP_IF_FALSE   380  'to 380'

 L. 928       364  LOAD_FAST                'result_shape'
              366  LOAD_METHOD              append
              368  LOAD_FAST                'shape'
              370  LOAD_CONST               -1
              372  BINARY_SUBSCR    
              374  CALL_METHOD_1         1  ''
              376  POP_TOP          
              378  JUMP_BACK           218  'to 218'
            380_0  COME_FROM           360  '360'

 L. 929       380  LOAD_FAST                'shape'
              382  LOAD_CONST               -1
              384  BINARY_SUBSCR    
              386  LOAD_CONST               1
              388  COMPARE_OP               !=
              390  POP_JUMP_IF_FALSE   218  'to 218'
              392  LOAD_FAST                'result_shape'
              394  LOAD_FAST                'dim'
              396  BINARY_SUBSCR    
              398  LOAD_CONST               1
              400  COMPARE_OP               ==
              402  POP_JUMP_IF_FALSE   218  'to 218'

 L. 930       404  LOAD_FAST                'shape'
              406  LOAD_CONST               -1
              408  BINARY_SUBSCR    
              410  LOAD_FAST                'result_shape'
              412  LOAD_FAST                'dim'
              414  STORE_SUBSCR     
              416  JUMP_BACK           218  'to 218'

 L. 931       418  LOAD_GLOBAL              any
              420  LOAD_FAST                'use'
              422  CALL_FUNCTION_1       1  ''
              424  POP_JUMP_IF_TRUE    130  'to 130'

 L. 932       426  POP_TOP          
          428_430  JUMP_ABSOLUTE       434  'to 434'
              432  JUMP_BACK           130  'to 130'

 L. 934       434  LOAD_FAST                'result_shape'
              436  LOAD_CONST               None
              438  LOAD_GLOBAL              max
              440  LOAD_GLOBAL              map
              442  LOAD_GLOBAL              len
              444  LOAD_DEREF               'self'
              446  LOAD_ATTR                base_shape
              448  BUILD_LIST_1          1 
              450  LOAD_FAST                'shapes'
              452  BINARY_ADD       
              454  CALL_FUNCTION_2       2  ''
              456  CALL_FUNCTION_1       1  ''
              458  BUILD_SLICE_2         2 
              460  BINARY_SUBSCR    
              462  STORE_FAST               'result_shape'

 L. 936       464  LOAD_GLOBAL              len
              466  LOAD_FAST                'shapes'
              468  CALL_FUNCTION_1       1  ''
              470  LOAD_DEREF               'self'
              472  LOAD_ATTR                num_shapes
              474  COMPARE_OP               ==
          476_478  POP_JUMP_IF_TRUE    484  'to 484'
              480  LOAD_ASSERT              AssertionError
              482  RAISE_VARARGS_1       1  'exception instance'
            484_0  COME_FROM           476  '476'

 L. 937       484  LOAD_GLOBAL              all
              486  LOAD_CLOSURE             'self'
              488  BUILD_TUPLE_1         1 
              490  LOAD_GENEXPR             '<code_object <genexpr>>'
              492  LOAD_STR                 'MutuallyBroadcastableShapesStrategy._draw_loop_dimensions.<locals>.<genexpr>'
              494  MAKE_FUNCTION_8          'closure'
              496  LOAD_FAST                'shapes'
              498  GET_ITER         
              500  CALL_FUNCTION_1       1  ''
              502  CALL_FUNCTION_1       1  ''
          504_506  POP_JUMP_IF_TRUE    512  'to 512'
              508  LOAD_ASSERT              AssertionError
              510  RAISE_VARARGS_1       1  'exception instance'
            512_0  COME_FROM           504  '504'

 L. 938       512  LOAD_GLOBAL              all
              514  LOAD_CLOSURE             'self'
              516  BUILD_TUPLE_1         1 
              518  LOAD_GENEXPR             '<code_object <genexpr>>'
              520  LOAD_STR                 'MutuallyBroadcastableShapesStrategy._draw_loop_dimensions.<locals>.<genexpr>'
              522  MAKE_FUNCTION_8          'closure'
              524  LOAD_FAST                'shapes'
              526  GET_ITER         
              528  CALL_FUNCTION_1       1  ''
              530  CALL_FUNCTION_1       1  ''
          532_534  POP_JUMP_IF_TRUE    540  'to 540'
              536  LOAD_ASSERT              AssertionError
              538  RAISE_VARARGS_1       1  'exception instance'
            540_0  COME_FROM           532  '532'

 L. 940       540  LOAD_GLOBAL              BroadcastableShapes

 L. 941       542  LOAD_GLOBAL              tuple
              544  LOAD_GENEXPR             '<code_object <genexpr>>'
              546  LOAD_STR                 'MutuallyBroadcastableShapesStrategy._draw_loop_dimensions.<locals>.<genexpr>'
              548  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              550  LOAD_FAST                'shapes'
              552  GET_ITER         
              554  CALL_FUNCTION_1       1  ''
              556  CALL_FUNCTION_1       1  ''

 L. 942       558  LOAD_GLOBAL              tuple
              560  LOAD_GLOBAL              reversed
              562  LOAD_FAST                'result_shape'
              564  CALL_FUNCTION_1       1  ''
              566  CALL_FUNCTION_1       1  ''

 L. 940       568  LOAD_CONST               ('input_shapes', 'result_shape')
              570  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              572  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 428_430


_DIMENSION = '\\w+\\??'
_SHAPE = '\\((?:{0}(?:,{0})'.format(_DIMENSION) + '{0,31})?\\)'
_ARGUMENT_LIST = '{0}(?:,{0})*'.format(_SHAPE)
_SIGNATURE = '^{}->{}$'.format(_ARGUMENT_LIST, _SHAPE)
_SIGNATURE_MULTIPLE_OUTPUT = '^{0}->{0}$'.format(_ARGUMENT_LIST)
_GUfuncSig = namedtuple('_GUfuncSig', ['input_shapes', 'result_shape'])

def _hypothesis_parse_gufunc_signature(signature, all_checks=True):
    if not re.match(_SIGNATURE, signature):
        if re.match(_SIGNATURE_MULTIPLE_OUTPUT, signature):
            raise InvalidArgument("Hypothesis does not yet support generalised ufunc signatures with multiple output arrays - mostly because we don't know of anyone who uses them!  Please get in touch with us to fix that.\n (signature=%r)" % (
             signature,))
        if re.match(np.lib.function_base._SIGNATURE, signature):
            raise InvalidArgument("signature=%r matches Numpy's regex for gufunc signatures, but contains shapes with more than 32 dimensions and is thus invalid." % (
             signature,))
        raise InvalidArgument('%r is not a valid gufunc signature' % (signature,))
    else:
        input_shapes, output_shapes = (tuple((tuple(re.findall(_DIMENSION, a)) for a in re.findall(_SHAPE, arg_list))) for arg_list in signature.split('->'))
        assert len(output_shapes) == 1
        result_shape = output_shapes[0]
        if all_checks:
            frozen_optional_err = 'Got dimension %r, but handling of frozen optional dimensions is ambiguous.  If you known how this should work, please contact us to get this fixed and documented (signature=%r).'
            only_out_err = 'The %r dimension only appears in the output shape, and is not frozen, so the size is not determined (signature=%r).'
            names_in = {n.strip('?') for shp in input_shapes for n in shp}
            names_out = {n.strip('?') for n in result_shape}
            for shape in input_shapes + (result_shape,):
                for name in shape:
                    try:
                        int(name.strip('?'))
                        if '?' in name:
                            raise InvalidArgument(frozen_optional_err % (name, signature))
                    except ValueError:
                        if name.strip('?') in names_out - names_in:
                            raise InvalidArgument(only_out_err % (name, signature)) from None

    return _GUfuncSig(input_shapes=input_shapes, result_shape=result_shape)


@st.defines_strategy
def mutually_broadcastable_shapes(*, num_shapes: Union[(UniqueIdentifier, int)]=not_set, signature: Union[(UniqueIdentifier, str)]=not_set, base_shape: Shape=(), min_dims: int=0, max_dims: int=None, min_side: int=1, max_side: int=None) -> st.SearchStrategy[BroadcastableShapes]:
    """Return a strategy for generating a specified number of shapes, N, that are
    mutually-broadcastable with one another and with the provided "base-shape".

    The strategy will generate a named-tuple of:

    * input_shapes: the N generated shapes
    * result_shape: the resulting shape, produced by broadcasting the
      N shapes with the base-shape

    Each shape produced from this strategy shrinks towards a shape with length
    ``min_dims``. The size of an aligned dimension shrinks towards being having
    a size of 1. The size of an unaligned dimension shrink towards ``min_side``.

    * ``num_shapes`` The number of mutually broadcast-compatible shapes to generate.
    * ``base-shape`` The shape against which all generated shapes can broadcast.
      The default shape is empty, which corresponds to a scalar and thus does not
      constrain broadcasting at all.
    * ``min_dims`` The smallest length that any generated shape can possess.
    * ``max_dims`` The largest length that any generated shape can possess.
      It cannot exceed 32, which is the greatest supported dimensionality for a
      numpy array. The default-value for ``max_dims`` is
      ``2 + max(len(shape), min_dims)``, capped at 32.
    * ``min_side`` The smallest size that an unaligned dimension can possess.
    * ``max_side`` The largest size that an unaligned dimension can possess.
      The default value is 2 + 'size-of-largest-aligned-dimension'.

    The following are some examples drawn from this strategy.

    .. code-block:: pycon

        >>> # Draw three shapes, and each shape is broadcast-compatible with `(2, 3)`
        >>> for _ in range(5):
        ...     mutually_broadcastable_shapes(num_shapes=3, base_shape=(2, 3)).example()
        BroadcastableShapes(input_shapes=((4, 1, 3), (4, 2, 3), ()), result_shape=(4, 2, 3))
        BroadcastableShapes(input_shapes=((3,), (1,), (2, 1)), result_shape=(2, 3))
        BroadcastableShapes(input_shapes=((3,), (1, 3), (2, 3)), result_shape=(2, 3))
        BroadcastableShapes(input_shapes=((), (), ()), result_shape=(2, 3))
        BroadcastableShapes(input_shapes=((3,), (), (3,)), result_shape=(2, 3))

    **Use with Generalised Universal Function signatures**

    A :np-ref:`universal function <ufuncs.html>` (or ufunc for short) is a function
    that operates on ndarrays in an element-by-element fashion, supporting array
    broadcasting, type casting, and several other standard features.
    A :np-ref:`generalised ufunc <c-api.generalized-ufuncs.html>` operates on
    sub-arrays rather than elements, based on the "signature" of the function.
    Compare e.g. :obj:`numpy:numpy.add` (ufunc) to :obj:`numpy:numpy.matmul` (gufunc).

    To generate shapes for a gufunc, you can pass the ``signature`` argument instead of
    ``num_shapes``.  This must be a gufunc signature string; which you can write by
    hand or access as e.g. ``np.matmul.signature`` on generalised ufuncs.

    In this case, the ``side`` arguments are applied to the 'core dimensions' as well,
    ignoring any frozen dimensions.  ``base_shape``  and the ``dims`` arguments are
    applied to the 'loop dimensions', and if necessary, the dimensionality of each
    shape is silently capped to respect the 32-dimension limit.

    The generated ``result_shape`` is the real result shape of applying the gufunc
    to arrays of the generated ``input_shapes``, even where this is different to
    broadcasting the loop dimensions.

    gufunc-compatible shapes shrink their loop dimensions as above, towards omitting
    optional core dimensions, and smaller-size core dimensions.

    .. code-block:: pycon

        >>> # np.matmul.signature == "(m?,n),(n,p?)->(m?,p?)"
        >>> for _ in range(3):
        ...     mutually_broadcastable_shapes(signature=np.matmul.signature).example()
        BroadcastableShapes(input_shapes=((2,), (2,)), result_shape=())
        BroadcastableShapes(input_shapes=((3, 4, 2), (1, 2)), result_shape=(3, 4))
        BroadcastableShapes(input_shapes=((4, 2), (1, 2, 3)), result_shape=(4, 3))
    """
    arg_msg = 'Pass either the `num_shapes` or the `signature` argument, but not both.'
    if num_shapes is not not_set:
        check_argument(signature is not_set, arg_msg)
        check_type(int, num_shapes, 'num_shapes')
        assert isinstance(num_shapes, int)
        check_argument(num_shapes >= 1, 'num_shapes={} must be at least 1', num_shapes)
        parsed_signature = None
        sig_dims = 0
    else:
        check_argument(signature is not not_set, arg_msg)
        if signature is None:
            raise InvalidArgument('Expected a string, but got invalid signature=None.  (maybe .signature attribute of an element-wise ufunc?)')
        else:
            check_type(str, signature, 'signature')
            parsed_signature = _hypothesis_parse_gufunc_signature(signature)
            sig_dims = min(map(len, parsed_signature.input_shapes + (parsed_signature.result_shape,)))
            num_shapes = len(parsed_signature.input_shapes)
            if not num_shapes >= 1:
                raise AssertionError
            else:
                check_type(tuple, base_shape, 'base_shape')
                strict_check = max_dims is not None
                check_type(int, min_side, 'min_side')
                check_type(int, min_dims, 'min_dims')
                if max_dims is None:
                    max_dims = min(32 - sig_dims, max(len(base_shape), min_dims) + 2)
                else:
                    check_type(int, max_dims, 'max_dims')
            if max_side is None:
                max_side = max(tuple(base_shape[-max_dims:]) + (min_side,)) + 2
            else:
                check_type(int, max_side, 'max_side')
        order_check('dims', 0, min_dims, max_dims)
        order_check('side', 0, min_side, max_side)
        if 32 - sig_dims < max_dims:
            if sig_dims == 0:
                raise InvalidArgument('max_dims cannot exceed 32')
            raise InvalidArgument('max_dims=%r would exceed the 32-dimension limit given signature=%r' % (
             signature, parsed_signature))
        dims, bnd_name = (max_dims, 'max_dims') if strict_check else (min_dims, 'min_dims')
        if not all((min_side <= s for s in base_shape[::-1][:dims] if s != 1)):
            raise InvalidArgument('Given base_shape=%r, there are no broadcast-compatible shapes that satisfy: %s=%s and min_side=%s' % (
             base_shape, bnd_name, dims, min_side))
        if not min_side <= 1 <= max_side:
            if not all((s <= max_side for s in base_shape[::-1][:dims])):
                raise InvalidArgument('Given base_shape=%r, there are no broadcast-compatible shapes that satisfy all of %s=%s, min_side=%s, and max_side=%s' % (
                 base_shape, bnd_name, dims, min_side, max_side))
        for n, s in strict_check or zip(range(max_dims), reversed(base_shape)):
            if s < min_side and s != 1:
                max_dims = n
                break
            elif not min_side <= 1 <= max_side:
                if not s <= max_side:
                    max_dims = n
                    break
                else:
                    return MutuallyBroadcastableShapesStrategy(num_shapes=num_shapes,
                      signature=parsed_signature,
                      base_shape=base_shape,
                      min_dims=min_dims,
                      max_dims=max_dims,
                      min_side=min_side,
                      max_side=max_side)


class BasicIndexStrategy(SearchStrategy):

    def __init__--- This code section failed: ---

 L.1205         0  LOAD_CONST               0
                2  LOAD_FAST                'min_dims'
                4  DUP_TOP          
                6  ROT_THREE        
                8  COMPARE_OP               <=
               10  POP_JUMP_IF_FALSE    30  'to 30'
               12  LOAD_FAST                'max_dims'
               14  DUP_TOP          
               16  ROT_THREE        
               18  COMPARE_OP               <=
               20  POP_JUMP_IF_FALSE    30  'to 30'
               22  LOAD_CONST               32
               24  COMPARE_OP               <=
               26  POP_JUMP_IF_TRUE     36  'to 36'
               28  JUMP_FORWARD         32  'to 32'
             30_0  COME_FROM            20  '20'
             30_1  COME_FROM            10  '10'
               30  POP_TOP          
             32_0  COME_FROM            28  '28'
               32  LOAD_GLOBAL              AssertionError
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L.1206        36  LOAD_GLOBAL              SearchStrategy
               38  LOAD_METHOD              __init__
               40  LOAD_FAST                'self'
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          

 L.1207        46  LOAD_FAST                'shape'
               48  LOAD_FAST                'self'
               50  STORE_ATTR               shape

 L.1208        52  LOAD_FAST                'min_dims'
               54  LOAD_FAST                'self'
               56  STORE_ATTR               min_dims

 L.1209        58  LOAD_FAST                'max_dims'
               60  LOAD_FAST                'self'
               62  STORE_ATTR               max_dims

 L.1210        64  LOAD_FAST                'allow_ellipsis'
               66  LOAD_FAST                'self'
               68  STORE_ATTR               allow_ellipsis

 L.1211        70  LOAD_FAST                'allow_newaxis'
               72  LOAD_FAST                'self'
               74  STORE_ATTR               allow_newaxis

Parse error at or near `None' instruction at offset -1

    def do_draw(self, data):
        result = []
        for dim_size in self.shape:
            if dim_size == 0:
                result.append(slice(None))
            else:
                strategy = st.integers(-dim_size, dim_size - 1) | st.slices(dim_size)
                result.append(data.draw(strategy))
        else:
            result_dims = sum((isinstance(idx, slice) for idx in result))
            while self.allow_newaxis:
                if result_dims < self.max_dims:
                    if result_dims < self.min_dims or data.draw(st.booleans()):
                        result.insert(data.draw(st.integers(0, len(result))), np.newaxis)
                        result_dims += 1

            assume(self.min_dims <= result_dims <= self.max_dims)
            if self.allow_ellipsis and data.draw(st.booleans()):
                i = j = data.draw(st.integers(0, len(result)))
                if i > 0:
                    if result[(i - 1)] == slice(None):
                        i -= 1
                else:
                    while j < len(result):
                        if result[j] == slice(None):
                            j += 1

                result[i:j] = [
                 Ellipsis]
            else:
                while result[-1:] == [slice(None, None)]:
                    if data.draw(st.integers(0, 7)):
                        result.pop()

                return tuple(result)


@st.defines_strategy
def basic_indices(shape: Shape, *, min_dims: int=0, max_dims: int=None, allow_newaxis: bool=False, allow_ellipsis: bool=True) -> st.SearchStrategy[BasicIndex]:
    """
    The ``basic_indices`` strategy generates `basic indexes
    <https://docs.scipy.org/doc/numpy/reference/arrays.indexing.html>`__  for
    arrays of the specified shape, which may include dimensions of size zero.

    It generates tuples containing some mix of integers, :obj:`python:slice` objects,
    ``...`` (Ellipsis), and :obj:`numpy:numpy.newaxis`; which when used to index a
    ``shape``-shaped array will produce either a scalar or a shared-memory view.

    * ``shape``: the array shape that will be indexed, as a tuple of integers >= 0.
      This must be at least two-dimensional for a tuple to be a valid basic index;
      for one-dimensional arrays use :func:`~hypothesis.strategies.slices` instead.
    * ``min_dims``: the minimum dimensionality of the resulting view from use of
      the generated index.  When ``min_dims == 0``, scalars and zero-dimensional
      arrays are both allowed.
    * ``max_dims``: the maximum dimensionality of the resulting view.
      If not specified, it defaults to ``max(len(shape), min_dims) + 2``.
    * ``allow_ellipsis``: whether ``...``` is allowed in the index.
    * ``allow_newaxis``: whether :obj:`numpy:numpy.newaxis` is allowed in the index.

    Note that the length of the generated tuple may be anywhere between zero
    and ``min_dims``.  It may not match the length of ``shape``, or even the
    dimensionality of the array view resulting from its use!
    """
    check_type(tuple, shape, 'shape')
    check_type(bool, allow_ellipsis, 'allow_ellipsis')
    check_type(bool, allow_newaxis, 'allow_newaxis')
    check_type(int, min_dims, 'min_dims')
    if max_dims is None:
        max_dims = min(max(len(shape), min_dims) + 2, 32)
    else:
        check_type(int, max_dims, 'max_dims')
    order_check('dims', 0, min_dims, max_dims)
    check_argument(max_dims <= 32, 'max_dims=%r, but numpy arrays have at most 32 dimensions' % (max_dims,))
    check_argument(all((isinstance(x, int) and x >= 0 for x in shape)), 'shape=%r, but all dimensions must be of integer size >= 0' % (shape,))
    return BasicIndexStrategy(shape,
      min_dims=min_dims,
      max_dims=max_dims,
      allow_ellipsis=allow_ellipsis,
      allow_newaxis=allow_newaxis)


@st.defines_strategy
def integer_array_indices(shape: Shape, result_shape: SearchStrategy[Shape]=array_shapes(), dtype: np.dtype='int') -> st.SearchStrategy[Tuple[(np.ndarray, ...)]]:
    """Return a search strategy for tuples of integer-arrays that, when used
    to index into an array of shape ``shape``, given an array whose shape
    was drawn from ``result_shape``.

    Examples from this strategy shrink towards the tuple of index-arrays::

        len(shape) * (np.zeros(drawn_result_shape, dtype), )

    * ``shape`` a tuple of integers that indicates the shape of the array,
      whose indices are being generated.
    * ``result_shape`` a strategy for generating tuples of integers, which
      describe the shape of the resulting index arrays. The default is
      :func:`~hypothesis.extra.numpy.array_shapes`.  The shape drawn from
      this strategy determines the shape of the array that will be produced
      when the corresponding example from ``integer_array_indices`` is used
      as an index.
    * ``dtype`` the integer data type of the generated index-arrays. Negative
      integer indices can be generated if a signed integer type is specified.

    Recall that an array can be indexed using a tuple of integer-arrays to
    access its members in an arbitrary order, producing an array with an
    arbitrary shape. For example:

    .. code-block:: pycon

        >>> from numpy import array
        >>> x = array([-0, -1, -2, -3, -4])
        >>> ind = (array([[4, 0], [0, 1]]),)  # a tuple containing a 2D integer-array
        >>> x[ind]  # the resulting array is commensurate with the indexing array(s)
        array([[-4,  0],
               [0, -1]])

    Note that this strategy does not accommodate all variations of so-called
    'advanced indexing', as prescribed by NumPy's nomenclature.  Combinations
    of basic and advanced indexes are too complex to usefully define in a
    standard strategy; we leave application-specific strategies to the user.
    Advanced-boolean indexing can be defined as ``arrays(shape=..., dtype=bool)``,
    and is similarly left to the user.
    """
    check_type(tuple, shape, 'shape')
    check_argument(shape and all((isinstance(x, int) and x > 0 for x in shape)), 'shape=%r must be a non-empty tuple of integers > 0' % (shape,))
    check_type(SearchStrategy, result_shape, 'result_shape')
    check_argument(np.issubdtype(dtype, np.integer), 'dtype=%r must be an integer dtype' % (dtype,))
    signed = np.issubdtype(dtype, np.signedinteger)

    def array_for(index_shape, size):
        return arrays(dtype=dtype,
          shape=index_shape,
          elements=(st.integers(-size if signed else 0, size - 1)))

    return result_shape.flatmap(lambda index_shape: (st.tuples)(*[array_for(index_shape, size) for size in shape]))
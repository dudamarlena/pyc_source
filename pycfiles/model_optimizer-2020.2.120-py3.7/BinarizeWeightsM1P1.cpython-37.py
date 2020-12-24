# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/middle/BinarizeWeightsM1P1.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 6759 bytes
"""
 Copyright (C) 2018-2020 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import logging as log, numpy as np
import extensions.middle.CheckForCycle as CheckForCycle
import extensions.middle.DeleteNotExecutable as DeleteNotExecutable
from extensions.ops.elementwise import Mul, Pow
from mo.front.common.partial_infer.utils import int64_array
from mo.graph.graph import Graph
from mo.middle.replacement import MiddleReplacementPattern
from mo.ops.const import Const
from mo.ops.reshape import Reshape

class BinarizeWeightsM1P1(MiddleReplacementPattern):
    __doc__ = " Convert weights to -1/+1 form\n\n        Applicable for convolutions and other operations that have 'weights' that combined with the input data\n        by mean of multiplication operation. So any linear operator suits. Detect such operations by\n        multiplication_transparent attribute -- if it is presents and set to True, then multiplication term\n        can be passed through the operation. If multiplication_transparent attribute is set to True for an operation,\n        such operation should also has multiplication_transparent_ports that contain a list of pairs with\n        port indices (in_port, out_port) that defines which port pairs can pass multiplication through.\n\n        For example for some convolutional operation which has 2 ports (input tensor and weights) and 1 output port\n        this list includes [(0,0)(1,0)]. If convolutional operation also has biases at port 2, it is not included into\n        this list because this port is not transparent for multiplication operation.\n\n        multiplication_transparent_ports can be None if all possible input/output pairs are multiplication\n        transparent.\n\n        #TODO Describe how to apply multiplication at output ports -- this is not specified. In the current definition\n        we can pass through only scalar multiplication, but we already requre passing it channel-wise.\n    "
    enabled = True

    def run_after(self):
        return []

    def run_before(self):
        return [
         CheckForCycle, DeleteNotExecutable]

    def pattern(self):
        return dict(nodes=[
         (
          'quantize', dict(kind='op', op='FakeQuantize')),
         (
          'quantized', dict()),
         (
          'operator', dict(kind='op', multiplication_transparent=True))],
          edges=[
         ('quantize', 'quantized'),
         ('quantized', 'operator')])

    def replace_pattern--- This code section failed: ---

 L.  74         0  LOAD_FAST                'match'
                2  LOAD_STR                 'operator'
                4  BINARY_SUBSCR    
                6  LOAD_METHOD              has
                8  LOAD_STR                 'multiplication_transparent_ports'
               10  CALL_METHOD_1         1  '1 positional argument'
               12  POP_JUMP_IF_TRUE     18  'to 18'
               14  LOAD_ASSERT              AssertionError
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM            12  '12'

 L.  76        18  LOAD_FAST                'match'
               20  LOAD_STR                 'operator'
               22  BINARY_SUBSCR    
               24  LOAD_METHOD              input_ports_with
               26  LOAD_FAST                'match'
               28  LOAD_STR                 'quantized'
               30  BINARY_SUBSCR    
               32  CALL_METHOD_1         1  '1 positional argument'
               34  STORE_DEREF              'port'

 L.  77        36  LOAD_GLOBAL              len
               38  LOAD_DEREF               'port'
               40  CALL_FUNCTION_1       1  '1 positional argument'
               42  LOAD_CONST               1
               44  COMPARE_OP               >=
               46  POP_JUMP_IF_TRUE     52  'to 52'
               48  LOAD_ASSERT              AssertionError
               50  RAISE_VARARGS_1       1  'exception instance'
             52_0  COME_FROM            46  '46'

 L.  78        52  LOAD_GLOBAL              len
               54  LOAD_DEREF               'port'
               56  CALL_FUNCTION_1       1  '1 positional argument'
               58  LOAD_CONST               1
               60  COMPARE_OP               >
               62  POP_JUMP_IF_FALSE    90  'to 90'

 L.  79        64  LOAD_GLOBAL              log
               66  LOAD_METHOD              debug
               68  LOAD_STR                 'BinarizeWeightsM1P1 cannot apply transformation for data {} because it consumed more than once'
               70  LOAD_METHOD              format

 L.  80        72  LOAD_FAST                'match'
               74  LOAD_STR                 'quantized'
               76  BINARY_SUBSCR    
               78  LOAD_ATTR                name
               80  CALL_METHOD_1         1  '1 positional argument'
               82  CALL_METHOD_1         1  '1 positional argument'
               84  POP_TOP          

 L.  81        86  LOAD_CONST               None
               88  RETURN_VALUE     
             90_0  COME_FROM            62  '62'

 L.  83        90  LOAD_GLOBAL              len
               92  LOAD_DEREF               'port'
               94  CALL_FUNCTION_1       1  '1 positional argument'
               96  LOAD_CONST               1
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_TRUE    106  'to 106'
              102  LOAD_ASSERT              AssertionError
              104  RAISE_VARARGS_1       1  'exception instance'
            106_0  COME_FROM           100  '100'

 L.  84       106  LOAD_DEREF               'port'
              108  LOAD_CONST               0
              110  BINARY_SUBSCR    
              112  STORE_DEREF              'port'

 L.  85       114  LOAD_CLOSURE             'port'
              116  BUILD_TUPLE_1         1 
              118  LOAD_LISTCOMP            '<code_object <listcomp>>'
              120  LOAD_STR                 'BinarizeWeightsM1P1.replace_pattern.<locals>.<listcomp>'
              122  MAKE_FUNCTION_8          'closure'
              124  LOAD_FAST                'match'
              126  LOAD_STR                 'operator'
              128  BINARY_SUBSCR    
              130  LOAD_ATTR                multiplication_transparent_ports
              132  GET_ITER         
              134  CALL_FUNCTION_1       1  '1 positional argument'
              136  STORE_FAST               'applicable'

 L.  86       138  LOAD_GLOBAL              len
              140  LOAD_FAST                'applicable'
              142  CALL_FUNCTION_1       1  '1 positional argument'
              144  LOAD_CONST               0
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   154  'to 154'

 L.  87       150  LOAD_CONST               None
              152  RETURN_VALUE     
            154_0  COME_FROM           148  '148'

 L.  91       154  LOAD_FAST                'match'
              156  LOAD_STR                 'quantize'
              158  BINARY_SUBSCR    
              160  STORE_FAST               'quantize'

 L.  92       162  LOAD_FAST                'quantize'
              164  LOAD_METHOD              in_node
              166  LOAD_CONST               3
              168  CALL_METHOD_1         1  '1 positional argument'
              170  STORE_FAST               'output_low'

 L.  93       172  LOAD_FAST                'quantize'
              174  LOAD_METHOD              in_node
              176  LOAD_CONST               4
              178  CALL_METHOD_1         1  '1 positional argument'
              180  STORE_FAST               'output_high'

 L.  95       182  LOAD_FAST                'output_low'
              184  LOAD_METHOD              has_valid
              186  LOAD_STR                 'value'
              188  CALL_METHOD_1         1  '1 positional argument'
              190  POP_JUMP_IF_TRUE    206  'to 206'
              192  LOAD_FAST                'output_high'
              194  LOAD_METHOD              has_valid
              196  LOAD_STR                 'value'
              198  CALL_METHOD_1         1  '1 positional argument'
              200  POP_JUMP_IF_TRUE    206  'to 206'

 L.  96       202  LOAD_CONST               None
              204  RETURN_VALUE     
            206_0  COME_FROM           200  '200'
            206_1  COME_FROM           190  '190'

 L.  98       206  LOAD_FAST                'output_low'
              208  LOAD_ATTR                value
              210  STORE_FAST               'output_low'

 L.  99       212  LOAD_FAST                'output_high'
              214  LOAD_ATTR                value
              216  STORE_FAST               'output_high'

 L. 102       218  LOAD_FAST                'quantize'
              220  LOAD_ATTR                levels
              222  LOAD_CONST               2
              224  COMPARE_OP               !=
              226  POP_JUMP_IF_FALSE   232  'to 232'

 L. 103       228  LOAD_CONST               None
              230  RETURN_VALUE     
            232_0  COME_FROM           226  '226'

 L. 106       232  LOAD_GLOBAL              np
              234  LOAD_METHOD              all
              236  LOAD_FAST                'output_low'
              238  LOAD_CONST               0
              240  COMPARE_OP               ==
              242  CALL_METHOD_1         1  '1 positional argument'
          244_246  JUMP_IF_TRUE_OR_POP   260  'to 260'
              248  LOAD_GLOBAL              np
              250  LOAD_METHOD              all
              252  LOAD_FAST                'output_high'
              254  LOAD_CONST               0
              256  COMPARE_OP               ==
              258  CALL_METHOD_1         1  '1 positional argument'
            260_0  COME_FROM           244  '244'
              260  STORE_FAST               'zp1'

 L. 107       262  LOAD_GLOBAL              np
              264  LOAD_METHOD              all
              266  LOAD_FAST                'output_low'
              268  UNARY_NEGATIVE   
              270  LOAD_FAST                'output_high'
              272  COMPARE_OP               ==
              274  CALL_METHOD_1         1  '1 positional argument'
              276  STORE_FAST               'm1p1'

 L. 108       278  LOAD_FAST                'zp1'
          280_282  POP_JUMP_IF_TRUE    290  'to 290'
              284  LOAD_FAST                'm1p1'
          286_288  POP_JUMP_IF_FALSE   302  'to 302'
            290_0  COME_FROM           280  '280'
              290  LOAD_FAST                'zp1'
          292_294  POP_JUMP_IF_FALSE   328  'to 328'
              296  LOAD_FAST                'm1p1'
          298_300  POP_JUMP_IF_FALSE   328  'to 328'
            302_0  COME_FROM           286  '286'

 L. 109       302  LOAD_GLOBAL              log
              304  LOAD_METHOD              debug
              306  LOAD_STR                 "BinarizeWeightsM1P1 cannot apply transformation for data {} because it does't has one of 0/+1 or -1/+1 forms."
              308  LOAD_METHOD              format

 L. 110       310  LOAD_FAST                'match'
              312  LOAD_STR                 'quantized'
              314  BINARY_SUBSCR    
              316  LOAD_ATTR                name
              318  CALL_METHOD_1         1  '1 positional argument'
              320  CALL_METHOD_1         1  '1 positional argument'
              322  POP_TOP          

 L. 111       324  LOAD_CONST               None
              326  RETURN_VALUE     
            328_0  COME_FROM           298  '298'
            328_1  COME_FROM           292  '292'

 L. 116       328  LOAD_GLOBAL              np
              330  LOAD_METHOD              all
              332  LOAD_FAST                'output_high'
              334  LOAD_CONST               0
              336  COMPARE_OP               ==
              338  CALL_METHOD_1         1  '1 positional argument'
          340_342  POP_JUMP_IF_FALSE   354  'to 354'
              344  LOAD_FAST                'quantize'
              346  LOAD_METHOD              in_node
              348  LOAD_CONST               3
              350  CALL_METHOD_1         1  '1 positional argument'
              352  JUMP_FORWARD        362  'to 362'
            354_0  COME_FROM           340  '340'
              354  LOAD_FAST                'quantize'
              356  LOAD_METHOD              in_node
              358  LOAD_CONST               4
              360  CALL_METHOD_1         1  '1 positional argument'
            362_0  COME_FROM           352  '352'
              362  STORE_FAST               'mult_term'

 L. 118       364  LOAD_GLOBAL              Const
              366  LOAD_FAST                'graph'
              368  LOAD_STR                 'value'
              370  LOAD_GLOBAL              int64_array
              372  LOAD_CONST               -1
              374  LOAD_CONST               1
              376  LOAD_CONST               1
              378  BUILD_LIST_3          3 
              380  CALL_FUNCTION_1       1  '1 positional argument'
              382  BUILD_MAP_1           1 
              384  CALL_FUNCTION_2       2  '2 positional arguments'
              386  LOAD_METHOD              create_node_with_data
              388  CALL_METHOD_0         0  '0 positional arguments'
              390  STORE_FAST               'new_shape'

 L. 119       392  LOAD_GLOBAL              Reshape
              394  LOAD_FAST                'graph'
              396  BUILD_MAP_0           0 
              398  CALL_FUNCTION_2       2  '2 positional arguments'
              400  LOAD_METHOD              create_node_with_data
              402  LOAD_FAST                'mult_term'
              404  LOAD_FAST                'new_shape'
              406  BUILD_LIST_2          2 
              408  CALL_METHOD_1         1  '1 positional argument'
              410  STORE_FAST               'reshape'

 L. 125       412  LOAD_GLOBAL              len
              414  LOAD_FAST                'match'
              416  LOAD_STR                 'quantized'
              418  BINARY_SUBSCR    
              420  LOAD_METHOD              out_nodes
              422  CALL_METHOD_0         0  '0 positional arguments'
              424  CALL_FUNCTION_1       1  '1 positional argument'
              426  LOAD_CONST               1
              428  COMPARE_OP               >
          430_432  POP_JUMP_IF_FALSE   448  'to 448'

 L. 126       434  LOAD_GLOBAL              log
              436  LOAD_METHOD              debug
              438  LOAD_STR                 "BinarizeWeightsM1P1: len(match['quantized'].out_nodes()) > 1"
              440  CALL_METHOD_1         1  '1 positional argument'
              442  POP_TOP          

 L. 127       444  LOAD_CONST               None
              446  RETURN_VALUE     
            448_0  COME_FROM           430  '430'

 L. 128       448  LOAD_GLOBAL              Const
              450  LOAD_FAST                'graph'
              452  LOAD_STR                 'value'
              454  LOAD_GLOBAL              np
              456  LOAD_METHOD              array
              458  LOAD_CONST               -1.0
              460  CALL_METHOD_1         1  '1 positional argument'
              462  BUILD_MAP_1           1 
              464  CALL_FUNCTION_2       2  '2 positional arguments'
              466  LOAD_METHOD              create_node_with_data
              468  CALL_METHOD_0         0  '0 positional arguments'
              470  STORE_FAST               'power_of_exponent'

 L. 129       472  LOAD_GLOBAL              Pow
              474  LOAD_FAST                'graph'
              476  LOAD_STR                 'name'
              478  LOAD_FAST                'quantize'
              480  LOAD_ATTR                name
              482  LOAD_STR                 '/DivNormalize'
              484  BINARY_ADD       
              486  BUILD_MAP_1           1 
              488  CALL_FUNCTION_2       2  '2 positional arguments'
              490  STORE_FAST               'div_op'

 L. 130       492  LOAD_FAST                'div_op'
              494  LOAD_METHOD              create_node_with_data
              496  LOAD_FAST                'mult_term'
              498  LOAD_FAST                'power_of_exponent'
              500  BUILD_LIST_2          2 
              502  CALL_METHOD_1         1  '1 positional argument'
              504  STORE_FAST               'div_output'

 L. 132       506  SETUP_LOOP          568  'to 568'
              508  LOAD_CONST               (3, 4)
              510  GET_ITER         
              512  FOR_ITER            566  'to 566'
              514  STORE_FAST               'i'

 L. 133       516  LOAD_FAST                'match'
              518  LOAD_STR                 'quantize'
              520  BINARY_SUBSCR    
              522  LOAD_ATTR                insert_node_with_data_before

 L. 134       524  LOAD_FAST                'match'
              526  LOAD_STR                 'quantize'
              528  BINARY_SUBSCR    
              530  LOAD_METHOD              in_node
              532  LOAD_FAST                'i'
              534  CALL_METHOD_1         1  '1 positional argument'

 L. 135       536  LOAD_GLOBAL              Mul

 L. 136       538  LOAD_GLOBAL              dict
              540  LOAD_FAST                'quantize'
              542  LOAD_ATTR                name
              544  LOAD_STR                 '/MulNormalize'
              546  BINARY_ADD       
              548  LOAD_CONST               ('name',)
              550  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 137       552  LOAD_FAST                'div_output'
              554  BUILD_LIST_1          1 
              556  LOAD_CONST               ('additional_inputs',)
              558  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              560  POP_TOP          
          562_564  JUMP_BACK           512  'to 512'
              566  POP_BLOCK        
            568_0  COME_FROM_LOOP      506  '506'

 L. 140       568  LOAD_CONST               None
              570  LOAD_FAST                'match'
              572  LOAD_STR                 'quantized'
              574  BINARY_SUBSCR    
              576  STORE_ATTR               value

 L. 141       578  LOAD_FAST                'match'
              580  LOAD_STR                 'quantize'
              582  BINARY_SUBSCR    
              584  LOAD_METHOD              infer
              586  LOAD_FAST                'match'
              588  LOAD_STR                 'quantize'
              590  BINARY_SUBSCR    
              592  CALL_METHOD_1         1  '1 positional argument'
              594  POP_TOP          

 L. 145       596  LOAD_FAST                'match'
              598  LOAD_STR                 'operator'
              600  BINARY_SUBSCR    
              602  LOAD_METHOD              insert_node_with_data_after

 L. 146       604  LOAD_FAST                'match'
              606  LOAD_STR                 'operator'
              608  BINARY_SUBSCR    
              610  LOAD_METHOD              out_node
              612  CALL_METHOD_0         0  '0 positional arguments'

 L. 147       614  LOAD_GLOBAL              Mul

 L. 148       616  LOAD_GLOBAL              dict
              618  LOAD_FAST                'match'
              620  LOAD_STR                 'operator'
              622  BINARY_SUBSCR    
              624  LOAD_ATTR                name
              626  LOAD_STR                 '/MulNormalize'
              628  BINARY_ADD       
              630  LOAD_CONST               ('name',)
              632  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 149       634  LOAD_FAST                'reshape'
              636  BUILD_LIST_1          1 
              638  CALL_METHOD_4         4  '4 positional arguments'
              640  POP_TOP          

 L. 153       642  LOAD_CONST               False
              644  LOAD_FAST                'match'
              646  LOAD_STR                 'operator'
              648  BINARY_SUBSCR    
              650  LOAD_STR                 'can_be_fused'
              652  STORE_SUBSCR     

Parse error at or near `LOAD_STR' instruction at offset 650
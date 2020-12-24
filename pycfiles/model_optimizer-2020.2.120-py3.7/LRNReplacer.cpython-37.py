# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/LRNReplacer.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 1877 bytes
"""
 Copyright (C) 2017-2020 Intel Corporation

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
import numpy as np
from mo.front.common.replacement import FrontReplacementOp
from mo.graph.graph import Graph
from extensions.ops.elementwise import Mul
from mo.ops.const import Const

class LRNReplacer(FrontReplacementOp):
    op = 'AttributedLRN'
    enabled = True
    graph_condition = [lambda graph: not graph.graph['cmd_params'].generate_experimental_IR_V10]

    def replace_sub_graph--- This code section failed: ---

 L.  31         0  LOAD_FAST                'match'
                2  LOAD_STR                 'op'
                4  BINARY_SUBSCR    
                6  STORE_FAST               'node'

 L.  33         8  LOAD_FAST                'node'
               10  LOAD_METHOD              has_valid
               12  LOAD_STR                 'bias'
               14  CALL_METHOD_1         1  '1 positional argument'
               16  POP_JUMP_IF_FALSE    38  'to 38'
               18  LOAD_FAST                'node'
               20  LOAD_METHOD              has_valid
               22  LOAD_STR                 'bias'
               24  CALL_METHOD_1         1  '1 positional argument'
               26  POP_JUMP_IF_FALSE    42  'to 42'
               28  LOAD_FAST                'node'
               30  LOAD_ATTR                bias
               32  LOAD_CONST               1
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    42  'to 42'
             38_0  COME_FROM            16  '16'

 L.  34        38  LOAD_CONST               None
               40  RETURN_VALUE     
             42_0  COME_FROM            36  '36'
             42_1  COME_FROM            26  '26'

 L.  37        42  LOAD_GLOBAL              np
               44  LOAD_METHOD              array
               46  LOAD_CONST               1.0
               48  LOAD_GLOBAL              pow
               50  LOAD_FAST                'node'
               52  LOAD_ATTR                bias
               54  LOAD_FAST                'node'
               56  LOAD_ATTR                beta
               58  CALL_FUNCTION_2       2  '2 positional arguments'
               60  BINARY_TRUE_DIVIDE
               62  CALL_METHOD_1         1  '1 positional argument'
               64  STORE_FAST               'scale_value'

 L.  38        66  LOAD_FAST                'node'
               68  DUP_TOP          
               70  LOAD_ATTR                alpha
               72  LOAD_FAST                'node'
               74  LOAD_ATTR                bias
               76  INPLACE_TRUE_DIVIDE
               78  ROT_TWO          
               80  STORE_ATTR               alpha

 L.  39        82  LOAD_GLOBAL              Const
               84  LOAD_FAST                'graph'
               86  LOAD_FAST                'scale_value'
               88  LOAD_FAST                'scale_value'
               90  LOAD_ATTR                shape

 L.  40        92  LOAD_FAST                'node'
               94  LOAD_ATTR                name
               96  LOAD_STR                 '/Const_Mul_'
               98  BINARY_ADD       
              100  LOAD_CONST               ('value', 'shape', 'name')
              102  BUILD_CONST_KEY_MAP_3     3 
              104  CALL_FUNCTION_2       2  '2 positional arguments'
              106  LOAD_METHOD              create_node
              108  CALL_METHOD_0         0  '0 positional arguments'
              110  STORE_FAST               'const_node'

 L.  43       112  LOAD_GLOBAL              Mul
              114  LOAD_FAST                'graph'
              116  LOAD_STR                 'name'
              118  LOAD_FAST                'node'
              120  LOAD_ATTR                name
              122  LOAD_STR                 '/Mul_'
              124  BINARY_ADD       
              126  BUILD_MAP_1           1 
              128  CALL_FUNCTION_2       2  '2 positional arguments'
              130  LOAD_METHOD              create_node
              132  CALL_METHOD_0         0  '0 positional arguments'
              134  STORE_FAST               'mul_node'

 L.  46       136  LOAD_FAST                'const_node'
              138  LOAD_METHOD              out_port
              140  LOAD_CONST               0
              142  CALL_METHOD_1         1  '1 positional argument'
              144  LOAD_METHOD              connect
              146  LOAD_FAST                'mul_node'
              148  LOAD_METHOD              in_port
              150  LOAD_CONST               1
              152  CALL_METHOD_1         1  '1 positional argument'
              154  CALL_METHOD_1         1  '1 positional argument'
              156  POP_TOP          

 L.  47       158  LOAD_FAST                'node'
              160  LOAD_METHOD              out_port
              162  LOAD_CONST               0
              164  CALL_METHOD_1         1  '1 positional argument'
              166  LOAD_METHOD              get_connection
              168  CALL_METHOD_0         0  '0 positional arguments'
              170  LOAD_METHOD              set_source
              172  LOAD_FAST                'mul_node'
              174  LOAD_METHOD              out_port
              176  LOAD_CONST               0
              178  CALL_METHOD_1         1  '1 positional argument'
              180  CALL_METHOD_1         1  '1 positional argument'
              182  POP_TOP          

 L.  48       184  LOAD_FAST                'node'
              186  LOAD_METHOD              out_port
              188  LOAD_CONST               0
              190  CALL_METHOD_1         1  '1 positional argument'
              192  LOAD_METHOD              connect
              194  LOAD_FAST                'mul_node'
              196  LOAD_METHOD              in_port
              198  LOAD_CONST               0
              200  CALL_METHOD_1         1  '1 positional argument'
              202  CALL_METHOD_1         1  '1 positional argument'
              204  POP_TOP          

 L.  51       206  LOAD_FAST                'node'
              208  LOAD_STR                 'bias'
              210  DELETE_SUBSCR    

Parse error at or near `LOAD_STR' instruction at offset 208
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/middle/FusedBatchNormNonConstant.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 3805 bytes
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
import numpy as np
from extensions.ops.elementwise import Mul, Add, Pow
from mo.graph.graph import Graph
from mo.middle.replacement import MiddleReplacementPattern
from mo.ops.const import Const

class FusedBatchNormNonConstant(MiddleReplacementPattern):
    __doc__ = '\n    Replaces FusedBatchNorm(input, beta, gamma, mean, variance) with non-constant mean and variance,\n    but with constant beta and gamma to a sub-expression consisting of a combinatin of Eltwise layers and ScaleShift.\n    '
    enabled = True

    def run_after(self):
        from extensions.middle.pass_separator import MiddleStart
        return [
         MiddleStart]

    def run_before(self):
        from extensions.middle.pass_separator import MiddleFinish
        return [
         MiddleFinish]

    def pattern(self):
        return dict(nodes=[
         (
          'op', dict(kind='op', op='FusedBatchNorm'))],
          edges=[])

    def replace_pattern--- This code section failed: ---

 L.  48         0  LOAD_FAST                'match'
                2  LOAD_STR                 'op'
                4  BINARY_SUBSCR    
                6  STORE_FAST               'node'

 L.  49         8  LOAD_FAST                'node'
               10  LOAD_ATTR                data_format
               12  LOAD_CONST               b'NHWC'
               14  COMPARE_OP               !=
               16  POP_JUMP_IF_TRUE    150  'to 150'

 L.  50        18  LOAD_GLOBAL              len
               20  LOAD_FAST                'node'
               22  LOAD_METHOD              in_nodes
               24  CALL_METHOD_0         0  '0 positional arguments'
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  LOAD_CONST               5
               30  COMPARE_OP               !=
               32  POP_JUMP_IF_TRUE    150  'to 150'

 L.  51        34  LOAD_FAST                'node'
               36  LOAD_METHOD              in_node
               38  LOAD_CONST               0
               40  CALL_METHOD_1         1  '1 positional argument'
               42  LOAD_ATTR                value
               44  LOAD_CONST               None
               46  COMPARE_OP               is-not
               48  POP_JUMP_IF_TRUE    150  'to 150'

 L.  52        50  LOAD_FAST                'node'
               52  LOAD_METHOD              in_node
               54  LOAD_CONST               1
               56  CALL_METHOD_1         1  '1 positional argument'
               58  LOAD_ATTR                value
               60  LOAD_CONST               None
               62  COMPARE_OP               is
               64  POP_JUMP_IF_TRUE    150  'to 150'

 L.  53        66  LOAD_FAST                'node'
               68  LOAD_METHOD              in_node
               70  LOAD_CONST               2
               72  CALL_METHOD_1         1  '1 positional argument'
               74  LOAD_ATTR                value
               76  LOAD_CONST               None
               78  COMPARE_OP               is
               80  POP_JUMP_IF_TRUE    150  'to 150'

 L.  54        82  LOAD_FAST                'node'
               84  LOAD_METHOD              in_node
               86  LOAD_CONST               3
               88  CALL_METHOD_1         1  '1 positional argument'
               90  LOAD_ATTR                value
               92  LOAD_CONST               None
               94  COMPARE_OP               is-not
               96  POP_JUMP_IF_TRUE    150  'to 150'

 L.  55        98  LOAD_FAST                'node'
              100  LOAD_METHOD              in_node
              102  LOAD_CONST               4
              104  CALL_METHOD_1         1  '1 positional argument'
              106  LOAD_ATTR                value
              108  LOAD_CONST               None
              110  COMPARE_OP               is-not
              112  POP_JUMP_IF_TRUE    150  'to 150'

 L.  56       114  LOAD_FAST                'node'
              116  LOAD_METHOD              in_node
              118  LOAD_CONST               1
              120  CALL_METHOD_1         1  '1 positional argument'
              122  LOAD_ATTR                value
              124  LOAD_ATTR                ndim
              126  LOAD_CONST               1
              128  COMPARE_OP               !=
              130  POP_JUMP_IF_TRUE    150  'to 150'

 L.  57       132  LOAD_FAST                'node'
              134  LOAD_METHOD              in_node
              136  LOAD_CONST               2
              138  CALL_METHOD_1         1  '1 positional argument'
              140  LOAD_ATTR                value
              142  LOAD_ATTR                ndim
              144  LOAD_CONST               1
              146  COMPARE_OP               !=
              148  POP_JUMP_IF_FALSE   154  'to 154'
            150_0  COME_FROM           130  '130'
            150_1  COME_FROM           112  '112'
            150_2  COME_FROM            96  '96'
            150_3  COME_FROM            80  '80'
            150_4  COME_FROM            64  '64'
            150_5  COME_FROM            48  '48'
            150_6  COME_FROM            32  '32'
            150_7  COME_FROM            16  '16'

 L.  58       150  LOAD_CONST               None
              152  RETURN_VALUE     
            154_0  COME_FROM           148  '148'

 L.  60       154  LOAD_GLOBAL              Mul
              156  LOAD_FAST                'graph'
              158  LOAD_GLOBAL              dict
              160  LOAD_FAST                'node'
              162  LOAD_ATTR                name
              164  LOAD_STR                 '/scale_mul_'
              166  BINARY_ADD       
              168  LOAD_CONST               ('name',)
              170  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              172  CALL_FUNCTION_2       2  '2 positional arguments'
              174  STORE_FAST               'scale_mul'

 L.  61       176  LOAD_GLOBAL              Add
              178  LOAD_FAST                'graph'
              180  LOAD_GLOBAL              dict
              182  LOAD_FAST                'node'
              184  LOAD_ATTR                name
              186  LOAD_STR                 '/shift_add_'
              188  BINARY_ADD       
              190  LOAD_CONST               ('name',)
              192  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              194  CALL_FUNCTION_2       2  '2 positional arguments'
              196  STORE_FAST               'shift_add'

 L.  62       198  LOAD_GLOBAL              Add
              200  LOAD_FAST                'graph'
              202  LOAD_GLOBAL              dict
              204  LOAD_FAST                'node'
              206  LOAD_ATTR                name
              208  LOAD_STR                 '/mean_add_'
              210  BINARY_ADD       
              212  LOAD_CONST               ('name',)
              214  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              216  CALL_FUNCTION_2       2  '2 positional arguments'
              218  STORE_FAST               'mean_add'

 L.  63       220  LOAD_GLOBAL              Mul
              222  LOAD_FAST                'graph'
              224  LOAD_GLOBAL              dict
              226  LOAD_FAST                'node'
              228  LOAD_ATTR                name
              230  LOAD_STR                 '/variance_mul_'
              232  BINARY_ADD       
              234  LOAD_CONST               ('name',)
              236  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              238  CALL_FUNCTION_2       2  '2 positional arguments'
              240  STORE_FAST               'variance_mul'

 L.  65       242  LOAD_GLOBAL              Const
              244  LOAD_FAST                'graph'
              246  LOAD_GLOBAL              dict
              248  LOAD_GLOBAL              np
              250  LOAD_METHOD              array
              252  LOAD_CONST               -1
              254  CALL_METHOD_1         1  '1 positional argument'
              256  LOAD_FAST                'node'
              258  LOAD_ATTR                name
              260  LOAD_STR                 '/mean_negate_'
              262  BINARY_ADD       
              264  LOAD_CONST               ('value', 'name')
              266  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              268  CALL_FUNCTION_2       2  '2 positional arguments'
              270  STORE_FAST               'neg_const'

 L.  66       272  LOAD_GLOBAL              Mul
              274  LOAD_FAST                'graph'
              276  LOAD_GLOBAL              dict
              278  LOAD_FAST                'node'
              280  LOAD_ATTR                name
              282  LOAD_STR                 '/mean_negate_'
              284  BINARY_ADD       
              286  LOAD_CONST               ('name',)
              288  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              290  CALL_FUNCTION_2       2  '2 positional arguments'
              292  STORE_FAST               'mean_negate'

 L.  67       294  LOAD_FAST                'mean_add'
              296  LOAD_METHOD              create_node_with_data

 L.  68       298  LOAD_FAST                'node'
              300  LOAD_METHOD              in_node
              302  LOAD_CONST               0
              304  CALL_METHOD_1         1  '1 positional argument'

 L.  69       306  LOAD_FAST                'mean_negate'
              308  LOAD_METHOD              create_node_with_data
              310  LOAD_FAST                'node'
              312  LOAD_METHOD              in_node
              314  LOAD_CONST               3
              316  CALL_METHOD_1         1  '1 positional argument'

 L.  70       318  LOAD_FAST                'neg_const'
              320  LOAD_METHOD              create_node_with_data
              322  CALL_METHOD_0         0  '0 positional arguments'
              324  BUILD_LIST_2          2 
              326  CALL_METHOD_1         1  '1 positional argument'
              328  BUILD_LIST_2          2 
              330  CALL_METHOD_1         1  '1 positional argument'
              332  STORE_FAST               'mean_arg'

 L.  73       334  LOAD_GLOBAL              Const
              336  LOAD_FAST                'graph'
              338  LOAD_GLOBAL              dict
              340  LOAD_FAST                'node'
              342  LOAD_ATTR                eps
              344  LOAD_FAST                'node'
              346  LOAD_ATTR                name
              348  LOAD_STR                 '/variance_denom_shift_const_'
              350  BINARY_ADD       
              352  LOAD_CONST               ('value', 'name')
              354  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              356  CALL_FUNCTION_2       2  '2 positional arguments'
              358  STORE_FAST               'shift_const'

 L.  74       360  LOAD_GLOBAL              Const
              362  LOAD_FAST                'graph'
              364  LOAD_GLOBAL              dict
              366  LOAD_CONST               -0.5
              368  LOAD_FAST                'node'
              370  LOAD_ATTR                name
              372  LOAD_STR                 '/variance_denom_power_const_'
              374  BINARY_ADD       
              376  LOAD_CONST               ('value', 'name')
              378  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              380  CALL_FUNCTION_2       2  '2 positional arguments'
              382  STORE_FAST               'power_const'

 L.  75       384  LOAD_GLOBAL              Add
              386  LOAD_FAST                'graph'
              388  LOAD_GLOBAL              dict
              390  LOAD_FAST                'node'
              392  LOAD_ATTR                name
              394  LOAD_STR                 '/variance_denom_shift_'
              396  BINARY_ADD       
              398  LOAD_CONST               ('name',)
              400  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              402  CALL_FUNCTION_2       2  '2 positional arguments'
              404  STORE_FAST               'variance_denom_shift'

 L.  76       406  LOAD_GLOBAL              Pow
              408  LOAD_FAST                'graph'
              410  LOAD_GLOBAL              dict
              412  LOAD_FAST                'node'
              414  LOAD_ATTR                name
              416  LOAD_STR                 '/variance_denom_power_'
              418  BINARY_ADD       
              420  LOAD_CONST               ('name',)
              422  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              424  CALL_FUNCTION_2       2  '2 positional arguments'
              426  STORE_FAST               'variance_denom_power'

 L.  77       428  LOAD_FAST                'variance_mul'
              430  LOAD_METHOD              create_node_with_data

 L.  78       432  LOAD_FAST                'mean_arg'

 L.  79       434  LOAD_FAST                'variance_denom_power'
              436  LOAD_METHOD              create_node_with_data

 L.  80       438  LOAD_FAST                'variance_denom_shift'
              440  LOAD_METHOD              create_node_with_data
              442  LOAD_FAST                'node'
              444  LOAD_METHOD              in_node
              446  LOAD_CONST               4
              448  CALL_METHOD_1         1  '1 positional argument'
              450  LOAD_FAST                'shift_const'
              452  LOAD_METHOD              create_node_with_data
              454  CALL_METHOD_0         0  '0 positional arguments'
              456  BUILD_LIST_2          2 
              458  CALL_METHOD_1         1  '1 positional argument'

 L.  81       460  LOAD_FAST                'power_const'
              462  LOAD_METHOD              create_node_with_data
              464  CALL_METHOD_0         0  '0 positional arguments'
              466  BUILD_LIST_2          2 
              468  CALL_METHOD_1         1  '1 positional argument'
              470  BUILD_LIST_2          2 
              472  CALL_METHOD_1         1  '1 positional argument'
              474  STORE_FAST               'variance_arg'

 L.  84       476  LOAD_FAST                'shift_add'
              478  LOAD_ATTR                create_node_with_data

 L.  85       480  LOAD_FAST                'scale_mul'
              482  LOAD_METHOD              create_node_with_data

 L.  86       484  LOAD_FAST                'variance_arg'

 L.  87       486  LOAD_FAST                'node'
              488  LOAD_METHOD              in_node
              490  LOAD_CONST               1
              492  CALL_METHOD_1         1  '1 positional argument'
              494  BUILD_LIST_2          2 
              496  CALL_METHOD_1         1  '1 positional argument'

 L.  88       498  LOAD_FAST                'node'
              500  LOAD_METHOD              in_node
              502  LOAD_CONST               2
              504  CALL_METHOD_1         1  '1 positional argument'
              506  BUILD_LIST_2          2 

 L.  89       508  LOAD_FAST                'node'
              510  LOAD_METHOD              out_node
              512  CALL_METHOD_0         0  '0 positional arguments'
              514  LOAD_CONST               ('data_nodes',)
              516  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              518  POP_TOP          

 L.  91       520  LOAD_FAST                'node'
              522  LOAD_ATTR                graph
              524  LOAD_METHOD              remove_node
              526  LOAD_FAST                'node'
              528  LOAD_ATTR                id
              530  CALL_METHOD_1         1  '1 positional argument'
              532  POP_TOP          

Parse error at or near `CALL_METHOD_1' instruction at offset 530
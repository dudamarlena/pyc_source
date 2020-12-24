# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/ops/deconvolution.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 7154 bytes
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
from mo.front.common.partial_infer.utils import mark_input_bins, assign_dims_to_weights, tf_window_op_pad_infer
from mo.front.extractor import spatial_getter
from mo.front.onnx.extractors.utils import get_backend_pad
from mo.graph.graph import Node, Graph
from mo.graph.perm_inputs import PermuteInputs
from mo.ops.op import Op, PermuteAttrs

class Deconvolution(Op):
    op = 'Deconvolution'

    def __init__(self, graph, attrs):
        super().__init__(graph, {'kind':'op', 
         'type':__class__.op, 
         'op':__class__.op, 
         'infer':__class__.infer, 
         'in_ports_count':3, 
         'out_ports_count':1}, attrs)

    def backend_attrs(self):
        if self.ir_version == 10:
            return [('dilations', lambda node: ','.join(map(str, node['dilation'][node.spatial_dims]))),
             (
              'strides', lambda node: ','.join(map(str, node['stride'][node.spatial_dims]))),
             (
              'pads_begin',
              lambda node:               if node.has_valid('pad'):
','.join(map(str, get_backend_pad(node.pad, node.spatial_dims, 0))) # Avoid dead code: None),
             (
              'pads_end',
              lambda node:               if node.has_valid('pad'):
','.join(map(str, get_backend_pad(node.pad, node.spatial_dims, 1))) # Avoid dead code: None),
             'auto_pad']
        return [
         (
          'dilations',
          lambda node:           if node.has_valid('dilation'):
','.join(map(str, node['dilation'][node.spatial_dims])) # Avoid dead code: None),
         'auto_pad',
         'group',
         (
          'strides', lambda node: ','.join(map(str, node['stride'][node.spatial_dims]))),
         (
          'kernel', lambda node: ','.join(map(str, node['kernel_spatial']))),
         (
          'pads_begin', lambda node: ','.join(map(str, get_backend_pad(node.pad, node.spatial_dims, 0)))),
         (
          'pads_end', lambda node: ','.join(map(str, get_backend_pad(node.pad, node.spatial_dims, 1)))),
         'output']

    def backend_attrs_v2(self):
        return [
         spatial_getter('stride-x', 'stride', 1),
         spatial_getter('stride-y', 'stride', 0),
         (
          'kernel-x', lambda node: node.kernel_spatial[1]),
         (
          'kernel-y', lambda node: node.kernel_spatial[0]),
         spatial_getter('pad-x', 'pad', 1, lambda x: x[0]),
         spatial_getter('pad-y', 'pad', 0, lambda x: x[0]),
         spatial_getter('pad-r', 'pad', 1, lambda x: x[1]),
         spatial_getter('pad-b', 'pad', 0, lambda x: x[1]),
         'auto_pad',
         'output',
         'group']

    @staticmethod
    def infer--- This code section failed: ---

 L.  96         0  LOAD_GLOBAL              np
                2  LOAD_METHOD              array
                4  LOAD_FAST                'node'
                6  LOAD_METHOD              in_node
                8  LOAD_CONST               2
               10  CALL_METHOD_1         1  '1 positional argument'
               12  LOAD_ATTR                value
               14  CALL_METHOD_1         1  '1 positional argument'
               16  STORE_FAST               'output_shape'

 L.  97        18  LOAD_GLOBAL              np
               20  LOAD_METHOD              array
               22  LOAD_FAST                'node'
               24  LOAD_METHOD              in_node
               26  LOAD_CONST               0
               28  CALL_METHOD_1         1  '1 positional argument'
               30  LOAD_ATTR                shape
               32  CALL_METHOD_1         1  '1 positional argument'
               34  LOAD_CONST               0
               36  BINARY_SUBSCR    
               38  STORE_FAST               'batch'

 L.  98        40  LOAD_FAST                'batch'
               42  LOAD_FAST                'output_shape'
               44  LOAD_CONST               0
               46  STORE_SUBSCR     

 L.  99        48  LOAD_FAST                'node'
               50  LOAD_METHOD              in_node
               52  LOAD_CONST               1
               54  CALL_METHOD_1         1  '1 positional argument'
               56  LOAD_ATTR                shape
               58  STORE_FAST               'kernel_shape'

 L. 100        60  LOAD_FAST                'kernel_shape'
               62  LOAD_FAST                'node'
               64  LOAD_STR                 'kernel_shape'
               66  STORE_SUBSCR     

 L. 101        68  LOAD_FAST                'output_shape'
               70  LOAD_CONST               None
               72  COMPARE_OP               is
               74  POP_JUMP_IF_TRUE    104  'to 104'
               76  LOAD_FAST                'kernel_shape'
               78  LOAD_CONST               None
               80  COMPARE_OP               is
               82  POP_JUMP_IF_TRUE    104  'to 104'
               84  LOAD_FAST                'node'
               86  LOAD_ATTR                spatial_dims
               88  LOAD_CONST               None
               90  COMPARE_OP               is
               92  POP_JUMP_IF_TRUE    104  'to 104'
               94  LOAD_FAST                'node'
               96  LOAD_ATTR                stride
               98  LOAD_CONST               None
              100  COMPARE_OP               is
              102  POP_JUMP_IF_FALSE   108  'to 108'
            104_0  COME_FROM            92  '92'
            104_1  COME_FROM            82  '82'
            104_2  COME_FROM            74  '74'

 L. 102       104  LOAD_CONST               None
              106  RETURN_VALUE     
            108_0  COME_FROM           102  '102'

 L. 104       108  LOAD_FAST                'node'
              110  LOAD_METHOD              has_valid
              112  LOAD_STR                 'kernel_spatial_idx'
              114  CALL_METHOD_1         1  '1 positional argument'
              116  POP_JUMP_IF_TRUE    160  'to 160'

 L. 105       118  LOAD_GLOBAL              np
              120  LOAD_METHOD              delete
              122  LOAD_LISTCOMP            '<code_object <listcomp>>'
              124  LOAD_STR                 'Deconvolution.infer.<locals>.<listcomp>'
              126  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              128  LOAD_GLOBAL              range
              130  LOAD_GLOBAL              len
              132  LOAD_FAST                'kernel_shape'
              134  CALL_FUNCTION_1       1  '1 positional argument'
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  GET_ITER         
              140  CALL_FUNCTION_1       1  '1 positional argument'

 L. 106       142  LOAD_FAST                'node'
              144  LOAD_ATTR                input_feature_channel
              146  LOAD_FAST                'node'
              148  LOAD_ATTR                output_feature_channel
              150  BUILD_TUPLE_2         2 
              152  CALL_METHOD_2         2  '2 positional arguments'
              154  LOAD_FAST                'node'
              156  LOAD_STR                 'kernel_spatial_idx'
              158  STORE_SUBSCR     
            160_0  COME_FROM           116  '116'

 L. 108       160  LOAD_FAST                'node'
              162  LOAD_METHOD              has_valid
              164  LOAD_STR                 'dilation'
              166  CALL_METHOD_1         1  '1 positional argument'
              168  POP_JUMP_IF_TRUE    198  'to 198'

 L. 109       170  LOAD_GLOBAL              np
              172  LOAD_ATTR                full
              174  LOAD_GLOBAL              len
              176  LOAD_FAST                'output_shape'
              178  CALL_FUNCTION_1       1  '1 positional argument'
              180  BUILD_LIST_1          1 
              182  LOAD_CONST               1
              184  LOAD_GLOBAL              np
              186  LOAD_ATTR                int64
              188  LOAD_CONST               ('dtype',)
              190  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              192  LOAD_FAST                'node'
              194  LOAD_STR                 'dilation'
              196  STORE_SUBSCR     
            198_0  COME_FROM           168  '168'

 L. 111       198  LOAD_FAST                'node'
              200  LOAD_ATTR                spatial_dims
              202  STORE_FAST               'spatial_dims'

 L. 112       204  LOAD_GLOBAL              np
              206  LOAD_METHOD              array
              208  LOAD_FAST                'output_shape'
              210  LOAD_FAST                'spatial_dims'
              212  BINARY_SUBSCR    
              214  CALL_METHOD_1         1  '1 positional argument'
              216  STORE_FAST               'output_spatial'

 L. 113       218  LOAD_GLOBAL              np
              220  LOAD_METHOD              array
              222  LOAD_FAST                'node'
              224  LOAD_ATTR                stride
              226  LOAD_FAST                'spatial_dims'
              228  BINARY_SUBSCR    
              230  CALL_METHOD_1         1  '1 positional argument'
              232  STORE_FAST               'stride_spatial'

 L. 114       234  LOAD_GLOBAL              np
              236  LOAD_METHOD              array
              238  LOAD_FAST                'kernel_shape'
              240  LOAD_FAST                'node'
              242  LOAD_ATTR                kernel_spatial_idx
              244  BINARY_SUBSCR    
              246  CALL_METHOD_1         1  '1 positional argument'
              248  LOAD_FAST                'node'
              250  LOAD_STR                 'kernel_spatial'
              252  STORE_SUBSCR     

 L. 115       254  LOAD_GLOBAL              tf_window_op_pad_infer

 L. 116       256  LOAD_FAST                'output_spatial'
              258  LOAD_FAST                'node'
              260  LOAD_ATTR                kernel_spatial
              262  LOAD_FAST                'stride_spatial'
              264  LOAD_FAST                'node'
              266  LOAD_ATTR                auto_pad
              268  CALL_FUNCTION_4       4  '4 positional arguments'
              270  UNPACK_SEQUENCE_2     2 
              272  LOAD_FAST                'node'
              274  STORE_ATTR               pad_spatial_shape
              276  STORE_FAST               'input_spatial_for_check'

 L. 118       278  LOAD_GLOBAL              all
              280  LOAD_FAST                'input_spatial_for_check'
              282  LOAD_FAST                'node'
              284  LOAD_METHOD              in_node
              286  LOAD_CONST               0
              288  CALL_METHOD_1         1  '1 positional argument'
              290  LOAD_ATTR                shape
              292  LOAD_FAST                'spatial_dims'
              294  BINARY_SUBSCR    
              296  COMPARE_OP               ==
              298  CALL_FUNCTION_1       1  '1 positional argument'
          300_302  POP_JUMP_IF_TRUE    308  'to 308'
              304  LOAD_ASSERT              AssertionError
              306  RAISE_VARARGS_1       1  'exception instance'
            308_0  COME_FROM           300  '300'

 L. 120       308  LOAD_GLOBAL              np
              310  LOAD_ATTR                zeros
              312  LOAD_GLOBAL              len
              314  LOAD_FAST                'output_shape'
              316  CALL_FUNCTION_1       1  '1 positional argument'
              318  LOAD_CONST               2
              320  BUILD_TUPLE_2         2 
              322  LOAD_GLOBAL              np
              324  LOAD_ATTR                int64
              326  LOAD_CONST               ('dtype',)
              328  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              330  STORE_FAST               'pad'

 L. 121       332  LOAD_FAST                'node'
              334  LOAD_ATTR                pad_spatial_shape
              336  LOAD_FAST                'pad'
              338  LOAD_FAST                'spatial_dims'
              340  STORE_SUBSCR     

 L. 122       342  LOAD_FAST                'pad'
              344  LOAD_FAST                'node'
              346  STORE_ATTR               pad

 L. 124       348  LOAD_FAST                'output_shape'
              350  LOAD_FAST                'node'
              352  LOAD_ATTR                channel_dims
              354  BINARY_SUBSCR    
              356  LOAD_CONST               0
              358  BINARY_SUBSCR    
              360  LOAD_FAST                'node'
              362  STORE_ATTR               output

 L. 125       364  LOAD_FAST                'output_shape'
              366  LOAD_FAST                'node'
              368  STORE_ATTR               output_shape

 L. 126       370  LOAD_FAST                'output_shape'
              372  LOAD_FAST                'node'
              374  LOAD_METHOD              out_node
              376  CALL_METHOD_0         0  '0 positional arguments'
              378  STORE_ATTR               shape

 L. 128       380  LOAD_GLOBAL              mark_input_bins
              382  LOAD_FAST                'node'
              384  LOAD_STR                 'weights'
              386  BUILD_LIST_1          1 
              388  LOAD_CONST               1
              390  CALL_FUNCTION_3       3  '3 positional arguments'
              392  POP_TOP          

 L. 129       394  LOAD_GLOBAL              assign_dims_to_weights
              396  LOAD_FAST                'node'
              398  LOAD_METHOD              in_node
              400  LOAD_CONST               1
              402  CALL_METHOD_1         1  '1 positional argument'
              404  LOAD_FAST                'node'
              406  LOAD_ATTR                kernel_spatial_idx
              408  LOAD_FAST                'node'
              410  LOAD_ATTR                input_feature_channel

 L. 130       412  LOAD_FAST                'node'
              414  LOAD_ATTR                output_feature_channel
              416  LOAD_GLOBAL              len
              418  LOAD_FAST                'kernel_shape'
              420  CALL_FUNCTION_1       1  '1 positional argument'
              422  CALL_FUNCTION_5       5  '5 positional arguments'
              424  POP_TOP          

 L. 133       426  LOAD_STR                 'Deconvolution'
              428  LOAD_FAST                'node'
              430  STORE_ATTR               type

 L. 134       432  LOAD_STR                 'Deconv2D'
              434  LOAD_FAST                'node'
              436  STORE_ATTR               op

 L. 137       438  LOAD_GLOBAL              PermuteAttrs
              440  LOAD_ATTR                create_permute_attrs
              442  LOAD_FAST                'node'
              444  LOAD_CONST               ('pad', 'input:0')

 L. 138       446  LOAD_CONST               ('stride', 'input:0')

 L. 139       448  LOAD_CONST               ('output_shape', 'input:0')

 L. 140       450  LOAD_CONST               ('batch_dims', 'input:0')

 L. 141       452  LOAD_CONST               ('channel_dims', 'input:0')

 L. 142       454  LOAD_CONST               ('spatial_dims', 'input:0')

 L. 144       456  LOAD_CONST               ('kernel_shape', 'input:1')

 L. 145       458  LOAD_CONST               ('kernel_spatial_idx', 'input:1')

 L. 146       460  LOAD_CONST               ('input_feature_channel', 'input:1')

 L. 147       462  LOAD_CONST               ('output_feature_channel', 'input:1')
              464  BUILD_LIST_10        10 
              466  LOAD_CONST               ('attrs',)
              468  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              470  POP_TOP          

 L. 150       472  LOAD_GLOBAL              PermuteAttrs
              474  LOAD_METHOD              set_permutation
              476  LOAD_FAST                'node'
              478  LOAD_METHOD              in_node
              480  LOAD_CONST               1
              482  CALL_METHOD_1         1  '1 positional argument'
              484  LOAD_FAST                'node'

 L. 151       486  LOAD_FAST                'node'
              488  LOAD_METHOD              has_valid
              490  LOAD_STR                 'get_weights_permute'
              492  CALL_METHOD_1         1  '1 positional argument'
          494_496  POP_JUMP_IF_FALSE   504  'to 504'
              498  LOAD_FAST                'node'
              500  LOAD_ATTR                get_weights_permute
              502  JUMP_FORWARD        506  'to 506'
            504_0  COME_FROM           494  '494'
              504  LOAD_CONST               None
            506_0  COME_FROM           502  '502'
              506  CALL_METHOD_3         3  '3 positional arguments'
              508  POP_TOP          

 L. 152       510  LOAD_GLOBAL              PermuteInputs
              512  CALL_FUNCTION_0       0  '0 positional arguments'
              514  LOAD_METHOD              set_input_permutation
              516  LOAD_FAST                'node'
              518  LOAD_METHOD              in_node
              520  LOAD_CONST               2
              522  CALL_METHOD_1         1  '1 positional argument'
              524  LOAD_FAST                'node'
              526  LOAD_STR                 'input:0'
              528  LOAD_STR                 'shape'
              530  CALL_METHOD_4         4  '4 positional arguments'
              532  POP_TOP          

 L. 154       534  LOAD_FAST                'node'
              536  LOAD_ATTR                graph
              538  LOAD_ATTR                graph
              540  LOAD_STR                 'cmd_params'
              542  BINARY_SUBSCR    
              544  LOAD_ATTR                generate_experimental_IR_V10
          546_548  POP_JUMP_IF_TRUE    584  'to 584'

 L. 155       550  LOAD_FAST                'node'
              552  LOAD_ATTR                graph
              554  LOAD_METHOD              remove_edge
              556  LOAD_FAST                'node'
              558  LOAD_METHOD              in_node
              560  LOAD_CONST               2
              562  CALL_METHOD_1         1  '1 positional argument'
              564  LOAD_ATTR                id
              566  LOAD_FAST                'node'
              568  LOAD_ATTR                id
              570  CALL_METHOD_2         2  '2 positional arguments'
              572  POP_TOP          

 L. 156       574  LOAD_CONST               False
              576  LOAD_FAST                'node'
              578  LOAD_STR                 'shape_input'
              580  STORE_SUBSCR     
              582  JUMP_FORWARD        596  'to 596'
            584_0  COME_FROM           546  '546'

 L. 158       584  LOAD_CONST               2
              586  LOAD_STR                 'int64'
              588  BUILD_MAP_1           1 
              590  LOAD_FAST                'node'
              592  LOAD_STR                 'force_precision_in_ports'
              594  STORE_SUBSCR     
            596_0  COME_FROM           582  '582'

Parse error at or near `STORE_SUBSCR' instruction at offset 594
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/middle/passes/fusing/resnet_optimization.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 7271 bytes
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
from mo.graph.graph import Node, Graph
from mo.middle.passes.fusing.helpers import get_next_operation
from mo.ops.pooling import Pooling

def _clean_fw_tensor_attrs(node: Node):
    attrs = ['fw_tensor_debug_info']
    for attr in attrs:
        if node.has_valid(attr):
            node[attr] = None


def _insert_pooling(graph: Graph, first_node: Node, second_node: Node, spatial_dims):
    """
    This function inserts point wise pooling layer between two nodes
    """
    log.debug('STRIDE PROP: Insert pooling between {} and {}'.format(first_node.name, second_node.name))
    stride_prop = second_node.stride_prop
    assert len(graph.get_edge_data(first_node.id, second_node.id)) == 1
    eattrs = graph.get_edge_data(first_node.id, second_node.id)[0]
    graph.remove_edge(first_node.id, second_node.id)
    pooling = Pooling(graph, dict(name='Pooling_', spatial_dims=spatial_dims, window=(np.array([1, 1, 1, 1])), output_spatial_shape=None,
      stride=(np.array(stride_prop)),
      pad_spatial_shape=(np.array([[0, 0], [0, 0]])),
      pad=(np.array([[0, 0], [0, 0], [0, 0], [0, 0]])),
      pool_method='max',
      is_partial_inferred=False))
    pooling_data = pooling.create_node_with_data([first_node])
    _clean_fw_tensor_attrs(pooling_data)
    graph.add_edges_from([(pooling_data.id, second_node.id, eattrs)])


def _check_next_ops(next_ops: list):
    """
    This function checks list of operation to determine that all ops has same (not 1,1,1,1) stride_prop attr
    """
    stride_props = []
    for op in next_ops:
        if op.has_valid('stride_prop'):
            stride_props.append(np.array(op.stride_prop))
        continue

    status = not (len(next_ops) != len(stride_props) or len(stride_props) > 0 and not all((np.array_equal(x, stride_props[0]) and not np.array_equal(x, [1, 1, 1, 1]) for x in stride_props)))
    return (stride_props, status)


def _simple_stride_prop(graph: Graph, node: Node, spatial_dims, supported=True):
    """
    This function handles stride propagation for op nodes. If node is in supported ops dict so this is supported operation and we
    can propagate stride directly via this op (stride_prop will be set by using bottom stride_prop), otherwise we can't and
    stride_prop attr will be set as 1,1,1,1
    """
    next_ops = get_next_operation(node)
    stride_props, all_ops_are_valid = _check_next_ops(next_ops)
    if not (supported and all_ops_are_valid):
        for op in next_ops:
            if op.has_valid('stride_prop') and not np.array_equal(op.stride_prop[spatial_dims], np.array([1, 1])):
                if op.has_valid('has_stride') == False or op.soft_get('has_stride') == False:
                    _insert_pooling(graph, node.out_node(), op, spatial_dims)

        node['stride_prop'] = np.array([1, 1, 1, 1])
        return
    for op in next_ops:
        if op.soft_get('has_stride') == True:
            op.stride = np.array([1, 1, 1, 1])
            log.debug('STRIDE PROP: {} {} strides was moved upper via {}'.format(op.type, op.name, node.name))

    node['stride_prop'] = np.array(stride_props[0]) if len(stride_props) > 0 else np.array([1, 1, 1, 1])
    node['is_partial_inferred'] = False
    _clean_fw_tensor_attrs(node.out_node())


def _conv_stride_prop--- This code section failed: ---

 L. 105         0  LOAD_GLOBAL              get_next_operation
                2  LOAD_FAST                'node'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               'next_ops'

 L. 106         8  LOAD_GLOBAL              _check_next_ops
               10  LOAD_FAST                'next_ops'
               12  CALL_FUNCTION_1       1  '1 positional argument'
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'stride_props'
               18  STORE_FAST               'all_ops_are_valid'

 L. 108        20  LOAD_GLOBAL              Node
               22  LOAD_CONST               ('node',)
               24  BUILD_CONST_KEY_MAP_1     1 
               26  LOAD_CODE                <code_object _check_convolution>
               28  LOAD_STR                 '_conv_stride_prop.<locals>._check_convolution'
               30  MAKE_FUNCTION_4          'annotation'
               32  STORE_FAST               '_check_convolution'

 L. 112        34  LOAD_FAST                'all_ops_are_valid'
               36  POP_JUMP_IF_TRUE    110  'to 110'

 L. 114        38  SETUP_LOOP          238  'to 238'
               40  LOAD_FAST                'next_ops'
               42  GET_ITER         
             44_0  COME_FROM            84  '84'
             44_1  COME_FROM            56  '56'
               44  FOR_ITER            106  'to 106'
               46  STORE_FAST               'op'

 L. 115        48  LOAD_FAST                'op'
               50  LOAD_METHOD              has_valid
               52  LOAD_STR                 'stride_prop'
               54  CALL_METHOD_1         1  '1 positional argument'
               56  POP_JUMP_IF_FALSE    44  'to 44'
               58  LOAD_GLOBAL              np
               60  LOAD_METHOD              array_equal
               62  LOAD_FAST                'op'
               64  LOAD_ATTR                stride_prop
               66  LOAD_FAST                'spatial_dims'
               68  BINARY_SUBSCR    
               70  LOAD_GLOBAL              np
               72  LOAD_METHOD              array
               74  LOAD_CONST               1
               76  LOAD_CONST               1
               78  BUILD_LIST_2          2 
               80  CALL_METHOD_1         1  '1 positional argument'
               82  CALL_METHOD_2         2  '2 positional arguments'
               84  POP_JUMP_IF_TRUE     44  'to 44'

 L. 117        86  LOAD_GLOBAL              _insert_pooling
               88  LOAD_FAST                'graph'
               90  LOAD_FAST                'node'
               92  LOAD_METHOD              out_node
               94  CALL_METHOD_0         0  '0 positional arguments'
               96  LOAD_FAST                'op'
               98  LOAD_FAST                'spatial_dims'
              100  CALL_FUNCTION_4       4  '4 positional arguments'
              102  POP_TOP          
              104  JUMP_BACK            44  'to 44'
              106  POP_BLOCK        
              108  JUMP_FORWARD        238  'to 238'
            110_0  COME_FROM            36  '36'

 L. 118       110  LOAD_GLOBAL              len
              112  LOAD_FAST                'stride_props'
              114  CALL_FUNCTION_1       1  '1 positional argument'
              116  LOAD_CONST               0
              118  COMPARE_OP               >
              120  POP_JUMP_IF_FALSE   238  'to 238'

 L. 119       122  LOAD_FAST                'node'
              124  DUP_TOP          
              126  LOAD_ATTR                stride
              128  LOAD_FAST                'stride_props'
              130  LOAD_CONST               0
              132  BINARY_SUBSCR    
              134  INPLACE_MULTIPLY 
              136  ROT_TWO          
              138  STORE_ATTR               stride

 L. 120       140  LOAD_GLOBAL              log
              142  LOAD_METHOD              debug
              144  LOAD_STR                 'STRIDE PROP: {} got new strides {}'
              146  LOAD_METHOD              format
              148  LOAD_FAST                'node'
              150  LOAD_ATTR                name
              152  LOAD_FAST                'node'
              154  LOAD_ATTR                stride
              156  CALL_METHOD_2         2  '2 positional arguments'
              158  CALL_METHOD_1         1  '1 positional argument'
              160  POP_TOP          

 L. 121       162  SETUP_LOOP          210  'to 210'
              164  LOAD_FAST                'next_ops'
              166  GET_ITER         
            168_0  COME_FROM           184  '184'
              168  FOR_ITER            208  'to 208'
              170  STORE_FAST               'op'

 L. 122       172  LOAD_FAST                'op'
              174  LOAD_METHOD              soft_get
              176  LOAD_STR                 'has_stride'
              178  CALL_METHOD_1         1  '1 positional argument'
              180  LOAD_CONST               True
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_FALSE   168  'to 168'

 L. 123       186  LOAD_GLOBAL              np
              188  LOAD_METHOD              array
              190  LOAD_CONST               1
              192  LOAD_CONST               1
              194  LOAD_CONST               1
              196  LOAD_CONST               1
              198  BUILD_LIST_4          4 
              200  CALL_METHOD_1         1  '1 positional argument'
              202  LOAD_FAST                'op'
              204  STORE_ATTR               stride
              206  JUMP_BACK           168  'to 168'
              208  POP_BLOCK        
            210_0  COME_FROM_LOOP      162  '162'

 L. 124       210  LOAD_CONST               False
              212  LOAD_FAST                'node'
              214  LOAD_STR                 'is_partial_inferred'
              216  STORE_SUBSCR     

 L. 125       218  LOAD_CONST               False
              220  LOAD_FAST                'node'
              222  LOAD_STR                 'output_spatial_shape'
              224  STORE_SUBSCR     

 L. 126       226  LOAD_GLOBAL              _clean_fw_tensor_attrs
              228  LOAD_FAST                'node'
              230  LOAD_METHOD              out_node
              232  CALL_METHOD_0         0  '0 positional arguments'
              234  CALL_FUNCTION_1       1  '1 positional argument'
              236  POP_TOP          
            238_0  COME_FROM           120  '120'
            238_1  COME_FROM           108  '108'
            238_2  COME_FROM_LOOP       38  '38'

 L. 129       238  LOAD_FAST                '_check_convolution'
              240  LOAD_FAST                'node'
              242  CALL_FUNCTION_1       1  '1 positional argument'
          244_246  POP_JUMP_IF_FALSE   260  'to 260'
              248  LOAD_GLOBAL              np
              250  LOAD_METHOD              array
              252  LOAD_FAST                'node'
              254  LOAD_ATTR                stride
              256  CALL_METHOD_1         1  '1 positional argument'
              258  JUMP_FORWARD        276  'to 276'
            260_0  COME_FROM           244  '244'
              260  LOAD_GLOBAL              np
              262  LOAD_METHOD              array
              264  LOAD_CONST               1
              266  LOAD_CONST               1
              268  LOAD_CONST               1
              270  LOAD_CONST               1
              272  BUILD_LIST_4          4 
              274  CALL_METHOD_1         1  '1 positional argument'
            276_0  COME_FROM           258  '258'
              276  LOAD_FAST                'node'
              278  LOAD_STR                 'stride_prop'
              280  STORE_SUBSCR     

Parse error at or near `COME_FROM_LOOP' instruction at offset 238_2


supported_ops = {'ReLU':{'stride_prop':_simple_stride_prop, 
  'attrs':{}}, 
 'Maximum':{'stride_prop':_simple_stride_prop, 
  'attrs':{}}, 
 'Mul':{'stride_prop':_simple_stride_prop, 
  'attrs':{}}, 
 'Add':{'stride_prop':_simple_stride_prop, 
  'attrs':{}}, 
 'Convolution':{'stride_prop':_conv_stride_prop, 
  'attrs':{'has_stride': True}}}

def _stride_propagation(graph: Graph, spatial_dims):
    """
    This function do stride propagation for all op nodes
    """
    nodes = [node for node in graph.pseudo_topological_sort(reverse=True) if node.kind == 'op' if node.soft_get('type') != 'Const']
    for node in nodes:
        if node.soft_get('type') in supported_ops:
            op = supported_ops[node.type]
            for key in op['attrs'].keys():
                node[key] = op['attrs'][key]

            op['stride_prop'](graph, node, spatial_dims, True)
        else:
            _simple_stride_prop(graph, node, spatial_dims, False)


def stride_optimization(graph: Graph):
    """
    This is main function for stride optimization pass
    """
    layout = graph.graph['layout']
    if layout == 'NCHW':
        spatial_dims = np.array([2, 3])
    else:
        if layout == 'NHWC':
            spatial_dims = np.array([1, 2])
        else:
            log.warning('STRIDE PROP: layout {} is not supported'.format(layout))
            return
    _stride_propagation(graph, spatial_dims)
    nodes = [node for node in graph.pseudo_topological_sort() if node.soft_get('is_partial_inferred') == False]
    for node in nodes:
        node.infer(node)
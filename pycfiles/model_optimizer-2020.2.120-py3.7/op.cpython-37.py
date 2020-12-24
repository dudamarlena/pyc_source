# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/ops/op.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 19722 bytes
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
import copy, logging as log
from collections import namedtuple
import networkx as nx, numpy as np
from mo.front.extractor import add_attrs_props
from mo.front.extractor import update_ie_fields
from mo.graph.graph import Node, Graph
from mo.utils import class_registration
from mo.utils.error import Error

class Op(object):
    registered_ops = {}
    registered_cls = []
    excluded_classes = []

    def __init__(self, graph: Graph, attrs1: dict=None, attrs2: dict=None):
        self.graph = graph
        try:
            self.ir_version = graph.graph['ir_version']
        except:
            self.ir_version = None

        self.attrs = {'kind': 'op'}
        self.default_backend_attrs = []
        if attrs1 is not None:
            self.attrs.update(attrs1)
        if attrs2 is not None:
            self.attrs.update(attrs2)

    def add_node(self, attrs: dict=None):
        new_attrs = {}
        new_attrs.update(self.attrs)
        if attrs is not None:
            new_attrs.update(attrs)
        id_prefix = new_attrs['name'] if 'name' in new_attrs else ''
        id = self.graph.unique_id(id_prefix)
        new_attrs['name'] = id
        new_attrs = add_attrs_props(new_attrs)
        update_ie_fields(new_attrs, self.ir_version)
        self.substitute_ie_attrs(new_attrs)
        (self.graph.add_node)(id, **new_attrs)
        node = Node(self.graph, id)
        return node

    def substitute_ie_attrs(self, new_attrs: dict):
        """
        Replace standard list of attribute in layer/data by attributes
        delivered by backend_attrs
        """
        backend_attrs_mapping = {None:self.backend_attrs, 
         10:self.backend_attrs, 
         7:self.backend_attrs, 
         6:self.backend_attrs, 
         5:self.backend_attrs, 
         4:self.backend_attrs, 
         3:self.backend_attrs, 
         2:self.backend_attrs_v2}
        if self.ir_version not in backend_attrs_mapping.keys():
            raise Error('Unrecognized IR version was specified: {}'.format(self.ir_version))
        new_attrs.update({'IE': [
                (
                 'layer',
                 [
                  (
                   'id', lambda node: node.node), 'name', 'type', 'version'],
                 [
                  (
                   'data', backend_attrs_mapping[self.ir_version]() + self.default_backend_attrs, []),
                  '@ports',
                  '@consts'])]})

    @staticmethod
    def extract_port(node_port):
        if isinstance(node_port, tuple):
            node = node_port[0]
            port = node_port[1]
        else:
            node = node_port
            port = 0
        out_ids = [attr['out'] for _, __, attr in node.graph.out_edges((node.id), data=True) if 'out' in attr]
        if len(set(out_ids)) > 1:
            if not isinstance(node_port, tuple):
                raise Error('Node {} has more than one outputs. Provide output port explicitly. '.format(node.name))
        return (
         node, port)

    def create_node_on_port(self, node: Node, out_port: int, attrs: dict=None, edge_attrs: dict=None):
        """
        Removes an edge, that is connected to nodes out_port. Creates new_node with attrs attributes and
        connects it to node by edge that stores the same information as cutted edge.
        :param node: Input node, to cut the edge from
        :param out_port: output port of edge to cut
        :param attrs: attributes of new node
        :param edge_attrs: attributes to be changed/added to new edge
        :return: Node instance of created new_node
        """
        if edge_attrs is None:
            edge_attrs = {'in': 0}
        prev_edge_attrs = copy.deepcopy(node.out_edge(out_port))
        prev_edge_attrs.update(edge_attrs)
        new_edge_attrs = prev_edge_attrs
        if attrs is None:
            attrs = dict()
        new_node = self.add_node(attrs)
        (self.graph.add_edge)((node.id), (new_node.id), **new_edge_attrs)
        return new_node

    def create_node--- This code section failed: ---

 L. 136         0  LOAD_FAST                'inputs'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    24  'to 24'

 L. 137         8  LOAD_LISTCOMP            '<code_object <listcomp>>'
               10  LOAD_STR                 'Op.create_node.<locals>.<listcomp>'
               12  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               14  LOAD_FAST                'inputs'
               16  GET_ITER         
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  STORE_FAST               'inputs'
               22  JUMP_FORWARD         28  'to 28'
             24_0  COME_FROM             6  '6'

 L. 139        24  BUILD_LIST_0          0 
               26  STORE_FAST               'inputs'
             28_0  COME_FROM            22  '22'

 L. 140        28  LOAD_FAST                'attrs'
               30  LOAD_CONST               None
               32  COMPARE_OP               is
               34  POP_JUMP_IF_FALSE    42  'to 42'

 L. 141        36  LOAD_GLOBAL              dict
               38  CALL_FUNCTION_0       0  '0 positional arguments'
               40  STORE_FAST               'attrs'
             42_0  COME_FROM            34  '34'

 L. 142        42  LOAD_FAST                'self'
               44  LOAD_METHOD              add_node
               46  LOAD_FAST                'attrs'
               48  CALL_METHOD_1         1  '1 positional argument'
               50  STORE_FAST               'new_node'

 L. 144        52  SETUP_LOOP          224  'to 224'
               54  LOAD_GLOBAL              enumerate
               56  LOAD_FAST                'inputs'
               58  CALL_FUNCTION_1       1  '1 positional argument'
               60  GET_ITER         
               62  FOR_ITER            222  'to 222'
               64  UNPACK_SEQUENCE_2     2 
               66  STORE_FAST               'i'
               68  STORE_FAST               'inp'

 L. 148        70  LOAD_FAST                'inp'
               72  LOAD_CONST               0
               74  BINARY_SUBSCR    
               76  LOAD_METHOD              has_valid
               78  LOAD_STR                 'kind'
               80  CALL_METHOD_1         1  '1 positional argument'
               82  POP_JUMP_IF_FALSE    98  'to 98'
               84  LOAD_FAST                'inp'
               86  LOAD_CONST               0
               88  BINARY_SUBSCR    
               90  LOAD_ATTR                kind
               92  LOAD_STR                 'op'
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   126  'to 126'
             98_0  COME_FROM            82  '82'
               98  LOAD_FAST                'i'
              100  LOAD_FAST                'inp'
              102  LOAD_CONST               1
              104  BINARY_SUBSCR    
              106  LOAD_STR                 'in'
              108  LOAD_STR                 'permutation'
              110  BUILD_LIST_2          2 
              112  LOAD_STR                 'out'
              114  LOAD_STR                 'permutation'
              116  BUILD_LIST_2          2 
              118  BUILD_LIST_0          0 
              120  LOAD_CONST               ('in', 'out', 'in_attrs', 'out_attrs', 'data_attrs')
              122  BUILD_CONST_KEY_MAP_5     5 
              124  JUMP_FORWARD        138  'to 138'
            126_0  COME_FROM            96  '96'

 L. 149       126  LOAD_FAST                'i'
              128  LOAD_STR                 'in'
              130  LOAD_STR                 'permutation'
              132  BUILD_LIST_2          2 
              134  LOAD_CONST               ('in', 'in_attrs')
              136  BUILD_CONST_KEY_MAP_2     2 
            138_0  COME_FROM           124  '124'
              138  STORE_FAST               'edge_attr'

 L. 150       140  LOAD_FAST                'edge_attrs'
              142  LOAD_CONST               None
              144  COMPARE_OP               is-not
              146  POP_JUMP_IF_FALSE   158  'to 158'

 L. 151       148  LOAD_FAST                'edge_attr'
              150  LOAD_METHOD              update
              152  LOAD_FAST                'edge_attrs'
              154  CALL_METHOD_1         1  '1 positional argument'
              156  POP_TOP          
            158_0  COME_FROM           146  '146'

 L. 152       158  LOAD_FAST                'new_node'
              160  LOAD_ATTR                add_input_port
              162  LOAD_FAST                'i'
              164  LOAD_CONST               True
              166  LOAD_CONST               ('skip_if_exist',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          

 L. 153       172  LOAD_FAST                'inp'
              174  LOAD_CONST               0
              176  BINARY_SUBSCR    
              178  LOAD_ATTR                add_output_port
              180  LOAD_FAST                'inp'
              182  LOAD_CONST               1
              184  BINARY_SUBSCR    
              186  LOAD_CONST               True
              188  LOAD_CONST               ('skip_if_exist',)
              190  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              192  POP_TOP          

 L. 154       194  LOAD_FAST                'self'
              196  LOAD_ATTR                graph
              198  LOAD_ATTR                add_edge
              200  LOAD_FAST                'inp'
              202  LOAD_CONST               0
              204  BINARY_SUBSCR    
              206  LOAD_ATTR                id
              208  LOAD_FAST                'new_node'
              210  LOAD_ATTR                id
              212  BUILD_TUPLE_2         2 
              214  LOAD_FAST                'edge_attr'
              216  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              218  POP_TOP          
              220  JUMP_BACK            62  'to 62'
              222  POP_BLOCK        
            224_0  COME_FROM_LOOP       52  '52'

 L. 155       224  LOAD_FAST                'new_node'
              226  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 126_0

    def create_node_with_data(self, inputs: list=None, attrs: dict=None, data_nodes: [Node, np.ndarray, list]=None, edge_attrs: list=None):
        """
        Creates a new node with given inputs and attrs and also creates data node that
        holds the op output value. Inputs should be data nodes (not op nodes).
        Work for ops with a single output port only.
        Edge attributes in edge_attrs go in order of items in 'inputs'
        """
        if inputs is None:
            inputs = []
        else:
            if attrs is None:
                attrs = {}
            new_op_node = self.add_node(attrs)
            inputs_with_edge_attrs = []
            for i, inp in enumerate(inputs):
                if inp is None:
                    continue
                edge_attr = {'in': i}
                if edge_attrs is not None:
                    if i < len(edge_attrs):
                        edge_attr.update(edge_attrs[i])
                inputs_with_edge_attrs.append((inp.id, new_op_node.id, edge_attr))
                new_op_node.add_input_port(i, skip_if_exist=True)

            self.graph.add_edges_from(inputs_with_edge_attrs)
            old_data_value = [
             None]
            old_data_shape = [None]
            if data_nodes is None:
                data_node = self.graph.unique_id()
                (self.graph.add_node)(data_node, **add_attrs_props(dict(kind='data', name=data_node, value=None, shape=None, data_type=None, infer=None)))
                data_nodes = [Node(self.graph, data_node)]
            else:
                if type(data_nodes) not in [list, np.ndarray]:
                    data_nodes = [
                     data_nodes]
            old_data_value = [data_node.value.copy() if data_node.has_valid('value') else None for data_node in data_nodes]
            old_data_shape = [data_node.shape.copy() if data_node.has_valid('shape') else None for data_node in data_nodes]
        for id, data_node in enumerate(data_nodes):
            self.graph.add_edges_from([(new_op_node.id, data_node.id, {'out': id})])

        if new_op_node.has_valid('infer'):
            if log.getLogger().isEnabledFor(log.DEBUG):
                log.debug('Start running infer function for individual op node with attributes: {}'.format(str(new_op_node)))
            else:
                new_op_node.infer(new_op_node)
                if new_op_node.has('nchw_layout'):
                    for out_node in new_op_node.out_nodes().values():
                        out_node['nchw_layout'] = new_op_node.nchw_layout

                if not all((old_value is None for old_value in old_data_value)):
                    assert all([np.array_equal(old_data_value[id], data_node.value) for id, data_node in enumerate(data_nodes)])
                if not all((old_shape is None for old_shape in old_data_shape)):
                    if not all([np.array_equal(old_data_shape[id], data_node.shape) for id, data_node in enumerate(data_nodes)]):
                        raise AssertionError('After re-inference of {} node, old and new shapes do not match. Old shapes: {}, new shapes: {}.'.format(new_op_node.soft_get('name'), [old_data_shape[id] for id in range(len(data_nodes))], [data_node.shape for data_node in data_nodes]))
            for data_node in data_nodes:
                if log.getLogger().isEnabledFor(log.DEBUG):
                    log.debug('Finished running infer function, data nodes attributes: {}'.format(data_node))

        if len(data_nodes) == 1:
            return data_nodes[0]
        return data_nodes

    @staticmethod
    def create_data_node(graph: Graph, op_node: Node, attrs: dict=None, edge_attrs: dict=None, out_port=0):
        if op_node is not None:
            raise op_node.kind == 'op' or AssertionError
        else:
            assert out_port not in op_node.out_nodes()
            if attrs is None:
                attrs = {}
            data_node = graph.unique_id(op_node.id)
            default_attrs = dict(kind='data', name=data_node, value=None, shape=None, data_type=None, infer=None)
            default_attrs.update(attrs)
            (graph.add_node)(data_node, **add_attrs_props(default_attrs))
            data_node = Node(graph, data_node)
            if edge_attrs is not None:
                graph.add_edges_from([(op_node.id, data_node.id, {**{'out': out_port}, **edge_attrs})])
            else:
                graph.add_edges_from([(op_node.id, data_node.id, {'out': out_port})])
        return data_node

    @staticmethod
    def _create_data_node(graph: Graph, name: str, attrs: dict=None):
        if attrs is None:
            attrs = {}
        data_node = graph.unique_id(name)
        default_attrs = dict(kind='data', name=data_node, value=None, shape=None, data_type=None, infer=None)
        default_attrs.update(attrs)
        (graph.add_node)(data_node, **add_attrs_props(default_attrs))
        data_node = Node(graph, data_node)
        return data_node

    @staticmethod
    def create_input_data_node(graph: Graph, name: str, value: np.array, attrs: dict=None):
        if attrs is None:
            attrs = {}
        data_node = graph.unique_id(name)
        default_attrs = dict(kind='data', name=data_node, value=(np.array(value)), shape=(np.array(value.shape)), data_type=None,
          infer=None)
        default_attrs.update(attrs)
        (graph.add_node)(data_node, **add_attrs_props(default_attrs))
        return Node(graph, data_node)

    @staticmethod
    def create_and_connect_input_data_node(graph: Graph, op_node: Node, attrs: dict=None, edge_attrs: dict=None):
        if not (op_node is not None and op_node.kind == 'op'):
            raise AssertionError
        if attrs is None:
            attrs = {}
        if edge_attrs is None:
            edge_attrs = {}
        data_node = graph.unique_id(op_node.id)
        default_attrs = dict(kind='data', name=data_node, value=None, shape=None, data_type=None, infer=None)
        default_attrs.update(attrs)
        (graph.add_node)(data_node, **add_attrs_props(default_attrs))
        data_node = Node(graph, data_node)
        op_node.add_input_port((edge_attrs['in']), skip_if_exist=True)
        graph.add_edges_from([(data_node.id, op_node.id, edge_attrs)])
        return data_node

    def update_node(self, node: Node, attrs: dict=None):
        """
        Updates/creates new attributes in node based on self.attrs and attrs.
        """
        new_attrs = {}
        new_attrs.update(self.attrs)
        if attrs:
            new_attrs.update(attrs)
        new_attrs = add_attrs_props(new_attrs)
        update_ie_fields(new_attrs, self.ir_version)
        self.substitute_ie_attrs(new_attrs)
        for k, v in new_attrs.items():
            node[k] = v

        node.update_node()

    @classmethod
    def update_node_stat(cls, node: Node, attrs: dict=None):
        if attrs is None:
            attrs = dict()
        op = cls(node.graph, attrs)
        op.update_node(node)

    def supported_attrs(self):
        """
        Attributes that user should/can set for the operation
        """
        return []

    def backend_attrs(self):
        """
        Attributes that will be translated to back-end IR
        """
        return self.supported_attrs()

    def backend_attrs_v2(self):
        return self.backend_attrs()

    @staticmethod
    def get_op_class_by_name(name):
        return __class__.registered_ops[name]

    @classmethod
    def class_type(cls):
        return class_registration.ClassType.OP

    @staticmethod
    def expand_node_shape(node: Node, dims_to_add):
        return node is None or node.has_valid('value') or None
        for idx in range(dims_to_add):
            node.value = np.expand_dims((node.value), axis=(-1))

        node.shape = np.array(node.value.shape)


class PermuteAttrs:
    Permutation = namedtuple('Permutation', ['perm', 'inv'])
    Attr = namedtuple('Attr', ['name', 'port', 'func'])
    common_permutation = lambda node, permutation, attr: node[attr][permutation.perm]
    common_permutation_inv = lambda node, permutation, attr: permutation.inv[node[attr]]
    common_attrs_permutation = {'dim':common_permutation, 
     'pad':common_permutation, 
     'pads':common_permutation, 
     'shape':common_permutation, 
     'order':lambda node, permutation, attr: permutation.inv[node[attr][permutation.perm]], 
     'stride':common_permutation, 
     'window':common_permutation, 
     'dilation':common_permutation, 
     'kernel_shape':common_permutation, 
     'output_shape':common_permutation, 
     'slices':common_permutation, 
     'shrink_axis_mask':common_permutation, 
     'new_axis_mask':common_permutation, 
     'axes':common_permutation_inv, 
     'axis':common_permutation_inv, 
     'batch_dims':common_permutation_inv, 
     'channel_dims':common_permutation_inv, 
     'spatial_dims':common_permutation_inv, 
     'input_channel_dim':common_permutation_inv, 
     'output_channel_dim':common_permutation_inv, 
     'kernel_spatial_idx':common_permutation_inv, 
     'input_feature_channel':common_permutation_inv, 
     'output_feature_channel':common_permutation_inv}

    @staticmethod
    def __attr(name, port, func=None):
        if func is None:
            if name in PermuteAttrs.common_attrs_permutation:
                func = PermuteAttrs.common_attrs_permutation[name]
            else:
                raise Error('Attr {} is missing in PermuteAttrs.common_attrs_permutation. Please update common_attrs_permutation with permutation for your attribute!'.format(name))
        if len(port.split(':')) != 2 or port.split(':')[0] not in ('input', 'output'):
            raise Error("Attribute port {} for {} wasn't set correctly!".format(port, name))
        return PermuteAttrs.Attr(name=name, port=port, func=func)

    def __init__(self):
        self.attrs = {}

    def update_attrs(self, attrs):
        for attr in attrs:
            if not isinstance(attr, tuple) or len(attr) not in (2, 3):
                raise Error('attr object must be a tuple: (attribute_name, port) or (attribute_name, port, func)')
            self.attrs.update({attr[0]: (self._PermuteAttrs__attr)(*attr)})

        return self

    def permute_attrs(self, node):
        for attr in self.attrs.keys():
            name, port, func = self.attrs[attr]
            node_type, port = port.split(':')
            port = int(port)
            node_with_permutation = node.in_node(port) if node_type == 'input' else node.out_node(port)
            if node_with_permutation.has_valid('permutation'):
                permutation = node_with_permutation.permutation
                if isinstance(permutation, type(lambda : 0)):
                    node[name] = func(node, permutation(node), name)
                else:
                    node[name] = func(node, permutation, name)

    @staticmethod
    def create_permute_attrs(node, attrs=None):
        if not node.has_valid('permute_attrs'):
            node['permute_attrs'] = PermuteAttrs()
        node['permute_attrs'].update_attrs(attrs)

    @staticmethod
    def set_permutation(node1, node2, permutation, override=False):
        edge_attrs = node1.graph.get_edge_data(node1.id, node2.id)[0]
        if 'permutation' not in edge_attrs or override:
            nx.set_edge_attributes(G=(node1.graph), values={(
 node1.id, node2.id, 0): permutation},
              name='permutation')
        else:
            raise edge_attrs['permutation'] is None and permutation is not None or np.array_equal(edge_attrs['permutation'], permutation) or Error('Permutation already exists in edge between {} and {}'.format(node1.id, node2.id))

    @staticmethod
    def get_inverse_permutation(perm):
        inv = [0] * len(perm)
        for index, pos in enumerate(perm):
            inv[pos] = index

        return inv

    @staticmethod
    def get_nhwc_to_nchw_permutation(dims_number: int):
        if dims_number != 3:
            perm = [0, dims_number - 1,
             *[x for x in range(1, dims_number - 1)]] if dims_number > 1 else [x for x in range(dims_number)]
        else:
            perm = list(range(0, dims_number))
        inv = PermuteAttrs.get_inverse_permutation(perm)
        return PermuteAttrs.Permutation(perm=(np.array(perm)), inv=(np.array(inv)))

    @staticmethod
    def get_nchw_to_nhwc_permutation(dims_number: int):
        if dims_number != 3:
            perm = [0,
             *[x for x in range(2, dims_number)], 1] if dims_number > 1 else [x for x in range(dims_number)]
        else:
            perm = list(range(0, dims_number))
        inv = PermuteAttrs.get_inverse_permutation(perm)
        return PermuteAttrs.Permutation(perm=(np.array(perm)), inv=(np.array(inv)))
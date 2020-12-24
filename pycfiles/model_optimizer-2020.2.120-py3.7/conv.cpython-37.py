# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/middle/passes/conv.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 11828 bytes
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
from mo.front.common.layout import get_batch_dim, get_features_dim
from mo.front.extractor import add_attrs_props
from mo.front.extractor import update_ie_fields
from mo.graph.graph import Node, Graph
from mo.middle.passes.fusing.helpers import get_value_id, get_tensor_id, get_tensor_in_port, get_value_in_port
from mo.middle.pattern_match import apply_pattern
from mo.ops.const import Const
from mo.ops.scale_shift import ScaleShiftOp

def pad_op_transform(graph: Graph, match: dict):
    op = match['op']
    pad_op = match['pad_op']
    input_data = pad_op.in_node(0)
    if pad_op.mode != 'constant':
        log.info('The pad node "{}" with pad mode "{}" cannot be fused.'.format(pad_op.soft_get('name'), pad_op.mode))
        return
    if pad_op.mode == 'constant':
        if pad_op.fill_value != 0.0:
            log.info('The pad node "{}" with non-zero fill value cannot be fused.'.format(pad_op.soft_get('name')))
            return
    input_tensor_dims = len(match['pad_output'].shape)
    for in_port in (1, 2):
        pads = pad_op.in_port(in_port).data.get_value()
        if pads[get_features_dim(op.graph.graph['layout'], input_tensor_dims)] != 0 or pads[get_batch_dim(op.graph.graph['layout'], input_tensor_dims)] != 0:
            log.info('The pad node "{}" with padding over feature/batch dimension cannot be fused.'.format(pad_op.soft_get('name')))
            return

    op.pad += np.concatenate([pad_op.in_port(1).data.get_value().reshape([-1, 1]),
     pad_op.in_port(2).data.get_value().reshape([-1, 1])],
      axis=1)
    op.pad_spatial_shape = op.pad[op.spatial_dims]
    op['auto_pad'] = None
    if op.type == 'Pooling':
        op['exclude_pad'] = False
    assert graph[match['pad_output'].node][match['op'].node][0]['in'] == 0
    edge_attrs = graph.get_edge_data(match['pad_output'].id, match['op'].id)[0]
    graph.remove_edge(match['pad_output'].id, match['op'].id)
    (graph.add_edge)((input_data.id), (match['op'].id), **{**{'in': 0}, **edge_attrs})


def fuse_pad(graph: Graph):
    for op_type in ('Convolution', 'Pooling', 'Deconvolution'):
        apply_pattern(graph,
          nodes=[
         (
          'pad_op', dict(kind='op', op='Pad')),
         (
          'pad_output', dict(kind='data')),
         (
          'op', dict(kind='op', type=op_type))],
          edges=[
         ('pad_op', 'pad_output'),
         (
          'pad_output', 'op', {'in': 0})],
          action=pad_op_transform)


def muladd_to_scaleshift_action(graph: Graph, match: dict):
    mul = match['mul']
    add = match['add']
    output = match['output']
    if len(mul.out_port(0).get_destinations()) > 1:
        return
    if mul.soft_get('can_be_scaleshift') is False or add.soft_get('can_be_scaleshift') is False:
        return
    mul_weights_id = get_value_id(mul)
    mul_input_id = get_tensor_id(mul)
    add_weights_id = get_value_id(add)
    if mul_weights_id is None:
        log.debug('Mul->Add to ScaleShift: Mul {} has no weights'.format(mul.name))
        return
    if mul_input_id is None:
        log.debug('Mul->Add to ScaleShift: Mul {} has no input'.format(mul.name))
        return
    if add_weights_id is None:
        log.debug('Mul->Add to ScaleShift: Add {} has no weights'.format(add.name))
        return
    input = mul.in_node(mul_input_id)
    weights = mul.in_node(mul_weights_id)
    bias = add.in_node(add_weights_id)
    weights.value = np.squeeze(weights.value)
    weights.shape = np.array((weights.value.shape), dtype=(np.int64))
    bias.value = np.squeeze(bias.value)
    bias.shape = np.array((bias.value.shape), dtype=(np.int64))
    if weights.value.ndim == 0:
        if bias.value.ndim == 1:
            weights.value = np.full(bias.shape, weights.value.item())
            weights.shape = np.array((weights.value.shape), dtype=(np.int64))
    if bias.shape != weights.shape:
        log.warning('Mul->Add to ScaleShift conversion stoped {} != {}'.format(weights.shape, bias.shape))
        return
    if bias.value.ndim != weights.value.ndim or bias.value.size != weights.value.size:
        log.debug('Skipping Mul->Add to ScaleShift conversion for nodes {}, {} because of different weights and biases'.format(mul.name, add.name))
        return
    if bias.value.size == 1:
        if weights.value.size == 1:
            log.debug('Skipping Mul->Add to ScaleShift conversion for nodes {}, {}. Will be converted to Power'.format(mul.name, add.name))
            return
    op_name = 'ScaleShift'
    log.debug('Fusing Mul->Add to {}. Input nodes: {} and {}, bias.shape = {}, weights.shape = {}'.format(op_name, mul.id, add.id, bias.shape, weights.shape))
    graph.remove_edge(input.node, mul.id)
    graph.remove_edge(weights.node, mul.id)
    graph.remove_edge(bias.node, add.id)
    graph.remove_edge(add.node, output.id)
    op_node = graph.unique_id(mul.name + '/Fused{}_'.format(op_name))
    (graph.add_node)(op_node, **add_attrs_props(dict(kind='op', type=op_name, name=op_node, op=op_name, data_type=(input.data_type))))
    scsh = Node(graph, op_node)
    scsh.add_input_port(0)
    scsh.add_input_port(1)
    scsh.add_input_port(2)
    scsh.add_output_port(0)
    update_ie_fields(graph.node[op_node])
    graph.add_edges_from([
     (
      input.node, op_node, {'in': 0}),
     (
      weights.node, op_node, {'in':1,  'bin':'weights'}),
     (
      bias.node, op_node, {'in':2,  'bin':'biases'}),
     (
      op_node, output.node, {'out': 0})])


def convert_muladd_to_scaleshift(graph: Graph):
    if hasattr(graph, 'graph'):
        if 'cmd_params' in graph.graph:
            if graph.graph['cmd_params'].generate_experimental_IR_V10:
                return
    apply_pattern(graph,
      nodes=[
     (
      'input', dict(kind='data')),
     (
      'weights', dict(kind='data')),
     (
      'bias', dict(kind='data')),
     (
      'mout', dict(kind='data')),
     (
      'output', dict(kind='data')),
     (
      'mul', dict(kind='op', op='Mul')),
     (
      'add', dict(kind='op', op='Add'))],
      edges=[
     ('weights', 'mul'),
     ('input', 'mul'),
     ('mul', 'mout'),
     ('mout', 'add'),
     ('bias', 'add'),
     ('add', 'output')],
      action=muladd_to_scaleshift_action)


def batch_norm_fuse_action(graph: Graph, match: dict):
    """
    Multiply convolution kernel by batch normalization coefficient and remove mul op.
    """
    if match['norm'].value is None or match['kernel'].value is None:
        return
    if len(graph.out_edges(match['conv_output'].node)) > 1 or len(graph.out_edges(match['kernel'].node)) > 1:
        return
    match['kernel'].value = match['kernel'].value * match['norm'].value
    graph.remove_edge(match['conv_output'].node, match['mul'].node)
    graph.remove_edge(match['mul'].node, match['mul_output'].node)
    graph.add_edge((match['conv'].node), (match['mul_output'].node), out=0)


def batch_norm_fuse(graph: Graph):
    apply_pattern(graph,
      nodes=[
     (
      'kernel', dict(kind='data')),
     (
      'conv', dict(kind='op', op='Conv2D')),
     (
      'conv_output', dict(kind='data')),
     (
      'norm', dict(kind='data')),
     (
      'mul', dict(kind='op', op='Mul')),
     (
      'mul_output', dict(kind='data'))],
      edges=[
     (
      'kernel', 'conv', {'in': 1}),
     ('conv', 'conv_output'),
     (
      'conv_output', 'mul', {'in': 0}),
     (
      'norm', 'mul', {'in': 1}),
     ('mul', 'mul_output')],
      action=batch_norm_fuse_action)
    return graph


def convert_add_or_mul_to_scaleshift(graph: Graph):
    if graph.graph['cmd_params'].generate_experimental_IR_V10:
        return
    graph.strict_mode = False
    for node in graph.get_op_nodes():
        if node.soft_get('op') in ('Add', 'Mul') and len(node.in_ports()) == 2:
            tensor_port, value_port = get_tensor_in_port(node), get_value_in_port(node)
        if tensor_port is not None:
            if tensor_port.disconnected() or value_port is not None and node.soft_get('can_be_scaleshift') is not False:
                original_value = value_port.data.get_value()
                if original_value.size == 1:
                    continue
                value_port.data.set_value(np.squeeze(original_value))
                scsh_op = ScaleShiftOp(graph, dict(name=('ScaleShift/{}'.format(node.name)))).create_node()
                if node.op == 'Mul':
                    const_op = Const(graph, dict(name=('{}/biases'.format(scsh_op.name)), value=np.zeros((value_port.data.get_shape()), dtype=(np.float32)),
                      shape=(np.array(value_port.data.get_shape())))).create_node()
                    const_op.out_port(0).connect(scsh_op.in_port(2))
                    scsh_op.in_port(2).bin = 'biases'
                    tensor_port.get_connection().set_destination(scsh_op.in_port(0))
                    value_port.get_connection().set_destination(scsh_op.in_port(1))
                else:
                    const_op = Const(graph, dict(name=('{}/weights'.format(scsh_op.name)), value=np.ones((value_port.data.get_shape()), dtype=(np.float32)),
                      shape=(np.array(value_port.data.get_shape())))).create_node()
                    tensor_port.get_connection().set_destination(scsh_op.in_port(0))
                    const_op.out_port(0).connect(scsh_op.in_port(1))
                    value_port.get_connection().set_destination(scsh_op.in_port(2))
                scsh_op.in_port(2).bin = 'biases'
            node.out_port(0).get_connection().set_source(scsh_op.out_port(0))
            scsh_op.in_port(1).bin = 'weights'

    graph.strict_mode = True
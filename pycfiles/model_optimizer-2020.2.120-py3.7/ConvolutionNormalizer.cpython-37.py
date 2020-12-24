# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/back/ConvolutionNormalizer.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 14009 bytes
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
import extensions.back.ReshapeMutation as ReshapeMutation
from extensions.back.ReverseInputChannels import ApplyReverseChannels
from mo.back.replacement import BackReplacementPattern
from mo.front.common.partial_infer.utils import int64_array
from mo.front.tf.graph_utils import create_op_node_with_second_input
from mo.graph.graph import Graph
from mo.ops.const import Const
from mo.ops.reshape import Reshape
from mo.ops.strided_slice import StridedSlice

class ConvolutionNormalizer(BackReplacementPattern):
    enabled = True
    graph_condition = [lambda graph: graph.graph['cmd_params'].generate_experimental_IR_V10]

    def pattern(self):
        return dict(nodes=[
         (
          'node', dict(kind='op', type='Convolution'))],
          edges=[])

    def replace_pattern(self, graph: Graph, match: dict):
        node = match['node']
        if node.has_valid('kernel_spatial'):
            del node['kernel_spatial']


class ConvolutionReshaper(BackReplacementPattern):
    __doc__ = '\n        Workarounds absence of 1D Convolution support in Inference Engine by converting it to 2D Convolution\n            - updating shape dependent Convolution parameters with fake H: dilation, kernel, pad, stride\n            - reshape weights from [OIX] -> [OIYX] = [OI1X]\n            - inserting fake H dimension by adding reshapes before and after Convolution: [NCW] -> [NCHW] = [NC1W]\n    '
    enabled = True
    graph_condition = [lambda graph: not graph.graph['cmd_params'].generate_experimental_IR_V10]

    def run_before(self):
        return [
         ReshapeMutation]

    @staticmethod
    def pattern():
        return dict(nodes=[
         (
          'conv', dict(type='Convolution'))],
          edges=[])

    def replace_pattern(self, graph: Graph, match: dict):
        conv = match['conv']
        assert len(conv.out_nodes()) == 1, 'Convolution operation {} should have 1 output data node'.format(conv.id)
        out_data = conv.out_node()
        assert out_data.has_valid('shape'), 'Output shape is undefined for {} in back phase'.format(conv.id)
        out_shape = out_data.shape
        if out_shape.size != 3:
            return
        assert len(conv.in_nodes()) >= 1, 'Convolution operation {} should have more than 1 input data node'.format(conv.id)
        inp_data = conv.in_node()
        assert inp_data.has_valid('shape'), 'Input shape is undefined for {} in back phase'.format(conv.id)
        inp_shape = inp_data.shape
        new_inp_shape = np.insert(inp_shape, 2, 1)
        conv.kernel_spatial_idx = None
        conv.spatial_dims = None
        conv.dilation = np.insert(conv.dilation, 2, 1)
        conv.kernel_spatial = np.append([1], conv.kernel_spatial)
        conv.pad = np.insert((conv.pad), 2, [0, 0], axis=0)
        conv.stride = np.insert(conv.stride, 2, 1)
        weights_node = conv.in_node(1)
        weights_node.value = np.reshape(weights_node.value, np.insert(weights_node.value.shape, 2, 1))
        weights_node.shape = np.array((weights_node.value.shape), dtype=(np.int64))
        reshape = Reshape(graph, {'name': conv.name + '/reshape'}).create_node()
        reshape_dim = Const(graph, {'value':new_inp_shape,  'name':reshape.id + '/Dim'}).create_node()
        conv.in_port(0).get_connection().insert_node(reshape)
        reshape.in_port(1).connect(reshape_dim.out_port(0))
        reshape_back = Reshape(graph, {'name': conv.name + '/reshape_back'}).create_node()
        reshape_back_dim = Const(graph, {'value':out_shape,  'name':reshape.id + '/Dim'}).create_node()
        conv.out_port(0).get_connection().insert_node(reshape_back)
        reshape_back.in_port(1).connect(reshape_back_dim.out_port(0))
        reshape_dim.infer(reshape_dim)
        reshape.infer(reshape)
        conv.infer(conv)


class V7ConvolutionWithGroupsResolver(BackReplacementPattern):
    __doc__ = '\n    Normalizes grouped convolution weights shape to fit special weights format [G*O I X Y]\n    '
    enabled = False

    @staticmethod
    def pattern():
        return dict(nodes=[
         (
          'node', dict(type='Convolution', group=(lambda g: g is not None and g != 1)))],
          edges=[])

    def replace_pattern(self, graph: Graph, match: dict):
        node = match['node']
        group = node.group
        assert group > 1
        weights_shape = node.in_port(1).data.get_shape()
        assert weights_shape is not None
        assert weights_shape[0] % group == 0
        if weights_shape[0] == node.output:
            return
        new_shape = int64_array([node.output, -1, *weights_shape[2:]])
        reshape = create_op_node_with_second_input(graph, Reshape, int64_array(new_shape), {'override_output_shape': True})
        node.in_port(1).get_connection().insert_node(reshape)


class V10ConvolutionWithGroupsResolver(BackReplacementPattern):
    __doc__ = '\n    Normalizes grouped convolution weights shape to fit special weights format\n        V10 IR:                 [G O I X Y]\n    '
    enabled = False

    @staticmethod
    def pattern():
        return dict(nodes=[
         (
          'node', dict(type='Convolution', group=(lambda g: g is not None and g != 1)))],
          edges=[])

    def replace_pattern(self, graph: Graph, match: dict):
        node = match['node']
        group = node.group
        assert group > 1
        weights_shape = node.in_port(1).data.get_shape()
        assert weights_shape is not None
        assert weights_shape[0] % group == 0
        I = node.in_port(0).data.get_shape()[1]
        new_shape = int64_array([group, node.output / group, I / group, *weights_shape[2:]])
        assert np.prod(weights_shape) == np.prod(new_shape), 'Initial weights shape {}, grouped weights shape {}'.format(weights_shape, new_shape)
        del node['group']
        node['type'] = 'GroupConvolution'
        reshape = create_op_node_with_second_input(graph, Reshape, int64_array(new_shape), {'override_output_shape': True})
        node.in_port(1).get_connection().insert_node(reshape)


class ConvolutionWithGroupsResolver(BackReplacementPattern):
    __doc__ = '\n    Normalizes grouped convolution weights shape to fit special weights format\n        V10 IR:                 [G O I X Y]\n        lower IR versions:      [G*O I X Y]\n    '
    enabled = True
    force_clean_up = True

    def run_before(self):
        return [
         ReshapeMutation]

    def run_after(self):
        return [
         ConvolutionReshaper, ApplyReverseChannels]

    def find_and_replace_pattern(self, graph: Graph):
        V7ConvolutionWithGroupsResolver().find_and_replace_pattern(graph)
        PullReshapeThroughFQ().find_and_replace_pattern(graph)
        if graph.graph['cmd_params'].generate_experimental_IR_V10:
            V10ConvolutionWithGroupsResolver().find_and_replace_pattern(graph)


class PullReshapeThroughFQ(BackReplacementPattern):
    __doc__ = '\n    Before:\n        ... -> FQ -> Reshape -> Convolution -> ...\n\n    After:\n        ... -> Reshape -> FQ (with aligned limits) -> Convolution -> ...\n    '
    enabled = False

    @staticmethod
    def pattern():
        return dict(nodes=[
         (
          'FQ', dict(type='FakeQuantize')),
         (
          'FQed', dict()),
         (
          'reshape', dict(type='Reshape')),
         (
          'reshaped', dict()),
         (
          'node', dict(type=(lambda t: t in ('Convolution', 'GroupConvolution'))))],
          edges=[
         ('FQ', 'FQed'),
         (
          'FQed', 'reshape', {'in': 0}),
         ('reshape', 'reshaped'),
         (
          'reshaped', 'node', {'in': 1})])

    def replace_pattern(self, graph: Graph, match: dict):
        FQ = match['FQ']
        reshape = match['reshape']
        conv = match['node']
        rank_reshape = reshape.in_port(0).data.get_shape().size != reshape.out_port(0).data.get_shape().size
        if not all([np.prod(FQ.in_port(i).data.get_shape()) == 1 for i in range(1, 5)]):
            return
        new_rank = reshape.out_port(0).data.get_shape().size
        reshape.in_port(0).disconnect()
        reshape.out_port(0).disconnect()
        FQ.out_port(0).connect(conv.in_port(1))
        FQ.in_port(0).get_connection().insert_node(reshape)
        reshape['need_shape_inference'] = True
        reshape['override_output_shape'] = True
        FQ['need_shape_inference'] = True
        FQ['override_output_shape'] = True
        if rank_reshape:
            for i in range(1, 5):
                reshape = create_op_node_with_second_input(graph, Reshape, int64_array([1] * new_rank), {'override_output_shape': True})
                FQ.in_port(i).get_connection().insert_node(reshape)


class DeconvolutionNormalizer(BackReplacementPattern):
    enabled = True
    graph_condition = [lambda graph: graph.graph['cmd_params'].generate_experimental_IR_V10]
    force_clean_up = True

    def run_before(self):
        return [
         ReshapeMutation]

    def run_after(self):
        return [
         ConvolutionReshaper, ApplyReverseChannels]

    @staticmethod
    def pattern():
        return dict(nodes=[
         (
          'node', dict(type='Deconvolution'))],
          edges=[])

    def replace_pattern(self, graph: Graph, match: dict):
        node = match['node']
        if 2 in node.in_ports():
            in_rank = node.in_port(2).disconnected() or node.in_port(0).data.get_shape().size
            shape_src = node.in_port(2).get_source()
            node.in_port(2).disconnect()
            begin = Const(graph, {'value': np.array([2], dtype=(np.int32))}).create_node()
            end = Const(graph, {'value': np.array([in_rank], dtype=(np.int32))}).create_node()
            stride = Const(graph, {'value': np.array([1], dtype=(np.int32))}).create_node()
            ss_0 = StridedSlice(graph, {'name':node.name + '/ss_0_port',  'begin_mask':np.array([1], dtype=np.int32), 
             'end_mask':np.array([0], dtype=np.int32), 
             'new_axis_mask':np.array([0], dtype=np.int32), 
             'shrink_axis_mask':np.array([0], dtype=np.int32), 
             'ellipsis_mask':np.array([0], dtype=np.int32)}).create_node()
            shape_src.connect(ss_0.in_port(0))
            begin.out_port(0).connect(ss_0.in_port(1))
            end.out_port(0).connect(ss_0.in_port(2))
            stride.out_port(0).connect(ss_0.in_port(3))
            ss_0.out_port(0).connect(node.in_port(2))
            del node['pad']
        else:
            if node.has_valid('original_output_spatial_shape'):
                const = Const(graph, {'value': int64_array(node.original_output_spatial_shape)}).create_node()
                node.add_input_port(2, skip_if_exist=True)
                const.out_port(0).connect(node.in_port(2))
                del node['pad']
            else:
                group = node.soft_get('group', 1)
                if group != 1:
                    assert group > 1
                    weights_shape = node.in_port(1).data.get_shape()
                    assert weights_shape is not None
                    I = node.in_port(0).data.get_shape()[1]
                    assert I % group == 0
                    assert node.output % group == 0
                    new_shape = int64_array([group, I / group, node.output / group, *weights_shape[2:]])
                    assert np.prod(weights_shape) == np.prod(new_shape), 'Initial weights shape {}, grouped weights shape {}'.format(weights_shape, new_shape)
                    reshape = create_op_node_with_second_input(graph, Reshape, int64_array(new_shape), {'override_output_shape': True}, node.in_port(1).get_source().node)
                    node.in_port(1).get_connection().set_source(reshape.out_port(0))
                    node['type'] = 'GroupConvolutionBackpropData'
                else:
                    node['type'] = 'ConvolutionBackpropData'
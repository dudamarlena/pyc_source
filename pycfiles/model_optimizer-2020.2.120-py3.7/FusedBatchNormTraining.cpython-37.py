# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/middle/FusedBatchNormTraining.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 3840 bytes
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
from extensions.ops.mvn import MVN
from mo.front.common.partial_infer.utils import int64_array
from mo.front.tf.graph_utils import create_op_node_with_second_input
from mo.graph.graph import Graph
from mo.middle.replacement import MiddleReplacementPattern
from mo.ops.const import Const
from mo.ops.reshape import Reshape
from mo.ops.shape import Shape

class FusedBatchNormTraining(MiddleReplacementPattern):
    __doc__ = '\n    Transformation looks for the BatchNorm layers in training mode and does the following:\n    1. Fuses batch dimension with one of the spatial dimensions of the input to BatchNorm because batch normalization is\n    performed over batch dimension also (per channel(features) dimension).\n    2. Inserts MVN layer.\n    3. Reshape MVN output back to the original one.\n    '
    enabled = True
    replacement_id = 'Fused_Batch_Norm_is_training_true'
    force_shape_inference = True
    force_clean_up = True
    graph_condition = [
     lambda graph: graph.graph['layout'] == 'NHWC']

    def pattern(self):
        return dict(nodes=[
         (
          'op', dict(kind='op', op='FusedBatchNorm', is_training=True))],
          edges=[])

    def replace_pattern(self, graph: Graph, match: dict):
        node = match['op']
        node.is_training = False
        shape = node.in_port(1).data.get_shape()
        assert shape is not None, 'The shape of scale input of the BatchNorm node {} is not defined'.format(node.name)
        bn_mean = Const(graph, {'name':node.name + '/mean',  'value':np.zeros(shape, dtype=np.float32),  'override_output_shape':True}).create_node()
        bn_std = Const(graph, {'name':node.name + '/std',  'value':np.ones(shape, dtype=np.float32),  'override_output_shape':True}).create_node()
        node.in_port(3).get_connection().set_source(bn_mean.out_port(0))
        node.in_port(4).get_connection().set_source(bn_std.out_port(0))
        original_shape = Shape(graph, {'name': node.in_port(0).get_source().node.soft_get('name')}).create_node()
        original_shape.in_port(0).connect(node.in_port(0).get_source())
        mvn = MVN(graph, {'name':node.name + '/mvn_',  'eps':node.soft_get('eps', 1e-06),  'override_output_shape':True}).create_node()
        node.in_port(0).get_connection().insert_node(mvn)
        reshape_4d = create_op_node_with_second_input(graph, Reshape, int64_array([1, -1, 0, 0]), {'override_output_shape':True, 
         'name':node.soft_get('name') + '/fused_batch_and_channels'})
        mvn.in_port(0).get_connection().insert_node(reshape_4d)
        reshape_back = Reshape(graph, {'name':mvn.soft_get('name') + '/restore_shape',  'override_output_shape':True}).create_node()
        reshape_back.in_port(1).connect(original_shape.out_port(0))
        mvn.out_port(0).get_connection().insert_node(reshape_back)
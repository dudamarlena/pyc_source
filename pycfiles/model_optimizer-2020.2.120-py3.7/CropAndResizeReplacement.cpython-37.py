# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/tf/CropAndResizeReplacement.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 3544 bytes
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
import logging as log
import extensions.ops.Cast as Cast
from mo.front.common.partial_infer.utils import int64_array
from mo.front.common.replacement import FrontReplacementOp
from mo.front.tf.graph_utils import add_convolution_to_swap_xy_coordinates, create_op_node_with_second_input
from mo.graph.graph import Node, Graph
from mo.middle.passes.convert_data_type import data_type_str_to_np
from mo.ops.concat import Concat
from mo.ops.reshape import Reshape
from mo.ops.unsqueeze import Unsqueeze

class CropAndResizeReplacement(FrontReplacementOp):
    __doc__ = '\n    The CropAndResize operation from TF gets separate input with boxes coordinates and image batch indices. But\n    ROIPooling operation in the Inference Engine receives them as a single concatenated input. This replacer\n    concatenates two inputs into a new one.\n    '
    op = 'CropAndResize'
    enabled = True

    def nodes_to_remove(self, graph: Graph, match: dict):
        return []

    def replace_op(self, graph: Graph, node: Node):
        if node.has_and_set('inputs_preprocessed'):
            log.debug('Node "{}" has already been preprocessed'.format(node.soft_get('name')))
            return []
        unsqueeze_node = create_op_node_with_second_input(graph, Unsqueeze, int64_array([1]), {'name': node.name + '/Unsqueeze'}, node.in_node(2))
        convert_node = Cast(graph, {'name':unsqueeze_node.name + '/ToFloat',  'dst_type':data_type_str_to_np(graph.graph['cmd_params'].data_type)}).create_node()
        convert_node.in_port(0).connect(unsqueeze_node.out_port(0))
        concat_op = Concat(graph, {'axis':1,  'name':node.name + '/concat_batch_indices_and_boxes',  'in_ports_count':2})
        concat_node = concat_op.create_node([convert_node, node.in_node(1)])
        graph.remove_edge(node.in_node(1).id, node.id)
        swapped_box_coordinates_node = add_convolution_to_swap_xy_coordinates(graph, concat_node, 5)
        reshape_2d_node = create_op_node_with_second_input(graph, Reshape, int64_array([-1, 5]), dict(name=(swapped_box_coordinates_node.id + '/reshape_2d_')), swapped_box_coordinates_node)
        graph.create_edge(reshape_2d_node, node, 0, 1)
        return []
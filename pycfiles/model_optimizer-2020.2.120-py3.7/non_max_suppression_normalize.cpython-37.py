# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/tf/non_max_suppression_normalize.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 3882 bytes
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
from mo.front.common.partial_infer.utils import int64_array
from mo.front.common.replacement import FrontReplacementSubgraph
from mo.front.tf.graph_utils import create_op_node_with_second_input
from mo.graph.graph import Graph
from mo.ops.crop import Crop
from mo.ops.reshape import Reshape
from mo.ops.squeeze import Squeeze
from mo.ops.unsqueeze import Unsqueeze

class TFNonMaxSuppressionNormalize(FrontReplacementSubgraph):
    __doc__ = '\n    The inputs and outputs format of the TF implementation of the NMS layer is different from the Inference Engine\n    implementation and supports just one batch and image class. This transformation converts inputs and outputs to\n    match the Inference Engine implementation.\n\n    TF inputs: boxes = [num_boxes, 4]\n               scores = [num_boxes]\n       outputs: box_indices [selected_boxes_count]\n\n    IE inputs: boxes = [num_batches, num_boxes, 4]\n               scores = [num_batches, num_classes, num_boxes]\n       outputs: selected_indices [num_selected_indices, 3] where each element is [batch_index, class_index, box_index]\n    '
    enabled = True

    @staticmethod
    def pattern(**kwargs):
        return dict(nodes=[
         (
          'nms', dict(op='NonMaxSuppression'))],
          edges=[])

    @staticmethod
    def replace_sub_graph(graph: Graph, match: dict, **kwargs):
        nms = match['nms']
        unsqueeze_boxes = create_op_node_with_second_input(graph, Unsqueeze, int64_array([0]), {'name': nms.soft_get('name') + '/Unsqueeze_0'})
        nms.in_port(0).get_connection().insert_node(unsqueeze_boxes)
        unsqueeze_box_scores = create_op_node_with_second_input(graph, Reshape, int64_array([1, 1, -1]), {'name': nms.soft_get('name') + '/Unsqueeze_1'})
        nms.in_port(1).get_connection().insert_node(unsqueeze_box_scores)
        crop_box_indices = Crop(graph, {'name':nms.soft_get('name') + '/Crop',  'axis':int64_array([1]),  'offset':int64_array([2]), 
         'dim':int64_array([1])}).create_node()
        nms.out_port(0).get_connection().insert_node(crop_box_indices)
        squeeze_output_boxes = create_op_node_with_second_input(graph, Squeeze, int64_array([1]), {'name': crop_box_indices.soft_get('name') + '/Squeeze'})
        crop_box_indices.out_port(0).get_connection().insert_node(squeeze_output_boxes)
        if 5 in nms.in_ports():
            soft_nms_sigma = nms.in_port(5).disconnected() or nms.in_port(5).get_source().data.get_value()
            if soft_nms_sigma is not None:
                if soft_nms_sigma != 0.0:
                    log.error('The input to layer "{}" with value for the soft_nms_sigma is equal to "{}" but only value 0is supported. The inference results will be incorrect.'.format(nms.soft_get('name'), soft_nms_sigma))
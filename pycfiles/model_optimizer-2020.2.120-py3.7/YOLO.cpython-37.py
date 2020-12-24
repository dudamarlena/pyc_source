# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/YOLO.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 3809 bytes
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
from extensions.front.no_op_eraser import NoOpEraser
from extensions.front.standalone_const_eraser import StandaloneConstEraser
from extensions.ops.regionyolo import RegionYoloOp
from mo.front.tf.replacement import FrontReplacementFromConfigFileGeneral
from mo.graph.graph import Node, Graph
from mo.ops.result import Result
from mo.utils.error import Error

class YoloRegionAddon(FrontReplacementFromConfigFileGeneral):
    __doc__ = '\n    Replaces all Result nodes in graph with YoloRegion->Result nodes chain.\n    YoloRegion node attributes are taken from configuration file\n    '
    replacement_id = 'TFYOLO'

    def run_after(self):
        return [
         NoOpEraser, StandaloneConstEraser]

    def transform_graph(self, graph: Graph, replacement_descriptions):
        op_outputs = [n for n, d in graph.nodes(data=True) if 'op' in d if d['op'] == 'Result']
        for op_output in op_outputs:
            last_node = Node(graph, op_output).in_node(0)
            op_params = dict(name=(last_node.id + '/YoloRegion'), axis=1, end_axis=(-1))
            op_params.update(replacement_descriptions)
            region_layer = RegionYoloOp(graph, op_params)
            region_layer_node = region_layer.create_node([last_node])
            region_layer_node.dim_attrs.remove('axis')
            Result(graph).create_node([region_layer_node])
            graph.remove_node(op_output)


class YoloV3RegionAddon(FrontReplacementFromConfigFileGeneral):
    __doc__ = '\n    Replaces all Result nodes in graph with YoloRegion->Result nodes chain.\n    YoloRegion node attributes are taken from configuration file\n    '
    replacement_id = 'TFYOLOV3'

    def transform_graph(self, graph: Graph, replacement_descriptions):
        graph.remove_nodes_from(graph.get_nodes_with_attributes(op='Result'))
        for i, input_node_name in enumerate(replacement_descriptions['entry_points']):
            if input_node_name not in graph.nodes():
                raise Error('TensorFlow YOLO V3 conversion mechanism was enabled. Entry points "{}" were provided in the configuration file. Entry points are nodes that feed YOLO Region layers. Node with name {} doesn\'t exist in the graph. Refer to documentation about converting YOLO models for more information.'.format(', '.join(replacement_descriptions['entry_points']), input_node_name))
            last_node = Node(graph, input_node_name).in_node(0)
            op_params = dict(name=(last_node.id + '/YoloRegion'), axis=1, end_axis=(-1), do_softmax=0)
            op_params.update(replacement_descriptions)
            if 'masks' in op_params:
                op_params['mask'] = op_params['masks'][i]
                del op_params['masks']
            region_layer_node = RegionYoloOp(graph, op_params).create_node([last_node])
            region_layer_node.dim_attrs.remove('axis')
            Result(graph, {'name': region_layer_node.id + '/Result'}).create_node([region_layer_node])
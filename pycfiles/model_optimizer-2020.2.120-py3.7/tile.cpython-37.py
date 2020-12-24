# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/ops/tile.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 4188 bytes
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
from mo.front.common.partial_infer.utils import int64_array
from mo.graph.graph import Node, Graph
from mo.graph.perm_inputs import PermuteInputs
from mo.ops.op import Op, PermuteAttrs

class Tile(Op):
    op = 'Tile'
    enabled = False

    def __init__(self, graph, attrs):
        super().__init__(graph, {'op':self.op, 
         'type':self.op, 
         'infer':self.infer, 
         'in_ports_count':2, 
         'out_ports_count':1}, attrs)

    @staticmethod
    def infer(node: Node):
        name = node.soft_get('name', node.id)
        connected_in_ports = {idx:port for idx, port in node.in_ports().items() if not port.disconnected() if not port.disconnected()}
        if not (len(connected_in_ports) == 2 and 0 in connected_in_ports and 1 in connected_in_ports):
            raise AssertionError("Tile should have 2 connected input port, but it doesn't for node: `{}`. Ports: {}".format(name, connected_in_ports))
        shape = node.in_port(0).data.get_shape()
        assert shape is not None, "Undefined input shape for Tile node '{}'.".format(name)
        tile_array = node.in_port(1).data.get_value()
        assert tile_array is not None, "Undefined `repeats` (1st port input value) of Tile node '{}'".format(name)
        if shape.size < tile_array.size:
            shape = np.insert(shape, 0, [1] * (tile_array.size - shape.size))
        else:
            if shape.size > tile_array.size:
                tile_array = np.insert(tile_array, 0, [1] * (shape.size - tile_array.size))
            elif node.in_port(0).data.get_value() is not None:
                node.out_port(0).data.set_value(np.tile(node.in_port(0).data.get_value().reshape(shape), tile_array))
            else:
                node.out_port(0).data.set_shape(shape * tile_array)
            PermuteInputs().set_input_permutation(node.in_node(1), node, 'input:0', 'shape')


class AttributedTile(Op):
    op = 'AttributedTile'
    enabled = False

    def __init__(self, graph, attrs):
        super().__init__(graph, {'op':self.op, 
         'type':'Tile', 
         'infer':self.infer, 
         'in_ports_count':1, 
         'out_ports_count':1}, attrs)
        assert 'axis' in self.attrs
        assert 'tiles' in self.attrs

    def supported_attrs(self):
        return [
         'axis', 'tiles']

    @staticmethod
    def infer(node):
        name = node.soft_get('name', node.id)
        connected_in_ports = {idx:port for idx, port in node.in_ports().items() if not port.disconnected() if not port.disconnected()}
        if not (len(connected_in_ports) == 1 and 0 in connected_in_ports):
            raise AssertionError("AttributedTile should have 1 connected input port, but it doesn't for node: `{}`. Ports: {}".format(name, connected_in_ports))
        shape = node.in_port(0).data.get_shape()
        assert shape is not None, "Undefined input shape for AttributedTile node '{}'.".format(name)
        axis = node.soft_get('axis', None)
        assert axis is not None
        tiles = node.soft_get('tiles', None)
        assert tiles is not None, "Undefined `tiles` attribute of Tile node '{}'".format(name)
        tile_array = int64_array(np.ones(shape.size))
        tile_array[node.axis] = node.tiles
        node.out_port(0).data.set_shape(shape * tile_array)
        if node.in_port(0).data.get_value() is not None:
            node.out_port(0).data.set_value(np.tile(node.in_port(0).data.get_value(), tile_array))
        PermuteAttrs.create_permute_attrs(node, attrs=[('axis', 'input:0')])
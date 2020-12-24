# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/middle/passes/mean_scale_values.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 2877 bytes
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
from mo.graph.graph import Graph
from mo.middle.pattern_match import apply_pattern

def move_scaleshift_to_preprocess_action(graph, match):
    mean_values = {}
    input_op = match['input_op']
    scale_shift = match['scale_shift']
    weights = np.squeeze(match['weights'].value)
    biases = np.squeeze(match['biases'].value)
    if graph.graph['cmd_params'].reverse_input_channels:
        biases = np.flip(biases)
    elif any([x != 1 for x in weights]):
        return
        graph.remove_edge(input_op.id, input_op.out_node().id)
        graph.add_edge((input_op.id), (scale_shift.out_node().id), out=0)
        graph.remove_edge(scale_shift.id, scale_shift.out_node().id)
        if all([x == 0 for x in biases]):
            return
        biases *= -1
        mean_values.update({input_op.name: np.array(biases)})
        if graph.graph.get('mean_values', None):
            graph.graph['mean_values'].update(mean_values)
    else:
        graph.graph['mean_values'] = mean_values


def move_scaleshift_to_preprocess(graph: Graph):
    """
    This function finds scaleshift layer after input layer and if it has weights with ones, it deletes scaleshift layer
    and creates graph dict attribute : {'input':np.array(...), 'input2': ... }
    """
    apply_pattern(graph,
      nodes=[
     (
      'weights', dict(kind='data')),
     (
      'biases', dict(kind='data')),
     (
      'input_output', dict(kind='data')),
     (
      'scsh_output', dict(kind='data')),
     (
      'input_op', dict(kind='op', type='Parameter')),
     (
      'scale_shift', dict(kind='op', type='ScaleShift'))],
      edges=[
     ('input_op', 'input_output'),
     ('scale_shift', 'scsh_output'),
     (
      'input_output', 'scale_shift', {'in': 0}),
     (
      'weights', 'scale_shift', {'in': 1}),
     (
      'biases', 'scale_shift', {'in': 2})],
      action=move_scaleshift_to_preprocess_action)
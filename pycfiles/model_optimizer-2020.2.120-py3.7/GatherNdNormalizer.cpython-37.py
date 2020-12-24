# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/middle/GatherNdNormalizer.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 4087 bytes
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
from extensions.ops.gather import Gather
from mo.front.common.partial_infer.utils import int64_array
from mo.graph.graph import Graph
from mo.middle.replacement import MiddleReplacementPattern
from mo.ops.const import Const
from mo.ops.reshape import Reshape

class GatherNdNormalize(MiddleReplacementPattern):
    __doc__ = '\n    Hot fix for new speech-to-text model enabling while GatherND is not implemented in IE.\n    We can replace GatherNd to Reshape + Gather in case when GatherNd indices have just one\n    meaningful dimension.\n    '
    enabled = True
    force_clean_up = True

    def run_before(self):
        import extensions.middle.BlockLSTMtoLSTMSequence as BlockLSTMtoLSTMSequence
        return [
         BlockLSTMtoLSTMSequence]

    def run_after(self):
        from extensions.middle.pass_separator import MiddleStart
        return [
         MiddleStart]

    def pattern(self):
        return dict(nodes=[
         (
          'GatherNd', dict(kind='op', op='GatherNd'))],
          edges=[])

    @staticmethod
    def indices_check(indices: np.array, input_shape: tuple):
        """
        Check that indices have just one meaningful dimension and all other dimensions of input have size 1.
        """
        n_dims = indices.shape[(-1)]
        non_zero = None
        for i in range(n_dims):
            if not all(np.take(indices, indices=[i], axis=(-1)) == 0):
                if non_zero is None:
                    non_zero = i
                else:
                    return

        return non_zero

    def replace_pattern(self, graph: Graph, match: dict):
        gather = match['GatherNd']
        input_shape = gather.in_node(0).shape
        indices = gather.in_node(1).value
        if indices is None:
            return
        gather_idx = self.indices_check(indices, input_shape)
        if gather_idx is None:
            log.warning("Node {} with op=GatherNd  can't be normalized to op=Gather.".format(gather.name))
            return
        new_shape = int64_array([-1] + list(input_shape[indices.shape[(-1)]:]))
        reshape = Reshape(graph, {'name': gather.name + '/Reshape_for_GatherNd/'}).create_node()
        reshape_const_node = Const(graph, {'name':reshape.name + '/Dim',  'value':new_shape}).create_node()
        gather.in_port(0).get_connection().set_destination(reshape.in_port(0))
        reshape.in_port(1).connect(reshape_const_node.out_port(0))
        new_indices = np.reshape(np.take(indices, indices=[gather_idx], axis=(-1)), [-1])
        new_indices_const = Const(graph, dict(value=new_indices)).create_node()
        axis_const = Const(graph, {'value': int64_array(0)}).create_node()
        new_gather = Gather(graph, {'name': gather.name + '/NewGather/'}).create_node()
        reshape.out_port(0).connect(new_gather.in_port(0))
        new_indices_const.out_port(0).connect(new_gather.in_port(1))
        axis_const.out_port(0).connect(new_gather.in_port(2))
        gather.out_port(0).get_connection().set_source(new_gather.out_port(0))
        graph.remove_node(gather.id)
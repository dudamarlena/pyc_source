# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/back/TransposeReduceFusing.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 3387 bytes
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
from typing import Dict
import numpy as np
import extensions.back.FuseTransposesSequence as FuseTransposesSequence
from extensions.back.ReduceToPooling import ReduceMerge
from extensions.ops.ReduceOps import reduce_map
from extensions.ops.gather import Gather
from mo.back.replacement import BackReplacementPattern
from mo.front.common.partial_infer.utils import int64_array
from mo.front.tf.graph_utils import create_op_with_const_inputs
from mo.graph.graph import Graph, Node

class TransposeReduce(BackReplacementPattern):
    __doc__ = '\n    Fuse Transpose--->Reduce to Reduce with correct reduce axis input\n    '
    enabled = True
    force_clean_up = True

    def run_before(self):
        return [
         ReduceMerge]

    def run_after(self):
        return [
         FuseTransposesSequence]

    @staticmethod
    def pattern():
        return dict(nodes=[
         (
          'transpose_const',
          dict(kind='op', type='Const', value=(lambda v: v is not None and np.array_equal(v, int64_array([0, 2, 3, 1]))))),
         (
          'transpose_const_data', dict(kind='data')),
         (
          'transpose', dict(kind='op', type='Transpose')),
         (
          'transpose_data', dict(kind='data')),
         (
          'reduce_const',
          dict(kind='op', type='Const', value=(lambda v: v is not None and np.array_equal(v, int64_array([1, 2]))))),
         (
          'reduce_const_data', dict(kind='data')),
         (
          'reduce', dict(kind='op', type=(lambda t: t in reduce_map.keys()), keep_dims=False))],
          edges=[
         ('transpose_const', 'transpose_const_data'),
         (
          'transpose_const_data', 'transpose', {'in': 1}),
         ('transpose', 'transpose_data'),
         (
          'transpose_data', 'reduce', {'in': 0}),
         ('reduce_const', 'reduce_const_data'),
         (
          'reduce_const_data', 'reduce', {'in': 1})])

    @staticmethod
    def replace_pattern(graph: Graph, match: Dict[(str, Node)]):
        transpose = match['transpose']
        reduce = match['reduce']
        gather = create_op_with_const_inputs(graph, op=Gather, port_value_dict={2: int64_array(0)}, op_attrs={'name': reduce.name + 'Gather'})
        transpose.in_port(1).get_connection().set_destination(gather.in_port(0))
        reduce.in_port(1).get_connection().set_destination(gather.in_port(1))
        gather.out_port(0).connect(reduce.in_port(1))
        transpose.out_port(0).disconnect()
        transpose.in_port(0).get_connection().set_destination(reduce.in_port(0))
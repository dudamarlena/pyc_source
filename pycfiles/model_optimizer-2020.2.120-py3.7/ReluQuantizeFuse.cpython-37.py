# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/middle/ReluQuantizeFuse.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 8148 bytes
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
from typing import Dict
import numpy as np
import extensions.middle.BinarizeWeightsM1P1 as BinarizeWeightsM1P1
from extensions.middle.MulFakeQuantizeFuse import resolve_shared_inputs
from mo.graph.graph import Graph, Node
from mo.middle.replacement import MiddleReplacementPattern

class ReluFakeQuantizeMark(MiddleReplacementPattern):
    __doc__ = '\n    This pass marks Relu operations that can be fused to FakeQuantize op with `removable_before_quantize` flag.\n\n    1. We count the number of Relu outputs that are Quantize and can absorb Relu (`quantized_to_fuse_count` attribute).\n    2. Relu is fusible if all its outputs can absorb it.\n\n    '
    enabled = True

    def run_after(self):
        return [
         BinarizeWeightsM1P1]

    def run_before(self):
        import extensions.middle.SharedWeightsDuplication as SharedWeightsDuplication
        return [
         SharedWeightsDuplication]

    def pattern(self):
        return dict(nodes=[
         (
          'relu', dict(op='ReLU')),
         (
          'relu_d', dict()),
         (
          'quantize', dict(op='FakeQuantize', keep_in_IR=True))],
          edges=[
         ('relu', 'relu_d'),
         (
          'relu_d', 'quantize', {'in': 0})])

    def replace_pattern(self, graph: Graph, match: Dict[(str, Node)]):
        relu = match['relu']
        quantize = match['quantize']
        if not relu.has_valid('quantized_to_fuse_count'):
            relu['quantized_to_fuse_count'] = 0
        elif quantize.in_node(1).id == quantize.in_node(2).id:
            if not (quantize.has_valid('levels') and quantize.levels == 2):
                raise AssertionError
            threshold = quantize.in_port(1).data.get_value()
            if threshold is None:
                log.debug('ReluQuantizeFuse: cannot fuse because FakeQuantize op has dynamic input on the 1st port. levels=`{}`'.format(quantize.levels))
                return
            relu['quantized_to_fuse_count'] += 1
        else:
            if not (quantize.has_valid('levels') and quantize.levels != 2):
                raise AssertionError
            min_value = quantize.in_port(1).data.get_value()
            if min_value is None:
                log.debug('ReluQuantizeFuse: cannot fuse because FakeQuantize op has dynamic input on the 1st port, levels=`{}`'.format(quantize.levels))
                return
            if np.all(min_value >= 0):
                relu['quantized_to_fuse_count'] += 1
        relu['removable_before_quantize'] = relu['quantized_to_fuse_count'] == len(relu.out_port(0).get_destinations())


class ClampQuantizeMark(MiddleReplacementPattern):
    __doc__ = '\n    This pass marks Clamp operations that can be fused to FakeQuantize op with `removable_before_quantize` flag.\n\n    1. We count the number of Clamp outputs that are FakeQuantize and can absorb Clamp (`quantized_to_fuse_count` attribute)\n    2. Clamp is fusible if all its outputs can absorb it.\n\n    '
    enabled = True

    def run_after(self):
        return [
         BinarizeWeightsM1P1]

    def run_before(self):
        import extensions.middle.SharedWeightsDuplication as SharedWeightsDuplication
        return [
         SharedWeightsDuplication]

    def pattern(self):
        return dict(nodes=[
         (
          'clamp', dict(op='Clamp')),
         (
          'clamp_d', dict()),
         (
          'quantize', dict(op='FakeQuantize', keep_in_IR=True))],
          edges=[
         ('clamp', 'clamp_d'),
         (
          'clamp_d', 'quantize', {'in': 0})])

    def replace_pattern(self, graph: Graph, match: Dict[(str, Node)]):
        clamp = match['clamp']
        quantize = match['quantize']
        clamp_min, clamp_max = clamp['min'], clamp['max']
        if not clamp.has_valid('quantized_to_fuse_count'):
            clamp['quantized_to_fuse_count'] = 0
        if quantize.in_node(1).id == quantize.in_node(2).id:
            if not (quantize.has_valid('levels') and quantize.levels == 2):
                raise AssertionError
            clamp['removable_before_quantize'] = False
        else:
            if not (quantize.has_valid('levels') and quantize.levels != 2):
                raise AssertionError
            min_value = quantize.in_port(1).data.get_value()
            if min_value is None:
                log.debug('ReluQuantizeFuse: cannot fuse because FakeQuantize op has dynamic input on the 1st port, levels=`{}`'.format(quantize.levels))
                return
            max_value = quantize.in_port(2).data.get_value()
            if max_value is None:
                log.debug('ReluQuantizeFuse: cannot fuse because FakeQuantize op has dynamic input on the 2st port, levels=`{}`'.format(quantize.levels))
                return
            if np.all(min_value >= clamp_min):
                if np.all(max_value <= clamp_max):
                    clamp['quantized_to_fuse_count'] += 1
            clamp['removable_before_quantize'] = clamp['quantized_to_fuse_count'] == len(clamp.out_port(0).get_destinations())


class ReluQuantizeFuse(MiddleReplacementPattern):
    __doc__ = ' Fuses ReLU --> FakeQuantize sequence if possible\n\n        Relu --> FakeQuantize fusion is possible if:\n            1. Relu is consumed to 0-th port of FakeQuantize\n            2. FakeQuantize ports 1 and 2 defines such input range that 0 is not included\n    '
    enabled = True

    def run_after(self):
        return [
         ReluFakeQuantizeMark]

    def run_before(self):
        import extensions.middle.SharedWeightsDuplication as SharedWeightsDuplication
        return [
         SharedWeightsDuplication]

    def pattern(self):
        return dict(nodes=[
         (
          'relu', dict(removable_before_quantize=True)),
         (
          'relu_d', dict()),
         (
          'quantize', dict(op='FakeQuantize', keep_in_IR=True))],
          edges=[
         ('relu', 'relu_d'),
         (
          'relu_d', 'quantize', {'in': 0})])

    def replace_pattern(self, graph: Graph, match: dict):
        quantize = match['quantize']
        if quantize.levels == 2:
            threshold = quantize.in_port(1).data.get_value()
            resolve_shared_inputs(node=quantize, port_ids_to_duplicate=[1])
            modification_mask = threshold < 0
            threshold[modification_mask] = float('-inf')
        in_relu_connection = quantize.in_port(0).get_source().node.in_port(0).get_connection()
        quantize.in_port(0).disconnect()
        in_relu_connection.add_destination(quantize.in_port(0))
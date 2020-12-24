# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/back/StridedSliceMasksNormalizer.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 1703 bytes
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
from extensions.back.ConvolutionNormalizer import DeconvolutionNormalizer
import extensions.back.CropToStridedSlice as CropToStridedSlice
from mo.back.replacement import BackReplacementPattern
from mo.front.common.partial_infer.utils import int64_array
from mo.graph.graph import Graph, Node

class StridedSliceMasksNormalizer(BackReplacementPattern):
    enabled = True
    force_clean_up = True
    graph_condition = [
     lambda graph: graph.graph['cmd_params'].generate_experimental_IR_V10]

    def run_after(self):
        return [
         CropToStridedSlice, DeconvolutionNormalizer]

    @staticmethod
    def pattern():
        return dict(nodes=[
         (
          'strided_slice', dict(type='StridedSlice'))],
          edges=[])

    def replace_pattern(self, graph: Graph, match: [str, Node]):
        node = match['strided_slice']
        assert node.has_valid('begin_mask')
        assert node.has_valid('end_mask')
        node.begin_mask = int64_array([1 - i for i in node.begin_mask])
        node.end_mask = int64_array([1 - i for i in node.end_mask])
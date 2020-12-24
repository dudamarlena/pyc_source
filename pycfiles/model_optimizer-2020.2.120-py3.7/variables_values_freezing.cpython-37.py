# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/tf/variables_values_freezing.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 1337 bytes
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
from mo.front.common.replacement import FrontReplacementPattern
from mo.front.tf.loader import variables_to_constants
from mo.graph.graph import Graph

class VariablesToConstants(FrontReplacementPattern):
    enabled = True
    force_clean_up = True
    graph_condition = [lambda graph: graph.graph['variables_values']]

    def run_after(self):
        from extensions.front.input_cut import InputCut
        return [
         InputCut]

    def run_before(self):
        from extensions.front.freeze_placeholder_value import FreezePlaceholderValue
        return [
         FreezePlaceholderValue]

    def find_and_replace_pattern(self, graph: Graph):
        variables_to_constants(graph, graph.graph['variables_values'])
        del graph.graph['variables_values']
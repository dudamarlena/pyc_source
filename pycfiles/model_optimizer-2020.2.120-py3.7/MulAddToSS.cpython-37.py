# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/middle/MulAddToSS.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 1764 bytes
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
import extensions.middle.EltwiseChecker as EltwiseChecker
from extensions.middle.LeakyReluPattern import LeakyReLU
from extensions.middle.pass_separator import PostMiddleStart
from mo.graph.graph import Graph
from mo.middle.passes.conv import convert_muladd_to_scaleshift, convert_add_or_mul_to_scaleshift
from mo.middle.pattern_match import for_graph_and_each_sub_graph_recursively
from mo.middle.replacement import MiddleReplacementPattern

class MulAddToSS(MiddleReplacementPattern):
    enabled = True
    run_not_recursively = True

    def run_after(self):
        return [
         LeakyReLU]

    def run_before(self):
        return [
         PostMiddleStart]

    def find_and_replace_pattern(self, graph: Graph):
        for_graph_and_each_sub_graph_recursively(graph, lambda G: G.clean_up())
        EltwiseChecker().find_and_replace_pattern(graph)
        convert_muladd_to_scaleshift(graph)
        graph.clean_up()
        convert_add_or_mul_to_scaleshift(graph)
        graph.clean_up()
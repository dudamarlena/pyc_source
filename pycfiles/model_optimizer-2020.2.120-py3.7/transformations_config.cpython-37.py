# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/transformations_config.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 2054 bytes
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
from mo.front.common.custom_replacement_registry import CustomReplacementRegistry
from mo.front.common.replacement import FrontReplacementPattern
from mo.front.tf.replacement import FrontReplacementFromConfigFileOp
from mo.graph.graph import Graph

class TransformationsConfig(FrontReplacementPattern):
    enabled = True
    graph_condition = [lambda graph: graph.graph['cmd_params'].transformations_config is not None]

    def run_before(self):
        from extensions.front.pass_separator import FrontStart
        return [
         FrontStart]

    def run_after(self):
        from extensions.load.loader import LoadFinish
        return [
         LoadFinish]

    def find_and_replace_pattern(self, graph: Graph):
        argv = graph.graph['cmd_params']
        transformations_config = argv.transformations_config
        registry = CustomReplacementRegistry()
        registry.add_custom_replacement_description_from_config(transformations_config)
        for replacement_desc in registry.get_all_replacements_descriptions():
            if replacement_desc.has('op'):
                transform = type('FrontReplacementFromConfigFileOp' + replacement_desc.op, (
                 FrontReplacementFromConfigFileOp,), {'replacement_id': replacement_desc.id})
                transform().find_and_replace_pattern(graph)
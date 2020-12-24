# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/back/ForceStrictPrecision.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 1907 bytes
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
import extensions.ops.Cast as Cast
from mo.back.replacement import BackReplacementPattern
from mo.graph.graph import Graph
from mo.middle.passes.convert_data_type import data_type_str_to_np

class ForceStrictPrecision(BackReplacementPattern):
    __doc__ = "\n    Assign precision for some inputs for specific layers depending on their semantics.\n\n    To identify ports which should be processed, this pass relies on special attributes\n    inside a node: force_precision_in_ports. This attribute should be a dictionary with\n    index of port as key and required precision code as value (e.g. 'int64' etc.).\n    "
    enabled = True

    @staticmethod
    def pattern():
        return dict(nodes=[
         (
          'node', {'force_precision_in_ports': lambda x: x is not None})],
          edges=[])

    @staticmethod
    def replace_pattern(graph: Graph, match: dict):
        node = match['node']
        for in_port, precision in node.force_precision_in_ports.items():
            if in_port in node.in_ports().keys():
                cast = node.in_port(in_port).disconnected() or Cast(graph, {'name':node.name + '/Cast_' + str(in_port),  'dst_type':data_type_str_to_np(precision)}).create_node()
                node.in_port(in_port).get_connection().insert_node(cast)
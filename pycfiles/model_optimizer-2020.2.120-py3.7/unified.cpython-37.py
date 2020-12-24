# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/pipeline/unified.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 1135 bytes
"""
 Copyright (C) 2020 Intel Corporation

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
import argparse
from mo.graph.graph import Graph
from mo.pipeline.common import get_ir_version
from mo.utils import class_registration

def unified_pipeline(argv: argparse.Namespace):
    graph = Graph(cmd_params=argv, name=(argv.model_name), ir_version=(get_ir_version(argv)))
    class_registration.apply_replacements(graph, [
     class_registration.ClassType.LOADER,
     class_registration.ClassType.FRONT_REPLACER,
     class_registration.ClassType.MIDDLE_REPLACER,
     class_registration.ClassType.BACK_REPLACER])
    return graph
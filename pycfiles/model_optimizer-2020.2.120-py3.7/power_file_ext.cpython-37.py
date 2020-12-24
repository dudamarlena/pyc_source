# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/caffe/power_file_ext.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 1126 bytes
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
from extensions.ops.power_file import PowerFileOp
import mo.front.caffe.collect_attributes as collect_attributes
from mo.front.extractor import FrontExtractorOp

class PowerFileFrontExtractor(FrontExtractorOp):
    op = 'PowerFile'
    enabled = True

    @classmethod
    def extract(cls, node):
        proto_layer = node.pb
        param = proto_layer.power_file_param
        attrs = collect_attributes(param)
        PowerFileOp.update_node_stat(node, attrs)
        return cls.enabled
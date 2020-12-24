# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/tf/placeholder_ext.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 1266 bytes
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
from extensions.ops.parameter import Parameter
from mo.front.extractor import FrontExtractorOp
from mo.front.tf.extractors.utils import tf_dtype_extractor, tf_tensor_shape
from mo.ops.op import PermuteAttrs

class PlaceholderFrontExtractor(FrontExtractorOp):
    op = 'Placeholder'
    enabled = True

    @classmethod
    def extract(cls, node):
        attrs = {'data_type':tf_dtype_extractor(node.pb.attr['dtype'].type), 
         'shape':tf_tensor_shape(node.pb.attr['shape'].shape), 
         'permute_attrs':PermuteAttrs().update_attrs(attrs=[('shape', 'output:0')])}
        Parameter.update_node_stat(node, attrs)
        return cls.enabled
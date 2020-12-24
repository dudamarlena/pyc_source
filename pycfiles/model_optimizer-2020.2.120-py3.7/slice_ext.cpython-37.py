# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/front/kaldi/extractors/slice_ext.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 1437 bytes
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
from mo.front.common.partial_infer.slice import caffe_slice_infer
from mo.front.extractor import FrontExtractorOp
from mo.front.kaldi.loader.utils import read_binary_integer32_token, read_blob
from mo.ops.slice import Slice

class SliceFrontExtractor(FrontExtractorOp):
    op = 'slice'
    enabled = True

    @classmethod
    def extract(cls, node):
        pb = node.parameters
        num_slice_points = read_binary_integer32_token(pb)
        mapping_rule = {'axis':1, 
         'slice_point':read_blob(pb, num_slice_points, np.int32), 
         'batch_dims':0, 
         'spatial_dims':1, 
         'out_ports_count':num_slice_points + 1, 
         'infer':caffe_slice_infer}
        node.parameters.close()
        Slice.update_node_stat(node, mapping_rule)
        return cls.enabled
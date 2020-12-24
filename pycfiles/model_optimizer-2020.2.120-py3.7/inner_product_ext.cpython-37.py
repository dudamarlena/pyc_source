# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/caffe/inner_product_ext.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 1727 bytes
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
from extensions.ops.MatMul import FullyConnected
from mo.front.caffe.extractors.utils import weights_biases
from mo.front.extractor import FrontExtractorOp

class InnerProductFrontExtractor(FrontExtractorOp):
    op = 'innerproduct'
    enabled = True

    @classmethod
    def extract(cls, node):
        param = node.pb.inner_product_param
        pb_model = node.model_pb
        attrs = {'out-size':param.num_output, 
         'transpose_weights':not param.transpose}
        attrs.update(weights_biases(param.bias_term, pb_model))
        FullyConnected.update_node_stat(node, attrs)
        return cls.enabled


class AnotherInnerProductFrontExtractor(FrontExtractorOp):
    op = 'inner_product'
    enabled = True

    @classmethod
    def extract(cls, node):
        param = node.pb.inner_product_param
        pb_model = node.model_pb
        attrs = {'out-size':param.num_output, 
         'transpose_weights':not param.transpose}
        attrs.update(weights_biases(param.bias_term, pb_model))
        FullyConnected.update_node_stat(node, attrs)
        return cls.enabled
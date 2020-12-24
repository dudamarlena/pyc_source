# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/caffe/binary_conv_ext.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 2105 bytes
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
from extensions.front.caffe.conv_ext import conv_create_attrs, conv_set_params
from mo.front.caffe.extractors.utils import weights_biases
from mo.front.common.extractors.utils import layout_attrs
from mo.front.extractor import FrontExtractorOp
from mo.ops.convolution import Convolution
from mo.utils.error import Error

class ConvFrontExtractor(FrontExtractorOp):
    op = 'ConvolutionBinary'
    enabled = True

    @classmethod
    def extract(cls, node):
        proto_layer, model_layer = node.pb, node.model_pb
        if not proto_layer:
            raise Error('Protobuf layer can not be empty')
        conv_param = proto_layer.convolution_param
        conv_type = 'ConvND' if len(proto_layer.bottom) > 1 else 'Conv2D'
        params = conv_set_params(conv_param, conv_type)
        attrs = conv_create_attrs(params)
        attrs.update({'op':__class__.op,  'get_group':lambda node: node.group, 
         'get_output_feature_dim':lambda node: node.output, 
         'weights_index':1 if conv_type == 'Conv2D' else 2})
        attrs.update(weights_biases((conv_param.bias_term), model_layer, start_index=(len(proto_layer.bottom)), proto=conv_param))
        attrs.update(layout_attrs())
        Convolution.update_node_stat(node, attrs)
        return cls.enabled
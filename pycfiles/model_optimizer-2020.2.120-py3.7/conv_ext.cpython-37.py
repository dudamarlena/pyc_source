# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/tf/conv_ext.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 4472 bytes
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
from mo.front.common.partial_infer.utils import convert_tf_padding_to_str, int64_array
from mo.front.extractor import FrontExtractorOp
from mo.front.tf.extractors.utils import tf_data_format_spatial, tf_data_format_channel, tf_data_format_batch, tf_int_list
from mo.ops.convolution import Convolution
from mo.ops.op import PermuteAttrs

class Conv2DFrontExtractor(FrontExtractorOp):
    op = 'Conv2D'
    enabled = True

    @classmethod
    def extract(cls, node):
        attrs = tf_create_attrs(node, 2, 3)
        attrs.update({'op':__class__.op,  'get_group':lambda node: 1, 
         'get_output_feature_dim':lambda node: node.kernel_shape[node.output_feature_channel], 
         'get_weights_permute':PermuteAttrs.Permutation(perm=int64_array([3, 2, 0, 1]), inv=int64_array([2, 3, 1, 0]))})
        Convolution.update_node_stat(node, attrs)
        return cls.enabled


class DepthwiseConv2dNativeFrontExtractor(FrontExtractorOp):
    op = 'DepthwiseConv2dNative'
    enabled = True

    @classmethod
    def extract(cls, node):
        attrs = tf_create_attrs(node, 2, 2)
        attrs.update({'op':__class__.op,  'kernel_spatial_idx':np.array([0, 1], dtype=np.int64), 
         'get_group':lambda node: node.kernel_shape[node.output_feature_channel], 
         'get_output_feature_dim':lambda node: node.kernel_shape[(-1)] * node.kernel_shape[(-2)], 
         'get_weights_permute':PermuteAttrs.Permutation(perm=int64_array([2, 3, 0, 1]), inv=int64_array([2, 3, 0, 1]))})
        Convolution.update_node_stat(node, attrs)
        return cls.enabled


class Conv3DFrontExtractor(FrontExtractorOp):
    op = 'Conv3D'
    enabled = True

    @classmethod
    def extract(cls, node):
        attrs = tf_create_attrs(node, 3, 4)
        attrs.update({'op':__class__.op,  'get_group':lambda node: 1, 
         'get_output_feature_dim':lambda node: node.kernel_shape[node.output_feature_channel], 
         'get_weights_permute':PermuteAttrs.Permutation(perm=int64_array([4, 3, 0, 1, 2]), inv=int64_array([2, 3, 4, 1, 0]))})
        Convolution.update_node_stat(node, attrs)
        return cls.enabled


def tf_create_attrs(node, input_feature_channel, output_feature_channel):
    data_format = node.pb.attr['data_format']
    dilations = tf_int_list(node.pb.attr['dilations'].list)
    if len(dilations) == 0:
        dilations = None
    attrs = {'type':'Convolution', 
     'auto_pad':convert_tf_padding_to_str(node.pb.attr['padding']), 
     'bias_addable':True, 
     'bias_term':False, 
     'dilation':dilations, 
     'stride':tf_int_list(node.pb.attr['strides'].list), 
     'channel_dims':tf_data_format_channel(data_format), 
     'batch_dims':tf_data_format_batch(data_format), 
     'input_feature_channel':input_feature_channel, 
     'output_feature_channel':output_feature_channel, 
     'layout':data_format.s.decode(), 
     'get_group':None, 
     'get_output_feature_dim':None}
    return attrs
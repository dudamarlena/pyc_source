# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/tf/deconv_ext.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 3336 bytes
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
from mo.ops.deconvolution import Deconvolution
from mo.ops.op import PermuteAttrs

class Conv2DBackpropInputFrontExtractor(FrontExtractorOp):
    op = 'Conv2DBackpropInput'
    enabled = True

    @classmethod
    def extract(cls, node):
        attrs = tf_create_attrs(node, 3, 2)
        attrs.update({'op':cls.op,  'get_weights_permute':PermuteAttrs.Permutation(perm=int64_array([3, 2, 0, 1]), inv=int64_array([2, 3, 1, 0])), 
         'swap_0_and_2_inputs':True, 
         'shape_input':True})
        Deconvolution.update_node_stat(node, attrs)
        return cls.enabled


class Conv3DBackpropInputV2InputFrontExtractor(FrontExtractorOp):
    op = 'Conv3DBackpropInputV2'
    enabled = True

    @classmethod
    def extract(cls, node):
        attrs = tf_create_attrs(node, 4, 3)
        attrs.update({'op':cls.op,  'get_weights_permute':PermuteAttrs.Permutation(perm=int64_array([4, 3, 0, 1, 2]), inv=int64_array([2, 3, 4, 1, 0])), 
         'swap_0_and_2_inputs':True, 
         'shape_input':True})
        Deconvolution.update_node_stat(node, attrs)
        return cls.enabled


def tf_create_attrs(node, input_feature_channel, output_feature_channel):
    data_format = node.pb.attr['data_format']
    return {'auto_pad':convert_tf_padding_to_str(node.pb.attr['padding']), 
     'bias_addable':True, 
     'bias_term':False, 
     'spatial_dims':tf_data_format_spatial(data_format), 
     'channel_dims':tf_data_format_channel(data_format), 
     'batch_dims':tf_data_format_batch(data_format), 
     'pad':None, 
     'pad_spatial_shape':None, 
     'output_spatial_shape':None, 
     'output_shape':None, 
     'output':None, 
     'stride':tf_int_list(node.pb.attr['strides'].list), 
     'type':None, 
     'group':None, 
     'layout':data_format.s.decode(), 
     'input_feature_channel':input_feature_channel, 
     'output_feature_channel':output_feature_channel}
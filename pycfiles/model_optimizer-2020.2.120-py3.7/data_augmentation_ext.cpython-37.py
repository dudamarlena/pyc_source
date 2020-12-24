# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/caffe/data_augmentation_ext.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 2282 bytes
"""
 Copyright (C) 2017-2020 Intel Corporation

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
from extensions.ops.data_augmentation import DataAugmentationOp
from mo.front.caffe.collect_attributes import merge_attrs
from mo.front.caffe.extractors.utils import embed_input
from mo.front.extractor import FrontExtractorOp

class DataAugmentationFrontExtractor(FrontExtractorOp):
    op = 'DataAugmentation'
    enabled = True

    @classmethod
    def extract(cls, node):
        proto_layer = node.pb
        param = proto_layer.augmentation_param
        update_attrs = {'crop_width':param.crop_width, 
         'crop_height':param.crop_height, 
         'write_augmented':param.write_augmented, 
         'max_multiplier':param.max_multiplier, 
         'augment_during_test':int(param.augment_during_test), 
         'recompute_mean':param.recompute_mean, 
         'write_mean':param.write_mean, 
         'mean_per_pixel':int(param.mean_per_pixel), 
         'mean':param.mean, 
         'mode':param.mode, 
         'bottomwidth':param.bottomwidth, 
         'bottomheight':param.bottomheight, 
         'num':param.num, 
         'chromatic_eigvec':param.chromatic_eigvec}
        mapping_rule = merge_attrs(param, update_attrs)
        if node.model_pb:
            for index in range(0, len(node.model_pb.blobs)):
                embed_input(mapping_rule, index + 1, 'custom_{}'.format(index), node.model_pb.blobs[index].data)

        DataAugmentationOp.update_node_stat(node, mapping_rule)
        return cls.enabled
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/mxnet/softmax_activation_ext.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 1258 bytes
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
from mo.front.mxnet.extractors.utils import get_mxnet_layer_attrs
from mo.front.extractor import FrontExtractorOp
from mo.ops.softmax import Softmax

class SoftmaxActivationExtractor(FrontExtractorOp):
    op = 'SoftmaxActivation'
    enabled = True

    @classmethod
    def extract(cls, node):
        attr = get_mxnet_layer_attrs(node.symbol_dict)
        mode = attr.str('mode', 'instance')
        if mode == 'channel':
            axis = 1
        else:
            axis = -1
        update_attrs = {'axis': axis}
        Softmax.update_node_stat(node, update_attrs)
        return cls.enabled
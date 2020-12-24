# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/front/common/partial_infer/multi_box_detection.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 2555 bytes
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
import logging as log, numpy as np
from mo.graph.graph import Node

def multi_box_detection_infer(node: Node):
    loc_shape = node.in_node(0).shape
    conf_shape = node.in_node(1).shape
    prior_boxes_shape = node.in_node(2).shape
    if loc_shape is None or conf_shape is None or prior_boxes_shape is None:
        log.warning('Shapes for the Detection Output are not defined')
        return
    prior_size = 4
    if node.has('normalized'):
        if not node.normalized:
            prior_size = 5
    if prior_boxes_shape[(-1)] % prior_size != 0:
        log.warning('Amount of confidences "{}" is not divisible by {}'.format(conf_shape[(-1)], prior_size))
        return
    num_priors = prior_boxes_shape[(-1)] // prior_size
    if not node.has_valid('keep_top_k') or node.keep_top_k == -1:
        node['keep_top_k'] = num_priors
    node.graph.node[node.id]['num_classes'] = conf_shape[(-1)] // num_priors
    num_loc_classes = node.num_classes
    if node.has_and_set('share_location'):
        if node.share_location:
            num_loc_classes = 1
    if num_priors * num_loc_classes * 4 != loc_shape[(-1)]:
        log.warning('Locations and prior boxes shapes mismatch: "{}" vs "{}"'.format(loc_shape, prior_boxes_shape))
        return
    if not node.variance_encoded_in_target:
        if prior_boxes_shape[(-2)] != 2:
            log.warning('The "-2" dimension of the prior boxes must be 2 but it is "{}".'.format(prior_boxes_shape[(-2)]))
            return
    if conf_shape[(-1)] % num_priors != 0:
        log.warning('Amount of confidences "{}" is not divisible by amount of priors "{}".'.format(conf_shape[(-1)], num_priors))
        return
    log.debug('Inferred amount of classes "{}"'.format(node.num_classes))
    node.out_node(0).shape = np.array([1, 1, conf_shape[0] * node.keep_top_k, 7], dtype=(np.int64))
    node.graph.node[node.out_node(0).id]['nchw_layout'] = True
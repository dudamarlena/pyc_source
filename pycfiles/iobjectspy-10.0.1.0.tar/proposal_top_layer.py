# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\faster_rcnn\layer_utils\proposal_top_layer.py
# Compiled at: 2019-12-31 04:09:02
# Size of source mod 2**32: 3128 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import numpy.random as npr
import tensorflow as tf
from model.bbox_transform import bbox_transform_inv, clip_boxes, bbox_transform_inv_tf, clip_boxes_tf
from model.config import cfg

def proposal_top_layer(rpn_cls_prob, rpn_bbox_pred, im_info, _feat_stride, anchors, num_anchors):
    """A layer that just selects the top region proposals
       without using non-maximal suppression,
       For details please see the technical report
    """
    rpn_top_n = cfg.TEST.RPN_TOP_N
    scores = rpn_cls_prob[:, :, :, num_anchors:]
    rpn_bbox_pred = rpn_bbox_pred.reshape((-1, 4))
    scores = scores.reshape((-1, 1))
    length = scores.shape[0]
    if length < rpn_top_n:
        top_inds = npr.choice(length, size=rpn_top_n, replace=True)
    else:
        top_inds = scores.argsort(0)[::-1]
        top_inds = top_inds[:rpn_top_n]
        top_inds = top_inds.reshape(rpn_top_n)
    anchors = anchors[top_inds, :]
    rpn_bbox_pred = rpn_bbox_pred[top_inds, :]
    scores = scores[top_inds]
    proposals = bbox_transform_inv(anchors, rpn_bbox_pred)
    proposals = clip_boxes(proposals, im_info[:2])
    batch_inds = np.zeros((proposals.shape[0], 1), dtype=(np.float32))
    blob = np.hstack((batch_inds, proposals.astype((np.float32), copy=False)))
    return (blob, scores)


def proposal_top_layer_tf(rpn_cls_prob, rpn_bbox_pred, im_info, _feat_stride, anchors, num_anchors):
    """A layer that just selects the top region proposals
       without using non-maximal suppression,
       For details please see the technical report
    """
    rpn_top_n = cfg.TEST.RPN_TOP_N
    scores = rpn_cls_prob[:, :, :, num_anchors:]
    rpn_bbox_pred = tf.reshape(rpn_bbox_pred, shape=(-1, 4))
    scores = tf.reshape(scores, shape=(-1, ))
    top_scores, top_inds = tf.nn.top_k(scores, k=rpn_top_n)
    top_scores = tf.reshape(top_scores, shape=(-1, 1))
    top_anchors = tf.gather(anchors, top_inds)
    top_rpn_bbox = tf.gather(rpn_bbox_pred, top_inds)
    proposals = bbox_transform_inv_tf(top_anchors, top_rpn_bbox)
    proposals = clip_boxes_tf(proposals, im_info[:2])
    proposals = tf.to_float(proposals)
    batch_inds = tf.zeros((rpn_top_n, 1))
    blob = tf.concat([batch_inds, proposals], 1)
    return (blob, top_scores)
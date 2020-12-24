# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\faster_rcnn\layer_utils\snippets.py
# Compiled at: 2019-12-31 04:09:02
# Size of source mod 2**32: 2257 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np, tensorflow as tf
import layer_utils.generate_anchors as generate_anchors

def generate_anchors_pre(height, width, feat_stride, anchor_scales=(8, 16, 32), anchor_ratios=(0.5, 1, 2)):
    """ A wrapper function to generate anchors given different scales
      Also return the number of anchors in variable 'length'
    """
    anchors = generate_anchors(ratios=(np.array(anchor_ratios)), scales=(np.array(anchor_scales)))
    A = anchors.shape[0]
    shift_x = np.arange(0, width) * feat_stride
    shift_y = np.arange(0, height) * feat_stride
    shift_x, shift_y = np.meshgrid(shift_x, shift_y)
    shifts = np.vstack((shift_x.ravel(), shift_y.ravel(), shift_x.ravel(), shift_y.ravel())).transpose()
    K = shifts.shape[0]
    anchors = anchors.reshape((1, A, 4)) + shifts.reshape((1, K, 4)).transpose((1,
                                                                                0,
                                                                                2))
    anchors = anchors.reshape((K * A, 4)).astype((np.float32), copy=False)
    length = np.int32(anchors.shape[0])
    return (
     anchors, length)


def generate_anchors_pre_tf(height, width, feat_stride=16, anchor_scales=(8, 16, 32), anchor_ratios=(0.5, 1, 2)):
    shift_x = tf.range(width) * feat_stride
    shift_y = tf.range(height) * feat_stride
    shift_x, shift_y = tf.meshgrid(shift_x, shift_y)
    sx = tf.reshape(shift_x, shape=(-1, ))
    sy = tf.reshape(shift_y, shape=(-1, ))
    shifts = tf.transpose(tf.stack([sx, sy, sx, sy]))
    K = tf.multiply(width, height)
    shifts = tf.transpose(tf.reshape(shifts, shape=[1, K, 4]), perm=(1, 0, 2))
    anchors = generate_anchors(ratios=(np.array(anchor_ratios)), scales=(np.array(anchor_scales)))
    A = anchors.shape[0]
    anchor_constant = tf.constant((anchors.reshape((1, A, 4))), dtype=(tf.int32))
    length = K * A
    anchors_tf = tf.reshape((tf.add(anchor_constant, shifts)), shape=(length, 4))
    return (
     tf.cast(anchors_tf, dtype=(tf.float32)), length)
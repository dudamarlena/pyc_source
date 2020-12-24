# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/model/retinanet/losses.py
# Compiled at: 2020-04-22 04:57:25
# Size of source mod 2**32: 3730 bytes
import tensorflow as tf
import tensorflow.keras as K

def focal(alpha=0.25, gamma=2.0):
    """ Create a functor for computing the focal loss.

    Args
        alpha: Scale the focal weight with alpha.
        gamma: Take the power of the focal weight with gamma.

    Returns
        A functor that computes the focal loss using the alpha and gamma.
    """

    def _focal(y_true, y_pred):
        labels = y_true[:, :, :-1]
        anchor_state = y_true[:, :, -1]
        classification = y_pred
        indices = tf.where(K.not_equal(anchor_state, -1))
        labels = tf.gather_nd(labels, indices)
        classification = tf.gather_nd(classification, indices)
        alpha_factor = K.ones_like(labels) * alpha
        alpha_factor = tf.where(K.equal(labels, 1), alpha_factor, 1 - alpha_factor)
        focal_weight = tf.where(K.equal(labels, 1), 1 - classification, classification)
        focal_weight = alpha_factor * focal_weight ** gamma
        cls_loss = focal_weight * K.binary_crossentropy(labels, classification)
        normalizer = tf.where(K.equal(anchor_state, 1))
        normalizer = K.cast(K.shape(normalizer)[0], K.floatx())
        normalizer = K.maximum(K.cast_to_floatx(1.0), normalizer)
        return K.sum(cls_loss) / normalizer

    return _focal


def smooth_l1(sigma=3.0):
    """ Create a smooth L1 loss functor.

    Args
        sigma: This argument defines the point where the loss changes from L2 to L1.

    Returns
        A functor for computing the smooth L1 loss given target data and predicted data.
    """
    sigma_squared = sigma ** 2

    def _smooth_l1(y_true, y_pred):
        regression = y_pred
        regression_target = y_true[:, :, :-1]
        anchor_state = y_true[:, :, -1]
        indices = tf.where(K.equal(anchor_state, 1))
        regression = tf.gather_nd(regression, indices)
        regression_target = tf.gather_nd(regression_target, indices)
        regression_diff = regression - regression_target
        regression_diff = K.abs(regression_diff)
        regression_loss = tf.where(K.less(regression_diff, 1.0 / sigma_squared), 0.5 * sigma_squared * K.pow(regression_diff, 2), regression_diff - 0.5 / sigma_squared)
        normalizer = K.maximum(1, K.shape(indices)[0])
        normalizer = K.cast(normalizer, dtype=(K.floatx()))
        return K.sum(regression_loss) / normalizer

    return _smooth_l1
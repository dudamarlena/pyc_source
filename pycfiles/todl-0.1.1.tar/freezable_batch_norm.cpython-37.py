# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/core/freezable_batch_norm.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 2982 bytes
"""A freezable batch norm layer that uses Keras batch normalization."""
import tensorflow as tf

class FreezableBatchNorm(tf.keras.layers.BatchNormalization):
    __doc__ = 'Batch normalization layer (Ioffe and Szegedy, 2014).\n\n  This is a `freezable` batch norm layer that supports setting the `training`\n  parameter in the __init__ method rather than having to set it either via\n  the Keras learning phase or via the `call` method parameter. This layer will\n  forward all other parameters to the default Keras `BatchNormalization`\n  layer\n\n  This is class is necessary because Object Detection model training sometimes\n  requires batch normalization layers to be `frozen` and used as if it was\n  evaluation time, despite still training (and potentially using dropout layers)\n\n  Like the default Keras BatchNormalization layer, this will normalize the\n  activations of the previous layer at each batch,\n  i.e. applies a transformation that maintains the mean activation\n  close to 0 and the activation standard deviation close to 1.\n\n  Arguments:\n    training: If False, the layer will normalize using the moving average and\n      std. dev, without updating the learned avg and std. dev.\n      If None or True, the layer will follow the keras BatchNormalization layer\n      strategy of checking the Keras learning phase at `call` time to decide\n      what to do.\n    **kwargs: The keyword arguments to forward to the keras BatchNormalization\n        layer constructor.\n\n  Input shape:\n      Arbitrary. Use the keyword argument `input_shape`\n      (tuple of integers, does not include the samples axis)\n      when using this layer as the first layer in a model.\n\n  Output shape:\n      Same shape as input.\n\n  References:\n      - [Batch Normalization: Accelerating Deep Network Training by Reducing\n        Internal Covariate Shift](https://arxiv.org/abs/1502.03167)\n  '

    def __init__(self, training=None, **kwargs):
        (super(FreezableBatchNorm, self).__init__)(**kwargs)
        self._training = training

    def call(self, inputs, training=None):
        if self._training is False:
            training = self._training
        return super(FreezableBatchNorm, self).call(inputs, training=training)
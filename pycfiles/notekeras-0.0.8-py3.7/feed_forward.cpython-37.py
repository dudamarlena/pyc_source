# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/layer/feed_forward.py
# Compiled at: 2019-12-29 21:52:46
# Size of source mod 2**32: 5703 bytes
import notekeras.backend as K
from notekeras.backend import keras, layers

class FeedForward(layers.Layer):
    __doc__ = 'Position-wise feed-forward layer.\n\n    # Arguments\n        units: int >= 0. Dimension of hidden units.\n        activation: Activation function to use\n        use_bias: Boolean, whether the layer uses a bias vector.\n        kernel_initializer: Initializer for the `kernel` weights matrix.\n        bias_initializer: Initializer for the bias vector.\n        kernel_regularizer: Regularizer function applied to the `kernel` weights matrix.\n        bias_regularizer: Regularizer function applied to the bias vector.\n        kernel_constraint: Constraint function applied to the `kernel` weights matrix.\n        bias_constraint: Constraint function applied to the bias vector.\n        dropout_rate: 0.0 <= float <= 1.0. Dropout rate for hidden units.\n\n    # Input shape\n        3D tensor with shape: `(batch_size, ..., input_dim)`.\n\n    # Output shape\n        3D tensor with shape: `(batch_size, ..., input_dim)`.\n\n    # References\n        - [Attention is All You Need](https://arxiv.org/pdf/1706.03762.pdf)\n    '

    def __init__(self, units, activation='relu', use_bias=True, kernel_initializer='glorot_normal', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, kernel_constraint=None, bias_constraint=None, dropout_rate=0.0, **kwargs):
        self.supports_masking = True
        self.units = units
        self.activation = keras.activations.get(activation)
        self.use_bias = use_bias
        self.kernel_initializer = keras.initializers.get(kernel_initializer)
        self.bias_initializer = keras.initializers.get(bias_initializer)
        self.kernel_regularizer = keras.regularizers.get(kernel_regularizer)
        self.bias_regularizer = keras.regularizers.get(bias_regularizer)
        self.kernel_constraint = keras.constraints.get(kernel_constraint)
        self.bias_constraint = keras.constraints.get(bias_constraint)
        self.dropout_rate = dropout_rate
        self.W1, self.b1 = (None, None)
        self.W2, self.b2 = (None, None)
        (super(FeedForward, self).__init__)(**kwargs)

    def get_config(self):
        config = {'units':self.units, 
         'activation':keras.activations.serialize(self.activation), 
         'use_bias':self.use_bias, 
         'kernel_initializer':keras.initializers.serialize(self.kernel_initializer), 
         'bias_initializer':keras.initializers.serialize(self.bias_initializer), 
         'kernel_regularizer':keras.regularizers.serialize(self.kernel_regularizer), 
         'bias_regularizer':keras.regularizers.serialize(self.bias_regularizer), 
         'kernel_constraint':keras.constraints.serialize(self.kernel_constraint), 
         'bias_constraint':keras.constraints.serialize(self.bias_constraint), 
         'dropout_rate':self.dropout_rate}
        base_config = super(FeedForward, self).get_config()
        return dict(base_config, **config)

    def compute_output_shape(self, input_shape):
        return input_shape

    def compute_mask(self, inputs, input_mask=None):
        return input_mask

    def build(self, input_shape):
        feature_dim = int(input_shape[(-1)])
        self.W1 = self.add_weight(shape=(feature_dim, self.units), initializer=(self.kernel_initializer),
          regularizer=(self.kernel_regularizer),
          constraint=(self.kernel_constraint),
          name=('{}_W1'.format(self.name)))
        if self.use_bias:
            self.b1 = self.add_weight(shape=(self.units,), initializer=(self.bias_initializer),
              regularizer=(self.bias_regularizer),
              constraint=(self.bias_constraint),
              name=('{}_b1'.format(self.name)))
        self.W2 = self.add_weight(shape=(self.units, feature_dim), initializer=(self.kernel_initializer),
          regularizer=(self.kernel_regularizer),
          constraint=(self.kernel_constraint),
          name=('{}_W2'.format(self.name)))
        if self.use_bias:
            self.b2 = self.add_weight(shape=(feature_dim,), initializer=(self.bias_initializer),
              regularizer=(self.bias_regularizer),
              constraint=(self.bias_constraint),
              name=('{}_b2'.format(self.name)))
        super(FeedForward, self).build(input_shape)

    def call(self, x, mask=None, training=None):
        h = K.dot(x, self.W1)
        if self.use_bias:
            h = K.bias_add(h, self.b1)
        if self.activation is not None:
            h = self.activation(h)
        if 0.0 < self.dropout_rate < 1.0:

            def dropped_inputs():
                return K.dropout(h, self.dropout_rate, K.shape(h))

            h = K.in_train_phase(dropped_inputs, h, training=training)
        y = K.dot(h, self.W2)
        if self.use_bias:
            y = K.bias_add(y, self.b2)
        return y
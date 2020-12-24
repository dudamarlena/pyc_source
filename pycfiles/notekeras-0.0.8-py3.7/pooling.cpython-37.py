# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/layer/pooling.py
# Compiled at: 2019-12-29 21:53:42
# Size of source mod 2**32: 646 bytes
import notekeras.backend as K
from notekeras.backend import layers

class MaskedGlobalMaxPool1D(layers.Layer):

    def __init__(self, **kwargs):
        (super(MaskedGlobalMaxPool1D, self).__init__)(**kwargs)
        self.supports_masking = True

    def compute_mask(self, inputs, mask=None):
        pass

    def compute_output_shape(self, input_shape):
        return input_shape[:-2] + (input_shape[(-1)],)

    def call(self, inputs, mask=None):
        if mask is not None:
            mask = K.cast(mask, K.floatx())
            inputs -= K.expand_dims(((1.0 - mask) * 1000000.0), axis=(-1))
        return K.max(inputs, axis=(-2))
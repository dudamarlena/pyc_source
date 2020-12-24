# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/layer/conv.py
# Compiled at: 2019-11-22 04:12:13
# Size of source mod 2**32: 672 bytes
import notekeras.backend as K
from notekeras.backend import keras

class MaskedConv1D(keras.layers.Conv1D):

    def __init__(self, **kwargs):
        (super(MaskedConv1D, self).__init__)(**kwargs)
        self.supports_masking = True

    def compute_mask(self, inputs, mask=None):
        if mask is not None:
            if self.padding == 'valid':
                mask = mask[:, self.kernel_size[0] // 2 * self.dilation_rate[0] * 2:]
        return mask

    def call(self, inputs, mask=None):
        if mask is not None:
            mask = K.cast(mask, K.floatx())
            inputs *= K.expand_dims(mask, axis=(-1))
        return super(MaskedConv1D, self).call(inputs)
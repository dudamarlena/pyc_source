# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/layer/extract.py
# Compiled at: 2019-12-29 21:52:31
# Size of source mod 2**32: 776 bytes
from notekeras.backend import layers
__all__ = ['Extract']

class Extract(layers.Layer):
    __doc__ = 'Extract from index.\n\n    See: https://arxiv.org/pdf/1810.04805.pdf\n    '

    def __init__(self, index, **kwargs):
        (super(Extract, self).__init__)(**kwargs)
        self.index = index
        self.supports_masking = True

    def get_config(self):
        config = {'index': self.index}
        base_config = super(Extract, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

    def compute_output_shape(self, input_shape):
        return input_shape[:1] + input_shape[2:]

    def compute_mask(self, inputs, mask=None):
        pass

    def call(self, x, mask=None):
        return x[:, self.index]
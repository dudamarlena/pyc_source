# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_seg_models\unet\builder.py
# Compiled at: 2019-12-31 04:09:04
# Size of source mod 2**32: 1491 bytes
from keras.layers import Conv2D
from keras.layers import Activation
from keras.models import Model
from .blocks import Transpose2D_block
from .blocks import Upsample2D_block
from ..utils import get_layer_number, to_tuple

def build_unet(backbone, classes, skip_connection_layers, decoder_filters=(256, 128, 64, 32, 16), upsample_rates=(2, 2, 2, 2, 2), n_upsample_blocks=5, block_type='upsampling', activation='sigmoid', use_batchnorm=True):
    input = backbone.input
    x = backbone.output
    if block_type == 'transpose':
        up_block = Transpose2D_block
    else:
        up_block = Upsample2D_block
    skip_connection_idx = [get_layer_number(backbone, l) if isinstance(l, str) else l for l in skip_connection_layers]
    for i in range(n_upsample_blocks):
        skip_connection = None
        if i < len(skip_connection_idx):
            skip_connection = backbone.layers[skip_connection_idx[i]].output
        upsample_rate = to_tuple(upsample_rates[i])
        x = up_block((decoder_filters[i]), i, upsample_rate=upsample_rate, skip=skip_connection,
          use_batchnorm=use_batchnorm)(x)

    x = Conv2D(classes, (3, 3), padding='same', name='final_conv')(x)
    x = Activation(activation, name=activation)(x)
    model = Model(input, x)
    return model
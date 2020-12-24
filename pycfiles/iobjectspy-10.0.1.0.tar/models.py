# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_seg_models\backbones\cls_models\cls_models\resnext\models.py
# Compiled at: 2019-12-31 04:09:04
# Size of source mod 2**32: 1197 bytes
from .builder import build_resnext
from ..utils import load_model_weights
from ..weights import weights_collection

def ResNeXt50(input_shape, input_tensor=None, weights=None, classes=1000, include_top=True):
    model = build_resnext(input_tensor=input_tensor, input_shape=input_shape,
      first_block_filters=128,
      repetitions=(3, 4, 6, 3),
      classes=classes,
      include_top=include_top)
    model.name = 'resnext50'
    if weights:
        load_model_weights(weights_collection, model, weights, classes, include_top)
    return model


def ResNeXt101(input_shape, input_tensor=None, weights=None, classes=1000, include_top=True):
    model = build_resnext(input_tensor=input_tensor, input_shape=input_shape,
      first_block_filters=128,
      repetitions=(3, 4, 23, 3),
      classes=classes,
      include_top=include_top)
    model.name = 'resnext101'
    if weights:
        load_model_weights(weights_collection, model, weights, classes, include_top)
    return model
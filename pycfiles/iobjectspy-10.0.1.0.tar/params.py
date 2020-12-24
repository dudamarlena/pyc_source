# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_seg_models\backbones\cls_models\cls_models\resnext\params.py
# Compiled at: 2019-12-31 04:09:04
# Size of source mod 2**32: 614 bytes


def get_conv_params(**params):
    default_conv_params = {'kernel_initializer':'glorot_uniform', 
     'use_bias':False, 
     'padding':'valid'}
    default_conv_params.update(params)
    return default_conv_params


def get_bn_params(**params):
    default_bn_params = {'axis':3, 
     'momentum':0.99, 
     'epsilon':2e-05, 
     'center':True, 
     'scale':True}
    default_bn_params.update(params)
    return default_bn_params
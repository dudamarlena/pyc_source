# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/inference/inference.py
# Compiled at: 2020-02-12 04:52:06
# Size of source mod 2**32: 1303 bytes


class Inference:
    __doc__ = 'This class implements the functionality of any Inference class.\n    '

    def __init__(self):
        raise NotImplementedError

    def compile(self, pmodel, data_size, extra_loss_tensor=None):
        raise NotImplementedError

    def update(self, sample_dict):
        raise NotImplementedError

    def get_interceptable_condition_variables(self):
        return (None, None)

    def posterior(self, target_names=None, data={}):
        raise NotImplementedError

    def posterior_predictive(self, target_names=None, data={}):
        raise NotImplementedError
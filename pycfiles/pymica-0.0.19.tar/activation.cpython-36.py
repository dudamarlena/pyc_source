# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymic/layer/activation.py
# Compiled at: 2019-12-07 03:31:58
# Size of source mod 2**32: 2398 bytes
from __future__ import print_function, division
import torch, torch.nn as nn

def get_acti_func(acti_func, params):
    acti_func = acti_func.lower()
    if acti_func == 'relu':
        inplace = params.get('relu_inplace', False)
        return nn.ReLU(inplace)
    if acti_func == 'leakyrelu':
        slope = params.get('leakyrelu_negative_slope', 0.01)
        inplace = params.get('leakyrelu_inplace', False)
        return nn.LeakyReLU(slope, inplace)
    if acti_func == 'prelu':
        num_params = params.get('prelu_num_parameters', 1)
        init_value = params.get('prelu_init', 0.25)
        return nn.PReLU(num_params, init_value)
    if acti_func == 'rrelu':
        lower = params.get('rrelu_lower', 0.125)
        upper = params.get('rrelu_upper', 0.3333333333333333)
        inplace = params.get('rrelu_inplace', False)
        return nn.RReLU(lower, upper, inplace)
    if acti_func == 'elu':
        alpha = params.get('elu_alpha', 1.0)
        inplace = params.get('elu_inplace', False)
        return nn.ELU(alpha, inplace)
    if acti_func == 'celu':
        alpha = params.get('celu_alpha', 1.0)
        inplace = params.get('celu_inplace', False)
        return nn.CELU(alpha, inplace)
    if acti_func == 'selu':
        inplace = params.get('selu_inplace', False)
        return nn.SELU(inplace)
    if acti_func == 'glu':
        dim = params.get('glu_dim', -1)
        return nn.GLU(dim)
    if acti_func == 'sigmoid':
        return nn.Sigmoid()
    if acti_func == 'logsigmoid':
        return nn.LogSigmoid()
    if acti_func == 'tanh':
        return nn.Tanh()
    if acti_func == 'hardtanh':
        min_val = params.get('hardtanh_min_val', -1.0)
        max_val = params.get('hardtanh_max_val', 1.0)
        inplace = params.get('hardtanh_inplace', False)
        return nn.Hardtanh(min_val, max_val, inplace)
    if acti_func == 'softplus':
        beta = params.get('softplus_beta', 1.0)
        threshold = params.get('softplus_threshold', 20)
        return nn.Softplus(beta, threshold)
    if acti_func == 'softshrink':
        lambd = params.get('softshrink_lambda', 0.5)
        return nn.Softshrink(lambd)
    if acti_func == 'softsign':
        return nn.Softsign()
    raise ValueError('Not implemented: {0:}'.format(acti_func))
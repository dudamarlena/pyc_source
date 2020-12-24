# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pymic/train_infer/get_optimizer.py
# Compiled at: 2019-12-07 03:31:59
# Size of source mod 2**32: 1348 bytes
from __future__ import print_function, division
import torch, torch.optim as optim

def get_optimiser(name, net_params, optim_params):
    lr = optim_params['learning_rate']
    momentum = optim_params['momentum']
    weight_decay = optim_params['weight_decay']
    if name == 'SGD':
        return optim.SGD(net_params, lr, momentum=momentum,
          weight_decay=weight_decay)
    if name == 'Adam':
        return optim.Adam(net_params, lr, weight_decay=1e-05)
    if name == 'SparseAdam':
        return optim.SparseAdam(net_params, lr)
    if name == 'Adadelta':
        return optim.Adadelta(net_params, lr, weight_decay=weight_decay)
    if name == 'Adagrad':
        return optim.Adagrad(net_params, lr, weight_decay=weight_decay)
    if name == 'Adamax':
        return optim.Adamax(net_params, lr, weight_decay=weight_decay)
    if name == 'ASGD':
        return optim.ASGD(net_params, lr, weight_decay=weight_decay)
    if name == 'LBFGS':
        return optim.LBFGS(net_params, lr)
    if name == 'RMSprop':
        return optim.RMSprop(net_params, lr, momentum=momentum, weight_decay=weight_decay)
    if name == 'Rprop':
        return optim.Rprop(net_params, lr)
    raise ValueError('unsupported optimizer {0:}'.format(name))
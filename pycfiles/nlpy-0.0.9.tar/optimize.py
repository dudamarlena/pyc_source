# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/deep/trainers/optimize.py
# Compiled at: 2015-02-08 20:24:29
import theano, theano.tensor as T, numpy as np
from collections import OrderedDict
from nlpy.deep.functions import FLOATX
import inspect, logging as loggers
logging = loggers.getLogger(__name__)

def optimize_parameters(params, gparams, shapes=None, max_norm=5.0, lr=0.01, eps=1e-06, rho=0.95, method='ADADELTA', beta=0.0, gsum_regularization=0, weight_l2=0, clip=True, monitor_norm=False):
    """
    Optimize by SGD, AdaGrad, or AdaDelta.
    Returns the shared variables for the gradient caches,
    and the updates dictionary for compilation by a
    theano function.

    :param params: parameters to optimize
    :param gparams: gradients
    :param max_norm: cap on excess gradients
    :param lr: base learning rate for adagrad and SGD
    :param eps: numerical stability value to not divide by zero sometimes
    :param rho: adadelta hyperparameter
    :param method: 'ADAGRAD', 'ADADELTA', or 'SGD'

    :returns updates: the updates to pass to theano function
    :returns gsums: gradient caches for Adagrad and AdaDelta
    :returns xsums: gradient caches for AdaDelta only
    :returns lr: theano shared : learning rate
    :returns max_norm theano_shared : normalizing clipping value for excessive gradients (exploding)
    """
    _, _, _, args = inspect.getargvalues(inspect.currentframe())
    logging.info('optimize params: %s' % str(args.items()))
    if method == 'FINETUNING_ADAGRAD':
        method = 'ADAGRAD'
        gsum_regularization = 0
    if not shapes:
        shapes = params
    oneMinusBeta = 1 - beta
    gsums = [ theano.shared(np.zeros_like(param.get_value(borrow=True), dtype=FLOATX), name='gsum_%s' % param.name) if method == 'ADADELTA' or method == 'ADAGRAD' else None for param in shapes ]
    xsums = [ theano.shared(np.zeros_like(param.get_value(borrow=True), dtype=FLOATX), name='xsum_%s' % param.name) if method == 'ADADELTA' else None for param in shapes ]
    if method == 'ADAGRAD':
        for gsum in gsums:
            gsum.set_value(gsum.get_value() ** 0)

    updates = OrderedDict()
    for gparam, param, gsum, xsum in zip(gparams, params, gsums, xsums):
        if max_norm and clip:
            grad_norm = gparam.norm(L=2)
            gparam = T.minimum(T.constant(max_norm, dtype=FLOATX), grad_norm) / grad_norm * gparam
        if method == 'ADADELTA':
            if weight_l2 > 0:
                gparam += 2 * weight_l2 * param
            updates[gsum] = rho * gsum + (1.0 - rho) * gparam ** 2
            dparam = -T.sqrt((xsum + eps) / (updates[gsum] + eps)) * gparam
            updates[xsum] = rho * xsum + (1.0 - rho) * dparam ** 2
            updates[param] = param * oneMinusBeta + dparam
        elif method == 'ADAGRAD':
            updates[gsum] = gsum + gparam ** 2 - gsum_regularization * gsum
            updates[param] = param * oneMinusBeta - lr * (gparam / T.sqrt(updates[gsum] + eps) + 2 * weight_l2 * param)
        else:
            updates[param] = param * oneMinusBeta - (gparam + 2 * weight_l2 * param) * lr

    return updates.items()
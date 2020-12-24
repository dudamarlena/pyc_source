# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plasma/utils/evaluation.py
# Compiled at: 2017-02-17 21:50:27
import numpy as np

def get_loss_from_list(y_pred_list, y_gold_list, mode):
    return np.mean([ get_loss(yp, yg, mode) for yp, yg in zip(y_pred_list, y_gold_list) ])


def get_loss(y_pred, y_gold, mode):
    if mode == 'mae':
        return np.mean(np.abs(y_pred - y_gold))
    if mode == 'binary_crossentropy':
        return np.mean(-(y_gold * np.log(y_pred) + (1 - y_gold) * np.log(1 - y_pred)))
    if mode == 'mse':
        return np.mean((y_pred - y_gold) ** 2)
    if mode == 'hinge':
        return np.mean(np.maximum(0.0, 1 - y_pred * y_gold))
    if mode == 'squared_hinge':
        return np.mean(np.maximum(0.0, 1 - y_pred * y_gold) ** 2)
    print 'mode not recognized'
    exit(1)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataprovider/label_transform.py
# Compiled at: 2016-11-29 20:56:28
"""

Label transform functions.

Kisuk Lee <kisuklee@mit.edu>, 2015-2016
"""
import numpy as np, transform, utils

class LabelFunction(object):
    """
    Transform label.
    """

    def evaluate(self, sample, key, spec):
        if spec is not None:
            d = dict(spec)
            func = d['type']
            del d['type']
            f = globals()[func]
            f(sample, key, **d)
        return


label_func = LabelFunction()

def binarize(sample, key, rebalancing=True):
    """Binarize label."""
    sample[key] = transform.binarize(sample[key])
    if rebalancing:
        wmsk = transform.rebalance_class(sample[key])
        sample[(key + '_mask')] *= wmsk


def binary_class(sample, key, rebalancing=True):
    binarize(sample, key, False)
    multiclass_expansion(sample, key, [0, 1], rebalancing)


def affinitize(sample, key, rebalancing=True):
    """Transfrom segmentation to 3D affinity graph."""
    affs = transform.affinitize(sample[key])
    msks = transform.affinitize_mask(sample[(key + '_mask')])
    sample[key] = affs
    sample[key + '_mask'] = msks
    if rebalancing:
        wmsk = transform.tensor_func.rebalance_class(affs)
        sample[(key + '_mask')] *= wmsk


def multiclass_expansion(sample, key, ids, rebalancing=True):
    """For semantic segmentation."""
    lbl = sample[key]
    msk = utils.check_volume(sample[(key + '_mask')])
    lbls, msk2 = transform.multiclass_expansion(lbl, ids)
    msk *= msk2
    msks = np.tile(msk, (len(ids), 1, 1, 1))
    sample[key] = lbls
    sample[key + '_mask'] = msks
    if rebalancing:
        wmsk = transform.rebalance_class(lbl)
        wmsk = np.tile(wmsk, (len(ids), 1, 1, 1))
        sample[(key + '_mask')] *= wmsk
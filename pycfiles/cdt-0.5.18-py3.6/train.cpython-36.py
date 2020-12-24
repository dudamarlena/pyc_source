# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/pairwise/Jarfo_model/train.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 1550 bytes
"""
Cause-effect model training

"""
import sys, numpy as np
from .estimator import CauseEffectSystemCombination
import pandas as pd
from .util import random_permutation
MODEL = CauseEffectSystemCombination
MODEL_PARAMS = {'weights':[0.383, 0.37, 0.247],  'njobs':1}

def train(df, tar):
    set1 = 'train' if len(sys.argv) < 2 else sys.argv[1]
    train_filter = None
    model = MODEL(**MODEL_PARAMS)
    print('Reading in training data ' + set1)
    train = df
    print('Extracting features')
    train = model.extract(train)
    train, target = random_permutation(train, tar)
    train_filter = None
    if train_filter is not None:
        train = train[train_filter]
        target = target[train_filter]
    print('Training model with optimal weights')
    X = pd.concat([train])
    y = np.concatenate(tar.values)
    model.fit(X, y)
    return model
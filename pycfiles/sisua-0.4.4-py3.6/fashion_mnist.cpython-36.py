# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/sisua/data/data_loader/fashion_mnist.py
# Compiled at: 2019-09-16 06:46:06
# Size of source mod 2**32: 2559 bytes
from __future__ import absolute_import, division, print_function
import os, pickle, shutil, numpy as np
from odin import fuel as F
from odin.utils import ctext, one_hot, select_path
from sisua.data.path import DOWNLOAD_DIR, PREPROCESSED_BASE_DIR

def _check_override(path, override):
    if override:
        if os.path.exists(path):
            shutil.rmtree(path)
            os.mkdir(path)
    elif not os.path.exists(path):
        os.mkdir(path)


def _preprocessing_dataset(ds, outpath):
    X_train = ds['X_train'].astype('float32').reshape(-1, 784)
    X_test = ds['X_test'].astype('float32').reshape(-1, 784)
    y_train = ds['y_train'].astype('float32')
    y_test = ds['y_test'].astype('float32')
    labels = ds['labels']
    n_classes = len(labels)
    y_train = one_hot(y_train, nb_classes=n_classes)
    y_test = one_hot(y_test, nb_classes=n_classes)
    X_train = np.concatenate((X_train, X_test), axis=0)
    y_train = np.concatenate((y_train, y_test), axis=0)
    example_names = np.array(['image {}'.format(i + 1) for i in range(X_train.shape[0])])
    feature_names = np.array(['pixel {}'.format(j + 1) for j in range(X_train.shape[1])])
    data_meta = {'X':X_train, 
     'X_row':example_names, 
     'X_col':feature_names, 
     'y':y_train, 
     'y_col':labels}
    for name, val in data_meta.items():
        path = os.path.join(outpath, name)
        with open(path, 'wb') as (f):
            pickle.dump(val, f)


def _validate_dataset(path):
    ds = F.Dataset(path, read_only=True)
    return ds


_FMNIST_PREPROCESSED = select_path((os.path.join(PREPROCESSED_BASE_DIR, 'FMNIST_preprocessed')),
  create_new=True)

def read_fashion_MNIST(override=False, verbose=False):
    _check_override(_FMNIST_PREPROCESSED, override)
    if not os.path.exists(os.path.join(_FMNIST_PREPROCESSED, 'X_train')):
        ds = F.FMNIST_original.load()
        _preprocessing_dataset(ds, outpath=_FMNIST_PREPROCESSED)
    return _validate_dataset(_FMNIST_PREPROCESSED)
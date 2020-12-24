# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gapml/dataset.py
# Compiled at: 2018-08-31 14:33:57
# Size of source mod 2**32: 2399 bytes
""" Dataset Module for handling datasets
Copyright, 2018(c), Andrew Ferlitsch
"""
import numpy as np
from .vision import Images

class Dataset(object):
    __doc__ = ' Manage Dataset for Training a Model '

    def __init__(self):
        self._init()

    def _init(self):
        """ re-initialize variables """
        self.X_train = []
        self.Y_train = []
        self.X_test = []
        self.Y_test = []


class ImageDataset(Dataset):
    __doc__ = ' Manage Image Dataset for Training a Model '

    def __init__(self, collections):
        self._collections = collections
        self._split = 0.2
        self._seed = 0

    def split(self, percent, seed, nlabels=None):
        """ Split dataset into training and test data """
        self._init()
        self._split = percent
        self._seed = seed
        for images in self._collections:
            images.split = (
             self._split, self._seed)
            x_train, x_test, y_train, y_test = images.split
            self.X_train.extend(x_train)
            self.X_test.extend(x_test)
            self.Y_train.extend(y_train)
            self.Y_test.extend(y_test)

        self.X_train = np.asarray(self.X_train)
        self.Y_train = np.asarray(self.Y_train)
        self.X_test = np.asarray(self.X_test)
        self.Y_test = np.asarray(self.Y_test)
        if nlabels == None:
            nlabels = len(self._collections)
        self.Y_train = self.convert_labels_to_one_hot_encoding(self.Y_train, nlabels)
        self.Y_test = self.convert_labels_to_one_hot_encoding(self.Y_test, nlabels)
        return (
         self.X_train, self.X_test, self.Y_train, self.Y_test)

    def convert_labels_to_one_hot_encoding(self, Y, C):
        """ This function will do the reshape and conversion """
        Y = np.eye(C)[Y.reshape(-1)]
        return Y
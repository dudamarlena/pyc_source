# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/dataset/mnist.py
# Compiled at: 2014-11-17 02:57:29
from nlpy.dataset import AbstractDataset
import logging, tempfile, sys, os, gzip, urllib, cPickle, numpy as np
logging = logging.getLogger(__name__)
MNIST_URL = 'http://deeplearning.net/data/mnist/mnist.pkl.gz'

class MnistDataset(AbstractDataset):

    def __init__(self, target_format=None):
        super(MnistDataset, self).__init__(target_format)
        self._target_size = 10
        logging.info('loading minst data')
        path = os.path.join(tempfile.gettempdir(), 'mnist.pkl.gz')
        if not os.path.exists(path):
            logging.info('downloading minst data')
            urllib.urlretrieve(MNIST_URL, path)
        self._train_set, self._valid_set, self._test_set = cPickle.load(gzip.open(path, 'rb'))

    def train_set(self):
        data, target = self._train_set
        return [(data, np.array(map(self._target_map, target)))]

    def valid_set(self):
        data, target = self._valid_set
        return [(data, np.array(map(self._target_map, target)))]

    def test_set(self):
        data, target = self._test_set
        return [(data, np.array(map(self._target_map, target)))]
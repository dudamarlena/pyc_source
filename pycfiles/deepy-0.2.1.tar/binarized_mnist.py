# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/dataset/binarized_mnist.py
# Compiled at: 2016-04-20 00:05:45
import logging as loggers
logging = loggers.getLogger(__name__)
import os, tempfile, numpy as np, urllib
from basic import BasicDataset
URL_MAP = {'train': 'http://www.cs.toronto.edu/~larocheh/public/datasets/binarized_mnist/binarized_mnist_train.amat', 
   'valid': 'http://www.cs.toronto.edu/~larocheh/public/datasets/binarized_mnist/binarized_mnist_valid.amat', 
   'test': 'http://www.cs.toronto.edu/~larocheh/public/datasets/binarized_mnist/binarized_mnist_test.amat'}
PATH_MAP = {'train': os.path.join(tempfile.gettempdir(), 'binarized_mnist_train.npy'), 
   'valid': os.path.join(tempfile.gettempdir(), 'binarized_mnist_valid.npy'), 
   'test': os.path.join(tempfile.gettempdir(), 'binarized_mnist_test.npy')}

class BinarizedMnistDataset(BasicDataset):

    def __init__(self):
        for name, url in URL_MAP.items():
            local_path = PATH_MAP[name]
            if not os.path.exists(local_path):
                logging.info('downloading %s dataset of binarized MNIST')
                np.save(local_path, np.loadtxt(urllib.urlretrieve(url)[0]))

        train_set = [ (x,) for x in np.load(PATH_MAP['train']) ]
        valid_set = [ (x,) for x in np.load(PATH_MAP['valid']) ]
        test_set = [ (x,) for x in np.load(PATH_MAP['test']) ]
        super(BinarizedMnistDataset, self).__init__(train_set, valid=valid_set, test=test_set)
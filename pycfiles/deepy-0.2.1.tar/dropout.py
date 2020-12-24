# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/layers/dropout.py
# Compiled at: 2016-04-20 00:05:45
import theano
from . import NeuralLayer
from deepy.utils import global_theano_rand, FLOATX

class Dropout(NeuralLayer):

    def __init__(self, p):
        super(Dropout, self).__init__('dropout')
        self.p = p

    def compute_tensor(self, x):
        if self.p > 0:
            backup_test_value_setting = theano.config.compute_test_value
            theano.config.compute_test_value = 'ignore'
            binomial_mask = global_theano_rand.binomial(x.shape, p=1 - self.p, dtype=FLOATX)
            theano.config.compute_test_value = backup_test_value_setting
            x *= binomial_mask
        return x

    def compute_test_tesnor(self, x):
        if self.p > 0:
            x *= 1.0 - self.p
        return x
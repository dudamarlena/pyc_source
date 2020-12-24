# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/layers/softmax3d.py
# Compiled at: 2016-04-20 00:05:45
from layer import NeuralLayer
import theano, theano.tensor as T

class Softmax3D(NeuralLayer):

    def __init__(self):
        super(Softmax3D, self).__init__('softmax')

    def compute_tensor(self, x):
        shape = x.shape
        x = x.reshape((-1, shape[(-1)]))
        softmax_tensor = T.nnet.softmax(x)
        return softmax_tensor.reshape(shape)
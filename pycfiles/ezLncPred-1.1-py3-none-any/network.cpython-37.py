# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/LncrnaPackage/models/LncADeep/LncADeep_lncRNA/LncADeep_partial/bin/network.py
# Compiled at: 2019-10-31 09:01:16
# Size of source mod 2**32: 2341 bytes
import sys, json, random, numpy as np
from .utils import *

class NeuralNetwork(object):

    def __init__(self, sizes=None, para=None, weights=None, biases=None):
        if sizes is not None:
            self.num_layers = len(sizes)
            self.sizes = sizes
        else:
            if para is not None:
                self.para = para
            if weights is not None and biases is not None:
                self.finetune_weight_init(weights, biases)

    def finetune_weight_init(self, weights, biases):
        """Initialize the weights and biases from RBM
           Both weights and biases are a list of numpy array
        """
        t_weights = []
        for w in weights:
            t_weights.append(w.T)

        r_biases = []
        for b in biases:
            r_biases.append(b.reshape(b.shape[0], 1))

        self.weights = t_weights
        self.biases = r_biases

    def propup(self, x):
        """forward the input x, and return the output"""
        for b, w in zip(self.biases, self.weights):
            x = sigmoid(np.dot(w, x) + b)

        return x

    def SaveNN(self, net, para_file):
        """Save the parameters of neural network"""
        try:
            para = open(para_file, 'w')
        except (IOError, ValueError) as e:
            try:
                (
                 print >> sys.stderr, str(e))
                sys.exit(1)
            finally:
                e = None
                del e

        json.dump(net, para)
        para.close()

    def GetParameters(self):
        """Get the parameters of neural network"""
        net = {'sizes':self.sizes, 
         'biases':[b.tolist() for b in self.biases], 
         'weights':[w.tolist() for w in self.weights]}
        return net


def LoadNN(para_file):
    """load prebuild neural network
    """
    try:
        para = open(para_file, 'r')
    except (IOError, ValueError) as e:
        try:
            (
             print >> sys.stderr, str(e))
            sys.exit(1)
        finally:
            e = None
            del e

    net = json.load(para)
    para.close()
    nn = NeuralNetwork(net['sizes'])
    nn.biases = [np.array(b) for b in net['biases']]
    nn.weights = [np.array(w) for w in net['weights']]
    return nn


def SelectPara(AC, SN, SP, n=1):
    """choose a balanced accuracy from the best n accuracies"""
    ac_rank = np.argsort(AC)
    return ac_rank[-n:]
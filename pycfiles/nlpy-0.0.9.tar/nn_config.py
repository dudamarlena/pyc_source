# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/deep/conf/nn_config.py
# Compiled at: 2014-11-17 03:02:24


class NetworkConfig(object):

    def __init__(self, input_size):
        """
        Create a config for neural network
        :param input_size: size of input vector
        :return:
        """
        self.input_size = input_size
        self.layers = []
        self.no_learn_biases = False
        self.input_noise = 0.0
        self.input_dropouts = 0.0
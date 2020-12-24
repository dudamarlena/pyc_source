# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/utils/gpu_transmitter.py
# Compiled at: 2016-04-20 00:05:45
import numpy as np, theano, theano.tensor as T

class GPUDataTransmitter(object):
    """
    Cache multiple batches on GPU.
    """

    def __init__(self, network, shapes, dtypes, cache_num=10):
        self.network = network
        self.shapes = shapes
        self.cache_num = cache_num
        self.dtypes = dtypes
        self.all_variables = self.network.input_variables + self.network.target_variables
        if len(self.all_variables) != len(shapes):
            raise Exception('The number of network variables is not identical with shapes')
        self.iterator = T.iscalar('i')
        self.gpu_caches = []
        self.cpu_datas = []
        for shape, dtype in zip(self.shapes, self.dtypes):
            cache_shape = [
             cache_num] + shape
            cache = theano.shared(np.zeros(cache_shape, dtype=dtype))
            self.gpu_caches.append(cache)

    def get_givens(self):
        givens = {}
        for var, cache in zip(self.all_variables, self.gpu_caches):
            givens[var] = cache[self.iterator]

        return givens

    def get_iterator(self):
        return self.iterator

    def transmit(self, *data_list):
        for cache, data in zip(self.gpu_caches, data_list):
            cache.set_value(data, borrow=True)

    def wrap(self, data_source):
        if not self.cpu_datas:
            datas = []
            for _ in self.shapes:
                datas.append([])

            for data_tuple in data_source:
                for i in range(len(data_tuple)):
                    datas[i].append(data_tuple[i])

            for i in range(len(datas)):
                datas[i] = datas[i][:-1]

            for data, dtype in zip(datas, self.dtypes):
                self.cpu_datas.append(np.array(data, dtype=dtype))

        data_len = self.cpu_datas[0].shape[0]
        for i in xrange(0, data_len, self.cache_num):
            if i + self.cache_num > data_len:
                continue
            transmit_datas = [ data[i:i + self.cache_num] for data in self.cpu_datas ]
            self.transmit(*transmit_datas)
            for n in range(self.cache_num):
                yield [
                 n]
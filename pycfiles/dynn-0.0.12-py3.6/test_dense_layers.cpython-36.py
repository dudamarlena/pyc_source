# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\layers\test_dense_layers.py
# Compiled at: 2018-09-11 18:30:44
# Size of source mod 2**32: 1618 bytes
import unittest
from unittest import TestCase
import dynet as dy
from dynn.layers import dense_layers

class TestDenseLayer(TestCase):

    def setUp(self):
        self.pc = dy.ParameterCollection()
        self.do = 10
        self.di = 20
        self.dropout = 0.1

    def test_forward_backward(self):
        dense = dense_layers.DenseLayer((self.pc),
          (self.di), (self.do), dropout=(self.dropout))
        dy.renew_cg()
        x = dy.random_uniform(self.di, -1, 1)
        dense.init(test=False, update=True)
        y = dense(x)
        z = dy.sum_elems(y)
        z.forward()
        z.backward()


class TestGatedLayer(TestCase):

    def setUp(self):
        self.pc = dy.ParameterCollection()
        self.do = 10
        self.di = 20
        self.dropout = 0.1

    def test_forward_backward(self):
        gated = dense_layers.GatedLayer((self.pc),
          (self.di), (self.do), dropout=(self.dropout))
        dy.renew_cg()
        x = dy.random_uniform(self.di, -1, 1)
        gated.init(test=False, update=True)
        y = gated(x)
        z = dy.sum_elems(y)
        z.forward()
        z.backward()


if __name__ == '__main__':
    unittest.main()
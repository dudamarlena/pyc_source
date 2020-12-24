# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\layers\test_lstm.py
# Compiled at: 2018-09-11 18:11:37
# Size of source mod 2**32: 972 bytes
import unittest
from unittest import TestCase
import dynet as dy
from dynn.layers import lstm

class TestLSTM(TestCase):

    def setUp(self):
        self.pc = dy.ParameterCollection()
        self.dh = 10
        self.di = 20
        self.dropout = 0.1

    def test_compactlstm(self):
        compact_lstm = lstm.CompactLSTM(self.di, self.dh, self.pc, self.dropout)
        dy.renew_cg()
        h0 = dy.random_uniform(self.dh, -1, 1)
        c0 = dy.random_uniform(self.dh, -1, 1)
        x = dy.random_uniform(self.di, -1, 1)
        compact_lstm.init(test=False, update=True)
        h, c = compact_lstm(h0, c0, x)
        z = dy.dot_product(h, c)
        z.forward()
        z.backward()


if __name__ == '__main__':
    unittest.main()
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_random_op.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 1630 bytes
import jittor as jt
from jittor import nn, Module
from jittor.models import vgg, resnet
import numpy as np, sys, os, random, math, unittest
from .test_reorder_tuner import simple_parser
from .test_log import find_log_with_re

class TestRandomOp(unittest.TestCase):

    @unittest.skipIf(not jt.has_cuda, 'Cuda not found')
    @jt.flag_scope(use_cuda=1)
    def test(self):
        jt.set_seed(3)
        with jt.log_capture_scope(log_silent=1,
          log_v=0,
          log_vprefix='op.cc=100') as (raw_log):
            t = jt.random([5, 5])
            t.data
        logs = find_log_with_re(raw_log, '(Jit op key (not )?found: curand_random.*)')
        assert len(logs) == 1

    @unittest.skipIf(not jt.has_cuda, 'Cuda not found')
    @jt.flag_scope(use_cuda=1)
    def test_float64(self):
        jt.set_seed(3)
        with jt.log_capture_scope(log_silent=1,
          log_v=0,
          log_vprefix='op.cc=100') as (raw_log):
            t = jt.random([5, 5], dtype='float64')
            t.data
        logs = find_log_with_re(raw_log, '(Jit op key (not )?found: curand_random.*)')
        assert len(logs) == 1


if __name__ == '__main__':
    unittest.main()
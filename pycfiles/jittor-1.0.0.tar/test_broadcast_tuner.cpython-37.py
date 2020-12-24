# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_broadcast_tuner.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 1762 bytes
import sys, os, jittor as jt, unittest, time, numpy as np
from .test_reorder_tuner import simple_parser
from .test_log import find_log_with_re

class TestBroadcastTuner(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def check(self, h, w, cs, rs, pa, rtp, dim):
        a = jt.random([h, w])
        a.data
        with jt.log_capture_scope(log_v=0,
          log_vprefix='tuner_manager=100',
          compile_options={'test_broadcast_tuner': 1}) as (logs):
            amean = jt.mean(a, dims=[dim], keepdims=1)
            a2mean = jt.mean((a * a), dims=[dim], keepdims=1)
            norm_aa = (a - amean.broadcast_var(a)) / jt.sqrt(a2mean - amean * amean).broadcast_var(a)
            norm_aa.data
        logs = find_log_with_re(logs, 'Run tuner broadcast: confidence\\((20)\\) candidates\\((.*)\\)$')
        assert len(logs) == 1, logs
        assert logs[0][0] == '20', 'confidence of reorder should be 20'
        candidates = simple_parser(logs[0][1])
        assert candidates == {'order0':[0],  'order1':[1],  'order2':[0],  'split1':[2048],  'use_movnt':[1]}, candidates

    def test_broadcast_tuner(self):
        self.check(8192, 8192, 0, 0, 0, 5, 0)


if __name__ == '__main__':
    unittest.main()
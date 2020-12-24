# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/max/code/oss/hyperopt/hyperopt/tests/test_atpe_basic.py
# Compiled at: 2019-10-16 11:29:50
# Size of source mod 2**32: 985 bytes
from __future__ import absolute_import
from builtins import range
import unittest
from hyperopt.base import Trials, trials_from_docs, miscs_to_idxs_vals
from hyperopt import rand

class TestATPE(unittest.TestCase):

    def test_run_basic_search(self):

        def objective(args):
            case, val = args
            if case == 'case 1':
                return val
            else:
                return val ** 2

        from hyperopt import hp
        space = hp.choice('a', [
         (
          'case 1', 1 + hp.lognormal('c1', 0, 1)),
         (
          'case 2', hp.uniform('c2', -10, 10))])
        from hyperopt import fmin, atpe, space_eval
        best = fmin(objective, space, algo=atpe.suggest, max_evals=10)
        print(best)
        print(space_eval(space, best))
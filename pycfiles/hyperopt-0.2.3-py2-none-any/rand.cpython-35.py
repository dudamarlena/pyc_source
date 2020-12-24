# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/max/code/oss/hyperopt/hyperopt/rand.py
# Compiled at: 2019-10-17 07:38:06
# Size of source mod 2**32: 1236 bytes
"""
Random search - presented as hyperopt.fmin_random
"""
from __future__ import absolute_import
import logging, numpy as np
from . import pyll
from .base import miscs_update_idxs_vals
logger = logging.getLogger(__name__)

def suggest(new_ids, domain, trials, seed):
    rng = np.random.RandomState(seed)
    rval = []
    for ii, new_id in enumerate(new_ids):
        idxs, vals = pyll.rec_eval(domain.s_idxs_vals, memo={domain.s_new_ids: [new_id], 
         domain.s_rng: rng})
        new_result = domain.new_result()
        new_misc = dict(tid=new_id, cmd=domain.cmd, workdir=domain.workdir)
        miscs_update_idxs_vals([new_misc], idxs, vals)
        rval.extend(trials.new_trial_docs([new_id], [
         None], [new_result], [new_misc]))

    return rval


def suggest_batch(new_ids, domain, trials, seed):
    rng = np.random.RandomState(seed)
    idxs, vals = pyll.rec_eval(domain.s_idxs_vals, memo={domain.s_new_ids: new_ids, 
     domain.s_rng: rng})
    return (
     idxs, vals)
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/run/repeat.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 619 bytes
import traceback, numpy as np, tensorflow as tf
from tensorflow import keras
from ....search import util
from .alpha import run as run_alpha
logger = util.conf_logger('deephyper.search.nas.run')

def run(config):
    seed = config['seed']
    repeat = 2
    if seed is not None:
        np.random.seed(seed)
        seeds = np.random.randint(0, 4294967295, repeat)
    res_list = []
    for i in range(repeat):
        tf.keras.backend.clear_session()
        if seed is not None:
            config['seed'] = seeds[i]
        res = run_alpha(config)
        res_list.append(res)

    return max(res_list)
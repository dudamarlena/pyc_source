# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/models/inference/loss_functions/elbo.py
# Compiled at: 2019-02-25 04:13:09
# Size of source mod 2**32: 707 bytes
from tensorflow_probability import edward2 as ed
import tensorflow as tf
from inferpy import util

def ELBO(pmodel, qvars, sample_dict):
    plate_size = pmodel._get_plate_size(sample_dict)
    with ed.interception((util.random_variable.set_values)(**{**qvars, **sample_dict})):
        pvars, _ = pmodel.expand_model(plate_size)
    energy = tf.reduce_sum([tf.reduce_sum(p.log_prob(p.value)) for p in pvars.values()])
    entropy = -tf.reduce_sum([tf.reduce_sum(q.log_prob(q.value)) for q in qvars.values()])
    ELBO = energy + entropy
    return -ELBO
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/unrandom.py
# Compiled at: 2019-08-29 04:25:36
# Size of source mod 2**32: 1009 bytes
import numpy as np, tensorflow as tf, random as rn
np.random.seed(42)
rn.seed(12345)
session_conf = tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
from tensorflow.python.keras import backend as K
tf.set_random_seed(1234)
sess = tf.Session(graph=(tf.get_default_graph()), config=session_conf)
K.set_session(sess)
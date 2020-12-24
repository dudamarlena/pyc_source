# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/utils/tensor_utils.py
# Compiled at: 2018-11-19 01:56:49
# Size of source mod 2**32: 1269 bytes
import numpy as np, tensorflow as tf

def fusion_tensor(emb_tensor1, emb_tensor2, emb_tensor3):
    """
    Fusion products between 3 tensors
    :param emb_tensor1:
    :param emb_tensor2:
    :param emb_tensor3:
    :return:
    """
    x1_dim = emb_tensor1.shape[2]
    x2_dim = emb_tensor2.shape[2]
    x3_dim = emb_tensor3.shape[2]
    fusion_W_dim = 5
    w = np.random.randn(x1_dim, x2_dim, x3_dim, fusion_W_dim)
    t1 = tf.tile(tf.expand_dims(tf.expand_dims(emb_tensor1, -1), -1), [1, 1, 1, x2_dim, x3_dim])
    t2 = tf.tile(tf.expand_dims(tf.expand_dims(emb_tensor2, 1), -1), [1, 1, x1_dim, 1, x3_dim])
    t3 = tf.tile(tf.expand_dims(tf.expand_dims(emb_tensor3, 1), 2), [1, 1, x1_dim, x2_dim, 1])
    tw = tf.convert_to_tensor(w, dtype=(tf.float64))
    t123 = t1 * t2 * t3
    h = tf.tensordot(t123, tw, axes=[[1, 2, 3], [0, 1, 2]])
    return h
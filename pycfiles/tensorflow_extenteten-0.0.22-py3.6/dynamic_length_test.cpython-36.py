# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/dynamic_length_test.py
# Compiled at: 2017-01-06 05:01:09
# Size of source mod 2**32: 506 bytes
import numpy as np, tensorflow as tf
from .dynamic_length import *

def test_id_tensor_to_length():
    with tf.Session() as (session):
        with session.as_default():
            id_tensor = tf.constant([[[1], [2], [3], [0], [0]]])
            assert id_tensor_to_length(id_tensor).eval() == np.array([3])


def test_id_vector_to_length():
    with tf.Session() as (session):
        with session.as_default():
            id_vector = tf.constant([[1, 2, 3, 0, 0]])
            assert id_vector_to_length(id_vector).eval() == np.array([3])
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qnd/test_test.py
# Compiled at: 2017-05-17 13:34:20
# Size of source mod 2**32: 200 bytes
import tensorflow as tf
from .test import *

def test_oracle_model():
    oracle_model(tf.zeros([100]), tf.zeros([100]))


def test_user_input_fn():
    user_input_fn(tf.FIFOQueue(64, [tf.string]))
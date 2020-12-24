# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/simple_tensor/tensor_metrics.py
# Compiled at: 2019-07-18 06:55:46
# Size of source mod 2**32: 1205 bytes
"""
    File name: test.py
    Author: [Mochammad F Rahman]
    Date created: / /2018
    Date last modified: 17/07/2019
    Python Version: >= 3.5
    Simple-tensor version: v0.6.2
    License: MIT License
    Maintainer: [Mochammad F Rahman]
"""
import tensorflow as tf, numpy as np

def calculate_acc(input_tensor, label, threshold=0.5):
    """[summary]
    
    Arguments:
        input_tensor {[type]} -- [description]
        label {[type]} -- [description]
    
    Keyword Arguments:
        threshold {float} -- [description] (default: {0.5})
    
    Returns:
        [type] -- [description]
    """
    mask = tf.fill(tf.shape(label), 1.0)
    input_tensor = tf.reshape(input_tensor, [tf.shape(input_tensor)[0], -1])
    label = tf.reshape(label, [tf.shape(label)[0], -1])
    input_tensor = tf.math.greater(input_tensor, tf.convert_to_tensor(np.array(threshold), tf.float32))
    input_tensor = tf.cast(input_tensor, tf.float32)
    label = tf.math.greater(label, tf.convert_to_tensor(np.array(threshold), tf.float32))
    label = tf.cast(label, tf.float32)
    error = tf.reduce_sum(tf.abs(input_tensor - label)) / (tf.reduce_sum(mask) + 0.0001)
    acc = 1.0 - error
    return acc
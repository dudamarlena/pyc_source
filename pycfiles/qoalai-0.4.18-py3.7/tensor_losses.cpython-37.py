# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qoalai/tensor_losses.py
# Compiled at: 2020-03-21 07:20:53
# Size of source mod 2**32: 2432 bytes
"""
    File name: tensor_losses.py
    Author: [Mochammad F Rahman]
    Date created: / /2018
    Date last modified: 17/07/2019
    Python Version: >= 3.5
    Qoalai version: v0.4.1
    License: MIT License
    Maintainer: [Mochammad F Rahman]
"""
import tensorflow as tf

def mse_loss_mean(output_tensor, label):
    """"[summary]
    
    Arguments:
        output_tensor {tensor} -- [description]
        label {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    loss = tf.square(tf.subtract(output_tensor, label))
    loss = tf.reduce_mean(loss)
    return loss


def mse_loss_sum(output_tensor, label):
    """"[summary]
    
    Arguments:
        output_tensor {tensor} -- [description]
        label {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    loss = tf.square(tf.subtract(output_tensor, label))
    loss = tf.reduce_sum(loss)
    return loss


def softmax_crosentropy_mean(output_tensor, label):
    """[summary]
    
    Arguments:
        output_tensor {[type]} -- [description]
        label {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    loss = tf.nn.softmax_cross_entropy_with_logits_v2(labels=label, logits=output_tensor)
    loss = tf.reduce_mean(loss)
    return loss


def softmax_crosentropy_sum(output_tensor, label):
    """[summary]
    
    Arguments:
        output_tensor {[type]} -- [description]
        label {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    loss = tf.nn.softmax_cross_entropy_with_logits_v2(labels=label, logits=output_tensor)
    loss = tf.reduce_sum(loss)
    return loss


def sigmoid_crossentropy_mean(output_tensor, label):
    """[summary]
    
    Arguments:
        output_tensor {[type]} -- [description]
        label {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    loss = tf.nn.sigmoid_cross_entropy_with_logits(labels=label, logits=output_tensor)
    loss = tf.reduce_mean(loss)
    return loss


def sigmoid_crossentropy_sum(output_tensor, label):
    """[summary]
    
    Arguments:
        output_tensor {[type]} -- [description]
        label {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    loss = tf.nn.sigmoid_cross_entropy_with_logits(labels=label, logits=output_tensor)
    loss = tf.reduce_sum(loss)
    return loss
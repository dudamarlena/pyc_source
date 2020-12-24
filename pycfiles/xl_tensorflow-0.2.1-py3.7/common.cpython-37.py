# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xl_tensorflow\models\vision\common.py
# Compiled at: 2020-04-26 06:01:39
# Size of source mod 2**32: 1325 bytes
import tensorflow as tf
MEAN_RGB = (123.675, 116.28, 103.53)
STDDEV_RGB = (58.395, 57.120000000000005, 57.375)

def _bytes_feature(value):
    """Returns a bytes_list from a string / byte."""
    if isinstance(value, type(tf.constant(0))):
        value = value.numpy()
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def _float_feature(value):
    """Returns a float_list from a float / double."""
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))


def _int64_feature(value):
    """Returns an int64_list from a bool / enum / int / uint."""
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def _int64_list_feature(value):
    """int64 list to feature(value don't need to and '[]")"""
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def _float_list_feature(value):
    """float list to feature(value don't need to and '[]")"""
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))


def _bytes_list_feature(value):
    """byte list to feature(value don't need to and '[]")"""
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=value))
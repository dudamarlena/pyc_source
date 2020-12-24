# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/collections.py
# Compiled at: 2017-01-06 05:01:09
# Size of source mod 2**32: 447 bytes
import tensorflow as tf
from . import util
ATTENTIONS = 'attentions'
METRICS = 'metrics'

def add_attention(tensor):
    return tf.add_to_collection(ATTENTIONS, tensor)


def get_attentions():
    return tf.get_collection(ATTENTIONS)


def add_metric(tensor, name=None):
    return tf.add_to_collection(METRICS, tensor if name is None else util.rename(tensor, name))


def get_metrics():
    return tf.get_collection(METRICS)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/summary.py
# Compiled at: 2017-01-18 22:10:05
# Size of source mod 2**32: 1023 bytes
import tensorflow as tf
from .util import func_scope, static_rank

@func_scope()
def tensor(variable, name=None):
    name = sanitize_summary_name(name or variable.name)
    mean = tf.reduce_mean(variable)
    return tf.summary.merge([
     tf.summary.scalar('mean/' + name, mean),
     tf.summary.scalar('stddev/' + name, tf.sqrt(tf.reduce_mean(tf.square(variable - mean)))),
     tf.summary.scalar('max/' + name, tf.reduce_max(variable)),
     tf.summary.scalar('min/' + name, tf.reduce_min(variable)),
     tf.summary.histogram(name, variable)])


@func_scope()
def image(variable, name=None):
    name = sanitize_summary_name(name or variable.name)
    rank = static_rank(variable)
    return tf.summary.image(name,
      (variable if rank == 4 else tf.expand_dims(variable, 3) if rank == 3 else tf.expand_dims(tf.expand_dims(variable, 0), 3)),
      max_outputs=64)


def sanitize_summary_name(name):
    return name.replace(':', '_')
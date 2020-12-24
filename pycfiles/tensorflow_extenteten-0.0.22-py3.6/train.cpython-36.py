# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/train.py
# Compiled at: 2017-01-06 05:01:09
# Size of source mod 2**32: 233 bytes
import tensorflow as tf
__all__ = [
 'global_step', 'minimize']

def global_step():
    return tf.contrib.framework.get_or_create_global_step()


def minimize(loss):
    return tf.train.AdamOptimizer().minimize(loss, global_step())
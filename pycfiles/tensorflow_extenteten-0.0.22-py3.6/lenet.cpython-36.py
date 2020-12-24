# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/cnn/lenet.py
# Compiled at: 2017-01-19 20:08:06
# Size of source mod 2**32: 434 bytes
import tensorflow as tf
from ..layer import linear
from ..util import func_scope

@func_scope()
def lenet(images, output_size):
    h = tf.contrib.slim.conv2d(images, 32, 5, scope='conv0')
    h = tf.contrib.slim.max_pool2d(h, 2, 2, scope='pool0')
    h = tf.contrib.slim.conv2d(h, 64, 5, scope='conv1')
    h = tf.contrib.slim.max_pool2d(h, 2, 2, scope='pool1')
    h = tf.contrib.slim.flatten(h)
    return linear(h, output_size)
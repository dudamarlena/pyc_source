# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/cnn/lenet_test.py
# Compiled at: 2017-01-19 19:58:16
# Size of source mod 2**32: 112 bytes
import tensorflow as tf
from .lenet import lenet

def test_lenet():
    lenet(tf.zeros([64, 24, 24, 1]), 200)
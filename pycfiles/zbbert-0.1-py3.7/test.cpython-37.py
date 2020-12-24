# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\zbbert\test.py
# Compiled at: 2019-06-05 02:14:38
# Size of source mod 2**32: 175 bytes
import tensorflow as tf, os
os.environ['CUDA_VISIABLE_DEVICES'] = '0'
gpu_device_name = tf.test.gpu_device_name()
print(gpu_device_name)
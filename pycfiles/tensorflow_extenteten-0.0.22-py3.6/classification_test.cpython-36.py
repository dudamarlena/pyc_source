# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/classification_test.py
# Compiled at: 2017-01-18 22:08:31
# Size of source mod 2**32: 1260 bytes
import numpy as np, tensorflow as tf
from .classification import classify

def test_classify():
    for logits_shape, labels_shape, num_classes, num_labels in [
     [
      64, 64, 2, None],
     [
      64, 64, 2, 1],
     [
      64, None, 2, 1],
     [
      [
       64, 3], [64, 3], 2, None],
     [
      [
       64, 3], [64, 3], 2, 3],
     [
      [
       64, 3], None, 2, 3],
     [
      [
       64, 5], 64, 5, None],
     [
      [
       64, 5], 64, 5, 1],
     [
      [
       64, 5], None, 5, 1],
     [
      [
       64, 15], [64, 3], 5, None],
     [
      [
       64, 15], [64, 3], 5, 3],
     [
      [
       64, 15], None, 5, 3]]:
        print(logits_shape, labels_shape, num_classes, num_labels)
        print(classify(tf.Variable((np.zeros(logits_shape)), collections=[
         tf.GraphKeys.GLOBAL_VARIABLES,
         tf.GraphKeys.WEIGHTS]),
          (None if labels_shape is None else tf.constant(np.zeros(labels_shape, np.int32))),
          num_classes=num_classes,
          num_labels=num_labels))
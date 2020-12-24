# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/tfimgsort/tfutil.py
# Compiled at: 2017-05-12 11:21:19
# Size of source mod 2**32: 1166 bytes
"""Utilities for creating and using a tensorflow image classifier."""
import os, sys, numpy as np, tensorflow as tf, ntpath
from functools import reduce
graph_created = False

def create_graph(file):
    """Given the path to a tensorflow model loads it as the default graph."""
    global graph_created
    if graph_created:
        return
    graph_created = True
    with tf.gfile.FastGFile(file, 'rb') as (f):
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def classify(img):
    """Given a path to a jpg image classifies it using the preloaded model.

  Note: this assumes a default graph has already been instantiated using the
  :func:`create_graph`.
  """
    answer = None
    if not tf.gfile.Exists(img):
        tf.logging.fatal('File does not exist %s', img)
        return answer
    image_data = tf.gfile.FastGFile(img, 'rb').read()
    with tf.Session() as (sess):
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)
    return predictions
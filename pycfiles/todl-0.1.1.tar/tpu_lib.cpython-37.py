# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/utils/misc/tpu_lib.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 1230 bytes
"""Initializes TPU system for TF 2.0."""
import tensorflow as tf

def tpu_initialize(tpu_address):
    """Initializes TPU for TF 2.0 training.

  Args:
    tpu_address: string, bns address of master TPU worker.

  Returns:
    A TPUClusterResolver.
  """
    cluster_resolver = tf.distribute.cluster_resolver.TPUClusterResolver(tpu=tpu_address)
    if tpu_address not in ('', 'local'):
        tf.config.experimental_connect_to_cluster(cluster_resolver)
    tf.tpu.experimental.initialize_tpu_system(cluster_resolver)
    return cluster_resolver
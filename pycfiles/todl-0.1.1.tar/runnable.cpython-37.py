# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/staging/training/runnable.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 3162 bytes
"""An abstraction that users can easily handle their custom training loops."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import abc, six
import tensorflow.compat.v2 as tf
from typing import Dict, Optional, Text

@six.add_metaclass(abc.ABCMeta)
class AbstractTrainable(tf.Module):
    __doc__ = 'An abstract class defining the APIs required for training.'

    @abc.abstractmethod
    def train(self, num_steps: Optional[tf.Tensor]) -> Optional[Dict[(Text, tf.Tensor)]]:
        """Implements model training with multiple steps.

    In training, it is common to break the total training steps into several
    training loops, so users can do checkpointing, write summaries and run some
    python callbacks. This is necessary for getting good performance in TPU
    training, as the overhead for launching a multi worker tf.function may be
    large in Eager mode. It is usually encouraged to create a host training loop
    (e.g. using a `tf.range` wrapping `strategy.run` inside a
    `tf.function`) in the TPU case. For the cases that don't require host
    training loop to acheive peak performance, users can just implement a simple
    python loop to drive each step.

    Args:
      num_steps: A guideline for how many training steps to run. Note that it is
        up to the model what constitutes a "step" (this may involve more than
        one update to model parameters, e.g. if training a GAN).

    Returns:
      The function may return a dictionary of `Tensors`, which will be
      written to logs and as TensorBoard summaries.
    """
        pass


@six.add_metaclass(abc.ABCMeta)
class AbstractEvaluable(tf.Module):
    __doc__ = 'An abstract class defining the APIs required for evaluation.'

    @abc.abstractmethod
    def evaluate(self, num_steps: Optional[tf.Tensor]) -> Optional[Dict[(Text, tf.Tensor)]]:
        """Implements model evaluation.

    Args:
      num_steps: A guideline for how many evaluation steps to run. Note that it
        is up to the model what constitutes a "step". Generally, it may be
        desirable to support both a limited number of eval steps and iterating
        over a full dataset (however many steps are required) when `num_steps`
        is `None`.

    Returns:
      The function may return a dictionary of `Tensors`, which will be
      written to logs and as TensorBoard summaries.
    """
        pass
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/staging/training/standard_runnable.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 6132 bytes
"""An abstraction that users can easily handle their custom training loops."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import abc, six
import tensorflow.compat.v2 as tf
from typing import Dict, Optional, Text
from official.staging.training import runnable
from official.staging.training import utils

@six.add_metaclass(abc.ABCMeta)
class StandardTrainable(runnable.AbstractTrainable):
    __doc__ = 'Implements the standard functionality of AbstractTrainable APIs.'

    def __init__(self, use_tf_while_loop=True, use_tf_function=True):
        if use_tf_while_loop:
            if not use_tf_function:
                raise ValueError('`use_tf_while_loop=True` and `use_tf_function=False` is not supported')
        self.use_tf_while_loop = use_tf_while_loop
        self.use_tf_function = use_tf_function
        self.train_dataset = None
        self.train_iter = None
        self.train_loop_fn = None

    @abc.abstractmethod
    def build_train_dataset(self):
        """Builds the training datasets.

    Returns:
      A tf.nest-compatible structure of tf.data.Dataset or DistributedDataset.
    """
        pass

    def train(self, num_steps: Optional[tf.Tensor]) -> Optional[Dict[(Text, tf.Tensor)]]:
        """See base class."""
        if self.train_dataset is None:
            self.train_dataset = self.build_train_dataset()
            self.train_iter = tf.nest.map_structure(iter, self.train_dataset)
        elif self.train_loop_fn is None:
            train_fn = self.train_step
            if self.use_tf_while_loop:
                self.train_loop_fn = utils.create_tf_while_loop_fn(train_fn)
            else:
                if self.use_tf_function:
                    train_fn = tf.function(train_fn)
            self.train_loop_fn = utils.create_loop_fn(train_fn)
        self.train_loop_begin()
        self.train_loop_fn(self.train_iter, num_steps)
        return self.train_loop_end()

    def train_loop_begin(self):
        """Called once at the beginning of the training loop.

    This is a good place to reset metrics that accumulate values over multiple
    steps of training.
    """
        pass

    @abc.abstractmethod
    def train_step(self, iterator):
        """Implements one step of training.

    What a "step" consists of is up to the implementer. If using distribution
    strategies, the call to this method should take place in the "cross-replica
    context" for generality, to allow e.g. multiple iterator dequeues and calls
    to `strategy.run`.

    Args:
      iterator: A tf.nest-compatible structure of tf.data Iterator or
        DistributedIterator.
    """
        pass

    def train_loop_end(self) -> Optional[Dict[(Text, tf.Tensor)]]:
        """Called at the end of the training loop.

    This is a good place to get metric results. The value returned from this
    function will be returned as-is from the train() method.

    Returns:
      The function may return a dictionary of `Tensors`, which will be
      written to logs and as TensorBoard summaries.
    """
        pass


@six.add_metaclass(abc.ABCMeta)
class StandardEvaluable(runnable.AbstractEvaluable):
    __doc__ = 'Implements the standard functionality of AbstractEvaluable APIs.'

    def __init__(self, use_tf_function=True):
        self.eval_use_tf_function = use_tf_function
        self.eval_dataset = None
        self.eval_loop_fn = None

    @abc.abstractmethod
    def build_eval_dataset(self):
        """Builds the evaluation datasets.

    Returns:
      A tf.nest-compatible structure of tf.data.Dataset or DistributedDataset.
    """
        pass

    def evaluate(self, num_steps: Optional[tf.Tensor]) -> Optional[Dict[(Text, tf.Tensor)]]:
        """See base class."""
        if self.eval_dataset is None:
            self.eval_dataset = self.build_eval_dataset()
        if self.eval_loop_fn is None:
            eval_fn = self.eval_step
            if self.eval_use_tf_function:
                eval_fn = tf.function(eval_fn)
            self.eval_loop_fn = utils.create_loop_fn(eval_fn)
        self.eval_iter = tf.nest.map_structure(iter, self.eval_dataset)
        self.eval_begin()
        self.eval_loop_fn(self.eval_iter, num_steps)
        return self.eval_end()

    def eval_begin(self):
        """Called once at the beginning of the evaluation.

    This is a good place to reset metrics that accumulate values over the entire
    evaluation.
    """
        pass

    @abc.abstractmethod
    def eval_step(self, iterator):
        """Implements one step of evaluation.

    What a "step" consists of is up to the implementer. If using distribution
    strategies, the call to this method should take place in the "cross-replica
    context" for generality, to allow e.g. multiple iterator dequeues and calls
    to `strategy.run`.

    Args:
      iterator: A tf.nest-compatible structure of tf.data Iterator or
        DistributedIterator.
    """
        pass

    def eval_end(self) -> Optional[Dict[(Text, tf.Tensor)]]:
        """Called at the end of the evaluation.

    This is a good place to get metric results. The value returned from this
    function will be returned as-is from the evaluate() method.

    Returns:
      The function may return a dictionary of `Tensors`, which will be
      written to logs and as TensorBoard summaries.
    """
        pass
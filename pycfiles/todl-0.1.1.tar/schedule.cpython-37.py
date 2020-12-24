# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/r1/transformer/schedule.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 4983 bytes
"""Abstract training on a step or epoch basis."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math
import tensorflow.compat.v1 as tf
_TRAIN, _EVAL = tf.estimator.ModeKeys.TRAIN, tf.estimator.ModeKeys.EVAL
NUM_EXAMPLES = {tf.estimator.ModeKeys.TRAIN: 4572160, 
 tf.estimator.ModeKeys.EVAL: 3000}

class Manager(object):
    __doc__ = 'Container for convenience functions to abstract step or epoch basis.\n  Transformer allows users to specify an epoch basis (generally recommended for\n  full training) or a number of steps basis (convenient since epochs are rather\n  large). TPUs furthermore require a step basis; however epochs are the norm in\n  the machine learning community and it is desirable to allow users to specify\n  epochs even when running with TPUS which requires behind the scenes\n  conversions.\n  This container simply groups what are largely mundane checks and conversions\n  rather than interspersing them throughout the run loop code.\n  '

    def __init__(self, train_steps, steps_between_evals, train_epochs, epochs_between_evals, default_train_epochs, batch_size, max_length, use_tpu=False, num_tpu_shards=8):
        if train_steps:
            if train_epochs:
                raise ValueError('Both train_steps or train_epochs were be defined.')
        elif train_steps:
            self.train_eval_iterations = train_steps // steps_between_evals
            self._single_iteration_train_steps = steps_between_evals
            self._single_iteration_train_epochs = None
        else:
            train_epochs = train_epochs or default_train_epochs
            self.train_eval_iterations = train_epochs // epochs_between_evals
            self._single_iteration_train_steps = None
            self._single_iteration_train_epochs = epochs_between_evals
        self.max_length = max_length
        self.batch_size = batch_size
        self.use_tpu = use_tpu
        self.num_tpu_shards = num_tpu_shards
        if self.use_tpu:
            assert self.batch_size // self.max_length % self.num_tpu_shards == 0

    @property
    def single_iteration_train_steps(self):
        return self._single_iteration_train_steps or self.use_tpu or self._single_iteration_train_steps
        return self.epochs_to_steps(num_epochs=(self._single_iteration_train_epochs),
          mode=_TRAIN)

    @property
    def single_iteration_eval_steps(self):
        if not self.use_tpu:
            return
        return self.epochs_to_steps(num_epochs=1, mode=_EVAL)

    @property
    def train_increment_str(self):
        if self._single_iteration_train_steps:
            return '{} steps.'.format(self._single_iteration_train_steps)
        else:
            return self.use_tpu or '{} epochs.'.format(self._single_iteration_train_epochs)
        return '~{} epochs. ({} steps)'.format(self._single_iteration_train_epochs, self.single_iteration_train_steps)

    @property
    def repeat_dataset(self):
        if self._single_iteration_train_epochs is None:
            if self._single_iteration_train_steps > NUM_EXAMPLES[_TRAIN]:
                return math.ceil(self._single_iteration_train_steps / NUM_EXAMPLES[_TRAIN])
        return self._single_iteration_train_epochs

    def epochs_to_steps(self, num_epochs, mode):
        """Converts a number of epochs to a number of training steps.

    TPU only: This function assumes that static_batch is True.

      TPU can not tolerate an OutOfRange error from a dataset. As a result the
    number of examples to be processed must be known ahead of time. TPUs also
    do not allow partial batches, so this function rounds down.

    Args:
      num_epochs: An integer of the number of epochs to convert to steps.
      mode: The estimator ModeKey of the computation

    Returns:
      An integer of the number of equivalent steps rounded down.
    """
        assert self.use_tpu, 'epochs_to_steps should only be reached when using TPU'
        total_num_tokens = NUM_EXAMPLES[mode] * self.max_length * num_epochs
        return total_num_tokens // self.batch_size
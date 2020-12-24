# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/utils/logs/hooks.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 4999 bytes
"""Hook that counts examples per second every N steps or seconds."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
from official.utils.logs import logger

class ExamplesPerSecondHook(tf.estimator.SessionRunHook):
    __doc__ = 'Hook to print out examples per second.\n\n  Total time is tracked and then divided by the total number of steps\n  to get the average step time and then batch_size is used to determine\n  the running average of examples per second. The examples per second for the\n  most recent interval is also logged.\n  '

    def __init__(self, batch_size, every_n_steps=None, every_n_secs=None, warm_steps=0, metric_logger=None):
        """Initializer for ExamplesPerSecondHook.

    Args:
      batch_size: Total batch size across all workers used to calculate
        examples/second from global time.
      every_n_steps: Log stats every n steps.
      every_n_secs: Log stats every n seconds. Exactly one of the
        `every_n_steps` or `every_n_secs` should be set.
      warm_steps: The number of steps to be skipped before logging and running
        average calculation. warm_steps steps refers to global steps across all
        workers, not on each worker
      metric_logger: instance of `BenchmarkLogger`, the benchmark logger that
          hook should use to write the log. If None, BaseBenchmarkLogger will
          be used.

    Raises:
      ValueError: if neither `every_n_steps` or `every_n_secs` is set, or
      both are set.
    """
        if (every_n_steps is None) == (every_n_secs is None):
            raise ValueError('exactly one of every_n_steps and every_n_secs should be provided.')
        self._logger = metric_logger or logger.BaseBenchmarkLogger()
        self._timer = tf.estimator.SecondOrStepTimer(every_steps=every_n_steps,
          every_secs=every_n_secs)
        self._step_train_time = 0
        self._total_steps = 0
        self._batch_size = batch_size
        self._warm_steps = warm_steps
        self.current_examples_per_sec_list = []

    def begin(self):
        """Called once before using the session to check global step."""
        self._global_step_tensor = tf.compat.v1.train.get_global_step()
        if self._global_step_tensor is None:
            raise RuntimeError('Global step should be created to use StepCounterHook.')

    def before_run(self, run_context):
        """Called before each call to run().

    Args:
      run_context: A SessionRunContext object.

    Returns:
      A SessionRunArgs object or None if never triggered.
    """
        return tf.estimator.SessionRunArgs(self._global_step_tensor)

    def after_run(self, run_context, run_values):
        """Called after each call to run().

    Args:
      run_context: A SessionRunContext object.
      run_values: A SessionRunValues object.
    """
        global_step = run_values.results
        if self._timer.should_trigger_for_step(global_step):
            if global_step > self._warm_steps:
                elapsed_time, elapsed_steps = self._timer.update_last_triggered_step(global_step)
                if elapsed_time is not None:
                    self._step_train_time += elapsed_time
                    self._total_steps += elapsed_steps
                    average_examples_per_sec = self._batch_size * (self._total_steps / self._step_train_time)
                    current_examples_per_sec = self._batch_size * (elapsed_steps / elapsed_time)
                    self.current_examples_per_sec_list.append(current_examples_per_sec)
                    self._logger.log_metric('average_examples_per_sec',
                      average_examples_per_sec, global_step=global_step)
                    self._logger.log_metric('current_examples_per_sec',
                      current_examples_per_sec, global_step=global_step)
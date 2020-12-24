# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/utils/logs/metric_hook.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 4026 bytes
"""Session hook for logging benchmark metric."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf

class LoggingMetricHook(tf.estimator.LoggingTensorHook):
    __doc__ = 'Hook to log benchmark metric information.\n\n  This hook is very similar as tf.train.LoggingTensorHook, which logs given\n  tensors every N local steps, every N seconds, or at the end. The metric\n  information will be logged to given log_dir or via metric_logger in JSON\n  format, which can be consumed by data analysis pipeline later.\n\n  Note that if `at_end` is True, `tensors` should not include any tensor\n  whose evaluation produces a side effect such as consuming additional inputs.\n  '

    def __init__(self, tensors, metric_logger=None, every_n_iter=None, every_n_secs=None, at_end=False):
        """Initializer for LoggingMetricHook.

    Args:
      tensors: `dict` that maps string-valued tags to tensors/tensor names,
          or `iterable` of tensors/tensor names.
      metric_logger: instance of `BenchmarkLogger`, the benchmark logger that
          hook should use to write the log.
      every_n_iter: `int`, print the values of `tensors` once every N local
          steps taken on the current worker.
      every_n_secs: `int` or `float`, print the values of `tensors` once every N
          seconds. Exactly one of `every_n_iter` and `every_n_secs` should be
          provided.
      at_end: `bool` specifying whether to print the values of `tensors` at the
          end of the run.

    Raises:
      ValueError:
        1. `every_n_iter` is non-positive, or
        2. Exactly one of every_n_iter and every_n_secs should be provided.
        3. Exactly one of log_dir and metric_logger should be provided.
    """
        super(LoggingMetricHook, self).__init__(tensors=tensors,
          every_n_iter=every_n_iter,
          every_n_secs=every_n_secs,
          at_end=at_end)
        if metric_logger is None:
            raise ValueError('metric_logger should be provided.')
        self._logger = metric_logger

    def begin(self):
        super(LoggingMetricHook, self).begin()
        self._global_step_tensor = tf.compat.v1.train.get_global_step()
        if self._global_step_tensor is None:
            raise RuntimeError('Global step should be created to use LoggingMetricHook.')
        if self._global_step_tensor.name not in self._current_tensors:
            self._current_tensors[self._global_step_tensor.name] = self._global_step_tensor

    def after_run(self, unused_run_context, run_values):
        if self._should_trigger:
            self._log_metric(run_values.results)
        self._iter_count += 1

    def end(self, session):
        if self._log_at_end:
            values = session.run(self._current_tensors)
            self._log_metric(values)

    def _log_metric(self, tensor_values):
        self._timer.update_last_triggered_step(self._iter_count)
        global_step = tensor_values[self._global_step_tensor.name]
        for tag in self._tag_order:
            self._logger.log_metric(tag, (tensor_values[tag]), global_step=global_step)
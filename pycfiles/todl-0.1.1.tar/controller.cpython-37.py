# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/staging/training/controller.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 13999 bytes
"""A light weight utilities to train TF2 models."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import time
from absl import logging
import tensorflow.compat.v2 as tf
from typing import Callable, Dict, Optional, Text
from official.staging.training import utils

class Controller(object):
    __doc__ = 'Class that facilitates training and evaluation of models.'

    def __init__(self, strategy: Optional[tf.distribute.Strategy]=None, train_fn: Optional[Callable[([tf.Tensor], Optional[Dict[(Text, tf.Tensor)]])]]=None, eval_fn: Optional[Callable[([tf.Tensor], Optional[Dict[(Text, tf.Tensor)]])]]=None, global_step: Optional[tf.Variable]=None, train_steps: Optional[int]=None, steps_per_loop: Optional[int]=None, summary_dir: Optional[Text]=None, checkpoint_manager: Optional[tf.train.CheckpointManager]=None, summary_interval: Optional[int]=None, eval_summary_dir: Optional[Text]=None, eval_steps: Optional[int]=None, eval_interval: Optional[int]=None):
        """Constructs a `Controller` instance.

    Args:
      strategy: An instance of `tf.distribute.Strategy`.
      train_fn: A callable defined as `def train_fn(num_steps)`, which
        `num_steps` indicates the number of steps to run for each loop.
      eval_fn: A callable defined as `def eval_fn(num_steps)`, which `num_steps`
        indicates the number of steps for one evaluation.
      global_step: An integer `tf.Variable` indicating the global training step
        number. Usually this can be obtained from `iterations` property of the
        model's optimizer (e.g. `self.optimizer.iterations`), or users can
        create their own global step variable as well. If the users create their
        own global step variable, it is recommended to create the `tf.Variable`
        inside strategy scope, and with
        `aggregation=tf.VariableAggregation.ONLY_FIRST_REPLICA`.
      train_steps: The total (maximum) number of training steps to perform.
      steps_per_loop: The number of steps to run in each "inner loop" of
        training (passed to the `num_steps` parameter of `train_fn`).
      summary_dir: The directory to restore and write checkpoints and summaries.
        If None, it will be set to `checkpoint_manager.directory`.
      checkpoint_manager: An instance of `tf.train.CheckpointManager`.
      summary_interval: Step interval for training summaries. Note that this
        argument only applies to the summaries outside the training loop. If the
        value is None, then training summaries are not enabled.
      eval_summary_dir: The directory to write eval summaries. If None, it will
        be set to `summary_dir`.
      eval_steps: Number of steps to run evaluation.
      eval_interval: Step interval for evaluation. If None, will skip evaluation
        in the middle of training. Note that evaluation only happens outside the
        training loop, which the loop iteration is specify by `steps_per_loop`
        parameter.

    Raises:
      ValueError: If both `train_fn` and `eval_fn` are None.
      ValueError: If `train_fn` is not None and `train_steps` is None.
      ValueError: If `steps_per_loop` is None when `train_fn` is provided.
      ValueError: If `steps_per_loop` is not a positive integer.
    """
        if train_fn is None:
            if eval_fn is None:
                raise ValueError('`train_fn` and `eval_fn` should not both be None')
            elif train_fn is not None:
                if train_steps is None:
                    raise ValueError('`train_steps` is required when `train_fn` is provided.')
                if steps_per_loop is None:
                    raise ValueError('`steps_per_loop` is required when `train_fn is provided.')
                if not isinstance(steps_per_loop, int) or steps_per_loop < 1:
                    raise ValueError('`steps_per_loop` should be a positive integer')
            if summary_interval is not None:
                if summary_interval <= 0:
                    raise ValueError('`summary_interval` should be larger than 0')
            self.strategy = strategy or tf.distribute.get_strategy()
            self.train_fn = train_fn
            self.eval_fn = eval_fn
            self.global_step = global_step
            self.checkpoint_manager = checkpoint_manager
            if self.train_fn is not None:
                self.train_steps = train_steps
                self.steps_per_loop = steps_per_loop
                if summary_dir:
                    self.summary_dir = summary_dir
                else:
                    if checkpoint_manager:
                        self.summary_dir = checkpoint_manager.directory
                    else:
                        self.summary_dir = None
                self.summary_interval = summary_interval
                if self.summary_dir and self.summary_interval:
                    summary_writer = tf.summary.create_file_writer(self.summary_dir)
                else:
                    summary_writer = None
                self.summary_manager = utils.SummaryManager(summary_writer,
                  (tf.summary.scalar),
                  global_step=(self.global_step),
                  summary_interval=(self.summary_interval))
            if self.eval_fn is not None:
                eval_summary_dir = eval_summary_dir or self.summary_dir
                eval_summary_writer = tf.summary.create_file_writer(eval_summary_dir) if eval_summary_dir else None
                self.eval_summary_manager = utils.SummaryManager(eval_summary_writer,
                  (tf.summary.scalar), global_step=(self.global_step))
                self.eval_steps = eval_steps
                self.eval_interval = eval_interval
                self.eval_trigger = utils.IntervalTrigger(self.eval_interval, self.global_step.numpy())
            if self.global_step:
                tf.summary.experimental.set_step(self.global_step)
        elif self.checkpoint_manager is not None:
            model_restored = self._restore_model()
            if not model_restored:
                if self.checkpoint_manager.checkpoint_interval:
                    ckpt_path = self.checkpoint_manager.save(checkpoint_number=(self.global_step))
                    logging.info('Saved checkpoins in %s', ckpt_path)

    def _restore_model(self, checkpoint_path=None):
        """Restore or initialize the model.

    Args:
      checkpoint_path: An optional string indicates the checkpoint path to
        restore. If None, will restore from `self.checkpoint_manager`.

    Returns:
      True if the latest checkpoint is found or restored. Otherwise False.
    """
        with self.strategy.scope():
            if checkpoint_path is not None:
                self.checkpoint_manager.checkpoint.restore(checkpoint_path)
                return True
            return self.checkpoint_manager.restore_or_initialize()

    def _evaluate_once(self, current_step):
        """Runs the evaluation once."""
        logging.info('Start evaluation at step: %s', current_step)
        with self.eval_summary_manager.summary_writer.as_default():
            eval_outputs = self.eval_fn(self.eval_steps)
        if eval_outputs:
            eval_outputs = tf.nest.map_structure(lambda x: x.numpy(), eval_outputs)
        info = 'step: {}        evaluation metric: {}'.format(current_step, eval_outputs)
        self._log_info(info)
        self.eval_summary_manager.write_summaries(eval_outputs)
        self.eval_summary_manager.flush()

    def _maybe_save_checkpoints(self, current_step, force_trigger=False):
        if self.checkpoint_manager:
            if self.checkpoint_manager.checkpoint_interval:
                ckpt_path = self.checkpoint_manager.save(checkpoint_number=current_step,
                  check_interval=(not force_trigger))
                if ckpt_path is not None:
                    logging.info('Saved checkpoins in %s', ckpt_path)

    def _maybe_evaluate(self, current_step, force_trigger=False):
        if self.eval_trigger(current_step, force_trigger):
            self._evaluate_once(current_step)

    def _log_info(self, message):
        """Logs `message` to the `info` log, and also prints to stdout."""
        logging.info(message)
        print(message)

    def train(self, evaluate=True):
        """Runs the training, with optional evaluation.

    This handles evaluation, gathering summaries, and saving checkpoints.

    Args:
      evaluate: A boolean indicates whether to perform evaluation during
        training.

    Raises:
      RuntimeError: If `global_step` is not updated correctly in `train_fn`.
    """
        if self.train_fn is None:
            raise ValueError('`self.train_fn` is required when calling `train` method.')
        else:
            if self.global_step is None:
                raise ValueError('`self.global_step` is required when calling `train` method.')
            if evaluate and self.eval_fn is None:
                raise ValueError('`self.eval_fn` is required when calling `train` method with `evaluate=True`')
        step_timer = _StepTimer(self.global_step)
        current_step = self.global_step.numpy()
        logging.info('Train at step %s of %s', current_step, self.train_steps)
        while current_step < self.train_steps:
            steps_per_loop = min(self.train_steps - current_step, self.steps_per_loop)
            logging.info('Entering training loop with %s steps, at step %s of %s', steps_per_loop, current_step, self.train_steps)
            current_step += steps_per_loop
            steps_per_loop = tf.convert_to_tensor(steps_per_loop, dtype=(tf.int32))
            with self.summary_manager.summary_writer.as_default():
                train_outputs = self.train_fn(steps_per_loop)
            if current_step != self.global_step.numpy():
                raise RuntimeError('`self.train_fn` is not updating `global_step` correctly, expected: %s, actual: %s' % (
                 current_step, self.global_step.numpy()))
            if train_outputs:
                train_outputs = tf.nest.map_structure(lambda x: x.numpy(), train_outputs)
            steps_per_second = step_timer.steps_per_second()
            info = 'step: {}        steps_per_second: {:.2f}        {}'.format(current_step, steps_per_second, train_outputs)
            self._log_info(info)
            train_outputs = train_outputs or {}
            train_outputs['steps_per_second'] = steps_per_second
            self.summary_manager.write_summaries(train_outputs)
            self._maybe_save_checkpoints(current_step)
            if evaluate:
                self._maybe_evaluate(current_step)

        self.summary_manager.write_summaries(train_outputs, always_write=True)
        self.summary_manager.flush()
        self._maybe_save_checkpoints(current_step, force_trigger=True)
        if evaluate:
            self._maybe_evaluate(current_step, force_trigger=True)

    def evaluate(self, continuous=False, timeout_fn=None):
        """Runs the evaluation.

    Args:
      continuous: If `True`, will continously monitor the checkpoint directory
        to evaluate on the latest checkpoint. If `False`, will do the evaluation
        once.
      timeout_fn: Optional callable to call after a timeout. If the function
        returns True, then it means that no new checkpoints will be generated
        and the iterator will exit.

    Raises:
      ValueError: If no checkpoint found in `self.checkpoint_manager.directory`.
    """
        if self.eval_fn is None:
            raise ValueError('`self.eval_fn` should not be None to call `evaluate()` method.')
        else:
            if not continuous:
                if timeout_fn is not None:
                    raise ValueError('`timeout_fn` can be only passed when `continuous` is True')
            if continuous:
                for checkpoint_path in tf.train.checkpoints_iterator((self.checkpoint_manager.directory), timeout_fn=timeout_fn):
                    self._restore_model(checkpoint_path)
                    self._evaluate_once(self.global_step.numpy())

                return
            latest_checkpoint = self.checkpoint_manager.latest_checkpoint
            assert latest_checkpoint, 'no checkpoint found in dir %s' % self.checkpoint_manager.directory
        self._restore_model()
        self._evaluate_once(self.global_step.numpy())


class _StepTimer(object):
    __doc__ = 'Utility class for measuring steps/second.'

    def __init__(self, step):
        self.step = step
        self.start()

    def start(self):
        self.last_iteration = self.step.numpy()
        self.last_time = time.time()

    def steps_per_second(self, restart=True):
        value = (self.step.numpy() - self.last_iteration) / (time.time() - self.last_time)
        if restart:
            self.start()
        return value
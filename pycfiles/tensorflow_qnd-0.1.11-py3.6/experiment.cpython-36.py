# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qnd/experiment.py
# Compiled at: 2017-05-20 06:01:46
# Size of source mod 2**32: 1781 bytes
import tensorflow as tf
from .flag import FlagAdder
from .estimator import def_estimator
from .inputs import def_def_train_input_fn, def_def_eval_input_fn

def def_def_experiment_fn(batch_inputs=True, prepare_filename_queues=True, distributed=False):
    adder = FlagAdder()
    for mode in [tf.contrib.learn.ModeKeys.TRAIN,
     tf.contrib.learn.ModeKeys.EVAL]:
        adder.add_flag(('{}_steps'.format(mode)),
          type=int,
          default=(100 if mode == tf.contrib.learn.ModeKeys.EVAL else None),
          help=('Maximum number of {} steps'.format(mode)))

    adder.add_flag('min_eval_frequency',
      type=int, default=1, help='Minimum evaluation frequency in number of train steps')
    estimator = def_estimator(distributed)
    def_train_input_fn = def_def_train_input_fn(batch_inputs, prepare_filename_queues)
    def_eval_input_fn = def_def_eval_input_fn(batch_inputs, prepare_filename_queues)

    def def_experiment_fn(model_fn, train_input_fn, eval_input_fn=None, serving_input_fn=None):

        def experiment_fn(output_dir):
            return (tf.contrib.learn.Experiment)(
 estimator(model_fn, output_dir),
 def_train_input_fn(train_input_fn),
 def_eval_input_fn(eval_input_fn or train_input_fn), export_strategies=serving_input_fn and [
                                 tf.contrib.learn.make_export_strategy(serving_input_fn)], **adder.flags)

        return experiment_fn

    return def_experiment_fn
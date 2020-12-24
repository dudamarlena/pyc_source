# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qnd/evaluate.py
# Compiled at: 2017-05-17 13:39:44
# Size of source mod 2**32: 1206 bytes
from .estimator import def_estimator
from .flag import FLAGS, add_output_dir_flag
from .inputs import def_def_infer_input_fn

def def_evaluate(batch_inputs=True, prepare_filename_queues=True):
    """Define `evaluate()` function.

    See also `help(def_evaluate())`.

    - Args
        - `batch_inputs`: Same as `def_train_and_evaluate()`'s.
        - `prepare_filename_queues`: Same as `def_train_and_evaluate()`'s.

    - Returns
        - `evaluate()` function.
    """
    add_output_dir_flag()
    estimator = def_estimator(distributed=False)
    def_eval_input_fn = def_def_infer_input_fn(batch_inputs, prepare_filename_queues)

    def evaluate(model_fn, input_fn):
        return estimator(model_fn, FLAGS.output_dir).evaluate(input_fn=(def_eval_input_fn(input_fn)))

    return evaluate
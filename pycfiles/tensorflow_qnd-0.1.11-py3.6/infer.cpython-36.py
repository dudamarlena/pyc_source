# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qnd/infer.py
# Compiled at: 2017-05-19 02:34:43
# Size of source mod 2**32: 1297 bytes
from .estimator import def_estimator
from .flag import FLAGS, add_output_dir_flag
from .inputs import def_def_infer_input_fn

def def_infer(batch_inputs=True, prepare_filename_queues=True):
    """Define `infer()` function.

    See also `help(def_infer())`.

    - Args
        - `batch_inputs`: Same as `def_train_and_evaluate()`'s.
        - `prepare_filename_queues`: Same as `def_train_and_evaluate()`'s.

    - Returns
        - `infer()` function.
    """
    add_output_dir_flag()
    estimator = def_estimator(distributed=False)
    def_infer_input_fn = def_def_infer_input_fn(batch_inputs, prepare_filename_queues)

    def infer(model_fn, input_fn):
        return estimator(model_fn, FLAGS.output_dir).predict(input_fn=(def_infer_input_fn(input_fn)))

    return infer
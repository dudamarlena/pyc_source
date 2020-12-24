# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/contrib/callbacks/stop_if_unfeasible.py
# Compiled at: 2019-06-18 16:53:11
# Size of source mod 2**32: 2000 bytes
import time, tensorflow as tf

class StopIfUnfeasible(tf.keras.callbacks.Callback):

    def __init__(self, time_limit=600, patience=20):
        super().__init__()
        self.time_limit = time_limit
        self.timing = list()
        self.stopped = False
        self.patience = patience

    def set_params(self, params):
        self.params = params
        if self.params['steps'] is None:
            self.steps = self.params['samples'] // self.params['batch_size']
            self.steps = self.params['samples'] // self.params['batch_size']
        else:
            if self.steps * self.params['batch_size'] < self.params['samples']:
                self.steps += 1
            else:
                self.steps = self.params['steps']

    def on_batch_begin(self, batch, logs=None):
        """Called at the beginning of a training batch in `fit` methods.
        Subclasses should override for any actions to run.
        # Arguments
            batch: integer, index of batch within the current epoch.
            logs: dict, has keys `batch` and `size` representing the current
                batch number and the size of the batch.
        """
        self.timing.append(time.time())

    def on_batch_end(self, batch, logs=None):
        """Called at the end of a training batch in `fit` methods.
        Subclasses should override for any actions to run.
        # Arguments
            batch: integer, index of batch within the current epoch.
            logs: dict, metric results for this batch.
        """
        self.timing[-1] = time.time() - self.timing[(-1)]
        self.avr_batch_time = sum(self.timing) / len(self.timing)
        self.estimate_training_time = sum(self.timing) + self.avr_batch_time * (self.steps - len(self.timing))
        if len(self.timing) >= self.patience:
            if self.estimate_training_time > self.time_limit:
                self.stopped = True
                self.model.stop_training = True
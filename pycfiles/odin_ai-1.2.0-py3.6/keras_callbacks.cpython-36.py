# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/backend/keras_callbacks.py
# Compiled at: 2019-08-29 18:11:54
# Size of source mod 2**32: 5241 bytes
from __future__ import absolute_import, division, print_function
import numpy as np
from tensorflow.python.keras.callbacks import Callback
from tensorflow.python.platform import tf_logging as logging

class EarlyStopping(Callback):
    __doc__ = ' Original implementation from keras, copied here with some\n  improvement.\n\n  Stop training when a monitored quantity has stopped improving.\n\n  Arguments:\n      monitor: Quantity to be monitored.\n      min_delta: Minimum change in the monitored quantity\n          to qualify as an improvement, i.e. an absolute\n          change of less than min_delta, will count as no\n          improvement.\n      patience: Number of epochs with no improvement\n          after which training will be stopped.\n      verbose: verbosity mode.\n      mode: One of `{"auto", "min", "max"}`. In `min` mode,\n          training will stop when the quantity\n          monitored has stopped decreasing; in `max`\n          mode it will stop when the quantity\n          monitored has stopped increasing; in `auto`\n          mode, the direction is automatically inferred\n          from the name of the monitored quantity.\n      baseline: Baseline value for the monitored quantity.\n          Training will stop if the model doesn\'t show improvement over the\n          baseline.\n      restore_best_weights: Whether to restore model weights from\n          the epoch with the best value of the monitored quantity.\n          If False, the model weights obtained at the last step of\n          training are used.\n\n  Example:\n\n  ```python\n  callback = tf.keras.callbacks.EarlyStopping(monitor=\'val_loss\', patience=3)\n  # This callback will stop the training when there is no improvement in\n  # the validation loss for three consecutive epochs.\n  model.fit(data, labels, epochs=100, callbacks=[callback],\n      validation_data=(val_data, val_labels))\n  ```\n  '

    def __init__(self, monitor='val_loss', min_delta=0, patience=0, verbose=0, mode='auto', baseline=None, terminate_on_nan=True, restore_best_weights=False):
        super(EarlyStopping, self).__init__()
        self.monitor = monitor
        self.patience = patience
        self.verbose = verbose
        self.baseline = baseline
        self.min_delta = abs(min_delta)
        self.wait = 0
        self.stopped_epoch = 0
        self.terminate_on_nan = bool(terminate_on_nan)
        self.restore_best_weights = restore_best_weights
        self.best_weights = None
        self.best_epoch = None
        if mode not in ('auto', 'min', 'max'):
            logging.warning('EarlyStopping mode %s is unknown, fallback to auto mode.', mode)
            mode = 'auto'
        else:
            if mode == 'min':
                self.monitor_op = np.less
            else:
                if mode == 'max':
                    self.monitor_op = np.greater
                else:
                    if 'acc' in self.monitor:
                        self.monitor_op = np.greater
                    else:
                        self.monitor_op = np.less
            if self.monitor_op == np.greater:
                self.min_delta *= 1
            else:
                self.min_delta *= -1

    def on_train_begin(self, logs=None):
        self.wait = 0
        self.stopped_epoch = 0
        if self.baseline is not None:
            self.best = self.baseline
        else:
            self.best = np.Inf if self.monitor_op == np.less else -np.Inf

    def on_batch_end(self, batch, logs=None):
        logs = logs or {}
        loss = logs.get('loss')
        if loss is not None:
            if np.isnan(loss) or np.isinf(loss):
                if self.terminate_on_nan:
                    print('Batch %d: Invalid loss, terminating training' % batch)
                    self.model.stop_training = True
                if self.restore_best_weights:
                    if self.best_weights is not None:
                        if self.verbose > 0:
                            print('Restoring model weights from the end of the best epoch #%d.' % self.best_epoch)
                        self.model.set_weights(self.best_weights)

    def on_epoch_end(self, epoch, logs=None):
        current = self.get_monitor_value(logs)
        if current is None:
            return
        if self.monitor_op(current - self.min_delta, self.best):
            self.best = current
            self.wait = 0
            if self.restore_best_weights:
                self.best_weights = self.model.get_weights()
                self.best_epoch = epoch
        else:
            self.wait += 1
        if self.wait >= self.patience:
            self.stopped_epoch = epoch
            self.model.stop_training = True
            if self.restore_best_weights:
                if self.verbose > 0:
                    print('Restoring model weights from the end of the best epoch #%d.' % self.best_epoch)
                self.model.set_weights(self.best_weights)

    def on_train_end(self, logs=None):
        if self.stopped_epoch > 0:
            if self.verbose > 0:
                print('Epoch %05d: early stopping' % (self.stopped_epoch + 1))

    def get_monitor_value(self, logs):
        logs = logs or {}
        monitor_value = logs.get(self.monitor)
        if monitor_value is None:
            logging.warning('Early stopping conditioned on metric `%s` which is not available. Available metrics are: %s', self.monitor, ','.join(list(logs.keys())))
        return monitor_value
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/contrib/callbacks/beholder.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 682 bytes
import tensorflow as tf
from tensorboard.plugins.beholder import Beholder

class BeholderCB(tf.keras.callbacks.Callback):
    __doc__ = 'Keras callback for tensorboard beholder plugin: https://github.com/tensorflow/tensorboard/tree/master/tensorboard/plugins/beholder\n\n    Args:\n        logdir (str): path to the tensorboard log directory.\n        sess: tensorflow session.\n    '

    def __init__(self, logdir, sess):
        super(BeholderCB, self).__init__()
        self.beholder = Beholder(logdir=logdir)
        self.session = sess

    def on_epoch_end(self, epoch, logs=None):
        super(BeholderCB, self).on_epoch_end(epoch, logs)
        self.beholder.update(session=(self.session))
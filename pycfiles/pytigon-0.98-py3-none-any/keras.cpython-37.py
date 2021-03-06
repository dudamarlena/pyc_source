# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-6brxc_kc/tqdm/tqdm/keras.py
# Compiled at: 2020-03-24 13:42:06
# Size of source mod 2**32: 3454 bytes
from __future__ import absolute_import, division
from .auto import tqdm as tqdm_auto
from copy import deepcopy
try:
    import keras
except ImportError as e:
    try:
        try:
            from tensorflow import keras
        except ImportError:
            raise e

    finally:
        e = None
        del e

__author__ = {'github.com/': ['casperdcl']}
__all__ = ['TqdmCallback']

class TqdmCallback(keras.callbacks.Callback):
    __doc__ = '`keras` callback for epoch and batch progress'

    @staticmethod
    def bar2callback(bar, pop=None, delta=lambda logs: 1):

        def callback(_, logs=None):
            n = delta(logs)
            if logs:
                if pop:
                    logs = deepcopy(logs)
                    [logs.pop(i, 0) for i in pop]
                bar.set_postfix(logs, refresh=False)
            bar.update(n)

        return callback

    def __init__(self, epochs=None, data_size=None, batch_size=None, verbose=1, tqdm_class=tqdm_auto):
        """
        Parameters
        ----------
        epochs  : int, optional
        data_size  : int, optional
            Number of training pairs.
        batch_size  : int, optional
            Number of training pairs per batch.
        verbose  : int
            0: epoch, 1: batch (transient), 2: batch. [default: 1].
            Will be set to `0` unless both `data_size` and `batch_size`
            are given.
        tqdm_class : optional
            `tqdm` class to use for bars [default: `tqdm.auto.tqdm`].
        """
        self.tqdm_class = tqdm_class
        self.epoch_bar = tqdm_class(total=epochs, unit='epoch')
        self.on_epoch_end = self.bar2callback(self.epoch_bar)
        if data_size and batch_size:
            self.batches = batches = (data_size + batch_size - 1) // batch_size
        else:
            self.batches = batches = None
        self.verbose = verbose
        if verbose == 1:
            self.batch_bar = tqdm_class(total=batches, unit='batch', leave=False)
            self.on_batch_end = self.bar2callback((self.batch_bar),
              pop=[
             'batch', 'size'],
              delta=(lambda logs: logs.get('size', 1)))

    def on_train_begin(self, *_, **__):
        params = self.params.get
        auto_total = params('epochs', params('nb_epoch', None))
        if auto_total is not None:
            self.epoch_bar.reset(total=auto_total)

    def on_epoch_begin(self, *_, **__):
        if self.verbose:
            params = self.params.get
            total = params('samples', params('nb_sample', params('steps', None))) or self.batches
            if self.verbose == 2:
                if hasattr(self, 'batch_bar'):
                    self.batch_bar.close()
                self.batch_bar = self.tqdm_class(total=total,
                  unit='batch',
                  leave=True,
                  unit_scale=(1 / (params('batch_size', 1) or 1)))
                self.on_batch_end = self.bar2callback((self.batch_bar),
                  pop=[
                 'batch', 'size'],
                  delta=(lambda logs: logs.get('size', 1)))
            else:
                if self.verbose == 1:
                    self.batch_bar.unit_scale = 1 / (params('batch_size', 1) or 1)
                    self.batch_bar.reset(total=total)
                else:
                    raise KeyError('Unknown verbosity')

    def on_train_end(self, *_, **__):
        if self.verbose:
            self.batch_bar.close()
        self.epoch_bar.close()
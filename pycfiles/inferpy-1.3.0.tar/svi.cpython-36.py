# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/inference/svi.py
# Compiled at: 2019-05-25 14:16:51
# Size of source mod 2**32: 4179 bytes
import tensorflow as tf, inspect, itertools
from . import loss_functions
import inferpy as inf
from inferpy import util
from inferpy import contextmanager

class SVI:

    def __init__(self, qmodel, loss='ELBO', optimizer='AdamOptimizer', batch_size=100, epochs=1000):
        if callable(qmodel):
            if len(inspect.signature(qmodel).parameters) > 0:
                raise ValueError('input qmodel can only be a callable object if this does not has any input parameter')
            self.qmodel = qmodel()
        else:
            self.qmodel = qmodel
        if isinstance(loss, str):
            self.loss_fn = getattr(loss_functions, loss)
        else:
            self.loss_fn = loss
        self.batch_size = batch_size
        self.epochs = epochs
        if isinstance(optimizer, str):
            self.optimizer = getattr(tf.train, optimizer)()
        else:
            self.optimizer = optimizer
        self._SVI__losses = []

    def run(self, pmodel, sample_dict):
        plate_size = util.iterables.get_plate_size(pmodel.vars, sample_dict)
        batches = int(plate_size / self.batch_size)
        batch_weight = self.batch_size / plate_size
        tfdataset = tf.data.Dataset.from_tensor_slices(sample_dict).shuffle(plate_size).batch((self.batch_size),
          drop_remainder=True).repeat()
        iterator = tfdataset.make_one_shot_iterator()
        input_data = iterator.get_next()
        loss_tensor = self.loss_fn(pmodel, (self.qmodel), plate_size=(self.batch_size), batch_weight=batch_weight)
        train = self.optimizer.minimize(loss_tensor)
        t = []
        sess = inf.get_session()
        model_variables = set([v for v in itertools.chain(pmodel.params.values(), (pmodel._last_expanded_params or {}).values(), (pmodel._last_fitted_params or {}).values(), self.qmodel.params.values(), (self.qmodel._last_expanded_params or {}).values(), (self.qmodel._last_fitted_params or {}).values())])
        sess.run(tf.variables_initializer([v for v in tf.global_variables() if v not in model_variables if not v.name.startswith('inferpy-')]))
        for i in range(self.epochs):
            for j in range(batches):
                local_input_data = sess.run(input_data)
                with contextmanager.observe(pmodel._last_expanded_vars, local_input_data):
                    with contextmanager.observe(self.qmodel._last_expanded_vars, local_input_data):
                        sess.run(train)
                        t.append(sess.run(loss_tensor))
                        if i % 200 == 0:
                            print(('\n {} epochs\t {}'.format(i, t[(-1)])), end='', flush=True)
                        if i % 20 == 0:
                            print('.', end='', flush=True)

        self._SVI__losses = t
        return (
         self.qmodel._last_expanded_vars, self.qmodel._last_expanded_params)

    @property
    def losses(self):
        return self._SVI__losses
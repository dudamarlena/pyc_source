# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/inference/vi.py
# Compiled at: 2019-05-24 03:28:16
# Size of source mod 2**32: 3453 bytes
import tensorflow as tf, inspect, itertools
from . import loss_functions
import inferpy as inf
from inferpy import util
from inferpy import contextmanager

class VI:

    def __init__(self, qmodel, loss='ELBO', optimizer='AdamOptimizer', epochs=1000):
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
        self.epochs = epochs
        if isinstance(optimizer, str):
            self.optimizer = getattr(tf.train, optimizer)()
        else:
            self.optimizer = optimizer
        self._VI__losses = []

    def run(self, pmodel, sample_dict):
        plate_size = util.iterables.get_plate_size(pmodel.vars, sample_dict)
        loss_tensor = self.loss_fn(pmodel, (self.qmodel), plate_size=plate_size)
        train = self.optimizer.minimize(loss_tensor)
        t = []
        sess = inf.get_session()
        model_variables = [v for v in itertools.chain(pmodel.params.values(), (pmodel._last_expanded_params or {}).values(), (pmodel._last_fitted_params or {}).values(), self.qmodel.params.values(), (self.qmodel._last_expanded_params or {}).values(), (self.qmodel._last_fitted_params or {}).values())]
        sess.run(tf.variables_initializer([v for v in tf.global_variables() if v not in model_variables if not v.name.startswith('inferpy-')]))
        with contextmanager.observe(pmodel._last_expanded_vars, sample_dict):
            with contextmanager.observe(self.qmodel._last_expanded_vars, sample_dict):
                for i in range(self.epochs):
                    sess.run(train)
                    t.append(sess.run(loss_tensor))
                    if i % 200 == 0:
                        print(('\n {} epochs\t {}'.format(i, t[(-1)])), end='', flush=True)
                    if i % 10 == 0:
                        print('.', end='', flush=True)

        self._VI__losses = t
        return (
         self.qmodel._last_expanded_vars, self.qmodel._last_expanded_params)

    @property
    def losses(self):
        return self._VI__losses
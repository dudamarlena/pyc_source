# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/models/inference/vi.py
# Compiled at: 2019-02-25 10:16:36
# Size of source mod 2**32: 1758 bytes
import tensorflow as tf, inspect
from . import loss_functions

class VI:

    def __init__(self, qmodel, loss='ELBO', optimizer='AdamOptimizer', epochs=1000):
        if callable(qmodel):
            if len(inspect.signature(qmodel).parameters) > 0:
                raise Exception('input qmodel can only be a callable object if this does not has any input parameter')
            self.qmodel = qmodel()
        else:
            self.qmodel
        if isinstance(loss, str):
            self.loss_fn = getattr(loss_functions, loss)
        else:
            self.loss_fn = loss
        self.epochs = epochs
        if isinstance(optimizer, str):
            self.optimizer = getattr(tf.train, optimizer)()
        else:
            self.optimizer = optimizer

    def run(self, pmodel, sample_dict):
        plate_size = pmodel._get_plate_size(sample_dict)
        qvars, qparams = self.qmodel.expand_model(plate_size)
        loss_tensor = self.loss_fn(pmodel, qvars, sample_dict)
        train = self.optimizer.minimize(loss_tensor)
        t = []
        with tf.Session() as (sess):
            sess.run(tf.global_variables_initializer())
            for i in range(self.epochs):
                sess.run(train)
                t.append(sess.run(loss_tensor))
                if i % 200 == 0:
                    print(('\n' + str(t[(-1)])), end='', flush=True)
                if i % 10 == 0:
                    print('.', end='', flush=True)

            params = {n:sess.run(p) for n, p in qparams.items()}
        return params
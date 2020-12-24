# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/external/baselines/baselines/acktr/value_functions.py
# Compiled at: 2018-04-01 14:21:44
# Size of source mod 2**32: 2703 bytes
from baselines import logger
import numpy as np, baselines.common as common
from baselines.common import tf_util as U
import tensorflow as tf
from baselines.acktr import kfac
from baselines.acktr.utils import dense

class NeuralNetValueFunction(object):

    def __init__(self, ob_dim, ac_dim):
        X = tf.placeholder(tf.float32, shape=[None, ob_dim * 2 + ac_dim * 2 + 2])
        vtarg_n = tf.placeholder(tf.float32, shape=[None], name='vtarg')
        wd_dict = {}
        h1 = tf.nn.elu(dense(X, 64, 'h1', weight_init=U.normc_initializer(1.0), bias_init=0, weight_loss_dict=wd_dict))
        h2 = tf.nn.elu(dense(h1, 64, 'h2', weight_init=U.normc_initializer(1.0), bias_init=0, weight_loss_dict=wd_dict))
        vpred_n = dense(h2, 1, 'hfinal', weight_init=U.normc_initializer(1.0), bias_init=0, weight_loss_dict=wd_dict)[:, 0]
        sample_vpred_n = vpred_n + tf.random_normal(tf.shape(vpred_n))
        wd_loss = tf.get_collection('vf_losses', None)
        loss = tf.reduce_mean(tf.square(vpred_n - vtarg_n)) + tf.add_n(wd_loss)
        loss_sampled = tf.reduce_mean(tf.square(vpred_n - tf.stop_gradient(sample_vpred_n)))
        self._predict = U.function([X], vpred_n)
        optim = kfac.KfacOptimizer(learning_rate=0.001, cold_lr=9.999999999999998e-05, momentum=0.9, clip_kl=0.3, epsilon=0.1, stats_decay=0.95, async=1, kfac_update=2, cold_iter=50, weight_decay_dict=wd_dict, max_grad_norm=None)
        vf_var_list = []
        for var in tf.trainable_variables():
            if 'vf' in var.name:
                vf_var_list.append(var)

        update_op, self.q_runner = optim.minimize(loss, loss_sampled, var_list=vf_var_list)
        self.do_update = U.function([X, vtarg_n], update_op)
        U.initialize()

    def _preproc(self, path):
        l = pathlength(path)
        al = np.arange(l).reshape(-1, 1) / 10.0
        act = path['action_dist'].astype('float32')
        X = np.concatenate([path['observation'], act, al, np.ones((l, 1))], axis=1)
        return X

    def predict(self, path):
        return self._predict(self._preproc(path))

    def fit(self, paths, targvals):
        X = np.concatenate([self._preproc(p) for p in paths])
        y = np.concatenate(targvals)
        logger.record_tabular('EVBefore', common.explained_variance(self._predict(X), y))
        for _ in range(25):
            self.do_update(X, y)

        logger.record_tabular('EVAfter', common.explained_variance(self._predict(X), y))


def pathlength(path):
    return path['reward'].shape[0]
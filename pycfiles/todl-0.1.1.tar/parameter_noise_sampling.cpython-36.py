# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/google/home/rikel/bandits_repo/deep-bayesian-contextual-bandits/research/bandits/algorithms/parameter_noise_sampling.py
# Compiled at: 2018-07-23 14:29:50
# Size of source mod 2**32: 6687 bytes
"""Contextual algorithm based on Thompson Sampling + direct noise injection."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
from scipy.special import logsumexp
import tensorflow as tf
from absl import flags
from bandits.core.bandit_algorithm import BanditAlgorithm
from bandits.core.contextual_dataset import ContextualDataset
from bandits.algorithms.neural_bandit_model import NeuralBanditModel
FLAGS = flags.FLAGS

class ParameterNoiseSampling(BanditAlgorithm):
    __doc__ = 'Parameter Noise Sampling algorithm based on adding noise to net params.\n\n  Described in https://arxiv.org/abs/1706.01905\n  '

    def __init__(self, name, hparams):
        """Creates the algorithm, and sets up the adaptive Gaussian noise."""
        self.name = name
        self.hparams = hparams
        self.verbose = getattr(self.hparams, 'verbose', True)
        self.noise_std = getattr(self.hparams, 'noise_std', 0.005)
        self.eps = getattr(self.hparams, 'eps', 0.05)
        self.d_samples = getattr(self.hparams, 'd_samples', 300)
        self.optimizer = getattr(self.hparams, 'optimizer', 'RMS')
        self.std_h = [
         self.noise_std]
        self.eps_h = [self.eps]
        self.kl_h = []
        self.t = 0
        self.freq_update = hparams.training_freq
        self.num_epochs = hparams.training_epochs
        self.data_h = ContextualDataset(hparams.context_dim, hparams.num_actions, hparams.buffer_s)
        self.bnn = NeuralBanditModel(self.optimizer, hparams, '{}-bnn'.format(name))
        with self.bnn.graph.as_default():
            self.bnn.noise_std_ph = tf.placeholder((tf.float32), shape=())
            tvars = tf.trainable_variables()
            self.bnn.noisy_grads = [tf.random_normal(v.get_shape(), 0, self.bnn.noise_std_ph) for v in tvars]
            with tf.control_dependencies(self.bnn.noisy_grads):
                self.bnn.noise_add_ops = [tvars[i].assign_add(n) for i, n in enumerate(self.bnn.noisy_grads)]
                with tf.control_dependencies(self.bnn.noise_add_ops):
                    self.bnn.noisy_nn, self.bnn.noisy_pred_val = self.bnn.forward_pass()
                    self.bnn.noisy_pred = tf.identity(self.bnn.noisy_pred_val)
                    with tf.control_dependencies([tf.identity(self.bnn.noisy_pred)]):
                        self.bnn.noise_sub_ops = [tvars[i].assign_add(-n) for i, n in enumerate(self.bnn.noisy_grads)]

    def action(self, context):
        """Selects action based on Thompson Sampling *after* adding noise."""
        if self.t < self.hparams.num_actions * self.hparams.initial_pulls:
            return self.t % self.hparams.num_actions
        with self.bnn.graph.as_default():
            c = context.reshape((1, self.hparams.context_dim))
            output, _ = self.bnn.sess.run([
             self.bnn.noisy_pred, self.bnn.noise_sub_ops],
              feed_dict={self.bnn.x: c, 
             self.bnn.noise_std_ph: self.noise_std})
            return np.argmax(output)

    def update(self, context, action, reward):
        """Updates the data buffer, and re-trains the BNN and noise level."""
        self.t += 1
        self.data_h.add(context, action, reward)
        if self.t % self.freq_update == 0:
            self.bnn.train(self.data_h, self.num_epochs)
            self.update_noise()

    def update_noise(self):
        """Increase noise if distance btw original and corrupted distrib small."""
        kl = self.compute_distance()
        delta = -np.log1p(-self.eps + self.eps / self.hparams.num_actions)
        if kl < delta:
            self.noise_std *= 1.01
        else:
            self.noise_std /= 1.01
        self.eps *= 0.99
        if self.verbose:
            print('Update eps={} | kl={} | std={} | delta={} | increase={}.'.format(self.eps, kl, self.noise_std, delta, kl < delta))
        self.std_h.append(self.noise_std)
        self.kl_h.append(kl)
        self.eps_h.append(self.eps)

    def compute_distance(self):
        """Computes empirical KL for original and corrupted output distributions."""
        random_inputs, _ = self.data_h.get_batch(self.d_samples)
        y_model = self.bnn.sess.run((self.bnn.y_pred),
          feed_dict={self.bnn.x: random_inputs, 
         self.bnn.noise_std_ph: self.noise_std})
        y_noisy, _ = self.bnn.sess.run([
         self.bnn.noisy_pred, self.bnn.noise_sub_ops],
          feed_dict={self.bnn.x: random_inputs, 
         self.bnn.noise_std_ph: self.noise_std})
        if self.verbose:
            s = np.sum([np.argmax(y_model[i, :]) == np.argmax(y_noisy[i, :]) for i in range(y_model.shape[0])])
            print('{} | % of agreement btw original / corrupted actions: {}.'.format(self.name, s / self.d_samples))
        kl = self.compute_kl_with_logits(y_model, y_noisy)
        return kl

    def compute_kl_with_logits(self, logits1, logits2):
        """Computes KL from logits samples from two distributions."""

        def exp_times_diff(a, b):
            return np.multiply(np.exp(a), a - b)

        logsumexp1 = logsumexp(logits1, axis=1)
        logsumexp2 = logsumexp(logits2, axis=1)
        logsumexp_diff = logsumexp2 - logsumexp1
        exp_diff = exp_times_diff(logits1, logits2)
        exp_diff = np.sum(exp_diff, axis=1)
        inv_exp_sum = np.sum((np.exp(logits1)), axis=1)
        term1 = np.divide(exp_diff, inv_exp_sum)
        kl = term1 + logsumexp_diff
        kl = np.maximum(kl, 0.0)
        kl = np.nan_to_num(kl)
        return np.mean(kl)
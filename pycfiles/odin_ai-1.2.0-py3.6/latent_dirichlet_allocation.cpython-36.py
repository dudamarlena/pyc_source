# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/bay/mixed_membership/latent_dirichlet_allocation.py
# Compiled at: 2019-07-15 09:21:37
# Size of source mod 2**32: 5038 bytes
from __future__ import print_function, division, absolute_import
import numpy as np, tensorflow as tf
from tensorflow.python.keras import Model, Sequential
from tensorflow.python.keras.layers import Dense, Layer
from tensorflow_probability.python.distributions import softplus_inverse, Dirichlet
from odin.bay.distribution_layers import DirichletLayer, OneHotCategoricalLayer
from odin.bay.helpers import kl_divergence
__all__ = [
 'LatentDirichletAllocation']

class LatentDirichletAllocation(Model):
    __doc__ = ' Variational Latent Dirichlet Allocation\n\n  To maintain good intuition behind the algorithm, we name the\n  attributes as for topics discovery task in natural language\n  processing.\n\n  Parameters\n  ----------\n  n_components : int, optional (default=10)\n    Number of topics in LDA.\n\n  components_prior : float (default=0.7)\n    the topic prior concentration for Dirichlet distribution\n\n  References\n  ----------\n  [1]: David M. Blei, Andrew Y. Ng, Michael I. Jordan. Latent Dirichlet\n       Allocation. In _Journal of Machine Learning Research_, 2003.\n       http://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf\n  [2]: Michael Figurnov, Shakir Mohamed, Andriy Mnih. Implicit Reparameterization\n       Gradients, 2018\n       https://arxiv.org/abs/1805.08498\n  [3]: Akash Srivastava, Charles Sutton. Autoencoding Variational Inference For\n       Topic Models. In _International Conference on Learning Representations_,\n       2017.\n       https://arxiv.org/abs/1703.01488\n  '

    def __init__(self, n_components=10, components_prior=0.7, encoder_layers=[
 64, 64], activation='relu', n_mcmc_samples=1, analytic_kl=True, random_state=None):
        super(LatentDirichletAllocation, self).__init__()
        self._random_state = np.random.RandomState(seed=random_state) if not isinstance(random_state, np.random.RandomState) else random_state
        self._initializer = tf.initializers.GlorotNormal(seed=(self._random_state.randint(100000000.0)))
        self.n_components = int(n_components)
        self.components_prior = np.array(softplus_inverse(components_prior))
        self.n_mcmc_samples = n_mcmc_samples
        self.analytic_kl = analytic_kl
        encoder = Sequential(name='Encoder')
        for num_hidden_units in encoder_layers:
            encoder.add(Dense(num_hidden_units, activation=activation,
              kernel_initializer=(self._initializer)))

        encoder.add(Dense(n_components, activation=(tf.nn.softplus),
          kernel_initializer=(self._initializer),
          name='DenseConcentration'))
        encoder.add(DirichletLayer(clip_for_stable=True, pre_softplus=False,
          name='topics_posterior'))
        self.encoder = encoder
        self.decoder = OneHotCategoricalLayer(probs_input=True,
          name='bag_of_words')

    def build(self, input_shape):
        n_features = input_shape[1]
        self.topics_words_logits = self.add_weight(name='topics_words_logits',
          shape=[
         self.n_components, n_features],
          initializer=(self._initializer))
        self.prior_logit = self.add_weight(name='prior_logit',
          shape=[
         1, self.n_components],
          trainable=False,
          initializer=(tf.initializers.Constant(self.components_prior)))
        super(LatentDirichletAllocation, self).build(input_shape)

    def call(self, inputs):
        docs_topics_posterior = self.encoder(inputs)
        docs_topics_samples = docs_topics_posterior.sample(self.n_mcmc_samples)
        topics_words_probs = tf.nn.softmax((self.topics_words_logits), axis=1)
        docs_words_probs = tf.matmul(docs_topics_samples, topics_words_probs)
        output_dist = self.decoder(tf.clip_by_value(docs_words_probs, 0.0001, 0.9999))
        concentration = tf.clip_by_value(tf.nn.softplus(self.prior_logit), 0.001, 1000.0)
        topics_prior = Dirichlet(concentration=concentration,
          name='topics_prior')
        kl = kl_divergence(q=docs_topics_posterior, p=topics_prior, use_analytic_kl=(self.analytic_kl),
          q_sample=(self.n_mcmc_samples),
          auto_remove_independent=True)
        if self.analytic_kl:
            kl = tf.expand_dims(kl, axis=0)
        llk = output_dist.log_prob(inputs)
        ELBO = llk - kl
        self.add_loss(tf.reduce_mean(-ELBO))
        self.add_metric((tf.reduce_mean(kl)), aggregation='mean', name='MeanKL')
        self.add_metric((tf.reduce_mean(-llk)), aggregation='mean', name='MeanNLLK')
        return output_dist
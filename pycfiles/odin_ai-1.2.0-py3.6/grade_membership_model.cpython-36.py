# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/bay/mixed_membership/grade_membership_model.py
# Compiled at: 2019-07-15 09:21:05
# Size of source mod 2**32: 5332 bytes
from __future__ import print_function, division, absolute_import
import numpy as np, tensorflow as tf
from tensorflow.python.keras import Model, Sequential
from tensorflow.python.keras.layers import Dense, Layer, Concatenate
from tensorflow_probability import distributions as tfd
from tensorflow_probability.python.distributions import softplus_inverse, Dirichlet
from odin.bay.distribution_layers import DirichletLayer, OneHotCategoricalLayer
__all__ = [
 'GradeMembershipModel']

class GradeMembershipModel(Model):
    __doc__ = ' Grade Membership Model\n\n  '

    def __init__(self, n_questions, n_answers, n_components=10, components_prior=0.7, encoder_layers=[
 16, 16], activation='relu', n_mcmc_samples=1, random_state=None):
        super(GradeMembershipModel, self).__init__()
        self._random_state = np.random.RandomState(seed=random_state) if not isinstance(random_state, np.random.RandomState) else random_state
        self._initializer = tf.initializers.GlorotNormal(seed=(self._random_state.randint(100000000.0)))
        self.n_questions = int(n_questions)
        self.n_answers = int(n_answers)
        self.n_components = int(n_components)
        self.components_prior = np.array(softplus_inverse(components_prior))
        self.n_mcmc_samples = n_mcmc_samples
        self.encoder = []
        self.decoder = []
        for question_idx in range(self.n_questions):
            encoder = Sequential(name=('EncoderQ%d' % question_idx))
            for num_hidden_units in encoder_layers:
                encoder.add(Dense(num_hidden_units, activation=activation,
                  kernel_initializer=(self._initializer)))

            encoder.add(Dense(n_components, activation=(tf.nn.softplus),
              kernel_initializer=(self._initializer),
              name='DenseConcentration'))
            encoder.add(DirichletLayer(clip_for_stable=True, pre_softplus=False, name=('topics_posteriorQ%d' % question_idx)))
            setattr(self, 'encoder%d' % question_idx, encoder)
            self.encoder.append(encoder)
            group_answer_logits = self.add_weight(name=('topics_words_logits%d' % question_idx),
              shape=[
             self.n_components, n_answers],
              initializer=(self._initializer))
            decoder = OneHotCategoricalLayer(probs_input=True, name=('AnswerSheetQ%d' % question_idx))
            setattr(self, 'decoder%d' % question_idx, decoder)
            self.decoder.append([group_answer_logits, decoder])

        self.prior_logit = self.add_weight(name='prior_logit',
          shape=[
         1, self.n_components],
          trainable=False,
          initializer=(tf.initializers.Constant(self.components_prior)))

    def call(self, inputs):
        n_questions = inputs.shape[1]
        tf.assert_equal(n_questions, (self.n_questions), message='Number of questions mismatches')
        all_llk = []
        all_kl = []
        all_elbo = []
        outputs = []
        concentration = tf.clip_by_value(tf.nn.softplus(self.prior_logit), 0.001, 1000.0)
        group_prior = Dirichlet(concentration=concentration,
          name='group_prior')
        for question_idx in range(n_questions):
            q = inputs[:, question_idx]
            q = tf.one_hot((tf.cast(q, 'int32')), depth=(self.n_answers))
            encoder = self.encoder[question_idx]
            sheet_group_posterior = encoder(q)
            sheet_group_samples = sheet_group_posterior.sample(self.n_mcmc_samples)
            group_answer_logits, decoder = self.decoder[question_idx]
            group_answer_probs = tf.nn.softmax(group_answer_logits, axis=1)
            sheet_answer_probs = tf.matmul(sheet_group_samples, group_answer_probs)
            output_dist = decoder(tf.clip_by_value(sheet_answer_probs, 0.0001, 0.9999))
            outputs.append(tf.argmax((output_dist.mean()), axis=(-1)))
            kl = tfd.kl_divergence(sheet_group_posterior.distribution, group_prior)
            kl = tf.expand_dims(kl, axis=0)
            llk = output_dist.log_prob(q)
            ELBO = llk - kl
            all_llk.append(llk)
            all_kl.append(kl)
            all_elbo.append(ELBO)

        self.add_loss(tf.reduce_mean(-sum(all_elbo) / self.n_questions))
        self.add_metric((tf.reduce_mean(sum(all_kl) / self.n_questions)), aggregation='mean', name='MeanKL')
        self.add_metric((tf.reduce_mean(-sum(all_llk) / self.n_questions)), aggregation='mean', name='MeanNLLK')
        outputs = tf.concat(outputs, -1)
        return outputs
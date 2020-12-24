# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/aidanrocke/anaconda/envs/py3k/lib/python3.6/site-packages/deep_rectifiers/weight_norm.py
# Compiled at: 2017-06-21 09:45:53
# Size of source mod 2**32: 8588 bytes
"""
Created on Tue May 30 17:33:37 2017

@author: OpenAI
"""
from keras import backend as K
from keras.optimizers import SGD, Adam
import tensorflow as tf

class SGDWithWeightnorm(SGD):

    def get_updates(self, params, constraints, loss):
        grads = self.get_gradients(loss, params)
        self.updates = []
        lr = self.lr
        if self.initial_decay > 0:
            lr *= 1.0 / (1.0 + self.decay * self.iterations)
            self.updates.append(K.update_add(self.iterations, 1))
        shapes = [K.get_variable_shape(p) for p in params]
        moments = [K.zeros(shape) for shape in shapes]
        self.weights = [self.iterations] + moments
        for p, g, m in zip(params, grads, moments):
            ps = K.get_variable_shape(p)
            if len(ps) > 1:
                V, V_norm, V_scaler, g_param, grad_g, grad_V = get_weightnorm_params_and_grads(p, g)
                V_scaler_shape = K.get_variable_shape(V_scaler)
                m_g = K.zeros(V_scaler_shape)
                v_g = self.momentum * m_g - lr * grad_g
                self.updates.append(K.update(m_g, v_g))
                if self.nesterov:
                    new_g_param = g_param + self.momentum * v_g - lr * grad_g
                else:
                    new_g_param = g_param + v_g
                v_v = self.momentum * m - lr * grad_V
                self.updates.append(K.update(m, v_v))
                if self.nesterov:
                    new_V_param = V + self.momentum * v_v - lr * grad_V
                else:
                    new_V_param = V + v_v
                if p in constraints:
                    c = constraints[p]
                    new_V_param = c(new_V_param)
                add_weightnorm_param_updates(self.updates, new_V_param, new_g_param, p, V_scaler)
            else:
                v = self.momentum * m - lr * g
                self.updates.append(K.update(m, v))
                if self.nesterov:
                    new_p = p + self.momentum * v - lr * g
                else:
                    new_p = p + v
                if p in constraints:
                    c = constraints[p]
                    new_p = c(new_p)
                self.updates.append(K.update(p, new_p))

        return self.updates


class AdamWithWeightnorm(Adam):

    def get_updates(self, params, constraints, loss):
        grads = self.get_gradients(loss, params)
        self.updates = [K.update_add(self.iterations, 1)]
        lr = self.lr
        if self.initial_decay > 0:
            lr *= 1.0 / (1.0 + self.decay * self.iterations)
        t = self.iterations + 1
        lr_t = lr * K.sqrt(1.0 - K.pow(self.beta_2, t)) / (1.0 - K.pow(self.beta_1, t))
        shapes = [K.get_variable_shape(p) for p in params]
        ms = [K.zeros(shape) for shape in shapes]
        vs = [K.zeros(shape) for shape in shapes]
        self.weights = [self.iterations] + ms + vs
        for p, g, m, v in zip(params, grads, ms, vs):
            ps = K.get_variable_shape(p)
            if len(ps) > 1:
                V, V_norm, V_scaler, g_param, grad_g, grad_V = get_weightnorm_params_and_grads(p, g)
                V_scaler_shape = K.get_variable_shape(V_scaler)
                m_g = K.zeros(V_scaler_shape)
                v_g = K.zeros(V_scaler_shape)
                m_g_t = self.beta_1 * m_g + (1.0 - self.beta_1) * grad_g
                v_g_t = self.beta_2 * v_g + (1.0 - self.beta_2) * K.square(grad_g)
                new_g_param = g_param - lr_t * m_g_t / (K.sqrt(v_g_t) + self.epsilon)
                self.updates.append(K.update(m_g, m_g_t))
                self.updates.append(K.update(v_g, v_g_t))
                m_t = self.beta_1 * m + (1.0 - self.beta_1) * grad_V
                v_t = self.beta_2 * v + (1.0 - self.beta_2) * K.square(grad_V)
                new_V_param = V - lr_t * m_t / (K.sqrt(v_t) + self.epsilon)
                self.updates.append(K.update(m, m_t))
                self.updates.append(K.update(v, v_t))
                if p in constraints:
                    c = constraints[p]
                    new_V_param = c(new_V_param)
                add_weightnorm_param_updates(self.updates, new_V_param, new_g_param, p, V_scaler)
            else:
                m_t = self.beta_1 * m + (1.0 - self.beta_1) * g
                v_t = self.beta_2 * v + (1.0 - self.beta_2) * K.square(g)
                p_t = p - lr_t * m_t / (K.sqrt(v_t) + self.epsilon)
                self.updates.append(K.update(m, m_t))
                self.updates.append(K.update(v, v_t))
                new_p = p_t
                if p in constraints:
                    c = constraints[p]
                    new_p = c(new_p)
                self.updates.append(K.update(p, new_p))

        return self.updates


def get_weightnorm_params_and_grads(p, g):
    ps = K.get_variable_shape(p)
    V_scaler_shape = (
     ps[(-1)],)
    V_scaler = K.ones(V_scaler_shape)
    norm_axes = [i for i in range(len(ps) - 1)]
    V = p / tf.reshape(V_scaler, [1] * len(norm_axes) + [-1])
    V_norm = tf.sqrt(tf.reduce_sum(tf.square(V), norm_axes))
    g_param = V_scaler * V_norm
    grad_g = tf.reduce_sum(g * V, norm_axes) / V_norm
    grad_V = tf.reshape(V_scaler, [1] * len(norm_axes) + [-1]) * (g - tf.reshape(grad_g / V_norm, [1] * len(norm_axes) + [-1]) * V)
    return (
     V, V_norm, V_scaler, g_param, grad_g, grad_V)


def add_weightnorm_param_updates(updates, new_V_param, new_g_param, W, V_scaler):
    ps = K.get_variable_shape(new_V_param)
    norm_axes = [i for i in range(len(ps) - 1)]
    new_V_norm = tf.sqrt(tf.reduce_sum(tf.square(new_V_param), norm_axes))
    new_V_scaler = new_g_param / new_V_norm
    new_W = tf.reshape(new_V_scaler, [1] * len(norm_axes) + [-1]) * new_V_param
    updates.append(K.update(W, new_W))
    updates.append(K.update(V_scaler, new_V_scaler))


def data_based_init(model, input):
    if type(input) is dict:
        feed_dict = input
    else:
        if type(input) is list:
            feed_dict = {tf_inp:np_inp for tf_inp, np_inp in zip(model.inputs, input)}
        else:
            feed_dict = {model.inputs[0]: input}
    if model.uses_learning_phase:
        if K.learning_phase() not in feed_dict:
            feed_dict.update({K.learning_phase(): 1})
    layer_output_weight_bias = []
    for l in model.layers:
        if hasattr(l, 'W'):
            if hasattr(l, 'b'):
                assert l.built
            layer_output_weight_bias.append((l.name, l.get_output_at(0), l.W, l.b))

    sess = K.get_session()
    for l, o, W, b in layer_output_weight_bias:
        print('Performing data dependent initialization for layer ' + l)
        m, v = tf.nn.moments(o, [i for i in range(len(o.get_shape()) - 1)])
        s = tf.sqrt(v + 1e-10)
        updates = tf.group(W.assign(W / tf.reshape(s, [1] * (len(W.get_shape()) - 1) + [-1])), b.assign((b - m) / s))
        sess.run(updates, feed_dict)
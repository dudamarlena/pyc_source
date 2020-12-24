# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/model/model.py
# Compiled at: 2018-04-01 15:02:11
# Size of source mod 2**32: 6542 bytes
"""Tensorflow model that helps to creates a Graph
"""
import tensorflow as tf, os, joblib
from yarlp.model.graph import Graph
from yarlp.utils.env_utils import GymEnv
from yarlp.utils import tf_utils

class Model:
    __doc__ = '\n    A Tensorflow model\n    '

    def __init__(self, env, build_graph, build_update_feed_dict, name='model'):
        """
        """
        self.num_outputs = GymEnv.get_env_action_space_dim(env)
        self.observation_space = env.observation_space
        self.build_update_feed_dict = build_update_feed_dict
        self.name = name
        tf_utils.reset_cache()
        self.G = Graph()
        with self.G:
            build_graph(self)
            self.create_weight_setter_ops()

    @classmethod
    def load(cls, path, name='model'):
        m = joblib.load(os.path.join(path, name + '.jbl'))
        tf_utils.reset_cache()
        m.G = Graph()
        m.G.load(os.path.join(path, name))
        return m

    def save(self, path, name=None):
        if name is None:
            name = self.name
        self.G.save(os.path.join(path, name))
        g = self.G
        self.G = None
        name += '.jbl'
        joblib.dump(self, os.path.join(path, name))
        self.G = g

    def __setitem__(self, var_name, tf_node):
        if hasattr(tf_node, '__module__') and tf_node.__module__.startswith('tensorflow'):
            if var_name in self.G:
                return
            self.G[var_name] = tf_node
        else:
            self.__setattr__(var_name, tf_node)

    def __getitem__(self, var_name):
        if var_name in self.G:
            return self.G[var_name]
        return self.__getattribute__(var_name)

    def get_session(self):
        return self.G._session

    def update(self, *args, **kwargs):
        name = kwargs.get('name', '')
        optimizer_op = self[('optimizer_op:' + name)]
        loss = self[('loss:' + name)]
        feed_dict = self.build_update_feed(*args)
        _, loss = self.G([optimizer_op, loss], feed_dict)
        return loss

    def eval_tensor(self, tensor, *args, **kwargs):
        feed_dict = self.build_update_feed(*args)
        return self.G(tensor, feed_dict)

    def build_update_feed(self, *args):
        """Create the feed dict for self.update
        """
        return self.build_update_feed_dict(self, *args)

    @property
    def weights(self):
        return self.G.TRAINABLE_VARIABLES

    @weights.setter
    def weights(self, weights):
        feed_dict = {self.G[('weight_input_var:' + n)]:w for n, w in weights.items()}
        ops = [self.G[('set_weight_op:' + n)] for n in weights]
        self.G(ops, feed_dict)

    def get_weight_names(self):
        return [w.name for w in self.G.TRAINABLE_VARIABLES]

    def get_weights(self):
        """Get weight values"""
        return self.G(self.weights)

    def run_op(self, var, feed):
        return self.G(var, feed)

    def set_weights(self, weights):
        """Set weights in model from a list of weight values.
        The weight values must be in the same order returned from get_weights()
        """
        weight_dict = {w.name:val for w, val in zip(self.weights, weights)}
        self.weights = weight_dict

    def add_loss(self, loss, name=''):
        self['loss:' + name] = loss

    def get_loss(self, name=''):
        return self[('loss:' + name)]

    def add_optimizer(self, optimizer, loss, name='', *args, **kwargs):
        self['optimizer_op:' + name] = optimizer.minimize(loss, *args, **kwargs)

    def add_input(self, name='observations', dtype=tf.float32, shape=None):
        if shape is None:
            shape = (
             *(None, ), *self.observation_space.shape)
        input_node = tf.placeholder(dtype=dtype, shape=shape)
        self.G['input:' + name] = input_node
        return input_node

    def add_input_node(self, node, name=''):
        if 'input:' + name in self.G:
            return node
        self.G['input:' + name] = node
        return node

    def add_output(self, network, num_outputs=None, name='', dtype=tf.float32, input_node=None):
        """ Add output node created from network
        """
        if num_outputs is None:
            num_outputs = self.num_outputs
        if input_node is None:
            input_node = self.G['input:observations']
        output_node = network(inputs=input_node, num_outputs=num_outputs)
        self.G['output:' + name] = output_node
        return output_node

    def add_output_node(self, node, name=''):
        """ Add output node
        """
        self.G['output:' + name] = node
        return node

    def create_weight_setter_ops(self):
        for w in self.weights:
            w_input = tf.placeholder_with_default(w, w.get_shape())
            self.G['weight_input_var:' + w.name] = w_input
            self.G['set_weight_op:' + w.name] = w.assign(w_input)

    def create_gradient_ops_for_node(self, optimizer, node, transform_grad_func=None, tvars=None, add_optimizer_op=False, optimizer_op_name=''):
        if tvars is None:
            tvars = self.G.TRAINABLE_VARIABLES
        grads_and_vars = optimizer.compute_gradients(node, tvars)
        if transform_grad_func:
            grads, grad_norm = transform_grad_func([g[0] for g in grads_and_vars])
            grads_and_vars = list(zip(grads, tvars))
        else:
            grads_and_vars = [(g, v) for g, v in grads_and_vars]
        self.G['gradients_ops:' + node.name] = optimizer.apply_gradients(grads_and_vars)
        if add_optimizer_op:
            self['optimizer_op:' + optimizer_op_name] = self[('gradients_ops:' + node.name)]

    def get_gradients(self, name, feed_dict):
        return self.G(self.G[('gradients:' + name)], feed_dict)

    def apply_gradient_ops(self, name, feed_dict):
        return self.G(self.G[('gradients_ops:' + name)], feed_dict)

    def predict(self, inputs):
        return self.G._session.run(self.G['output:'], feed_dict={self.G['input:observations']: inputs})
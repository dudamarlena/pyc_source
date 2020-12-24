# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/external/baselines/baselines/ppo1/cnn_policy.py
# Compiled at: 2018-04-01 14:21:44
# Size of source mod 2**32: 2417 bytes
import baselines.common.tf_util as U, tensorflow as tf, gym
from baselines.common.distributions import make_pdtype

class CnnPolicy(object):
    recurrent = False

    def __init__(self, name, ob_space, ac_space, kind='large'):
        with tf.variable_scope(name):
            self._init(ob_space, ac_space, kind)
            self.scope = tf.get_variable_scope().name

    def _init(self, ob_space, ac_space, kind):
        assert isinstance(ob_space, gym.spaces.Box)
        self.pdtype = pdtype = make_pdtype(ac_space)
        sequence_length = None
        ob = U.get_placeholder(name='ob', dtype=tf.float32, shape=[sequence_length] + list(ob_space.shape))
        x = ob / 255.0
        if kind == 'small':
            x = tf.nn.relu(U.conv2d(x, 16, 'l1', [8, 8], [4, 4], pad='VALID'))
            x = tf.nn.relu(U.conv2d(x, 32, 'l2', [4, 4], [2, 2], pad='VALID'))
            x = U.flattenallbut0(x)
            x = tf.nn.relu(tf.layers.dense(x, 256, name='lin', kernel_initializer=U.normc_initializer(1.0)))
        else:
            if kind == 'large':
                x = tf.nn.relu(U.conv2d(x, 32, 'l1', [8, 8], [4, 4], pad='VALID'))
                x = tf.nn.relu(U.conv2d(x, 64, 'l2', [4, 4], [2, 2], pad='VALID'))
                x = tf.nn.relu(U.conv2d(x, 64, 'l3', [3, 3], [1, 1], pad='VALID'))
                x = U.flattenallbut0(x)
                x = tf.nn.relu(tf.layers.dense(x, 512, name='lin', kernel_initializer=U.normc_initializer(1.0)))
            else:
                raise NotImplementedError
        logits = tf.layers.dense(x, pdtype.param_shape()[0], name='logits', kernel_initializer=U.normc_initializer(0.01))
        self.pd = pdtype.pdfromflat(logits)
        self.vpred = tf.layers.dense(x, 1, name='value', kernel_initializer=U.normc_initializer(1.0))[:, 0]
        self.state_in = []
        self.state_out = []
        stochastic = tf.placeholder(dtype=tf.bool, shape=())
        ac = self.pd.sample()
        self._act = U.function([stochastic, ob], [ac, self.vpred])

    def act(self, stochastic, ob):
        ac1, vpred1 = self._act(stochastic, ob[None])
        return (ac1[0], vpred1[0])

    def get_variables(self):
        return tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, self.scope)

    def get_trainable_variables(self):
        return tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, self.scope)

    def get_initial_state(self):
        return []
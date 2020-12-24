# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/liup/RL/rlsimpleParent/rlsimple/DDPG/Critic.py
# Compiled at: 2017-04-09 21:59:13
import tensorflow as tf
from NN import NN

class Critic(NN):

    def __init__(self, session, hasShadowNet, state_size, action_size, hidden_state_size):
        NN.__init__(self, session, hasShadowNet)
        inputStates = self.buildInputLayer('inputStates', shape=[None, state_size])
        inputActions = self.buildInputLayer('inputActions', shape=[None, action_size])
        inputYs = self.buildInputLayer('inputYs', shape=[None])
        h1 = self.buildLinearReluWire(inputStates, [state_size, hidden_state_size])
        h1 = self.buildLinearReluWire(h1, [hidden_state_size, hidden_state_size])
        h1 = self.buildJointLinearReluWire(h1, [hidden_state_size, hidden_state_size], inputActions, [action_size, hidden_state_size])
        tmp1 = self.buildLinearWire(h1, [hidden_state_size, action_size])
        out = self.buildReduceSum(tmp1, reduction_indices=1)
        self.setOutLayer(out)
        self.error = tf.reduce_mean(tf.square(inputYs - out))
        self.addMinimizeOperation(tf.train.AdamOptimizer(0.001).minimize(self.error))
        self.addAnyNamedOperation('goa', tf.gradients(out, inputActions))
        return
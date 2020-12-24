# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/liup/RL/rlsimpleParent/rlsimple/DDPG/Actor.py
# Compiled at: 2017-04-09 21:59:13
import tensorflow as tf
from NN import NN

class Actor(NN):

    def __init__(self, session, hasShadowNet, state_size, action_size, hidden_state_size):
        NN.__init__(self, session, hasShadowNet)
        inputLayer = self.buildInputLayer('inputStates', shape=[None, state_size])
        h1 = self.buildLinearReluWire(inputLayer, [state_size, hidden_state_size])
        h1 = self.buildLinearReluWire(h1, [hidden_state_size, hidden_state_size])
        out = self.buildLinearWire(h1, [hidden_state_size, action_size])
        self.setOutLayer(out)
        Qgradient = self.buildInputLayer('Qgradients', shape=[None, action_size])
        self.addAscentOperation(Qgradient)
        return
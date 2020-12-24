# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/huskarl/agent/a2c.py
# Compiled at: 2019-06-13 12:59:36
# Size of source mod 2**32: 4695 bytes
from tensorflow.keras.layers import Dense, Concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import tensorflow as tf, numpy as np
from huskarl.policy import Greedy, GaussianEpsGreedy
from huskarl.core import Agent
from huskarl import memory

class A2C(Agent):
    __doc__ = 'Advantage Actor-Critic (A2C)\n\n\tA2C is a synchronous version of A3C which gives equal or better performance.\n\tFor more information on A2C refer to the OpenAI blog post: https://blog.openai.com/baselines-acktr-a2c/.\n\tThe A3C algorithm is described in "Asynchronous Methods for Deep Reinforcement Learning" (Mnih et al., 2016)\n\n\tSince this algorithm is on-policy, it can and should be trained with multiple simultaneous environment instances.\n\tThe parallelism decorrelates the agents\' data into a more stationary process which aids learning.\n\t'

    def __init__(self, model, actions, optimizer=None, policy=None, test_policy=None, gamma=0.99, instances=8, nsteps=1, value_loss=0.5, entropy_loss=0.01):
        """
                TODO: Describe parameters
                """
        self.actions = actions
        self.optimizer = Adam(lr=0.003) if optimizer is None else optimizer
        self.memory = memory.OnPolicy(steps=nsteps, instances=instances)
        if policy is None:
            self.policy = [Greedy()] + [GaussianEpsGreedy(eps, 0.1) for eps in np.arange(0, 1, 1 / (instances - 1))]
        else:
            self.policy = policy
        self.test_policy = Greedy() if test_policy is None else test_policy
        self.gamma = gamma
        self.instances = instances
        self.nsteps = nsteps
        self.value_loss = value_loss
        self.entropy_loss = entropy_loss
        self.training = True
        raw_output = model.layers[(-1)].output
        actor = Dense(actions, activation='softmax')(raw_output)
        critic = Dense(1, activation='linear')(raw_output)
        output_layer = Concatenate()([actor, critic])
        self.model = Model(inputs=(model.input), outputs=output_layer)

        def a2c_loss(targets_actions, y_pred):
            targets, actions = targets_actions[:, 0], targets_actions[:, 1:]
            probs, values = y_pred[:, :-1], y_pred[:, -1]
            adv = targets - values
            logprob = tf.math.log(tf.reduce_sum((probs * actions), axis=1, keepdims=False) + 1e-10)
            loss_policy = -adv * logprob
            loss_value = self.value_loss * tf.square(adv)
            entropy = self.entropy_loss * tf.reduce_sum((probs * tf.math.log(probs + 1e-10)), axis=1, keepdims=False)
            return tf.reduce_mean(loss_policy + loss_value + entropy)

        self.model.compile(optimizer=(self.optimizer), loss=a2c_loss)

    def save(self, filename, overwrite=False):
        """Saves the model parameters to the specified file."""
        self.model.save_weights(filename, overwrite=overwrite)

    def act(self, state, instance=0):
        """Returns the action to be taken given a state."""
        qvals = self.model.predict(np.array([state]))[0][:-1]
        if self.training:
            if isinstance(self.policy, list):
                return self.policy[instance].act(qvals)
            return self.policy.act(qvals)
        else:
            if isinstance(self.test_policy, list):
                return self.test_policy[instance].act(qvals)
            return self.test_policy.act(qvals)

    def push(self, transition, instance=0):
        """Stores the transition in memory."""
        self.memory.put(transition, instance)

    def train(self, step):
        """Trains the agent for one step."""
        if len(self.memory) < self.instances:
            return
        state_batch, action_batch, reward_batches, end_state_batch, not_done_mask = self.memory.get()
        target_qvals = np.zeros(self.instances)
        non_final_last_next_states = [es for es in end_state_batch if es is not None]
        if len(non_final_last_next_states) > 0:
            non_final_mask = list(map(lambda s: s is not None, end_state_batch))
            target_qvals[non_final_mask] = self.model.predict_on_batch(np.array(non_final_last_next_states))[:, -1].squeeze()
        for n in reversed(range(self.nsteps)):
            rewards = np.array([b[n] for b in reward_batches])
            target_qvals *= np.array([t[n] for t in not_done_mask])
            target_qvals = rewards + self.gamma * target_qvals

        ran = np.arange(self.instances)
        targets_actions = np.zeros((self.instances, self.actions + 1))
        targets_actions[(ran, 0)] = target_qvals
        targets_actions[(ran, np.array(action_batch) + 1)] = 1
        self.model.train_on_batch(np.array(state_batch), targets_actions)
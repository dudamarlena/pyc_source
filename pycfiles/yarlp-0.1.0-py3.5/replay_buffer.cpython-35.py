# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/utils/replay_buffer.py
# Compiled at: 2018-04-01 15:02:11
# Size of source mod 2**32: 1288 bytes
import numpy as np

class ReplayBuffer:

    def __init__(self, max_size):
        self.max_size = max_size
        self.mem = []
        self._next_idx = 0
        self.size = 0

    def add(self, s, a, r, next_s, done):
        b = (
         s, a, r, next_s, done)
        if self.size < self.max_size:
            self.mem.append(b)
        else:
            self.mem[self._next_idx] = b
        self._next_idx += 1
        self.size = min(self.size + 1, self.max_size)
        self._next_idx = self._next_idx % self.max_size

    def __len__(self):
        return self.size

    def sample(self, batch_size):
        assert batch_size <= self.size
        idx = np.random.choice(self.size, size=batch_size, replace=False)
        minibatch = [self.mem[i] for i in idx]
        return self._flatten_batch(minibatch)

    def _flatten_batch(self, minibatch):
        states = np.array([np.array(m[0]) for m in minibatch])
        actions = np.array([m[1] for m in minibatch])
        rewards = np.array([m[2] for m in minibatch])
        next_states = np.array([np.array(m[3]) for m in minibatch])
        done = np.array([m[4] for m in minibatch])
        return (
         states, actions, rewards, next_states, done)

    def return_most_recent(self):
        return self._flatten_batch(self.mem[(-1)])
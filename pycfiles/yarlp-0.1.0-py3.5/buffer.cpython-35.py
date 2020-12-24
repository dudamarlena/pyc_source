# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/external/baselines/baselines/acer/buffer.py
# Compiled at: 2018-04-01 14:21:44
# Size of source mod 2**32: 4381 bytes
import numpy as np

class Buffer(object):

    def __init__(self, env, nsteps, nstack, size=50000):
        self.nenv = env.num_envs
        self.nsteps = nsteps
        self.nh, self.nw, self.nc = env.observation_space.shape
        self.nstack = nstack
        self.nbatch = self.nenv * self.nsteps
        self.size = size // self.nsteps
        self.enc_obs = None
        self.actions = None
        self.rewards = None
        self.mus = None
        self.dones = None
        self.masks = None
        self.next_idx = 0
        self.num_in_buffer = 0

    def has_atleast(self, frames):
        return self.num_in_buffer >= frames // self.nsteps

    def can_sample(self):
        return self.num_in_buffer > 0

    def decode(self, enc_obs, dones):
        nstack, nenv, nsteps, nh, nw, nc = (
         self.nstack, self.nenv, self.nsteps, self.nh, self.nw, self.nc)
        y = np.empty([nsteps + nstack - 1, nenv, 1, 1, 1], dtype=np.float32)
        obs = np.zeros([nstack, nsteps + nstack, nenv, nh, nw, nc], dtype=np.uint8)
        x = np.reshape(enc_obs, [nenv, nsteps + nstack, nh, nw, nc]).swapaxes(1, 0)
        y[3:] = np.reshape(1.0 - dones, [nenv, nsteps, 1, 1, 1]).swapaxes(1, 0)
        y[:3] = 1.0
        for i in range(nstack):
            obs[-(i + 1), i:] = x
            x = x[:-1] * y
            y = y[1:]

        return np.reshape(obs[:, 3:].transpose((2, 1, 3, 4, 0, 5)), [nenv, nsteps + 1, nh, nw, nstack * nc])

    def put(self, enc_obs, actions, rewards, mus, dones, masks):
        if self.enc_obs is None:
            self.enc_obs = np.empty([self.size] + list(enc_obs.shape), dtype=np.uint8)
            self.actions = np.empty([self.size] + list(actions.shape), dtype=np.int32)
            self.rewards = np.empty([self.size] + list(rewards.shape), dtype=np.float32)
            self.mus = np.empty([self.size] + list(mus.shape), dtype=np.float32)
            self.dones = np.empty([self.size] + list(dones.shape), dtype=np.bool)
            self.masks = np.empty([self.size] + list(masks.shape), dtype=np.bool)
        self.enc_obs[self.next_idx] = enc_obs
        self.actions[self.next_idx] = actions
        self.rewards[self.next_idx] = rewards
        self.mus[self.next_idx] = mus
        self.dones[self.next_idx] = dones
        self.masks[self.next_idx] = masks
        self.next_idx = (self.next_idx + 1) % self.size
        self.num_in_buffer = min(self.size, self.num_in_buffer + 1)

    def take(self, x, idx, envx):
        nenv = self.nenv
        out = np.empty([nenv] + list(x.shape[2:]), dtype=x.dtype)
        for i in range(nenv):
            out[i] = x[(idx[i], envx[i])]

        return out

    def get(self):
        nenv = self.nenv
        assert self.can_sample()
        idx = np.random.randint(0, self.num_in_buffer, nenv)
        envx = np.arange(nenv)
        take = lambda x: self.take(x, idx, envx)
        dones = take(self.dones)
        enc_obs = take(self.enc_obs)
        obs = self.decode(enc_obs, dones)
        actions = take(self.actions)
        rewards = take(self.rewards)
        mus = take(self.mus)
        masks = take(self.masks)
        return (obs, actions, rewards, mus, dones, masks)
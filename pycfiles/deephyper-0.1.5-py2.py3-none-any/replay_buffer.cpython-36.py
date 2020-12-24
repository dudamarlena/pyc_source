# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/her/replay_buffer.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 3669 bytes
import threading, numpy as np

class ReplayBuffer:

    def __init__(self, buffer_shapes, size_in_transitions, T, sample_transitions):
        """Creates a replay buffer.

        Args:
            buffer_shapes (dict of ints): the shape for all buffers that are used in the replay
                buffer
            size_in_transitions (int): the size of the buffer, measured in transitions
            T (int): the time horizon for episodes
            sample_transitions (function): a function that samples from the replay buffer
        """
        self.buffer_shapes = buffer_shapes
        self.size = size_in_transitions // T
        self.T = T
        self.sample_transitions = sample_transitions
        self.buffers = {key:np.empty([self.size, *shape]) for key, shape in buffer_shapes.items()}
        self.current_size = 0
        self.n_transitions_stored = 0
        self.lock = threading.Lock()

    @property
    def full(self):
        with self.lock:
            return self.current_size == self.size

    def sample(self, batch_size):
        """Returns a dict {key: array(batch_size x shapes[key])}
        """
        buffers = {}
        with self.lock:
            assert self.current_size > 0
            for key in self.buffers.keys():
                buffers[key] = self.buffers[key][:self.current_size]

        buffers['o_2'] = buffers['o'][:, 1:, :]
        buffers['ag_2'] = buffers['ag'][:, 1:, :]
        transitions = self.sample_transitions(buffers, batch_size)
        for key in ['r', 'o_2', 'ag_2'] + list(self.buffers.keys()):
            assert key in transitions, 'key %s missing from transitions' % key

        return transitions

    def store_episode(self, episode_batch):
        """episode_batch: array(batch_size x (T or T+1) x dim_key)
        """
        batch_sizes = [len(episode_batch[key]) for key in episode_batch.keys()]
        assert np.all(np.array(batch_sizes) == batch_sizes[0])
        batch_size = batch_sizes[0]
        with self.lock:
            idxs = self._get_storage_idx(batch_size)
            for key in self.buffers.keys():
                self.buffers[key][idxs] = episode_batch[key]

            self.n_transitions_stored += batch_size * self.T

    def get_current_episode_size(self):
        with self.lock:
            return self.current_size

    def get_current_size(self):
        with self.lock:
            return self.current_size * self.T

    def get_transitions_stored(self):
        with self.lock:
            return self.n_transitions_stored

    def clear_buffer(self):
        with self.lock:
            self.current_size = 0

    def _get_storage_idx(self, inc=None):
        inc = inc or 1
        if not inc <= self.size:
            raise AssertionError('Batch committed to replay is too large!')
        else:
            if self.current_size + inc <= self.size:
                idx = np.arange(self.current_size, self.current_size + inc)
            else:
                if self.current_size < self.size:
                    overflow = inc - (self.size - self.current_size)
                    idx_a = np.arange(self.current_size, self.size)
                    idx_b = np.random.randint(0, self.current_size, overflow)
                    idx = np.concatenate([idx_a, idx_b])
                else:
                    idx = np.random.randint(0, self.size, inc)
        self.current_size = min(self.size, self.current_size + inc)
        if inc == 1:
            idx = idx[0]
        return idx
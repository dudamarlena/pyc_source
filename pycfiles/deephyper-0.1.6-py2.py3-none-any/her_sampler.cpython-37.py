# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/her/her_sampler.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 2822 bytes
import numpy as np

def make_sample_her_transitions(replay_strategy, replay_k, reward_fun):
    """Creates a sample function that can be used for HER experience replay.

    Args:
        replay_strategy (in ['future', 'none']): the HER replay strategy; if set to 'none',
            regular DDPG experience replay is used
        replay_k (int): the ratio between HER replays and regular replays (e.g. k = 4 -> 4 times
            as many HER replays as regular replays are used)
        reward_fun (function): function to re-compute the reward with substituted goals
    """
    if replay_strategy == 'future':
        future_p = 1 - 1.0 / (1 + replay_k)
    else:
        future_p = 0

    def _sample_her_transitions(episode_batch, batch_size_in_transitions):
        T = episode_batch['u'].shape[1]
        rollout_batch_size = episode_batch['u'].shape[0]
        batch_size = batch_size_in_transitions
        episode_idxs = np.random.randint(0, rollout_batch_size, batch_size)
        t_samples = np.random.randint(T, size=batch_size)
        transitions = {key:episode_batch[key][(episode_idxs, t_samples)].copy() for key in episode_batch.keys()}
        her_indexes = np.where(np.random.uniform(size=batch_size) < future_p)
        future_offset = np.random.uniform(size=batch_size) * (T - t_samples)
        future_offset = future_offset.astype(int)
        future_t = (t_samples + 1 + future_offset)[her_indexes]
        future_ag = episode_batch['ag'][(episode_idxs[her_indexes], future_t)]
        transitions['g'][her_indexes] = future_ag
        info = {}
        for key, value in transitions.items():
            if key.startswith('info_'):
                info[key.replace('info_', '')] = value

        reward_params = {k:transitions[k] for k in ('ag_2', 'g')}
        reward_params['info'] = info
        transitions['r'] = reward_fun(**reward_params)
        transitions = {k:(transitions[k].reshape)(batch_size, *transitions[k].shape[1:]) for k in transitions.keys()}
        assert transitions['u'].shape[0] == batch_size_in_transitions
        return transitions

    return _sample_her_transitions
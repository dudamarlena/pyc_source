# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/subproc_vec_env.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 4064 bytes
import multiprocessing as mp, numpy as np
from .vec_env import VecEnv, CloudpickleWrapper, clear_mpi_env_vars

def worker(remote, parent_remote, env_fn_wrapper):
    parent_remote.close()
    env = env_fn_wrapper.x()
    try:
        try:
            while True:
                cmd, data = remote.recv()
                if cmd == 'step':
                    ob, reward, done, info = env.step(data)
                    if done:
                        ob = env.reset()
                    remote.send((ob, reward, done, info))
                elif cmd == 'reset':
                    ob = env.reset()
                    remote.send(ob)
                elif cmd == 'render':
                    remote.send(env.render(mode='rgb_array'))
                else:
                    if cmd == 'close':
                        remote.close()
                        break
                    else:
                        if cmd == 'get_spaces_spec':
                            remote.send((env.observation_space, env.action_space, env.spec))
                        else:
                            raise NotImplementedError

        except KeyboardInterrupt:
            print('SubprocVecEnv worker: got KeyboardInterrupt')

    finally:
        env.close()


class SubprocVecEnv(VecEnv):
    __doc__ = '\n    VecEnv that runs multiple environments in parallel in subproceses and communicates with them via pipes.\n    Recommended to use when num_envs > 1 and step() can be a bottleneck.\n    '

    def __init__(self, env_fns, spaces=None, context='spawn'):
        """
        Arguments:

        env_fns: iterable of callables -  functions that create environments to run in subprocesses. Need to be cloud-pickleable
        """
        self.waiting = False
        self.closed = False
        nenvs = len(env_fns)
        ctx = mp.get_context(context)
        self.remotes, self.work_remotes = zip(*[ctx.Pipe() for _ in range(nenvs)])
        self.ps = [ctx.Process(target=worker, args=(work_remote, remote, CloudpickleWrapper(env_fn))) for work_remote, remote, env_fn in zip(self.work_remotes, self.remotes, env_fns)]
        for p in self.ps:
            p.daemon = True
            with clear_mpi_env_vars():
                p.start()

        for remote in self.work_remotes:
            remote.close()

        self.remotes[0].send(('get_spaces_spec', None))
        observation_space, action_space, self.spec = self.remotes[0].recv()
        self.viewer = None
        VecEnv.__init__(self, len(env_fns), observation_space, action_space)

    def step_async(self, actions):
        self._assert_not_closed()
        for remote, action in zip(self.remotes, actions):
            remote.send(('step', action))

        self.waiting = True

    def step_wait(self):
        self._assert_not_closed()
        results = [remote.recv() for remote in self.remotes]
        self.waiting = False
        obs, rews, dones, infos = zip(*results)
        return (_flatten_obs(obs), np.stack(rews), np.stack(dones), infos)

    def reset(self):
        self._assert_not_closed()
        for remote in self.remotes:
            remote.send(('reset', None))

        return _flatten_obs([remote.recv() for remote in self.remotes])

    def close_extras(self):
        self.closed = True
        if self.waiting:
            for remote in self.remotes:
                remote.recv()

        for remote in self.remotes:
            remote.send(('close', None))

        for p in self.ps:
            p.join()

    def get_images(self):
        self._assert_not_closed()
        for pipe in self.remotes:
            pipe.send(('render', None))

        imgs = [pipe.recv() for pipe in self.remotes]
        return imgs

    def _assert_not_closed(self):
        assert not self.closed, 'Trying to operate on a SubprocVecEnv after calling close()'

    def __del__(self):
        if not self.closed:
            self.close()


def _flatten_obs(obs):
    if not isinstance(obs, (list, tuple)):
        raise AssertionError
    elif not len(obs) > 0:
        raise AssertionError
    if isinstance(obs[0], dict):
        keys = obs[0].keys()
        return {k:np.stack([o[k] for o in obs]) for k in keys}
    else:
        return np.stack(obs)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_cartpole.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 1106 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, gym
from deephyper.search.nas.baselines.run import get_learn_function
from deephyper.search.nas.baselines.common.tests.util import reward_per_episode_test
common_kwargs = dict(total_timesteps=30000,
  network='mlp',
  gamma=1.0,
  seed=0)
learn_kwargs = {'a2c':dict(nsteps=32, value_network='copy', lr=0.05), 
 'acer':dict(value_network='copy'), 
 'acktr':dict(nsteps=32, value_network='copy', is_async=False), 
 'deepq':dict(total_timesteps=20000), 
 'ppo2':dict(value_network='copy'), 
 'trpo_mpi':{}}

@pytest.mark.slow
@pytest.mark.parametrize('alg', learn_kwargs.keys())
def test_cartpole(alg):
    """
    Test if the algorithm (with an mlp policy)
    can learn to balance the cartpole
    """
    kwargs = common_kwargs.copy()
    kwargs.update(learn_kwargs[alg])

    def learn_fn(e):
        return (get_learn_function(alg))(env=e, **kwargs)

    def env_fn():
        env = gym.make('CartPole-v0')
        env.seed(0)
        return env

    reward_per_episode_test(env_fn, learn_fn, 100)


if __name__ == '__main__':
    test_cartpole('acer')
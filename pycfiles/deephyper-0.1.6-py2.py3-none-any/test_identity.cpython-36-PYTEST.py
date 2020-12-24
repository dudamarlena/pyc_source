# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_identity.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 2343 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from deephyper.search.nas.baselines.common.tests.envs.identity_env import DiscreteIdentityEnv, BoxIdentityEnv, MultiDiscreteIdentityEnv
from deephyper.search.nas.baselines.run import get_learn_function
from deephyper.search.nas.baselines.common.tests.util import simple_test
common_kwargs = dict(total_timesteps=30000,
  network='mlp',
  gamma=0.9,
  seed=0)
learn_kwargs = {'a2c':{},  'acktr':{},  'deepq':{},  'ddpg':dict(layer_norm=True), 
 'ppo2':dict(lr=0.001, nsteps=64, ent_coef=0.0), 
 'trpo_mpi':dict(timesteps_per_batch=100, cg_iters=10, gamma=0.9, lam=1.0, max_kl=0.01)}
algos_disc = [
 'a2c', 'acktr', 'deepq', 'ppo2', 'trpo_mpi']
algos_multidisc = ['a2c', 'acktr', 'ppo2', 'trpo_mpi']
algos_cont = ['a2c', 'acktr', 'ddpg', 'ppo2', 'trpo_mpi']

@pytest.mark.slow
@pytest.mark.parametrize('alg', algos_disc)
def test_discrete_identity(alg):
    """
    Test if the algorithm (with an mlp policy)
    can learn an identity transformation (i.e. return observation as an action)
    """
    kwargs = learn_kwargs[alg]
    kwargs.update(common_kwargs)
    learn_fn = lambda e: (get_learn_function(alg))(env=e, **kwargs)
    env_fn = lambda : DiscreteIdentityEnv(10, episode_len=100)
    simple_test(env_fn, learn_fn, 0.9)


@pytest.mark.slow
@pytest.mark.parametrize('alg', algos_multidisc)
def test_multidiscrete_identity(alg):
    """
    Test if the algorithm (with an mlp policy)
    can learn an identity transformation (i.e. return observation as an action)
    """
    kwargs = learn_kwargs[alg]
    kwargs.update(common_kwargs)
    learn_fn = lambda e: (get_learn_function(alg))(env=e, **kwargs)
    env_fn = lambda : MultiDiscreteIdentityEnv((3, 3), episode_len=100)
    simple_test(env_fn, learn_fn, 0.9)


@pytest.mark.slow
@pytest.mark.parametrize('alg', algos_cont)
def test_continuous_identity(alg):
    """
    Test if the algorithm (with an mlp policy)
    can learn an identity transformation (i.e. return observation as an action)
    to a required precision
    """
    kwargs = learn_kwargs[alg]
    kwargs.update(common_kwargs)
    learn_fn = lambda e: (get_learn_function(alg))(env=e, **kwargs)
    env_fn = lambda : BoxIdentityEnv((1, ), episode_len=100)
    simple_test(env_fn, learn_fn, -0.1)


if __name__ == '__main__':
    test_multidiscrete_identity('acktr')
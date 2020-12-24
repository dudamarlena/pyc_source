# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_mnist.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 1574 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from deephyper.search.nas.baselines.common.tests.envs.mnist_env import MnistEnv
from deephyper.search.nas.baselines.common.tests.util import simple_test
from deephyper.search.nas.baselines.run import get_learn_function
common_kwargs = {'seed':0, 
 'network':'cnn', 
 'gamma':0.9, 
 'pad':'SAME'}
learn_args = {'a2c':dict(total_timesteps=50000), 
 'acer':dict(total_timesteps=20000), 
 'deepq':dict(total_timesteps=5000), 
 'acktr':dict(total_timesteps=30000), 
 'ppo2':dict(total_timesteps=50000, lr=0.001, nsteps=128, ent_coef=0.0), 
 'trpo_mpi':dict(total_timesteps=80000, timesteps_per_batch=100, cg_iters=10, lam=1.0, max_kl=0.001)}

@pytest.mark.skip
@pytest.mark.slow
@pytest.mark.parametrize('alg', learn_args.keys())
def test_mnist(alg):
    """
    Test if the algorithm can learn to classify MNIST digits.
    Uses CNN policy.
    """
    learn_kwargs = learn_args[alg]
    learn_kwargs.update(common_kwargs)
    learn = get_learn_function(alg)

    def learn_fn(e):
        return learn(env=e, **learn_kwargs)

    def env_fn():
        return MnistEnv(episode_len=100)

    simple_test(env_fn, learn_fn, 0.6)


if __name__ == '__main__':
    test_mnist('acer')
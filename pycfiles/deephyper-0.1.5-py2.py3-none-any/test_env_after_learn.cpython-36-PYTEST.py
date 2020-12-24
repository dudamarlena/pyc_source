# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_env_after_learn.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 952 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, gym, tensorflow as tf
from deephyper.search.nas.baselines.common.vec_env.subproc_vec_env import SubprocVecEnv
from deephyper.search.nas.baselines.run import get_learn_function
from deephyper.search.nas.baselines.common.tf_util import make_session
algos = [
 'a2c', 'acer', 'acktr', 'deepq', 'ppo2', 'trpo_mpi']

@pytest.mark.parametrize('algo', algos)
def test_env_after_learn(algo):

    def make_env():
        env = gym.make('CartPole-v1' if algo == 'acktr' else 'PongNoFrameskip-v4')
        return env

    make_session(make_default=True, graph=(tf.Graph()))
    env = SubprocVecEnv([make_env])
    learn = get_learn_function(algo)
    learn(network='mlp', env=env, total_timesteps=0, load_path=None, seed=None)
    env.reset()
    env.close()
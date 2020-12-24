# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/ppo2/test_microbatches.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 1270 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, gym, tensorflow as tf, numpy as np
from functools import partial
from deephyper.search.nas.baselines.common.vec_env.dummy_vec_env import DummyVecEnv
from deephyper.search.nas.baselines.common.tf_util import make_session
from deephyper.search.nas.baselines.ppo2.ppo2 import learn
from deephyper.search.nas.baselines.ppo2.microbatched_model import MicrobatchedModel

def test_microbatches():

    def env_fn():
        env = gym.make('CartPole-v0')
        env.seed(0)
        return env

    learn_fn = partial(learn, network='mlp', nsteps=32, total_timesteps=32,
      seed=0)
    env_ref = DummyVecEnv([env_fn])
    sess_ref = make_session(make_default=True, graph=(tf.Graph()))
    learn_fn(env=env_ref)
    vars_ref = {v.name:sess_ref.run(v) for v in tf.trainable_variables()}
    env_test = DummyVecEnv([env_fn])
    sess_test = make_session(make_default=True, graph=(tf.Graph()))
    learn_fn(env=env_test, model_fn=partial(MicrobatchedModel,
      microbatch_size=2))
    vars_test = {v.name:sess_test.run(v) for v in tf.trainable_variables()}
    for v in vars_ref:
        np.testing.assert_allclose((vars_ref[v]), (vars_test[v]), atol=0.003)


if __name__ == '__main__':
    test_microbatches()
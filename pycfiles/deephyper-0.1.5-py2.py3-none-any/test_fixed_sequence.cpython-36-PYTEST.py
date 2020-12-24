# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_fixed_sequence.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 1493 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from deephyper.search.nas.baselines.common.tests.envs.fixed_sequence_env import FixedSequenceEnv
from deephyper.search.nas.baselines.common.tests.util import simple_test
from deephyper.search.nas.baselines.run import get_learn_function
common_kwargs = dict(seed=0,
  total_timesteps=50000)
learn_kwargs = {'a2c':{},  'ppo2':dict(nsteps=10, ent_coef=0.0, nminibatches=1)}
alg_list = learn_kwargs.keys()
rnn_list = ['lstm']

@pytest.mark.slow
@pytest.mark.parametrize('alg', alg_list)
@pytest.mark.parametrize('rnn', rnn_list)
def test_fixed_sequence(alg, rnn):
    """
    Test if the algorithm (with a given policy)
    can learn an identity transformation (i.e. return observation as an action)
    """
    kwargs = learn_kwargs[alg]
    kwargs.update(common_kwargs)
    if alg == 'ppo2':
        if rnn.endswith('lstm'):
            rnn = 'ppo_' + rnn

    def env_fn():
        return FixedSequenceEnv(n_actions=10, episode_len=5)

    def learn(e):
        return (get_learn_function(alg))(env=e, 
         network=rnn, **kwargs)

    simple_test(env_fn, learn, 0.7)


if __name__ == '__main__':
    test_fixed_sequence('ppo2', 'lstm')
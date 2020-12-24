# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/test_vec_env.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 3786 bytes
"""
Tests for asynchronous vectorized environments.
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, gym, numpy as np, pytest
from .dummy_vec_env import DummyVecEnv
from .shmem_vec_env import ShmemVecEnv
from .subproc_vec_env import SubprocVecEnv
from deephyper.search.nas.baselines.common.tests.test_with_mpi import with_mpi

def assert_venvs_equal(venv1, venv2, num_steps):
    """
    Compare two environments over num_steps steps and make sure
    that the observations produced by each are the same when given
    the same actions.
    """
    @py_assert1 = venv1.num_envs
    @py_assert5 = venv2.num_envs
    @py_assert3 = @py_assert1 == @py_assert5
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/test_vec_env.py', lineno=20)
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.num_envs\n} == %(py6)s\n{%(py6)s = %(py4)s.num_envs\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(venv1) if 'venv1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv1) else 'venv1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(venv2) if 'venv2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv2) else 'venv2',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = venv1.observation_space
    @py_assert3 = @py_assert1.shape
    @py_assert7 = venv2.observation_space
    @py_assert9 = @py_assert7.shape
    @py_assert5 = @py_assert3 == @py_assert9
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/test_vec_env.py', lineno=21)
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.observation_space\n}.shape\n} == %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s.observation_space\n}.shape\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(venv1) if 'venv1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv1) else 'venv1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(venv2) if 'venv2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv2) else 'venv2',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = venv1.observation_space
    @py_assert3 = @py_assert1.dtype
    @py_assert7 = venv2.observation_space
    @py_assert9 = @py_assert7.dtype
    @py_assert5 = @py_assert3 == @py_assert9
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/test_vec_env.py', lineno=22)
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.observation_space\n}.dtype\n} == %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s.observation_space\n}.dtype\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(venv1) if 'venv1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv1) else 'venv1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(venv2) if 'venv2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv2) else 'venv2',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = venv1.action_space
    @py_assert3 = @py_assert1.shape
    @py_assert7 = venv2.action_space
    @py_assert9 = @py_assert7.shape
    @py_assert5 = @py_assert3 == @py_assert9
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/test_vec_env.py', lineno=23)
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.action_space\n}.shape\n} == %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s.action_space\n}.shape\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(venv1) if 'venv1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv1) else 'venv1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(venv2) if 'venv2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv2) else 'venv2',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = venv1.action_space
    @py_assert3 = @py_assert1.dtype
    @py_assert7 = venv2.action_space
    @py_assert9 = @py_assert7.dtype
    @py_assert5 = @py_assert3 == @py_assert9
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/test_vec_env.py', lineno=24)
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.action_space\n}.dtype\n} == %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s.action_space\n}.dtype\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(venv1) if 'venv1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv1) else 'venv1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(venv2) if 'venv2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv2) else 'venv2',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    try:
        obs1, obs2 = venv1.reset(), venv2.reset()
        @py_assert1 = np.array
        @py_assert4 = @py_assert1(obs1)
        @py_assert6 = @py_assert4.shape
        @py_assert10 = np.array
        @py_assert13 = @py_assert10(obs2)
        @py_assert15 = @py_assert13.shape
        @py_assert8 = @py_assert6 == @py_assert15
        if @py_assert8 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/test_vec_env.py', lineno=28)
        if not @py_assert8:
            @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.array\n}(%(py3)s)\n}.shape\n} == %(py16)s\n{%(py16)s = %(py14)s\n{%(py14)s = %(py11)s\n{%(py11)s = %(py9)s.array\n}(%(py12)s)\n}.shape\n}', ), (@py_assert6, @py_assert15)) % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(obs1) if 'obs1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obs1) else 'obs1',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py11':@pytest_ar._saferepr(@py_assert10),  'py12':@pytest_ar._saferepr(obs2) if 'obs2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obs2) else 'obs2',  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
            @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
            raise AssertionError(@pytest_ar._format_explanation(@py_format19))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert13 = @py_assert15 = None
        @py_assert1 = np.array
        @py_assert4 = @py_assert1(obs1)
        @py_assert6 = @py_assert4.shape
        @py_assert9 = (
         venv1.num_envs,)
        @py_assert12 = venv1.observation_space
        @py_assert14 = @py_assert12.shape
        @py_assert16 = @py_assert9 + @py_assert14
        @py_assert8 = @py_assert6 == @py_assert16
        if @py_assert8 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/test_vec_env.py', lineno=29)
        if not @py_assert8:
            @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.array\n}(%(py3)s)\n}.shape\n} == (%(py10)s + %(py15)s\n{%(py15)s = %(py13)s\n{%(py13)s = %(py11)s.observation_space\n}.shape\n})', ), (@py_assert6, @py_assert16)) % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(obs1) if 'obs1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obs1) else 'obs1',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9),  'py11':@pytest_ar._saferepr(venv1) if 'venv1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(venv1) else 'venv1',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
            @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
            raise AssertionError(@pytest_ar._format_explanation(@py_format19))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert16 = None
        @py_assert1 = np.allclose
        @py_assert5 = @py_assert1(obs1, obs2)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/test_vec_env.py', lineno=30)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.allclose\n}(%(py3)s, %(py4)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(obs1) if 'obs1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obs1) else 'obs1',  'py4':@pytest_ar._saferepr(obs2) if 'obs2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obs2) else 'obs2',  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert5 = None
        venv1.action_space.seed(1337)
        for _ in range(num_steps):
            actions = np.array([venv1.action_space.sample() for _ in range(venv1.num_envs)])
            for venv in [venv1, venv2]:
                venv.step_async(actions)

            outs1 = venv1.step_wait()
            outs2 = venv2.step_wait()
            for out1, out2 in zip(outs1[:3], outs2[:3]):
                @py_assert1 = np.array
                @py_assert4 = @py_assert1(out1)
                @py_assert6 = @py_assert4.shape
                @py_assert10 = np.array
                @py_assert13 = @py_assert10(out2)
                @py_assert15 = @py_assert13.shape
                @py_assert8 = @py_assert6 == @py_assert15
                if @py_assert8 is None:
                    from _pytest.warning_types import PytestAssertRewriteWarning
                    from warnings import warn_explicit
                    warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/test_vec_env.py', lineno=39)
                if not @py_assert8:
                    @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.array\n}(%(py3)s)\n}.shape\n} == %(py16)s\n{%(py16)s = %(py14)s\n{%(py14)s = %(py11)s\n{%(py11)s = %(py9)s.array\n}(%(py12)s)\n}.shape\n}', ), (@py_assert6, @py_assert15)) % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(out1) if 'out1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out1) else 'out1',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py11':@pytest_ar._saferepr(@py_assert10),  'py12':@pytest_ar._saferepr(out2) if 'out2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out2) else 'out2',  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
                    @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format19))
                @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert13 = @py_assert15 = None
                @py_assert1 = np.allclose
                @py_assert5 = @py_assert1(out1, out2)
                if @py_assert5 is None:
                    from _pytest.warning_types import PytestAssertRewriteWarning
                    from warnings import warn_explicit
                    warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/test_vec_env.py', lineno=40)
                if not @py_assert5:
                    @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.allclose\n}(%(py3)s, %(py4)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(out1) if 'out1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out1) else 'out1',  'py4':@pytest_ar._saferepr(out2) if 'out2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out2) else 'out2',  'py6':@pytest_ar._saferepr(@py_assert5)}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format7))
                @py_assert1 = @py_assert5 = None

            @py_assert1 = outs1[3]
            @py_assert3 = list(@py_assert1)
            @py_assert7 = outs2[3]
            @py_assert9 = list(@py_assert7)
            @py_assert5 = @py_assert3 == @py_assert9
            if @py_assert5 is None:
                from _pytest.warning_types import PytestAssertRewriteWarning
                from warnings import warn_explicit
                warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/test_vec_env.py', lineno=41)
            if not @py_assert5:
                @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
                @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
                raise AssertionError(@pytest_ar._format_explanation(@py_format13))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None

    finally:
        venv1.close()
        venv2.close()


@pytest.mark.parametrize('klass', (ShmemVecEnv, SubprocVecEnv))
@pytest.mark.parametrize('dtype', ('uint8', 'float32'))
def test_vec_env(klass, dtype):
    """
    Test that a vectorized environment is equivalent to
    DummyVecEnv, since DummyVecEnv is less likely to be
    error prone.
    """
    num_envs = 3
    num_steps = 100
    shape = (3, 8)

    def make_fn(seed):
        return lambda : SimpleEnv(seed, shape, dtype)

    fns = [make_fn(i) for i in range(num_envs)]
    env1 = DummyVecEnv(fns)
    env2 = klass(fns)
    assert_venvs_equal(env1, env2, num_steps=num_steps)


class SimpleEnv(gym.Env):
    __doc__ = '\n    An environment with a pre-determined observation space\n    and RNG seed.\n    '

    def __init__(self, seed, shape, dtype):
        np.random.seed(seed)
        self._dtype = dtype
        self._start_obs = np.array(np.random.randint(0, 256, size=shape), dtype=dtype)
        self._max_steps = seed + 1
        self._cur_obs = None
        self._cur_step = 0
        self.action_space = gym.spaces.Box(low=0, high=255, shape=shape, dtype=dtype)
        self.observation_space = self.action_space

    def step(self, action):
        self._cur_obs += np.array(action, dtype=(self._dtype))
        self._cur_step += 1
        done = self._cur_step >= self._max_steps
        reward = self._cur_step / self._max_steps
        return (self._cur_obs, reward, done, {'foo': 'bar' + str(reward)})

    def reset(self):
        self._cur_obs = self._start_obs
        self._cur_step = 0
        return self._cur_obs

    def render(self, mode=None):
        raise NotImplementedError


@with_mpi()
def test_mpi_with_subprocvecenv():
    shape = (2, 3, 4)
    nenv = 1
    venv = SubprocVecEnv([lambda : SimpleEnv(0, shape, 'float32')] * nenv)
    ob = venv.reset()
    venv.close()
    @py_assert1 = ob.shape
    @py_assert4 = (
     nenv,)
    @py_assert7 = @py_assert4 + shape
    @py_assert3 = @py_assert1 == @py_assert7
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/test_vec_env.py', lineno=113)
    if not @py_assert3:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.shape\n} == (%(py5)s + %(py6)s)', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(ob) if 'ob' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ob) else 'ob',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(shape) if 'shape' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(shape) else 'shape'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert7 = None
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/test_video_recorder.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 1467 bytes
"""
Tests for asynchronous vectorized environments.
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, gym, pytest, os, glob, tempfile
from .dummy_vec_env import DummyVecEnv
from .shmem_vec_env import ShmemVecEnv
from .subproc_vec_env import SubprocVecEnv
from .vec_video_recorder import VecVideoRecorder

@pytest.mark.parametrize('klass', (DummyVecEnv, ShmemVecEnv, SubprocVecEnv))
@pytest.mark.parametrize('num_envs', (1, 4))
@pytest.mark.parametrize('video_length', (10, 100))
@pytest.mark.parametrize('video_interval', (1, 50))
def test_video_recorder(klass, num_envs, video_length, video_interval):
    """
    Wrap an existing VecEnv with VevVideoRecorder,
    Make (video_interval + video_length + 1) steps,
    then check that the file is present
    """

    def make_fn():
        env = gym.make('PongNoFrameskip-v4')
        return env

    fns = [make_fn for _ in range(num_envs)]
    env = klass(fns)
    with tempfile.TemporaryDirectory() as (video_path):
        env = VecVideoRecorder(env, video_path, record_video_trigger=(lambda x: x % video_interval == 0), video_length=video_length)
        env.reset()
        for _ in range(video_interval + video_length + 1):
            env.step([0] * num_envs)

        env.close()
        recorded_video = glob.glob(os.path.join(video_path, '*.mp4'))
        @py_assert2 = len(recorded_video)
        @py_assert5 = 2
        @py_assert4 = @py_assert2 == @py_assert5
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/test_video_recorder.py', lineno=45)
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(recorded_video) if 'recorded_video' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recorded_video) else 'recorded_video',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert1 = (os.stat(p).st_size != 0 for p in recorded_video)
        @py_assert3 = all(@py_assert1)
        if @py_assert3 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/test_video_recorder.py', lineno=47)
        if not @py_assert3:
            @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = @py_assert3 = None
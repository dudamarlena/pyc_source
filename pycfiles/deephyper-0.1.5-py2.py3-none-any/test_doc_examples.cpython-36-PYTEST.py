# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_doc_examples.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 1410 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
try:
    import mujoco_py
    _mujoco_present = True
except BaseException:
    mujoco_py = None
    _mujoco_present = False

@pytest.mark.skipif((not _mujoco_present),
  reason='error loading mujoco - either mujoco / mujoco key not present, or LD_LIBRARY_PATH is not pointing to mujoco library')
def test_lstm_example():
    import tensorflow as tf
    from deephyper.search.nas.baselines.common import policies, models, cmd_util
    from deephyper.search.nas.baselines.common.vec_env.dummy_vec_env import DummyVecEnv
    venv = DummyVecEnv([
     lambda : cmd_util.make_mujoco_env('Reacher-v2', seed=0)])
    with tf.Session() as (sess):
        policy = policies.build_policy(venv, models.lstm(128))(nbatch=1, nsteps=1)
        sess.run(tf.global_variables_initializer())
        ob = venv.reset()
        state = policy.initial_state
        done = [False]
        step_counter = 0
        while 1:
            action, _, state, _ = policy.step(ob, S=state, M=done)
            ob, reward, done, _ = venv.step(action)
            step_counter += 1
            if done:
                break

        @py_assert2 = 5
        @py_assert1 = step_counter > @py_assert2
        if @py_assert1 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_doc_examples.py', lineno=45)
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('>', ), (@py_assert1,), ('%(py0)s > %(py3)s', ), (step_counter, @py_assert2)) % {'py0':@pytest_ar._saferepr(step_counter) if 'step_counter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(step_counter) else 'step_counter',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
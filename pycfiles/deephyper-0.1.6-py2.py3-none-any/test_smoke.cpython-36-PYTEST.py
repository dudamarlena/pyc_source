# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/ddpg/test_smoke.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 529 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from multiprocessing import Process
import deephyper.search.nas.baselines.run

def _run(argstr):
    p = Process(target=(baselines.run.main), args=(('--alg=ddpg --env=Pendulum-v0 --num_timesteps=0 ' + argstr).split(' ')))
    p.start()
    p.join()


def test_popart():
    _run('--normalize_returns=True --popart=True')


def test_noise_normal():
    _run('--noise_type=normal_0.1')


def test_noise_ou():
    _run('--noise_type=ou_0.1')


def test_noise_adaptive():
    _run('--noise_type=adaptive-param_0.2,normal_0.1')
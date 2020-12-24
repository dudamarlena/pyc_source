# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/trpo_mpi/defaults.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 656 bytes
from deephyper.search.nas.baselines.common.models import mlp, cnn_small

def atari():
    return dict(network=(cnn_small()),
      timesteps_per_batch=512,
      max_kl=0.001,
      cg_iters=10,
      cg_damping=0.001,
      gamma=0.98,
      lam=1.0,
      vf_iters=3,
      vf_stepsize=0.0001,
      entcoeff=0.0)


def mujoco():
    return dict(network=mlp(num_hidden=32, num_layers=2),
      timesteps_per_batch=1024,
      max_kl=0.01,
      cg_iters=10,
      cg_damping=0.1,
      gamma=0.99,
      lam=0.98,
      vf_iters=5,
      vf_stepsize=0.001,
      normalize_observations=True)
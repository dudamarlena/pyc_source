# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/erwincoumans/dev/tmp/bullet3/examples/pybullet/gym/pybullet_envs/bullet/env_randomizer_base.py
# Compiled at: 2020-04-29 23:02:34
# Size of source mod 2**32: 622 bytes
"""Abstract base class for environment randomizer."""
import abc

class EnvRandomizerBase(object):
    __doc__ = 'Abstract base class for environment randomizer.\n\n  An EnvRandomizer is called in environment.reset(). It will\n  randomize physical parameters of the objects in the simulation.\n  The physical parameters will be fixed for that episode and be\n  randomized again in the next environment.reset().\n  '
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def randomize_env(self, env):
        """Randomize the simulated_objects in the environment.

    Args:
      env: The environment to be randomized.
    """
        pass
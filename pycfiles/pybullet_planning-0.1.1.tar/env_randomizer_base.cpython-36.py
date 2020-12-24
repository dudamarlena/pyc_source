# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/erwincoumans/dev/tmp/bullet3/examples/pybullet/gym/pybullet_envs/bullet/env_randomizer_base.py
# Compiled at: 2020-04-29 23:02:34
# Size of source mod 2**32: 622 bytes
__doc__ = 'Abstract base class for environment randomizer.'
import abc

class EnvRandomizerBase(object):
    """EnvRandomizerBase"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def randomize_env(self, env):
        """Randomize the simulated_objects in the environment.

    Args:
      env: The environment to be randomized.
    """
        pass
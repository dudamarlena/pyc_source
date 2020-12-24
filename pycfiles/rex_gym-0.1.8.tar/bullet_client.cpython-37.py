# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/seven/dev/rex-gym/rex_gym/util/bullet_client.py
# Compiled at: 2019-12-07 11:19:06
# Size of source mod 2**32: 1894 bytes
"""A wrapper for pybullet to manage different clients."""
from __future__ import absolute_import
from __future__ import division
import functools, inspect, pybullet

class BulletClient(object):
    __doc__ = 'A wrapper for pybullet to manage different clients.'

    def __init__(self, connection_mode=None):
        """Creates a Bullet client and connects to a simulation.

    Args:
      connection_mode:
        `None` connects to an existing simulation or, if fails, creates a
          new headless simulation,
        `pybullet.GUI` creates a new simulation with a GUI,
        `pybullet.DIRECT` creates a headless simulation,
        `pybullet.SHARED_MEMORY` connects to an existing simulation.
    """
        self._shapes = {}
        if connection_mode is None:
            self._client = pybullet.connect(pybullet.SHARED_MEMORY)
            if self._client >= 0:
                return
            connection_mode = pybullet.DIRECT
        self._client = pybullet.connect(connection_mode)

    def __del__(self):
        """Clean up connection if not already done."""
        try:
            pybullet.disconnect(physicsClientId=(self._client))
        except pybullet.error:
            pass

    def __getattr__(self, name):
        """Inject the client id into Bullet functions."""
        attribute = getattr(pybullet, name)
        if inspect.isbuiltin(attribute):
            if name not in ('invertTransform', 'multiplyTransforms', 'getMatrixFromQuaternion',
                            'getEulerFromQuaternion', 'computeViewMatrixFromYawPitchRoll',
                            'computeProjectionMatrixFOV', 'getQuaternionFromEuler'):
                attribute = functools.partial(attribute, physicsClientId=(self._client))
        return attribute
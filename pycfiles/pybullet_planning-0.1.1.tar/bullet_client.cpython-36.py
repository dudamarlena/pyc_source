# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/erwincoumans/dev/tmp/bullet3/examples/pybullet/gym/pybullet_utils/bullet_client.py
# Compiled at: 2020-04-29 23:02:34
# Size of source mod 2**32: 1523 bytes
__doc__ = 'A wrapper for pybullet to manage different clients.'
from __future__ import absolute_import
from __future__ import division
import functools, inspect, pybullet

class BulletClient(object):
    """BulletClient"""

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
        if self._client >= 0:
            try:
                pybullet.disconnect(physicsClientId=(self._client))
                self._client = -1
            except pybullet.error:
                pass

    def __getattr__(self, name):
        """Inject the client id into Bullet functions."""
        attribute = getattr(pybullet, name)
        if inspect.isbuiltin(attribute):
            attribute = functools.partial(attribute, physicsClientId=(self._client))
        if name == 'disconnect':
            self._client = -1
        return attribute
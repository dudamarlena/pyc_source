# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/erwincoumans/dev/tmp/bullet3/examples/pybullet/gym/pybullet_envs/scene_stadium.py
# Compiled at: 2020-04-29 23:02:34
# Size of source mod 2**32: 2130 bytes
import os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
os.sys.path.insert(0, parentdir)
import pybullet_data
from pybullet_envs.scene_abstract import Scene
import pybullet

class StadiumScene(Scene):
    zero_at_running_strip_start_line = True
    stadium_halflen = 26.25
    stadium_halfwidth = 12.5
    stadiumLoaded = 0

    def episode_restart(self, bullet_client):
        self._p = bullet_client
        Scene.episode_restart(self, bullet_client)
        if self.stadiumLoaded == 0:
            self.stadiumLoaded = 1
            filename = os.path.join(pybullet_data.getDataPath(), 'plane_stadium.sdf')
            self.ground_plane_mjcf = self._p.loadSDF(filename)
            for i in self.ground_plane_mjcf:
                self._p.changeDynamics(i, (-1), lateralFriction=0.8, restitution=0.5)
                self._p.changeVisualShape(i, (-1), rgbaColor=[1, 1, 1, 0.8])
                self._p.configureDebugVisualizer(pybullet.COV_ENABLE_PLANAR_REFLECTION, i)


class SinglePlayerStadiumScene(StadiumScene):
    """SinglePlayerStadiumScene"""
    multiplayer = False


class MultiplayerStadiumScene(StadiumScene):
    multiplayer = True
    players_count = 3

    def actor_introduce(self, robot):
        StadiumScene.actor_introduce(self, robot)
        i = robot.player_n - 1
        robot.move_robot(0, i, 0)
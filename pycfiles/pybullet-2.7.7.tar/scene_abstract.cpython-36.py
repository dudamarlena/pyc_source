# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/erwincoumans/dev/tmp/bullet3/examples/pybullet/gym/pybullet_envs/scene_abstract.py
# Compiled at: 2020-04-29 23:02:34
# Size of source mod 2**32: 2628 bytes
import sys, os
sys.path.append(os.path.dirname(__file__))
import pybullet, gym

class Scene:
    __doc__ = 'A base class for single- and multiplayer scenes'

    def __init__(self, bullet_client, gravity, timestep, frame_skip):
        self._p = bullet_client
        self.np_random, seed = gym.utils.seeding.np_random(None)
        self.timestep = timestep
        self.frame_skip = frame_skip
        self.dt = self.timestep * self.frame_skip
        self.cpp_world = World(self._p, gravity, timestep, frame_skip)
        self.test_window_still_open = True
        self.human_render_detected = False
        self.multiplayer_robots = {}

    def test_window(self):
        """Call this function every frame, to see what's going on. Not necessary in learning."""
        self.human_render_detected = True
        return self.test_window_still_open

    def actor_introduce(self, robot):
        """Usually after scene reset"""
        if not self.multiplayer:
            return
        self.multiplayer_robots[robot.player_n] = robot

    def actor_is_active(self, robot):
        """
        Used by robots to see if they are free to exclusiveley put their HUD on the test window.
        Later can be used for click-focus robots.
        """
        return not self.multiplayer

    def episode_restart(self, bullet_client):
        """This function gets overridden by specific scene, to reset specific objects into their start positions"""
        self.cpp_world.clean_everything()

    def global_step(self):
        """
        The idea is: apply motor torques for all robots, then call global_step(), then collect
        observations from robots using step() with the same action.
        """
        self.cpp_world.step(self.frame_skip)


class SingleRobotEmptyScene(Scene):
    multiplayer = False


class World:

    def __init__(self, bullet_client, gravity, timestep, frame_skip):
        self._p = bullet_client
        self.gravity = gravity
        self.timestep = timestep
        self.frame_skip = frame_skip
        self.numSolverIterations = 5
        self.clean_everything()

    def clean_everything(self):
        self._p.setGravity(0, 0, -self.gravity)
        self._p.setDefaultContactERP(0.9)
        self._p.setPhysicsEngineParameter(fixedTimeStep=(self.timestep * self.frame_skip), numSolverIterations=(self.numSolverIterations),
          numSubSteps=(self.frame_skip))

    def step(self, frame_skip):
        self._p.stepSimulation()
# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/erwincoumans/dev/tmp/bullet3/examples/pybullet/gym/pybullet_envs/bullet/cartpole_bullet.py
# Compiled at: 2020-04-29 23:02:34
# Size of source mod 2**32: 5705 bytes
__doc__ = '\nClassic cart-pole system implemented by Rich Sutton et al.\nCopied from https://webdocs.cs.ualberta.ca/~sutton/book/code/pole.c\n'
import os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0, parentdir)
import logging, math, gym
from gym import spaces
from gym.utils import seeding
import numpy as np, time, subprocess, pybullet as p2, pybullet_data, pybullet_utils.bullet_client as bc
from pkg_resources import parse_version
logger = logging.getLogger(__name__)

class CartPoleBulletEnv(gym.Env):
    metadata = {'render.modes':[
      'human', 'rgb_array'], 
     'video.frames_per_second':50}

    def __init__(self, renders=False, discrete_actions=True):
        self._renders = renders
        self._discrete_actions = discrete_actions
        self._render_height = 200
        self._render_width = 320
        self._physics_client_id = -1
        self.theta_threshold_radians = 24 * math.pi / 360
        self.x_threshold = 0.4
        high = np.array([
         self.x_threshold * 2,
         np.finfo(np.float32).max, self.theta_threshold_radians * 2,
         np.finfo(np.float32).max])
        self.force_mag = 10
        if self._discrete_actions:
            self.action_space = spaces.Discrete(2)
        else:
            action_dim = 1
            action_high = np.array([self.force_mag] * action_dim)
            self.action_space = spaces.Box(-action_high, action_high)
        self.observation_space = spaces.Box((-high), high, dtype=(np.float32))
        self.seed()
        self.viewer = None
        self._configure()

    def _configure(self, display=None):
        self.display = display

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [
         seed]

    def step(self, action):
        p = self._p
        if self._discrete_actions:
            force = self.force_mag if action == 1 else -self.force_mag
        else:
            force = action[0]
        p.setJointMotorControl2((self.cartpole), 0, (p.TORQUE_CONTROL), force=force)
        p.stepSimulation()
        self.state = p.getJointState(self.cartpole, 1)[0:2] + p.getJointState(self.cartpole, 0)[0:2]
        theta, theta_dot, x, x_dot = self.state
        done = x < -self.x_threshold or x > self.x_threshold or theta < -self.theta_threshold_radians or theta > self.theta_threshold_radians
        done = bool(done)
        reward = 1.0
        return (
         np.array(self.state), reward, done, {})

    def reset(self):
        if self._physics_client_id < 0:
            if self._renders:
                self._p = bc.BulletClient(connection_mode=(p2.GUI))
            else:
                self._p = bc.BulletClient()
            self._physics_client_id = self._p._client
            p = self._p
            p.resetSimulation()
            self.cartpole = p.loadURDF(os.path.join(pybullet_data.getDataPath(), 'cartpole.urdf'), [
             0, 0, 0])
            p.changeDynamics((self.cartpole), (-1), linearDamping=0, angularDamping=0)
            p.changeDynamics((self.cartpole), 0, linearDamping=0, angularDamping=0)
            p.changeDynamics((self.cartpole), 1, linearDamping=0, angularDamping=0)
            self.timeStep = 0.02
            p.setJointMotorControl2((self.cartpole), 1, (p.VELOCITY_CONTROL), force=0)
            p.setJointMotorControl2((self.cartpole), 0, (p.VELOCITY_CONTROL), force=0)
            p.setGravity(0, 0, -9.8)
            p.setTimeStep(self.timeStep)
            p.setRealTimeSimulation(0)
        p = self._p
        randstate = self.np_random.uniform(low=(-0.05), high=0.05, size=(4, ))
        p.resetJointState(self.cartpole, 1, randstate[0], randstate[1])
        p.resetJointState(self.cartpole, 0, randstate[2], randstate[3])
        self.state = p.getJointState(self.cartpole, 1)[0:2] + p.getJointState(self.cartpole, 0)[0:2]
        return np.array(self.state)

    def render(self, mode='human', close=False):
        if mode == 'human':
            self._renders = True
        if mode != 'rgb_array':
            return np.array([])
        else:
            base_pos = [
             0, 0, 0]
            self._cam_dist = 2
            self._cam_pitch = 0.3
            self._cam_yaw = 0
            if self._physics_client_id >= 0:
                view_matrix = self._p.computeViewMatrixFromYawPitchRoll(cameraTargetPosition=base_pos,
                  distance=(self._cam_dist),
                  yaw=(self._cam_yaw),
                  pitch=(self._cam_pitch),
                  roll=0,
                  upAxisIndex=2)
                proj_matrix = self._p.computeProjectionMatrixFOV(fov=60, aspect=(float(self._render_width) / self._render_height),
                  nearVal=0.1,
                  farVal=100.0)
                _, _, px, _, _ = self._p.getCameraImage(width=(self._render_width),
                  height=(self._render_height),
                  renderer=(self._p.ER_BULLET_HARDWARE_OPENGL),
                  viewMatrix=view_matrix,
                  projectionMatrix=proj_matrix)
            else:
                px = np.array(([[[255, 255, 255, 255]] * self._render_width] * self._render_height), dtype=(np.uint8))
            rgb_array = np.array(px, dtype=(np.uint8))
            rgb_array = np.reshape(np.array(px), (self._render_height, self._render_width, -1))
            rgb_array = rgb_array[:, :, :3]
            return rgb_array

    def configure(self, args):
        pass

    def close(self):
        if self._physics_client_id >= 0:
            self._p.disconnect()
        self._physics_client_id = -1


class CartPoleContinuousBulletEnv(CartPoleBulletEnv):
    metadata = {'render.modes':[
      'human', 'rgb_array'], 
     'video.frames_per_second':50}

    def __init__(self, renders=False):
        CartPoleBulletEnv.__init__(self, renders, discrete_actions=False)
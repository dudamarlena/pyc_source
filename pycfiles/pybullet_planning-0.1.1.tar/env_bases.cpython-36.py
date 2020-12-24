# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/erwincoumans/dev/tmp/bullet3/examples/pybullet/gym/pybullet_envs/env_bases.py
# Compiled at: 2020-04-29 23:02:34
# Size of source mod 2**32: 5809 bytes
import gym, gym.spaces, gym.utils, gym.utils.seeding, numpy as np, pybullet, os
from pybullet_utils import bullet_client
from pkg_resources import parse_version
try:
    if os.environ['PYBULLET_EGL']:
        import pkgutil
except:
    pass

class MJCFBaseBulletEnv(gym.Env):
    """MJCFBaseBulletEnv"""
    metadata = {'render.modes':[
      'human', 'rgb_array'], 
     'video.frames_per_second':60}

    def __init__(self, robot, render=False):
        self.scene = None
        self.physicsClientId = -1
        self.ownsPhysicsClient = 0
        self.camera = Camera(self)
        self.isRender = render
        self.robot = robot
        self.seed()
        self._cam_dist = 3
        self._cam_yaw = 0
        self._cam_pitch = -30
        self._render_width = 320
        self._render_height = 240
        self.action_space = robot.action_space
        self.observation_space = robot.observation_space

    def configure(self, args):
        self.robot.args = args

    def seed(self, seed=None):
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        self.robot.np_random = self.np_random
        return [
         seed]

    def reset(self):
        if self.physicsClientId < 0:
            self.ownsPhysicsClient = True
            if self.isRender:
                self._p = bullet_client.BulletClient(connection_mode=(pybullet.GUI))
            else:
                self._p = bullet_client.BulletClient()
            self._p.resetSimulation()
            self._p.setPhysicsEngineParameter(deterministicOverlappingPairs=1)
            try:
                if os.environ['PYBULLET_EGL']:
                    con_mode = self._p.getConnectionInfo()['connectionMethod']
                    if con_mode == self._p.DIRECT:
                        egl = pkgutil.get_loader('eglRenderer')
                        if egl:
                            self._p.loadPlugin(egl.get_filename(), '_eglRendererPlugin')
                        else:
                            self._p.loadPlugin('eglRendererPlugin')
            except:
                pass

            self.physicsClientId = self._p._client
            self._p.configureDebugVisualizer(pybullet.COV_ENABLE_GUI, 0)
        else:
            if self.scene is None:
                self.scene = self.create_single_player_scene(self._p)
            if not self.scene.multiplayer:
                if self.ownsPhysicsClient:
                    self.scene.episode_restart(self._p)
        self.robot.scene = self.scene
        self.frame = 0
        self.done = 0
        self.reward = 0
        dump = 0
        s = self.robot.reset(self._p)
        self.potential = self.robot.calc_potential()
        return s

    def camera_adjust(self):
        pass

    def render(self, mode='human', close=False):
        if mode == 'human':
            self.isRender = True
        if self.physicsClientId >= 0:
            self.camera_adjust()
        if mode != 'rgb_array':
            return np.array([])
        else:
            base_pos = [
             0, 0, 0]
            if hasattr(self, 'robot'):
                if hasattr(self.robot, 'body_real_xyz'):
                    base_pos = self.robot.body_real_xyz
            if self.physicsClientId >= 0:
                view_matrix = self._p.computeViewMatrixFromYawPitchRoll(cameraTargetPosition=base_pos, distance=(self._cam_dist),
                  yaw=(self._cam_yaw),
                  pitch=(self._cam_pitch),
                  roll=0,
                  upAxisIndex=2)
                proj_matrix = self._p.computeProjectionMatrixFOV(fov=60, aspect=(float(self._render_width) / self._render_height),
                  nearVal=0.1,
                  farVal=100.0)
                _, _, px, _, _ = self._p.getCameraImage(width=(self._render_width), height=(self._render_height),
                  viewMatrix=view_matrix,
                  projectionMatrix=proj_matrix,
                  renderer=(pybullet.ER_BULLET_HARDWARE_OPENGL))
                self._p.configureDebugVisualizer(self._p.COV_ENABLE_SINGLE_STEP_RENDERING, 1)
            else:
                px = np.array(([[[255, 255, 255, 255]] * self._render_width] * self._render_height), dtype=(np.uint8))
            rgb_array = np.array(px, dtype=(np.uint8))
            rgb_array = np.reshape(np.array(px), (self._render_height, self._render_width, -1))
            rgb_array = rgb_array[:, :, :3]
            return rgb_array

    def close(self):
        if self.ownsPhysicsClient:
            if self.physicsClientId >= 0:
                self._p.disconnect()
        self.physicsClientId = -1

    def HUD(self, state, a, done):
        pass

    if parse_version(gym.__version__) < parse_version('0.9.6'):
        _render = render
        _reset = reset
        _seed = seed


class Camera:

    def __init__(self, env):
        self.env = env

    def move_and_look_at(self, i, j, k, x, y, z):
        lookat = [
         x, y, z]
        camInfo = self.env._p.getDebugVisualizerCamera()
        distance = camInfo[10]
        pitch = camInfo[9]
        yaw = camInfo[8]
        self.env._p.resetDebugVisualizerCamera(distance, yaw, pitch, lookat)
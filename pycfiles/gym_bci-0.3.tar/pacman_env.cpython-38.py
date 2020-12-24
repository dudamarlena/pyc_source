# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yeison/Development/gcpds/gym-bci/test/gym_bci/envs/pacman/pacman_env.py
# Compiled at: 2019-12-18 17:12:41
# Size of source mod 2**32: 10395 bytes
import gym
from gym import spaces
from gym.utils import seeding
import numpy as np, time
from .graphicsDisplay import PacmanGraphics, DEFAULT_GRID_SIZE
from .game import Actions
from .pacman import ClassicGameRules
from .layout import getLayout, getRandomLayout
from .ghostAgents import DirectionalGhost
from .pacmanAgents import OpenAIAgent
from gym.utils import seeding
import json, os
DEFAULT_GHOST_TYPE = 'DirectionalGhost'
MAX_GHOSTS = 5
PACMAN_ACTIONS = [
 'north', 'south', 'east', 'west', 'stop']
PACMAN_DIRECTIONS = [
 'north', 'south', 'east', 'west']
ROTATION_ANGLES = [0, 180, 90, 270]
MAX_EP_LENGTH = 100
import os
fdir = '/'.join(os.path.split(__file__)[:-1])
print(fdir)

class PacmanEnv(gym.Env):
    layouts = [
     'capsuleClassic',
     'contestClassic',
     'mediumClassic',
     'mediumGrid',
     'minimaxClassic',
     'openClassic',
     'originalClassic',
     'smallClassic',
     'smallGrid',
     'testClassic',
     'trappedClassic',
     'trickyClassic']
    noGhost_layouts = [l + '_noGhosts' for l in layouts]
    MAX_MAZE_SIZE = (7, 7)
    num_envs = 1
    observation_space = spaces.Box(low=0, high=255, shape=(84, 84, 3),
      dtype=(np.uint8))

    def __init__(self):
        self.action_space = spaces.Discrete(4)
        self.display = PacmanGraphics(1.0)
        self._action_set = range(len(PACMAN_ACTIONS))
        self.location = None
        self.viewer = None
        self.done = False
        self.layout = None
        self.np_random = np.random

    def setObservationSpace(self):
        screen_width, screen_height = self.display.calculate_screen_dimensions(self.layout.width, self.layout.height)
        self.observation_space = spaces.Box(low=0, high=255, shape=(
         int(screen_height),
         int(screen_width),
         3),
          dtype=(np.uint8))

    def chooseLayout(self, randomLayout, chosenLayout, no_ghosts, **layout_params):
        if not randomLayout:
            if no_ghosts:
                if not chosenLayout.endswith('noGhost'):
                    chosenLayout += '_noGhosts'
        elif randomLayout:
            self.layout = getRandomLayout(layout_params, self.np_random)
        else:
            if chosenLayout is None:
                if not no_ghosts:
                    chosenLayout = self.np_random.choice(self.layouts)
                else:
                    chosenLayout = self.np_random.choice(self.noGhost_layouts)
            self.chosen_layout = chosenLayout
            print('Chose layout', chosenLayout)
            self.layout = getLayout(chosenLayout)
        self.maze_size = (
         self.layout.width, self.layout.height)

    def seed(self, seed=None):
        if self.np_random is None:
            self.np_random, seed = seeding.np_random(seed)
        self.chooseLayout(randomLayout=True)
        return [seed]

    def reset(self, randomLayout=False, chosenLayout=None, no_ghosts=False, no_finish=True, pacman_location=None, **layout_params):
        self.no_finish = no_finish
        (self.chooseLayout)(randomLayout, chosenLayout, no_ghosts, **layout_params)
        self.step_counter = 0
        self.cum_reward = 0
        self.done = False
        self.setObservationSpace()
        self.ghosts = [DirectionalGhost((i + 1), prob_attack=0.2, prob_scaredFlee=0.2) for i in range(MAX_GHOSTS)]
        self.pacman = OpenAIAgent()
        self.rules = ClassicGameRules(300)
        self.rules.quiet = False
        self.game = self.rules.newGame(self.layout, self.pacman, self.ghosts, self.display, False, False)
        self.game.init()
        self.display.initialize(self.game.state.data)
        self.display.updateView()
        if pacman_location:
            self.game.state.data.agentStates[0].configuration.pos = pacman_location
        self.location = self.game.state.data.agentStates[0].getPosition()
        self.ghostLocations = [a.getPosition() for a in self.game.state.data.agentStates[1:]]
        self.ghostInFrame = any([np.sum(np.abs(np.array(g) - np.array(self.location))) <= 2 for g in self.ghostLocations])
        self.location_history = [
         self.location]
        self.orientation = PACMAN_DIRECTIONS.index(self.game.state.data.agentStates[0].getDirection())
        self.orientation_history = [self.orientation]
        self.illegal_move_counter = 0
        self.cum_reward = 0
        self.initial_info = {'past_loc':[
          self.location_history[(-1)]], 
         'curr_loc':[
          self.location_history[(-1)]], 
         'past_orientation':[
          [
           self.orientation_history[(-1)]]], 
         'curr_orientation':[
          [
           self.orientation_history[(-1)]]], 
         'illegal_move_counter':[
          self.illegal_move_counter], 
         'ghost_positions':[
          self.ghostLocations], 
         'ghost_in_frame':[
          self.ghostInFrame], 
         'step_counter':[
          [
           0]]}
        return self._get_image()

    def step(self, action, pacman_location=(1, 1), delay=0):
        if action == 'move':
            self.game.state.data.agentStates[0].configuration.pos = pacman_location
        else:
            pacman_action = action.lower()
            legal_actions = self.game.state.getLegalPacmanActions()
            illegal_action = False
            if pacman_action not in legal_actions:
                self.illegal_move_counter += 1
                illegal_action = True
                pacman_action = 'stop'
            reward = self.game.step(pacman_action)
            self.cum_reward += reward
            if illegal_action:
                reward -= 10
            done = self.game.state.isWin() or self.game.state.isLose()
            self.location = self.game.state.data.agentStates[0].getPosition()
            self.location_history.append(self.location)
            self.ghostLocations = [a.getPosition() for a in self.game.state.data.agentStates[1:]]
            self.orientation = PACMAN_DIRECTIONS.index(self.game.state.data.agentStates[0].getDirection())
            self.orientation_history.append(self.orientation)
            extent = (
             (
              self.location[0] - 1, self.location[1] - 1), (self.location[0] + 1, self.location[1] + 1))
            self.ghostInFrame = any([g[0] >= extent[0][0] and g[1] >= extent[0][1] and g[0] <= extent[1][0] and g[1] <= extent[1][1] for g in self.ghostLocations])
            self.no_finish or self.step_counter += 1
        info = {'past_loc':[
          self.location_history[(-2)]], 
         'curr_loc':[
          self.location_history[(-1)]], 
         'past_orientation':[
          [
           self.orientation_history[(-2)]]], 
         'curr_orientation':[
          [
           self.orientation_history[(-1)]]], 
         'illegal_move_counter':[
          self.illegal_move_counter], 
         'step_counter':[
          [
           self.step_counter]], 
         'episode':[
          None], 
         'ghost_positions':[
          self.ghostLocations], 
         'ghost_in_frame':[
          self.ghostInFrame]}
        if self.step_counter >= MAX_EP_LENGTH:
            done = True
        self.done = done
        if self.done:
            info['episode'] = [
             {'r':self.cum_reward,  'l':self.step_counter}]
        time.sleep(delay)
        return (self._get_image(), reward, done, info)

    def get_action_meanings(self):
        return [PACMAN_ACTIONS[i] for i in self._action_set]

    def _get_image(self):
        image = self.display.image
        w, h = image.size
        DEFAULT_GRID_SIZE_X, DEFAULT_GRID_SIZE_Y = w / float(self.layout.width), h / float(self.layout.height)
        extent = [
         DEFAULT_GRID_SIZE_X * (self.location[0] - 1),
         DEFAULT_GRID_SIZE_Y * (self.layout.height - (self.location[1] + 2.2)),
         DEFAULT_GRID_SIZE_X * (self.location[0] + 2),
         DEFAULT_GRID_SIZE_Y * (self.layout.height - (self.location[1] - 1.2))]
        extent = tuple([int(e) for e in extent])
        self.image_sz = (84, 84)
        image = image.crop(extent).resize(self.image_sz)
        return np.array(image)

    def close(self):
        if self.viewer is not None:
            self.viewer.close()
        self.display.finish()

    def __del__(self):
        self.close()
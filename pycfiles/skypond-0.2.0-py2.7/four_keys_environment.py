# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skypond/games/four_keys/four_keys_environment.py
# Compiled at: 2019-05-02 00:18:49
from __future__ import absolute_import
import os, gym, time, math, numpy as np, urllib, hashlib
from collections import deque
from gym import error, spaces, utils
from gym.utils import seeding
from .four_keys_actions import FourKeysActions
from .four_keys_board_items import FourKeysBoardItems
from .four_keys_constants import ATTACK_FULL_CHARGE, MOVEMENT_FULL_CHARGE, HISTORY_QUEUE_LENGTH, TOTAL_KEYS, STARTING_PLAYER_NUMBER, BREADCRUMB_LIFESPAN

class FourKeysEnvironment(gym.Env):

    def __init__(self, shared_state, player_number, details=None):
        self._shared_state = shared_state
        self.actions = FourKeysActions
        self.action_space = self._shared_state.action_space
        self.observation_space = self._shared_state.observation_space
        self.last_action_keys = 0
        self.total_steps = 0
        self.max_steps = 200
        self.number = player_number
        self.status_update_handler = None
        self.last_breadcrumb = 0
        self.history_queue = deque([])
        self.breadcrumb_queue = deque([])
        self.prev_distance_reward = None
        self.current_distance_reward = 0
        self.breadcrumbs = []
        self.total_drops = 0
        self.homogenize_player_numbers = True
        self.custom_reward = None
        self._last_board_observation = None
        self.reset(reset_shared_state=False)
        self.status = {'number': player_number, 'name': 'Unknown ' + str(player_number + 1), 'pic': '', 'description': '', 'address': '', 'endpoint': '', 'pickups': 0, 'attacks': 0, 'status': 'live', 'position': {'x': 0, 'y': 0}}
        if details:
            if 'username' in details and details['username']:
                self.status['name'] = details['username']
            if 'eth_address' in details and details['eth_address']:
                self.status['address'] = details['eth_address']
            if 'email' in details and details['email']:
                gravatar_url = 'https://www.gravatar.com/avatar/' + hashlib.md5(details['email'].lower().encode('utf-8')).hexdigest() + '?'
                gravatar_url += 's=42'
                self.status['pic'] = gravatar_url
        size = int(math.sqrt(len(self._shared_state.board)))
        self.position = shared_state.starting_points[player_number]
        self.last_position = self.position
        pos = self.position[0] * size + self.position[1]
        self._shared_state.board[pos] = self.number + STARTING_PLAYER_NUMBER
        self._shared_state.register_attached_environment(self)
        return

    def process_status(self):
        self.status['keys'] = self.keys
        self.status['attack_recharge'] = self.attack_recharge
        self.status['move_recharge'] = self.move_recharge
        self.status['position']['x'] = self.position[1]
        self.status['position']['y'] = self.position[0]
        self.status['pickups'] = self.pickups
        self.status['attacks'] = self.attacks
        if self.status_update_handler is not None:
            self.status_update_handler(self)
        return

    def get_adjacent_players(self):
        max_item = len(self._shared_state.board)
        size = int(math.sqrt(max_item))
        pos = self.position[0] * size + self.position[1]
        locs = [pos - 1 if pos - 1 >= 0 and (pos - 1) % size != size - 1 else None,
         pos + 1 if pos + 1 < max_item and (pos + 1) % size != 0 else None,
         pos + size if pos + size < max_item else None,
         pos - size if pos - size >= 0 else None]
        adjacent_players = []
        for loc in locs:
            if loc is None:
                continue
            if self._shared_state.board[loc] >= STARTING_PLAYER_NUMBER and self._shared_state.board[loc] <= STARTING_PLAYER_NUMBER + 8:
                adjacent_players.append(loc)

        return adjacent_players

    def players_adjacent(self):
        return len(self.get_adjacent_players()) > 0

    def perform_action(self, action):
        if action == FourKeysActions.NOTHING:
            return True
        else:
            if action == FourKeysActions.DROP_KEY:
                self.drop_key()
                self.total_drops += 1
            if action == FourKeysActions.ATTACK:
                if self._shared_state.attack_handler is not None:
                    adjacent_players = self.get_adjacent_players()
                    self._shared_state.attack_handler(adjacent_players)
                    self.attack_recharge = 0
                    self.attacks += 1
                    return True
                else:
                    return False

            max_item = len(self._shared_state.board)
            size = int(math.sqrt(max_item))
            pos = self.position[0] * size + self.position[1]
            locs = [pos - 1 if pos - 1 >= 0 else None,
             pos + 1 if pos + 1 < max_item else None,
             pos + size if pos + size < max_item else None,
             pos - size if pos - size >= 0 else None]
            position_action_map = {FourKeysActions.LEFT: locs[0], FourKeysActions.RIGHT: locs[1], FourKeysActions.DOWN: locs[2], FourKeysActions.UP: locs[3]}
            if action in position_action_map.keys():
                return self.move(position_action_map[action])
            return

    def receive_attack(self):
        self.move_recharge = 0
        self.attack_recharge = math.floor(self.attack_recharge / 2)
        self.drop_keys()
        self.process_status()

    def drop_keys(self):
        while self.keys > 0:
            self.drop_key()

    def drop_key(self):
        if self.keys > 0:
            key_placement = self.closest_open_tile()
            self.keys -= 1
            self._shared_state.board[key_placement] = FourKeysBoardItems.KEY
            if self._shared_state.new_key_handler is not None:
                size = int(math.sqrt(len(self._shared_state.board)))
                coordinates = (math.floor(key_placement / size), key_placement % size)
                self._shared_state.new_key_handler(coordinates, self)
            return True
        return False
        return

    def closest_open_tile(self):
        spots = []
        layer = 1
        while len(spots) == 0:
            max_item = len(self._shared_state.board)
            size = int(math.sqrt(max_item))
            pos = self.position[0] * size + self.position[1]
            locs = [pos - layer if pos - layer >= 0 and (pos - layer) % size != size - 1 else None,
             pos + layer if pos + layer < max_item and (pos + layer) % size != 0 else None,
             pos + size * layer if pos + size * layer < max_item else None,
             pos - size * layer if pos - size * layer >= 0 else None]
            for loc in locs:
                if loc is None:
                    continue
                if self._shared_state.board[loc] == FourKeysBoardItems.EMPTY:
                    spots.append(loc)

            layer += 1

        if len(spots) > 0:
            key_placement = spots[0]
            if len(spots) > 1:
                spot_selection = self._shared_state.rng.randint(0, len(spots) - 1)
                key_placement = spots[spot_selection]
            return key_placement
        return

    def move(self, new_position_flat):
        size = int(math.sqrt(len(self._shared_state.board)))
        pos_flat = self.position[0] * size + self.position[1]
        self.position = (
         math.floor(new_position_flat / size), new_position_flat % size)
        if self._shared_state.board[new_position_flat] == FourKeysBoardItems.KEY:
            self.keys += 1
            self.pickups += 1
            if self._shared_state.key_consumed_handler is not None:
                self._shared_state.key_consumed_handler(self.position, self)
        self._shared_state.board[pos_flat] = FourKeysBoardItems.EMPTY
        self._shared_state.board[new_position_flat] = STARTING_PLAYER_NUMBER + self.number
        return

    def is_action_valid(self, action):
        if action == FourKeysActions.NOTHING:
            return True
        else:
            if action == FourKeysActions.DROP_KEY:
                return self.keys > 0
            if action == FourKeysActions.ATTACK and self.attack_recharge >= ATTACK_FULL_CHARGE:
                return self.players_adjacent()
            max_item = len(self._shared_state.board)
            size = int(math.sqrt(max_item))
            pos = self.position[0] * size + self.position[1]
            locs = [
             pos - 1 if pos - 1 >= 0 and (pos - 1) % size != size - 1 else None,
             pos + 1 if pos + 1 < max_item and (pos + 1) % size != 0 else None,
             pos + size if pos + size < max_item else None,
             pos - size if pos - size >= 0 else None]
            board = self._shared_state.board
            if action == FourKeysActions.LEFT and locs[0] is not None and (board[locs[0]] == FourKeysBoardItems.EMPTY or board[locs[0]] == FourKeysBoardItems.KEY):
                return self.move_recharge >= MOVEMENT_FULL_CHARGE
            if action == FourKeysActions.RIGHT and locs[1] is not None and (board[locs[1]] == FourKeysBoardItems.EMPTY or board[locs[1]] == FourKeysBoardItems.KEY):
                return self.move_recharge >= MOVEMENT_FULL_CHARGE
            if action == FourKeysActions.DOWN and locs[2] is not None and (board[locs[2]] == FourKeysBoardItems.EMPTY or board[locs[2]] == FourKeysBoardItems.KEY):
                return self.move_recharge >= MOVEMENT_FULL_CHARGE
            if action == FourKeysActions.UP and locs[3] is not None and (board[locs[3]] == FourKeysBoardItems.EMPTY or board[locs[3]] == FourKeysBoardItems.KEY):
                return self.move_recharge >= MOVEMENT_FULL_CHARGE
            return False

    def step(self, action):
        self.last_action_keys = self.keys
        self.prev_distance_reward = self.current_distance_reward
        self.last_position = self.position
        previous_value = self.breadcrumbs[(self.position[0], self.position[1])]
        self.breadcrumbs[(self.position[0], self.position[1])] = min(previous_value + 1, 20)
        self.breadcrumb_queue.append(self.position)
        if len(self.breadcrumb_queue) > BREADCRUMB_LIFESPAN:
            expired_breadcrumb_location = self.breadcrumb_queue.popleft()
            if self.breadcrumbs[(expired_breadcrumb_location[0], expired_breadcrumb_location[1])] > 0:
                self.breadcrumbs[(expired_breadcrumb_location[0], expired_breadcrumb_location[1])] -= 1
        if self.is_action_valid(action):
            self.perform_action(action)
        self.last_breadcrumb = self.breadcrumbs[(self.position[0], self.position[1])]
        if self.attack_recharge < ATTACK_FULL_CHARGE:
            self.attack_recharge += 1
        if self.move_recharge < 8:
            self.move_recharge += 1
        self.total_steps += 1
        self.process_status()
        observation = self.observe()
        self.snapshot_state(use_cached_observation=True)
        return observation

    def generate_current_observation(self):
        attack_recharge_percent = self.attack_recharge / ATTACK_FULL_CHARGE * 100
        movement_recharge_percent = self.move_recharge / MOVEMENT_FULL_CHARGE * 100
        result, board, visible_breadcrumbs = self._shared_state.generate_observation(self.position, self.history_queue, self.keys, attack_recharge_percent, movement_recharge_percent, self.homogenize_player_numbers, self.breadcrumbs)
        self._last_board_observation = board
        self._last_visible_breadcrumbs = visible_breadcrumbs
        return result

    def observe(self, include_status=False):
        attack_recharge_percent = self.attack_recharge / ATTACK_FULL_CHARGE * 100
        movement_recharge_percent = self.move_recharge / MOVEMENT_FULL_CHARGE * 100
        observation = self.generate_current_observation()
        done = self._shared_state.any_agent_won or self.total_steps >= self.max_steps
        if self.max_steps < 99999999:
            if self.custom_reward is None:
                reward = self.keys - self.last_action_keys
                if reward < 0:
                    reward = (self.keys - self.last_action_keys) * 1.05
                if done and self.keys == TOTAL_KEYS:
                    final_key_reward = self.max_steps / self.total_steps
                    reward += final_key_reward
                else:
                    if self.last_breadcrumb == 0:
                        reward += (1 - self.total_steps / self.max_steps * 4) * 0.01
                    if self.last_breadcrumb >= 10:
                        reward -= self.total_steps / self.max_steps * 4 * 0.01
            else:
                values = dict(last_breadcrumb=self.last_breadcrumb, total_steps=self.total_steps, max_steps=self.max_steps, current_keys=self.keys, previous_keys=self.last_action_keys, done=done)
                reward = self.custom_reward(values)
        else:
            reward = 0
        info = self.status if include_status else {}
        return (
         observation, reward, done, info)

    def snapshot_state(self, use_cached_observation=False):
        board_observation = self._last_board_observation
        if not use_cached_observation:
            board_observation = self._shared_state.get_observable_board(self.position)
        self.history_queue.append(board_observation)
        if len(self.history_queue) > HISTORY_QUEUE_LENGTH:
            self.history_queue.popleft()

    def reset(self, reset_shared_state=True):
        self.position = self._shared_state.starting_points[self.number]
        side = int(math.sqrt(self._shared_state.board.shape[0]))
        pos = self.position[0] * side + self.position[1]
        self._shared_state.board[pos] = self.number + STARTING_PLAYER_NUMBER
        self.history_queue = deque([])
        self.breadcrumb_queue = deque([])
        for i in range(HISTORY_QUEUE_LENGTH):
            self.snapshot_state()

        self.keys = 0
        self.attack_recharge = 0
        self.move_recharge = MOVEMENT_FULL_CHARGE
        self.pickups = 0
        self.attacks = 0
        self.total_drops = 0
        self.total_steps = 0
        self.last_action_keys = 0
        self.breadcrumbs = np.zeros((side, side))
        if reset_shared_state:
            self._shared_state.reset()
        obs = self.generate_current_observation()
        return obs

    def describe(self, state_item):
        descriptions = {FourKeysBoardItems.EMPTY: '   ', FourKeysBoardItems.WALL: '███', FourKeysBoardItems.KEY: ' K ', 3: ' 1 ', 4: ' 2 ', 5: ' 3 ', 6: ' 4 ', 7: ' 5 ', 8: ' 6 ', 9: ' 7 ', 10: ' 8 ', 11: ' O '}
        return descriptions[state_item]

    def describe_prob(self, probability, max, min):
        if probability == 0:
            return '   '
        if probability >= max:
            return '███'
        if probability > max / 8 * 7:
            return '▓▓▓'
        if probability > max / 8 * 5:
            return '▒▒▒'
        if probability > min:
            return '░░░'

    def describe_raw(self, probability, scale=2):
        return '[%01d]' % probability * scale

    def render(self, label='', clear=True):
        board_square = self._shared_state.get_observable_board(self.position, flat=False)
        side = int(board_square.shape[0])
        history = []
        for i in range(len(self.history_queue)):
            history.append(self.history_queue[i].reshape((side, side)))

        row_index = 0
        divider = ' ┃ '
        output = ''
        for row in board_square:
            history_row_print = ''
            for i in reversed(range(len(history))):
                history_item_row = history[i][row_index]
                history_row_print += '   ' + ('').join([ self.describe(i) for i in history_item_row ])

            breadcrumbs_square = self._last_visible_breadcrumbs.reshape((side, side))
            breadcrumb_row_print = ('').join([ self.describe_prob(i, 20, 0) for i in breadcrumbs_square[row_index] ])
            output += ('').join([ self.describe(i) for i in row ]) + divider + breadcrumb_row_print + '\n'
            row_index += 1

        whole_board_square = self._shared_state.get_whole_square_board()
        side_length = whole_board_square.shape[0]
        min_divider_length = 46
        divider_length = max(min_divider_length, side_length)
        output += '━' * divider_length + '\n'
        for row in whole_board_square:
            output += ('').join([ self.describe(i) for i in row ]) + '\n'

        if clear:
            os.system('cls' if os.name == 'nt' else 'clear')
        print output
        if label:
            print label
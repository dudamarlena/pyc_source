# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skypond/games/four_keys/four_keys_shared_state.py
# Compiled at: 2019-04-30 19:59:45
from __future__ import absolute_import
import numpy as np, math
from ..base.shared_state import SharedState
from gym import error, spaces, utils
from gym.utils import seeding
from gym import wrappers
from .four_keys_board_items import FourKeysBoardItems
from .four_keys_actions import FourKeysActions
from .four_keys_constants import ATTACK_FULL_CHARGE, MOVEMENT_FULL_CHARGE, HISTORY_QUEUE_LENGTH, TOTAL_KEYS
from random import shuffle
import random, operator

class FourKeysSharedState(SharedState):

    def __init__(self, side_length=15, num_seed_walls=6, wall_growth_factor=4, padding=1, seed=None):
        self._side_length = side_length
        self._num_seed_walls = num_seed_walls
        self._wall_growth_factor = wall_growth_factor
        self._padding = padding
        self._attached_envs = {}
        self.any_agent_won = False
        self.agent_centered_observation = True
        self.view_size = 7
        self.reward_shaping_mask_cache = {}
        self.seed(seed)
        self.board, _, _, self.global_base_state, self.keys = self.build_board(side_length - padding * 2, num_seed_walls, wall_growth_factor, padding)
        size = side_length
        half_size = math.floor(size / 2)
        self.starting_points = [(0, 0), (size - 1, size - 1), (0, size - 1), (size - 1, 0), (half_size, 0), (half_size, size - 1), (0, half_size), (size - 1, half_size)]
        max_item = len(FourKeysBoardItems)
        board_blank = [
         max_item] * (self.view_size ** 2 * (2 + HISTORY_QUEUE_LENGTH))
        supplement = [side_length, side_length, 4, 100, 100]
        high = np.array(board_blank + supplement)
        self.observation_space = spaces.Box(high * 0, high, dtype=np.int8)
        self.action_space = spaces.Discrete(len(FourKeysActions))

    def reset_starting_points(self):
        size = self._side_length
        half_size = math.floor(size / 2)
        self.starting_points = [(0, 0), (size - 1, size - 1), (0, size - 1), (size - 1, 0), (half_size, 0), (half_size, size - 1), (0, half_size), (size - 1, half_size)]

    def shuffle_starting_points(self):
        shuffle(self.starting_points)

    def get_status(self):
        running = self.any_agent_won == False
        status = {'running': running, 'players': [], 'keys': []}
        for key in self.keys:
            status['keys'].append([int(key[0]), int(key[1])])

        for i in range(len(self._attached_envs)):
            env = self._attached_envs[i]
            status['players'].append(env.status)

        return status

    def register_attached_environment(self, env):
        self._attached_envs[env.number] = env

    def generate_observation(self, position, history, keys, attack_recharge_percent, movement_recharge_percent, homogenize_player_numbers, breadcrumbs):
        supplement = [
         position[0], position[1], keys, attack_recharge_percent, movement_recharge_percent]
        return_board = self.get_observable_board(position, homogenize_player_numbers=homogenize_player_numbers)
        board_section = return_board
        visible_breadcrumbs = self.get_observable_breadcrumbs(position, breadcrumbs)
        for i in reversed(range(len(history))):
            board_section = np.concatenate((board_section, history[i]), axis=None)

        return (
         np.array(np.concatenate((board_section, visible_breadcrumbs, supplement), axis=None)), return_board, visible_breadcrumbs)

    def get_observable_breadcrumbs(self, position, breadcrumbs, flat=True):
        if self.agent_centered_observation:
            margin = int((self.view_size - 1) / 2)
            full_side = self._side_length + margin * 2
            margined_board = np.full((full_side, full_side), 21)
            margined_board[margin:margin + self._side_length, margin:margin + self._side_length] = breadcrumbs
            y = position[0]
            x = position[1]
            square_output = margined_board[y:y + self.view_size, x:x + self.view_size]
            if flat:
                return self.flatten(square_output)
            return square_output
        else:
            if flat:
                return self.breadcrumbs
            else:
                return self.squarify(self.breadcrumbs)

    def get_whole_square_board(self):
        return self.squarify(self.board)

    def get_observable_board(self, position, flat=True, homogenize_player_numbers=True):
        if self.agent_centered_observation:
            margin = int((self.view_size - 1) / 2)
            full_side = self._side_length + margin * 2
            margined_board = np.full((full_side, full_side), FourKeysBoardItems.WALL)
            board_square = self.squarify(np.copy(self.board))
            if homogenize_player_numbers:
                first_player = FourKeysBoardItems.PLAYER1
                last_player = FourKeysBoardItems.PLAYER8
                for y in range(self._side_length):
                    for x in range(self._side_length):
                        val = board_square[(y, x)]
                        if val >= first_player and val <= last_player:
                            board_square[(y, x)] = FourKeysBoardItems.OTHER_PLAYER

                board_square[(position[0], position[1])] = first_player
            margined_board[margin:margin + self._side_length, margin:margin + self._side_length] = board_square
            y = position[0]
            x = position[1]
            square_output = margined_board[y:y + self.view_size, x:x + self.view_size]
            if flat:
                return self.flatten(square_output)
            return square_output
        else:
            if flat:
                return self.board
            else:
                return self.squarify(self.board)

    def seed(self, seed=None):
        self.rng, self._seed = seeding.np_random(seed)

    def reset(self):
        self.reward_shaping_mask_cache = {}
        self.board, _, _, self.global_base_state, self.keys = self.build_board(self._side_length - self._padding * 2, self._num_seed_walls, self._wall_growth_factor, self._padding)

    def key_consumed_handler(self, location, consuming_env):
        self.keys.remove(location)
        if consuming_env.keys == TOTAL_KEYS:
            self.any_agent_won = True

    def new_key_handler(self, location, source_env):
        self.keys.append(location)

    def attack_handler(self, adjacent_players_locs):
        for adjacent_player_loc in adjacent_players_locs:
            env_index = int(self.board[adjacent_player_loc] - 3)
            env = self._attached_envs[env_index]
            if env.keys > 0:
                env.receive_attack()

    def squarify(self, board):
        side = int(math.sqrt(board.shape[0]))
        return board.reshape((side, side))

    def flatten(self, square_board):
        side = square_board.shape[0]
        return square_board.reshape(side * side)

    def pad(self, square_board, amount):
        side = square_board.shape[0]
        new_side = side + amount * 2
        padded_board = np.zeros((new_side, new_side), dtype=np.int8)
        padded_board[amount:side + amount, amount:side + amount] = square_board
        return padded_board

    def explore_to_mask(self, board, mask, pos):
        if mask[pos] == 1 or board[pos] == FourKeysBoardItems.WALL:
            return
        mask[pos] = 1
        max_item = board.shape[0]
        size = int(math.sqrt(board.shape[0]))
        locs = [
         pos - 1 if pos - 1 >= 0 else None,
         pos + 1 if pos + 1 < max_item else None,
         pos + size if pos + size < max_item else None,
         pos - size if pos - size >= 0 else None, None]
        for loc in [ loc for loc in locs if loc is not None ]:
            self.explore_to_mask(board, mask, loc)

        return

    def build_reachability_mask(self, board, padding):
        board_square = self.squarify(board)
        padded_board = self.pad(board_square, padding)
        padded_length = padded_board.shape[0]
        mask = np.zeros(padded_length ** 2, dtype=np.int8)
        start = 0
        flat_padded_board = self.flatten(padded_board)
        self.explore_to_mask(flat_padded_board, mask, start)
        return mask

    def calculate_board_weight(self, board, pos, size, max_item):
        locs = [
         pos - 1 if pos - 1 >= 0 else None,
         pos + 1 if pos + 1 < max_item else None,
         pos + size if pos + size < max_item else None,
         pos - size if pos - size >= 0 else None, None]
        weight = 0
        for loc in locs:
            if loc is not None:
                weight += 1 if board[loc] != 0 else 0

        return weight

    def calculate_board_weight(self, board, pos, size, max_item):
        locs = [
         pos - 1 if pos - 1 >= 0 else None,
         pos + 1 if pos + 1 < max_item else None,
         pos + size if pos + size < max_item else None,
         pos - size if pos - size >= 0 else None, None]
        weight = 0
        for loc in locs:
            if loc is not None:
                weight += 1 if board[loc] != 0 else 0

        return weight

    def fill_gaps(self, board, reachability_mask):
        for i in range(len(board)):
            if reachability_mask[i] == 0 and board[i] == 0:
                board[i] = FourKeysBoardItems.WALL

    def build_current_distance_to_keys(self, square_board, position):
        closest_key_distance = -1
        closest_key_mask = None
        for key in self.keys:
            mask = self.build_path_mask(square_board, key, position)
            action, distance = self.get_shortest_path_action(square_board, mask, position)
            if distance < closest_key_distance or closest_key_distance == -1:
                closest_key_distance = distance
                closest_key_mask = mask

        if closest_key_distance != -1:
            return closest_key_distance
        else:
            return 999
            return

    def build_key_possibilities(self, board, mask, key_placements, size, max_item):
        placements = []
        probabilities = []
        center_offset = math.floor(size / 2)
        center = size * center_offset + center_offset
        for i in range(max_item):
            if mask[i] == 1 and not self.on_edge(i, size):
                placements.append(i)
                probability = 200 * (size * 2 - self.distance(i, center, size))
                weight = self.calculate_board_weight(board, i, size, max_item)
                probability += 500 * weight
                for existing_key in key_placements:
                    probability += 100 * self.distance(i, existing_key, size)

                probabilities.append(probability)

        prob_factor = 1 / sum(probabilities)
        probabilities = [ prob_factor * p for p in probabilities ]
        probability_mask = np.zeros(max_item)
        for p in range(len(placements)):
            probability_mask[placements[p]] = probabilities[p]

        return (placements, probabilities, probability_mask)

    def get_allowable_movements(self, board, coordinate, only_consider_walls=False):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        actions = [FourKeysActions.UP, FourKeysActions.DOWN, FourKeysActions.LEFT, FourKeysActions.RIGHT]
        allowed_coordinates = []
        action_map = []
        max_offset = board.shape[0] - 1
        candidate_index = 0
        for direction in directions:
            candidate = tuple(map(operator.add, coordinate, direction))
            if candidate[0] < 0 or candidate[0] > max_offset or candidate[1] < 0 or candidate[1] > max_offset:
                candidate_index += 1
                continue
            tile = board[candidate[0]][candidate[1]]
            allowed = False
            if only_consider_walls:
                allowed = not tile == FourKeysBoardItems.WALL
            else:
                allowed = tile == FourKeysBoardItems.EMPTY or tile == FourKeysBoardItems.KEY
            if allowed:
                allowed_coordinates.append(candidate)
                action_map.append(actions[candidate_index])
            candidate_index += 1

        return (allowed_coordinates, action_map)

    def explore_path_cache_bfs(self, board, mask, point):
        queue = []
        queue.append(point)
        while queue:
            point = queue.pop(0)
            reachable_points, _ = self.get_allowable_movements(board, point, only_consider_walls=True)
            distance = mask[(point[0], point[1])] + 1
            for new_point in reachable_points:
                mask_value = mask[(new_point[0], new_point[1])]
                if mask_value == 999:
                    mask[(new_point[0], new_point[1])] = distance
                    queue.append(new_point)

        return mask

    def build_path_mask(self, board, destination, current_location):
        cache_key = str(destination[0]) + '_' + str(destination[1])
        if cache_key in self.reward_shaping_mask_cache.keys():
            mask = self.reward_shaping_mask_cache[cache_key]
            return mask
        side_size = board.shape[0]
        mask = np.full((side_size, side_size), 999)
        mask[(destination[0], destination[1])] = 0
        mask = self.explore_path_cache_bfs(board, mask, destination)
        self.reward_shaping_mask_cache[cache_key] = mask
        return mask

    def get_shortest_path_action(self, board, mask, coordinate):
        reachable_points, actions = self.get_allowable_movements(board, coordinate)
        shortest_path = 99999
        shortest_action = None
        for i in range(len(reachable_points)):
            point = reachable_points[i]
            mask_value = mask[(point[0], point[1])]
            if mask_value < shortest_path:
                shortest_action = actions[i]
                shortest_path = mask_value

        return (
         shortest_action, shortest_path)

    def distance(self, a, b, size):
        coordinates_a = np.array([math.floor(a / size), a % size])
        coordinates_b = np.array([math.floor(b / size), b % size])
        return np.linalg.norm(coordinates_a - coordinates_b)

    def on_edge(self, position, size):
        if position % size == size - 1 or position % size == 0:
            return True
        if position <= size or position > size ** 2 - size:
            return True
        return False

    def build_board(self, size=28, num_seed_walls=20, wall_growth_factor=8, padding=1):
        max_item = size ** 2
        padded_size = size + padding * 2
        padded_max_item = padded_size ** 2
        board = np.zeros(max_item, dtype=np.int8)
        walls = self.rng.choice(max_item - 1, num_seed_walls)
        board[walls] = FourKeysBoardItems.WALL
        for i in range(wall_growth_factor):
            for pos in range(max_item):
                if board[pos] == FourKeysBoardItems.WALL:
                    locs = [pos - 1 if pos - 1 >= 0 else None,
                     pos + 1 if pos + 1 < max_item else None,
                     pos + size if pos + size < max_item else None,
                     pos - size if pos - size >= 0 else None, None]
                    next_item = self.rng.randint(0, 4)
                    if locs[next_item] is not None:
                        next_item_pos = locs[next_item]
                        weight = self.calculate_board_weight(board, next_item_pos, size, max_item)
                        weight_ideal = weight < 3
                        if not weight_ideal:
                            skip_range = self.rng.randint(0, 9 - weight)
                            if skip_range != 0:
                                continue
                        board[next_item_pos] = FourKeysBoardItems.WALL

        reachability_mask = self.build_reachability_mask(board, padding)
        padded_board = self.flatten(self.pad(self.squarify(board), padding))
        self.fill_gaps(padded_board, reachability_mask)
        global_base_state = padded_board.copy()
        unique_reachable_keys = 0
        keys = []
        key_coordinates = []
        key_probability_mask = []
        max_attempts = 1000
        attempts = 0
        while unique_reachable_keys < TOTAL_KEYS and attempts < max_attempts:
            possibilities, key_probabilities, key_probability_mask = self.build_key_possibilities(padded_board, reachability_mask, keys, padded_size, padded_max_item)
            next_key = np.squeeze(self.rng.choice(possibilities, p=key_probabilities))
            if next_key not in keys:
                keys.append(next_key)
                key_coordinates.append((math.floor(next_key / padded_size), next_key % padded_size))
                unique_reachable_keys += 1
            attempts += 1

        padded_board[keys] = FourKeysBoardItems.KEY
        return (
         padded_board, reachability_mask, key_probability_mask, global_base_state, key_coordinates)
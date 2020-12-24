# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/christian/documented/ctf/ctf/board.py
# Compiled at: 2020-04-17 20:38:02
# Size of source mod 2**32: 10033 bytes
import numpy as np
from ctf.pieces import Unit, Flag

class Board(object):

    def __init__(self, dimensions=(16, 9), num_units=3, max_score=1, jail_timer=5):
        self._dimensions = dimensions
        self._num_units = num_units
        self._max_score = max_score
        self._jail_timer = jail_timer
        self._jail = {}
        self._renderer = None

    @property
    def board(self):
        return np.copy(self._board)

    @property
    def key(self):
        key = {k:vars(v) for k, v in self._key.items() if v != 'EMPTY' if v != 'EMPTY'}
        key[0] = 'EMPTY'
        return key

    @property
    def log(self):
        return list(self._game_log)

    @property
    def moved_units(self):
        return dict(self._moved_units)

    @property
    def need_to_move(self):
        return [unit for unit, moved in self._moved_units.items() if not moved]

    @property
    def observation(self):
        data = {'board':self._board, 
         'key':self.key, 
         'log':self.log, 
         'moved_units':self.moved_units, 
         'turn':self._turn, 
         'winner':self.winner}
        return data

    @property
    def turn(self):
        return self._turn

    @property
    def winner(self):
        if max(self._score.values()) >= self._max_score:
            return max((self._score), key=(self._score.get))
        else:
            return False

    def _apply_movement(self, unit, direction):
        instance = self._key[unit]
        self._board[instance.position] = 0
        y, x = instance.position
        if direction == 'N':
            y -= 1
        else:
            if direction == 'E':
                x += 1
            else:
                if direction == 'S':
                    y += 1
                else:
                    if direction == 'W':
                        x -= 1
        other = self._key[self._board[(y, x)]]
        if other == 'EMPTY':
            self._move(instance, x, y)
        else:
            if isinstance(other, Unit):
                if other.has_flag:
                    self._capture(instance, other)
                    self._move(instance, x, y)
                else:
                    if (instance.team == 1) & (y < self._board.shape[0] // 2):
                        self._capture(instance, other)
                        self._move(instance, x, y)
                    else:
                        if (instance.team == 1) & (y >= self._board.shape[0] // 2):
                            self._capture(other, instance)
                        else:
                            if (instance.team == 2) & (y >= self._board.shape[0] // 2):
                                self._capture(instance, other)
                                self._move(instance, x, y)
                            elif (instance.team == 2) & (y < self._board.shape[0] // 2):
                                self._capture(other, instance)
            unit_pos = np.array(instance.position)
            if instance.team == 1:
                home_flag = self._key[1]
                away_flag = self._key[2]
            elif instance.team == 2:
                home_flag = self._key[2]
                away_flag = self._key[1]
        away_flag_pos = np.array(away_flag.position)
        home_flag_pos = np.array(home_flag.position)
        if (np.linalg.norm(unit_pos - away_flag_pos) == 1) & away_flag.grounded:
            instance.has_flag = True
            away_flag.grounded = False
            self._board[away_flag.position] = 0
            away_flag.position = instance.position
        if (np.linalg.norm(unit_pos - home_flag_pos) == 1) & home_flag.grounded & instance.has_flag:
            instance.has_flag = False
            self._place_flag(away_flag.team)
            self._score[instance.team] += 1

    def _capture(self, capturer, capturee):
        self._send_to_jail(capturee.idx)
        if capturee.has_flag:
            capturee.has_flag = False
            self._place_flag(capturer.team)

    def _legal_moves(self, unit):
        instance = self._key[unit]
        if instance.in_jail:
            return ['PASS']
        else:
            legal_moves = [
             'N', 'E', 'S', 'W']
            y, x = instance.position
            if y - 1 < 0:
                legal_moves.remove('N')
            if x + 1 >= self._board.shape[1]:
                legal_moves.remove('E')
            if y + 1 >= self._board.shape[0]:
                legal_moves.remove('S')
            if x - 1 < 0:
                legal_moves.remove('W')
            movement_dict = {}
            for move in legal_moves:
                if move == 'N':
                    movement_dict[move] = (
                     y - 1, x)
                else:
                    if move == 'E':
                        movement_dict[move] = (
                         y, x + 1)
                    else:
                        if move == 'S':
                            movement_dict[move] = (
                             y + 1, x)
                        else:
                            if move == 'W':
                                movement_dict[move] = (
                                 y, x - 1)

            for direction, pos in movement_dict.items():
                if self._board[pos] != 0:
                    if self._board[pos] in (1, 2):
                        try:
                            legal_moves.remove(direction)
                        except ValueError:
                            pass

                    elif isinstance(self._key[self._board[pos]], Unit):
                        other = self._key[self._board[pos]]
                        if other.team == instance.team:
                            try:
                                legal_moves.remove(direction)
                            except ValueError:
                                pass

            if len(legal_moves) > 0:
                return legal_moves
            return ['PASS']

    def _move(self, instance, x, y):
        instance.position = (y, x)
        self._board[instance.position] = instance.idx
        if instance.has_flag:
            if instance.team == 1:
                flag = self._key[2]
            else:
                if instance.team == 2:
                    flag = self._key[1]
            flag.position = instance.position

    def _place_flag(self, team):
        y, x = self._dimensions
        middle = x // 2
        if team == 1:
            self._board[(1, middle)] = team
            self._key[team].position = (1, middle)
        elif team == 2:
            self._board[(y - 2, middle)] = team
            self._key[team].position = (y - 2, middle)
        self._key[team].grounded = True

    def _send_to_jail(self, unit):
        instance = self._key[unit]
        if instance.team == 1:
            y = 0
            for x in range(self._board.shape[1]):
                if self._board[(y, x)] == 0:
                    break

        else:
            y = self._board.shape[0] - 1
            for x in reversed(range(self._board.shape[1])):
                if self._board[(y, x)] == 0:
                    break

        self._board[instance.position] = 0
        self._board[(y, x)] = unit
        instance.position = (y, x)
        instance.in_jail = True
        self._jail[unit] = self._jail_timer

    def legal_moves(self):
        moves = {}
        for k, v in self._key.items():
            if isinstance(v, Unit):
                moves[k] = self._legal_moves(k)

        return moves

    def move(self, unit, direction):
        assert direction in self.legal_moves()[unit]
        self._apply_movement(unit, direction)
        self._game_log.append({'unit':unit,  'direction':direction})
        self._moved_units[unit] = True
        if all(self._moved_units.values()):
            if self._turn == 1:
                self._turn = 2
            else:
                if self._turn == 2:
                    self._turn = 1
            self._moved_units = {}
            for k, v in self._key.items():
                if isinstance(v, Unit) and v.team == self._turn:
                    self._moved_units[k] = False

            freedom = []
            for unit in self._jail:
                self._jail[unit] -= 1
                if self._jail[unit] == 0:
                    freedom.append(unit)

            for f in freedom:
                del self._jail[f]
                self._key[f].in_jail = False

    def new_game(self):
        self._game_log = []
        self._key = {0:'EMPTY',  1:Flag(team=1, position=None), 
         2:Flag(team=2, position=None)}
        self._score = {1:0, 
         2:0}
        y, x = self._dimensions
        self._board = np.zeros(self._dimensions)
        for team in range(1, 3):
            self._place_flag(team)
            for unit in range(self._num_units):
                available = False
                while not available:
                    if team == 1:
                        pos = (np.random.randint(0, y / 2),
                         np.random.randint(0, x))
                    else:
                        if team == 2:
                            pos = (np.random.randint(y / 2, y),
                             np.random.randint(0, x))
                    if self._board[pos] == 0:
                        available = True

                idx = max(self._key) + 1
                self._key[idx] = Unit(idx=idx, team=team, position=pos)
                self._board[pos] = idx

        self._turn = np.random.randint(1, 3)
        self._moved_units = {}
        for k, v in self._key.items():
            if isinstance(v, Unit) and v.team == self._turn:
                self._moved_units[k] = False

    def render(self):
        if self._renderer is None:
            from ctf.rendering import Renderer
            self._renderer = Renderer(width=800,
              height=600,
              x_pad=60.0,
              y_pad=20.0,
              box=(560.0 / self._dimensions[0]),
              unit_pad=(560.0 / self._dimensions[0] // 5))
        self._renderer.init_window()
        self._renderer.draw_scoreboard(dims=(self._dimensions),
          score=(self._score),
          logs=(self._game_log[-12:]),
          key=(self._key))
        self._renderer.draw_grid(self._dimensions)
        self._renderer.draw_pieces(self._dimensions, self._key)
        self._renderer.show()
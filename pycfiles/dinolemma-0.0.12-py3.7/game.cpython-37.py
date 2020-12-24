# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dinolemma/game.py
# Compiled at: 2020-01-24 17:24:10
# Size of source mod 2**32: 12661 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from itertools import chain
from dinolemma.dinosaurs import Dinosaurs
from dinolemma.avocados import AvocadoTrees
import random, numpy, sys, time

class DinosaurDilemma:
    __doc__ = 'A dinosaur dilemma simulation contains basic variables to control\n       the environment (season, climate) along with probabilities\n       for events. Largely, if values are undefined, they are randomly\n       selected from within some range.\n    '

    def __init__(self, days_left_season=None, season=None, days_in_season=90, number_dinos=None, number_trees=None, max_temperature=86, min_temperature=0, grid_size=25, verbose=False):
        self.days_in_season = days_in_season
        self.season = random.choice(['summer', 'spring', 'winter', 'fall']) or season
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        self.days_left_season = random.choice(range(self.days_in_season)) or days_left_season
        self.grid_size = grid_size
        self.verbose = verbose
        self.dinosaurs = Dinosaurs(number_dinos)
        self.trees = AvocadoTrees(number_trees)
        self._init_grid()
        self.newday()

    def interact(self, entity):
        """Given an entity, find other entities around it (and have them interact).
           This is run during a simulation directly after an entity moves.
        """
        neighbors = self.get_neighbors(entity.x, entity.y)
        for neighbor in neighbors:
            outcomes = entity.interact(neighbor)
            if 'reproduce' in outcomes:
                self.reproduce(entity)
            if 'death' in outcomes:
                self.remove(outcomes['death'])

    def remove(self, entity):
        """If an entity dies (or is otherwise killed) remove from the grid
           and list of entities.
        """
        name = entity.name
        if hasattr(entity, 'x'):
            self.grid[(entity.x, entity.y)] = None
        elif name.endswith('tree'):
            del self.trees[name]
        else:
            del self.dinosaurs[name]

    def get_neighbors(self, x, y):
        """Given an x and y coordinate, find all adjacent entities
        """
        neighbors = []
        for coord in self.get_adjacent_coords(x, y):
            cx, cy = coord
            if self.grid[(cx, cy)]:
                name = self.grid[(cx, cy)]
                if name.endswith('tree'):
                    neighbors.append(self.trees[name])
                else:
                    neighbors.append(self.dinosaurs[name])

        return neighbors

    def reproduce(self, parent):
        """Given that an entity reproduces (via interaction) or on its own,
           this function generates the new entity (depending on the parent
           type) and places it on the grid.
        """
        if parent.name.endswith('tree'):
            offspring = self.trees.new()
        else:
            offspring = self.dinosaurs.new()
        coords = self.get_open_coords(parent.x, parent.y)
        if coords:
            x, y = random.choice(coords)
            self._move(offspring, x, y)
            print('Joy! Welcome %s to the world at (%s,%s)' % (offspring, x, y))
        else:
            print('%s is too cramped to reproduce!' % parent)
            self.remove(offspring)

    def change(self, entity):
        """After moving, an entity can change depending on it's environment.
           Each entity should have a change function that accepts any or all
           current environment variables.
        """
        (entity.change)(**self.get_environment())

    def summary(self, return_summary=False):
        """Print a summary of the season, day, and general weather for the 
           simulation. If return summary is True, instead return as text
           for rendering elsewhere.
        """
        if return_summary:
            return 'There are %s days left in the %s season. \nThere are %s dinosaurs, and %s avocado trees. \nThe temperate is %s°F, humidity %0.2f' % (
             self.days_left_season,
             self.season,
             self.dinosaurs.count,
             self.trees.count,
             self.temperature,
             self.humidity)
        print('There are %s days left in the %s season.' % (
         self.days_left_season, self.season))
        print('There are %s dinosaurs, and %s avocado trees.' % (
         self.dinosaurs.count, self.trees.count))
        print('The temperate is %s°F, humidity %s' % (self.temperature, self.humidity))

    def _init_grid(self):
        """Initialize the grid, meaning creating it, ensuring it's large 
           enough, and placing dinosaurs and avocado trees on it
        """
        self.grid = numpy.empty(shape=(self.grid_size, self.grid_size), dtype=object)
        choices = [x[0] for x in list(numpy.ndenumerate(self.grid))]
        random.shuffle(choices)
        if self.dinosaurs.count + self.trees.count + 10 > len(choices):
            sys.exit('You must increase grid size or decrease entities.')
        for entity in chain(self.dinosaurs, self.trees):
            x, y = choices.pop()
            self._move(entity, x, y)

    def _move(self, entity, x, y):
        """Handle assigning an entity to a new spot, along with assigning the
           entity name to the spot. This function expects an x and y coordinate.
           to move to an open spot, use move() instead.
        """
        if entity.on_grid:
            self.grid[(entity.x, entity.y)] = None
            if self.verbose:
                print('Moving dinosaur %s from (%s,%s) to (%s,%s)' % (
                 entity.name, entity.x, entity.y, x, y))
        entity.set_location(x, y)
        self.grid[(x, y)] = entity.name

    def move(self, entity):
        """Given an entity, move it in the grid. This means that if there
           are surrounding (other) entities after the move, we interact with
           them (even if the second entity has not moved yet!) This makes
           the simulation more interesting, as a single entity can have 
           multiple interactions per turn.
        """
        if entity.can_move:
            coords = self.get_open_coords(entity.x, entity.y)
            if coords:
                x, y = random.choice(coords)
                self._move(entity, x, y)

    def get_open_coords(self, x, y):
        """Given an x and y coordinate, return surrounding empty coordinates.
        """
        coords = []
        for coord in self.get_adjacent_coords(x, y):
            cx, cy = coord
            if not self.grid[(cx, cy)]:
                coords.append((cx, cy))

        return coords

    def get_adjacent_coords(self, x, y):
        """Given an x and y coordinate, return surrounding coordinates.
        """
        coords = []
        width, height = self.grid.shape
        if x - 1 >= 0:
            coords.append((x - 1, y))
        if x + 1 < width:
            coords.append((x + 1, y))
        if y - 1 >= 0:
            coords.append((x, y - 1))
        if y + 1 < height:
            coords.append((x, y + 1))
        return coords

    def get_environment(self):
        """A general function that returns a lookup of the environment
        """
        environ = {'humidity':self.humidity, 
         'temperature':self.temperature, 
         'season':self.season, 
         'days_in_season':self.days_in_season, 
         'days_left_season':self.days_left_season, 
         'number_dinos':self.dinosaurs.count, 
         'number_trees':self.trees.count}
        return environ

    def set_climate(self):
        """Set the climate, meaning the temperature (depending on the season)
           and the humidity (also largely depending on the season
        """
        chance_humid = 0.5
        if self.season == 'winter':
            self.temperature = random.choice(range(self.min_temperature, 32))
            chance_humid = 0.1
        else:
            if self.season == 'fall':
                self.temperature = random.choice(range(30, 62))
                chance_humid = 0.6
            else:
                if self.season == 'spring':
                    self.temperature = random.choice(range(40, 55))
                    chance_humid = 0.4
                else:
                    if self.season == 'summer':
                        self.temperature = random.choice(range(56, self.max_temperature))
                        chance_humid = 0.75
        self.set_humidity(chance_humid)

    def set_humidity(self, chance_humid):
        """Determine the humidity, a percentage value.
        """
        low_humidity = random.choice(range(30, 50)) * 0.01
        high_humidity = random.choice(range(50, 80)) * 0.01
        self.humidity = numpy.random.choice([
         low_humidity, high_humidity],
          p=[1 - chance_humid, chance_humid])

    def next_season(self):
        """return the next season"""
        return {'summer':'fall', 
         'fall':'winter', 
         'winter':'spring', 
         'spring':'summer'}[self.season]

    def newday(self):
        """For each new day, these is a different value for water and sunlight,
           depending on the season.
        """
        if self.days_left_season == 0:
            self.season = self.next_season()
            self.days_left_season = self.days_in_season
        self.days_left_season -= 1
        self.set_climate()
        self.summary()

    def run(self, days=100, verbose=False, delay=1):
        """After the grid is initialized and we've set the initial client, 
           run the simulation for a certain number of days. Also add a delay
           (seconds) to sleep between days
        """
        self.verbose = verbose
        for day in range(days):
            print('\nDAY %s' % day)
            self.run_day()
            time.sleep(delay)

    def run_day(self):
        """manually run a day (an alternative to "run"). This function
           also returns a data structure that can be used to update some
           graphical rendering of the result.
        """
        self.newday()
        for entity in chain(self.dinosaurs, self.trees):
            if entity.is_dead:
                print('DEAD: %s' % entity)
                self.remove(entity)
                continue
            self.move(entity)
            self.change(entity)
            if entity.reproduce():
                self.reproduce(entity)
            self.interact(entity)
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dinolemma/entity.py
# Compiled at: 2020-01-24 17:33:15
# Size of source mod 2**32: 4590 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from dinolemma.namer import GenericNamer
import random

class Entity:
    __doc__ = 'An Entity is a base class for a living thing in the world. An entity\n       that can move is allowed to change location on the grid.\n    '

    def __init__(self, name, can_move=True):
        self.name = name
        self.can_move = can_move
        self._interactions = {}

    def __str__(self):
        return '[%s: %s]' % (self.type, self.name)

    def set_location(self, x, y):
        """set an entity location on the board - an x and y coordinate
        """
        self.x = x
        self.y = y

    def interact(self, entity):
        """Given a second entity, based on its type, interact with it.
        """
        outcomes = {}
        if not entity:
            return outcomes
        if entity.type in self._interactions:
            outcomes = self._interactions[entity.type](self, entity)
        return outcomes

    def reproduce(self, **kwargs):
        """By default, an entity will not reproduce (this function returns false)
           however the subclass should instantiate the function to have a custom
           reproductive behavior
        """
        return False

    def change(self, **kwargs):
        """The change function should accept any number of variables from
           the environment, and the entity is free to use them as needed.
           If no change function is subclassed, the entity does not change
        """
        pass

    @property
    def is_dead(self):
        """By default, this function always returns True (entities do not die).
           It's up to the subclass to decide under what conditions an entity
           can die.
        """
        return False

    @property
    def on_grid(self):
        """An entity with an x and y coordinate is assumed to be on the grid
        """
        if hasattr(self, 'x'):
            if hasattr(self, 'y'):
                return True
        return False

    @property
    def type(self):
        """Return the type of an entity"""
        return self.__class__.__name__


class Group:
    __doc__ = 'A group is a generic base class to hold a group of entities.\n       An implementing subclass should add a name (e.g., dinosaurs) along\n       with a class of entity to implement (e.g., Dinosaur). Custom functions \n       for interaction based on the names of other groups.\n    '

    def __init__(self, name, Entity, number=None, namer=None):
        number = number or random.choice(range(15))
        self.entities = {}
        namer = namer or GenericNamer
        self.namer = namer()
        self.name = name
        self.Entity = Entity
        names = []
        for _ in range(number):
            name = self.namer.generate()
            while name in names:
                name = self.namer.generate()

            names.append(name)
            self.entities[name] = Entity(name)

    def new(self, **kwargs):
        """Create a new entity"""
        name = self.namer.generate()
        entity = (self.Entity)(name, **kwargs)
        self.entities[name] = entity
        return entity

    @property
    def count(self):
        return len(self.entities)

    def random(self):
        """Randomly select an entity"""
        if len(self.entities) > 0:
            return random.choice(list(self.entities.values()))

    def __str__(self):
        return '[%s %s]' % (self.count, self.name)

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, key):
        if key in self.entities:
            return self.entities[key]

    def __delitem__(self, key):
        del self.entities[key]

    def __iter__(self, randomize=True):
        """iterator over entities. By default, we randomize the order
        """
        entities = list(self.entities.keys())
        if randomize:
            random.shuffle(entities)
        for name in entities:
            if name in self.entities:
                yield self.entities[name]
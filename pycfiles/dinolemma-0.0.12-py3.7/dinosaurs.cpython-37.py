# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dinolemma/dinosaurs.py
# Compiled at: 2020-01-14 14:31:25
# Size of source mod 2**32: 5495 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from dinolemma.interactions import dinosaurXdinosaur, dinosaurXavocado
from dinolemma.entity import Group, Entity
from dinolemma.namer import GenericNamer
import random, numpy

class Dinosaur(Entity):

    def __init__(self, name, can_move=True):
        super().__init__(name=name, can_move=can_move)
        self.size = random.choice(range(100)) * 0.01
        self.hunger = random.choice(range(80, 100)) * 0.01
        self.dead = False
        self.gender = numpy.random.choice([
         'male', 'female', 'hybrid'],
          p=[0.48, 0.48, 0.04])
        self.freezing_point = random.choice(range(-20, 5))
        self.boiling_point = random.choice(range(85, 500))
        self.probability_fight = random.choice(range(0, 100)) * 0.01
        self.probability_reproduce = random.choice(range(0, 100)) * 0.01
        self._interactions['AvocadoTree'] = dinosaurXavocado
        self._interactions['Dinosaur'] = dinosaurXdinosaur

    def stats(self):
        """Return stats for a dinosaur, primarily the size and hunger
         """
        stats = {'hunger':self.hunger, 
         'size':self.size}
        return stats

    @property
    def is_aggressive(self):
        """Regardless of size, a starving dinosaur is aggressive
        """
        return self.hunger > 0.9

    def reproduce(self, **kwargs):
        """If a dinosaur is a hybrid, it can reproduce on it's own. Otherwise,
           it requires another dinosaur.
        """
        if hasattr(kwargs, 'entity'):
            entity = kwargs.get('entity')
            prob_reproduce = (self.probability_reproduce + entity.probability_reproduce) / 2
            return numpy.random.choice([
             self.gender != 'hybrid' and self.gender != entity.gender, False],
              p=[
             prob_reproduce, 1 - prob_reproduce])
        if self.gender == 'hybrid':
            return numpy.random.choice([
             True, False],
              p=[
             self.probability_reproduce, 1 - self.probability_reproduce])
        return False

    @property
    def strength(self):
        """Strength is inverse of hunger. A starving dinosaur (hunger 0.9+)
           is going to be very weak (<0.10 strength). A well fed dinosaur
           (hunger close to 0) will have a strength closer to 1.
        """
        return 1 - self.hunger

    @property
    def is_mature(self):
        """determine if a dinosaur is mature, when the size is greater than or 
           == 80% of full grown, whatever unit that happens to be. A mature
           dinosaur eats more, but can also mate.
        """
        return self.size >= 0.8

    @property
    def is_dead(self):
        """A dinosaur dies if it's hunger goes above 1 (or has dead property)
        """
        return self.hunger >= 1 or self.dead

    def change(self, **kwargs):
        """The change function should accept any number of variables from
           the environment, and the entity is free to use them as needed.
           If no change function is subclassed, the entity does not change
        """
        temperature = kwargs.get('temperature', 55)
        humidity = kwargs.get('humidity', 0.5)
        self.hunger = max(0, self.hunger + numpy.power(self.size, 10))
        if temperature <= self.freezing_point:
            self.dead = random.choice([True, False])
        else:
            if temperature >= self.boiling_point:
                self.dead = random.choice([True, False])
            else:
                self.size = self.is_dead or min(0, self.size + 1 / max(1, numpy.power(temperature, 2)))


class DinosaurNamer(GenericNamer):
    __doc__ = 'The DinosaurNamer subclasses a GenericNamer, but adds a dinosaur extension\n       to complete the name.\n    '

    def __init__(self):
        self.suffix = [
         'asaurus',
         'isaurus',
         'iraptor',
         'raptor',
         'us',
         'docus',
         'podus']
        super().__init__()

    def __str__(self):
        return '[dinosaur-namer]'

    def __repr__(self):
        return self.__str__()

    def generate(self, delim='-'):
        prefix = self._generate(delim)
        suffix = self.select(self.suffix)
        return '%s%s' % (prefix, suffix)


class Dinosaurs(Group):
    __doc__ = 'A group of dinosaurs\n    '

    def __init__(self, number=None):
        super().__init__(name='dinosaurs',
          number=number,
          Entity=Dinosaur,
          namer=DinosaurNamer)
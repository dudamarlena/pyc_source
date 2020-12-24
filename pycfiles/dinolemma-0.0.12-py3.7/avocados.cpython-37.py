# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dinolemma/avocados.py
# Compiled at: 2020-01-14 14:00:16
# Size of source mod 2**32: 4331 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from dinolemma.entity import Group, Entity
from dinolemma.namer import GenericNamer
import random, numpy

class AvocadoTree(Entity):

    def __init__(self, name, can_move=False):
        super().__init__(name=name, can_move=can_move)
        self.height = random.choice(range(100)) * 0.01
        self.dead = False
        self.happy = True
        self.is_diseased = False
        self.avocados = 0
        if self.height > 0.8:
            self.avocados = random.choice(range(0, 5))
        self.freezing_point = random.choice(range(-100, 32))
        self.probability_disease = random.choice(range(0, 5)) * 0.01
        self.probability_reproduce = random.choice(range(0, 5)) * 0.01

    def stats(self):
        """Return stats for an avocado tree
         """
        stats = {'avocados':self.avocados, 
         'height':self.height,  'happy':self.happy}
        return stats

    @property
    def is_dead(self):
        """A dead avocado tree has size 0 or less, meaning it could have been
           stepped on, or destroyed/ eaten by a dinosaur
        """
        return self.height <= 0 or self.dead

    @property
    def is_mature(self):
        """A mature tree can reproduce
        """
        return self.height > 0.8

    def change(self, **kwargs):
        """If the avocado tree is less than it's full size, allow it to grow.
           The growth is an equation of the current sunlight and water 
           conditions.
        """
        temperature = kwargs.get('temperature', 55)
        humidity = kwargs.get('humidity', 0.5)
        self.happy = False
        if temperature > 40:
            if temperature < 65:
                if not self.is_diseased:
                    self.height = max(1, self.height + numpy.power(humidity, 10))
                    self.happy = True
        if temperature <= self.freezing_point:
            p = [0.5, 0.5] if self.is_diseased else [0.6, 0.4]
            self.dead = numpy.random.choice([True, False], p=p)
        self.is_diseased = numpy.random.choice([
         True, self.is_diseased],
          p=[
         self.probability_disease, 1 - self.probability_disease])
        if not self.is_dead:
            if not self.is_diseased:
                self.grow_avocado()

    def grow_avocado(self):
        """A healthy avocado tree can generate a new avocado!
        """
        if self.is_mature:
            self.avocados += numpy.random.choice([
             0, random.choice(range(0, 5))],
              p=[0.2, 0.8])

    def reproduce(self, **kwargs):
        """An avocado tree has a small percentage of reproducing if it's over
           a particular height (mature) and the weather is good.
        """
        if self.is_mature:
            if self.happy:
                return numpy.random.choice([
                 True, False],
                  p=[
                 self.probability_reproduce, 1 - self.probability_reproduce])
        return False


class AvocadoNamer(GenericNamer):
    __doc__ = 'The AvocadoNamer subclasses a GenericNamer, but adds a tree extension\n    '

    def __str__(self):
        return '[avocado-namer]'

    def __repr__(self):
        return self.__str__()

    def generate(self, delim='-'):
        prefix = self._generate(delim)
        return '%s%stree' % (prefix, delim)


class AvocadoTrees(Group):
    __doc__ = 'A group of avocado trees\n    '

    def __init__(self, number=None):
        super().__init__(name='trees',
          number=number,
          Entity=AvocadoTree,
          namer=AvocadoNamer)
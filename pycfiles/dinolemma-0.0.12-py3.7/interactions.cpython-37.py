# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dinolemma/interactions.py
# Compiled at: 2020-01-24 16:06:56
# Size of source mod 2**32: 2685 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
import numpy, random

def dinosaurXdinosaur(dino1, dino2):
    """A dinosaur by dinosaur interaction. The first (dino1) is the entity
       that has come upon the second (dino2) in the game. More than one
       interaction are possible (e.g., mate then death, fight then mate, etc.).
    """
    outcomes = {}
    print('INTERACT: %s and %s' % (dino1, dino2))
    if dino1.gender != 'hybrid':
        if dino2.gender != 'hybrid':
            if dino1.gender != dino2.gender:
                if dino1.reproduce(entity=dino2):
                    print('REPRODUCE: %s and %s!' % (dino1, dino2))
                    outcomes['reproduce'] = True
    elif dino1.is_aggressive:
        if dino2.is_aggressive:
            p_fight = (dino1.hunger + dino2.hunger) / 2
            if p_fight > 1.0:
                p_fight = 1.0
            they_fight = numpy.random.choice([True, False], p=[p_fight, 1 - p_fight])
            if they_fight:
                print('FIGHT: %s and %s!' % (dino1, dino2))
                if abs(dino1.strength - dino2.strength) > 0.4:
                    outcomes['death'] = dino1 if dino1.strength > dino2.strength else dino2
    return outcomes


def dinosaurXavocado(dino, tree):
    """A dinosaur by avocado interaction, meaning that the dinosaur was moving
       and finds an avocado tree.
    """
    outcomes = {}
    print('INTERACT: %s and %s' % (dino, tree))
    if tree.is_mature:
        if tree.avocados > 0:
            eaten = random.choice(range(tree.avocados))
            if eaten > 0 and tree.is_diseased:
                dino.hunger = dino.hunger - 0.1 * eaten
                print('EATING %s %s avocados from a diseased tree!' % (dino, eaten))
            else:
                dino.hunger = dino.hunger + 0.1 * eaten
                print('EATING %s %s avocados!' % (dino, eaten))
            tree.avocados -= eaten
    if tree.height <= 0.1:
        if random.choice([True, False]):
            print('TRAMPLED: %s by %s' % (tree, dino))
            outcomes['death'] = tree
    return outcomes
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fungus_swarm.py
# Compiled at: 2009-02-26 08:25:43
"""A fungus blob swarm.

Ideas: 
- Use a lightweight sprite instead of the normal core sprite to avoid unecessary overhead. 

"""
from fungus_core import Sprite
from fungus_scene import BaseScene
from os.path import join, dirname
from random import random, choice, randint
from time import sleep
NUMBER_OF_BLOBS = 100
SEARCH_DISTANCE = 20
MAX_SEARCH_DISTANCE = 4294967296
MAX_FLIGHT_STEP = 2.0
STEPS_TO_FLEE = 20
NEVER_SELECT_LAST_AS_NEXT = False
SEX_DISTRIBUTION = [
 'male', 'male', 'female', 'female', None]
RANDOM_MOVEMENT = 0.5
BIASED_RANDOM_MOVEMENT = 4.0
SPEED_TOWARDS_PARTNER_INVERSE = 10
STARTING_POSITIONS = 'random'
COMPATIBLE_SEXES = {None: [
        'male', 'female', None], 
   'male': [
          'female', None], 
   'female': [
            'male', None]}
UNBONDED = {}
for sex in SEX_DISTRIBUTION:
    if sex not in UNBONDED:
        UNBONDED[sex] = []

IMAGE_BASE_PATH = join(dirname(__file__), 'graphics')

class Blob(Sprite):
    """One of the moving blobs.
        
        Ideas: 
                - sex = None => hostile; no sexual interest
                - sex = undecided => what None currently does
                """
    _unbonded = UNBONDED

    def __init__(self, sex=None, *args, **kwds):
        if sex is None:
            super(Blob, self).__init__(image_path=join(IMAGE_BASE_PATH, 'blobn.png'), *args, **kwds)
        elif sex == 'female':
            super(Blob, self).__init__(image_path=join(IMAGE_BASE_PATH, 'blobf.png'), *args, **kwds)
        else:
            super(Blob, self).__init__(image_path=join(IMAGE_BASE_PATH, 'blob.png'), *args, **kwds)
        self.partner = None
        self.last_partner = None
        self.sex = sex
        self.steps_to_flee = 0
        self.max_flight_step = MAX_FLIGHT_STEP
        self.search_distance = SEARCH_DISTANCE
        self.safe_distance = (self.width ** 2 + self.height ** 2) / 2.0
        self.x_bias = (random() - 0.5) * BIASED_RANDOM_MOVEMENT
        self.y_bias = (random() - 0.5) * BIASED_RANDOM_MOVEMENT
        self.compatible_sexes = COMPATIBLE_SEXES[self.sex]
        self.dx = 0
        self.dy = 0
        self._unbonded[self.sex].append(self)
        return

    def distance_to(self, other):
        """Squared distance to the partner. Calculated from the centers."""
        x = other.x + 0.5 * other.width - (self.x + 0.5 * self.width)
        y = other.y + 0.5 * other.height - (self.y + 0.5 * self.height)
        return x ** 2 + y ** 2

    def is_valid_partner_for(self, other):
        """Check, if we are a valid partner for the other blob.
                
                We don't check the sex, since the blob only looks among blobs with fitting sex."""
        if other is self:
            return False
        if NEVER_SELECT_LAST_AS_NEXT and self.last_partner is other:
            return False
        if self.distance_to(other) > self.search_distance:
            return False
        return True

    def flee(self):
        """Jump one random step away."""
        self.dx += (2 * random() - 1.0) * self.max_flight_step
        self.dy += (2 * random() - 1.0) * self.max_flight_step
        self.x += self.dx
        self.y += self.dy
        self.steps_to_flee -= 1
        if not self.steps_to_flee:
            self.dx = self.dy = 0
            self._unbonded[self.sex].append(self)

    def update(self):
        self.move_random()
        if self.steps_to_flee:
            self.flee()
        elif self.partner is None:
            self.search_partner()
        else:
            self.move_towards_partner()
            self.is_partner_too_close()
        return

    def move_random(self):
        """Random movement."""
        if BIASED_RANDOM_MOVEMENT:
            self.x += (2 * random() - 1.0 + self.x_bias) * RANDOM_MOVEMENT
            self.y += (2 * random() - 1.0 + self.y_bias) * RANDOM_MOVEMENT
        else:
            self.x += (2 * random() - 1.0) * RANDOM_MOVEMENT
            self.y += (2 * random() - 1.0) * RANDOM_MOVEMENT

    def search_partner(self):
        """Check if there's a compatible partner in range."""
        for sex in self.compatible_sexes:
            for other in self._unbonded[sex]:
                if self.is_valid_partner_for(other):
                    self.partner = other
                    other.partner = self
                    self._unbonded[self.sex].remove(self)
                    self._unbonded[other.sex].remove(other)
                    self.search_distance = SEARCH_DISTANCE
                    other.search_distance = SEARCH_DISTANCE
                    return

        if self.search_distance < MAX_SEARCH_DISTANCE:
            self.search_distance *= self.search_distance
        elif self.search_distance > MAX_SEARCH_DISTANCE:
            self.search_distance = MAX_SEARCH_DISTANCE

    def move_towards_partner(self):
        """Walk 10% of the way towards your partner."""
        self.x += (self.partner.x - self.x) / SPEED_TOWARDS_PARTNER_INVERSE
        self.y += (self.partner.y - self.y) / SPEED_TOWARDS_PARTNER_INVERSE

    def break_bond(self):
        """Break the partnership."""
        self.steps_to_flee = STEPS_TO_FLEE
        self.partner.steps_to_flee = STEPS_TO_FLEE
        self.partner.last_partner = self
        self.last_partner = self.partner
        self.partner.partner = None
        self.partner = None
        return

    def is_partner_too_close(self):
        """If the partner did come too close."""
        if self.distance_to(self.partner) < self.safe_distance:
            self.break_bond()


class Scene(BaseScene):
    """A dummy scene - mostly just the Scene API."""

    def __init__(self, core, *args, **kwds):
        """Initialize the scene with a core object for basic functions."""
        super(Scene, self).__init__(core, *args, **kwds)
        self.blobs = []
        for i in range(NUMBER_OF_BLOBS):
            sex = choice(SEX_DISTRIBUTION)
            (x, y) = self.get_starting_position(sex)
            blob = Blob(x=x, y=y, sex=sex)
            self.blobs.append(blob)
            self.visible.append(blob)

    def keep_on_screen(self, blob):
        if blob.x < 0:
            blob.x = 0
        if blob.y < 0:
            blob.y = 0
        if blob.x + blob.width > self.core.win.width:
            blob.x = self.core.win.width - blob.width
        if blob.y + blob.height > self.core.win.height:
            blob.y = self.core.win.height - blob.height

    def get_starting_position(self, sex):
        """Select a starting position based on the config parameters."""
        if STARTING_POSITIONS is None:
            x = 0.5 * self.core.win.width
            y = 0.5 * self.core.win.height
        elif STARTING_POSITIONS == 'random':
            x = random() * self.core.win.width
            y = random() * self.core.win.height
        elif STARTING_POSITIONS == 'sex seperated':
            if sex is None:
                pos_x = 0.0
                pos_y = 1.0
            elif sex == 'male':
                pos_x = pos_y = 1.0
            else:
                pos_x = pos_y = 0.0
            x = pos_x * self.core.win.width
            y = pos_y * self.core.win.height
        return (
         x, y)

    def update(self):
        """Update the stats of all scene objects. 

Don't blit them, though. That's done by the Game itself.

To show something, add it to the self.visible list. 
To add a collider, add it to the self.colliding list. 
To add an overlay sprite, add it to the self.overlay list. 
"""
        for blob in self.blobs:
            blob.update()
            self.keep_on_screen(blob)

        sleep(0.01)
# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/iii/Documents/projects/ahorn/venv/lib/python3.4/site-packages/ahorn/Actors/RandomActor.py
# Compiled at: 2016-08-02 10:00:55
# Size of source mod 2**32: 664 bytes
import random
from ..GameBase import Actor

class RandomActor(Actor):
    """RandomActor"""

    def __init__(self):
        pass

    def get_action(self, state):
        """Return a random action from the legal actions

        Parameters
        ----------
        State:
            The state in which the actor must perform an action

        Returns
        -------
        Action:
            A random action from the legal actions"""
        return random.choice(state.get_legal_actions(self))

    def __str__(self):
        return 'RandomActor'
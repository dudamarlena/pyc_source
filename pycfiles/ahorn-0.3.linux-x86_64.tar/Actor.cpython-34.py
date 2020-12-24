# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/iii/Documents/projects/ahorn/venv/lib/python3.4/site-packages/ahorn/GameBase/Actor.py
# Compiled at: 2016-08-02 10:00:55
# Size of source mod 2**32: 850 bytes
import abc

class Actor(metaclass=abc.ABCMeta):
    __doc__ = 'An actor performs actions and drives a game from state to state.\n\n    Parameters\n    ----------\n\n    Returns\n    -------\n    '

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_action(self, state):
        """Return the action the actor wants to take in a given state.

        Parameters
        ----------
        State:
            The state in which the actor must perform an action

        Returns
        -------
        action: Action
            The action the actor wants to take in this state."""
        pass

    @abc.abstractmethod
    def __str__(self):
        """A name for this actor

        Parameters
        ----------

        Returns
        -------
        name: str
            The name for this actor."""
        pass
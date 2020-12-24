# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/iii/Documents/projects/ahorn/venv/lib/python3.4/site-packages/ahorn/GameBase/Action.py
# Compiled at: 2016-08-01 05:03:01
# Size of source mod 2**32: 1002 bytes
import abc

class Action(metaclass=abc.ABCMeta):
    __doc__ = 'An action modifies one game state into the other.\n\n    Parameters\n    ----------\n\n    Returns\n    -------'

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def execute(self, state):
        """Perform the action on a given state

        Parameters
        ----------
        State:
            The state that must be modified

        Returns
        -------
        State:
            The modified state
        """
        pass

    @abc.abstractmethod
    def __str__(self):
        """A string representation of this action.

        Parameters
        ----------

        Returns
        -------
        str
            String representation of this action."""
        pass

    def __hash__(self):
        """Get a hash of the current action.

        Parameters
        ----------

        Returns
        -------
        int
            The hash of the action"""
        return hash(str(self))
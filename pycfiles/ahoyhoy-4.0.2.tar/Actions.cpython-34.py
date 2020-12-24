# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/iii/Documents/projects/ahorn/venv/lib/python3.4/site-packages/ahorn/TicTacToe/Actions.py
# Compiled at: 2016-08-01 05:02:22
# Size of source mod 2**32: 1164 bytes
from ..GameBase import Action as BaseAction

class TicTacToeAction(BaseAction):
    """TicTacToeAction"""

    def __init__(self, symbol, where):
        self.symbol = symbol
        self.where = where

    def execute(self, state):
        """Execute the action.

        Modifies the board of the state, and the current player index.

        Parameters
        ----------
        state: TTTState
            The state which to modify

        Returns
        -------"""
        r, c = self.where
        state.board[r][c] = self.symbol
        state.pi = (state.pi + 1) % 2
        return state

    def __str__(self):
        """A string representation of this action.

        For example: "Put a X in position 1, 2"

        Parameters
        ----------

        Returns
        -------
        str
            String representation of this action."""
        return 'Put a {} in position {}'.format(self.symbol, self.where)
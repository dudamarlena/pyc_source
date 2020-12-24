# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/iii/Documents/projects/ahorn/venv/lib/python3.4/site-packages/ahorn/TicTacToe/Actions.py
# Compiled at: 2016-08-01 05:02:22
# Size of source mod 2**32: 1164 bytes
from ..GameBase import Action as BaseAction

class TicTacToeAction(BaseAction):
    __doc__ = 'In Tac-Tac-Toe the only action is puttin an O or an X in a free space\n\n    Parameters\n    ----------\n        symbol: str\n            Either "X" or "O"\n        where: (int, int)\n            A tuple with row and column index\n\n    Returns\n    -------'

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
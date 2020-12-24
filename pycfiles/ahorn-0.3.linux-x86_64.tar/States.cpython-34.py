# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/iii/Documents/projects/ahorn/venv/lib/python3.4/site-packages/ahorn/TicTacToe/States.py
# Compiled at: 2016-08-02 10:00:55
# Size of source mod 2**32: 5884 bytes
from ..GameBase import State as BaseState
from .Actions import TicTacToeAction

class TicTacToeState(BaseState):
    __doc__ = 'Describes a Tic-Tac-Toe state\n\n    Parameters\n    ----------\n    players: List\n        A list containing 2 Player objects\n\n    Returns\n    -------'

    def __init__(self, players):
        self.board = [
         [
          '-', '-', '-'],
         [
          '-', '-', '-'],
         [
          '-', '-', '-']]
        assert len(players) == 2
        self.players = players
        self.pi = 0

    def copy(self, other):
        """Copy the content of another state into this state

        Deep copy, i.e. modifying the copied state can not influence the
        content of the original state.

        Parameters
        ----------
        other : State
            The state from which to copy the content

        Returns
        -------"""
        for i, row in enumerate(other.board):
            for j, item in enumerate(row):
                self.board[i][j] = item

        self.pi = other.pi

    def _find_success(self):
        """Find OOO or XXX rows.

        Parameters
        ----------

        Returns
        -------
        row: List
            Either OOO or XXX, depending in which one has been found.
            Or None if none found"""

        def _row_identical(a, b):
            return all([aa == bb for aa, bb in zip(a, b)])

        ooo = [
         'O', 'O', 'O']
        xxx = ['X', 'X', 'X']
        for row in self.board:
            if _row_identical(row, ooo):
                return ooo
            if _row_identical(row, xxx):
                return xxx

        transpose = zip(*self.board)
        for collumn in transpose:
            if _row_identical(collumn, ooo):
                return ooo
            if _row_identical(collumn, xxx):
                return xxx

        diagonals = [[self.board[0][0], self.board[1][1], self.board[2][2]],
         [
          self.board[0][2], self.board[1][1], self.board[2][0]]]
        for diagonal in diagonals:
            if _row_identical(diagonal, ooo):
                return ooo
            if _row_identical(diagonal, xxx):
                return xxx

    def is_final(self):
        """Return true if there is an OOO or XXX on the board, or the board is full.

        Parameters
        ----------

        Returns
        -------
        bool
            True if the state is an OXO on the board, false otherwise"""
        if self._find_success():
            return True
        free_spots = sum([1 if item == '-' else 0 for row in self.board for item in row])
        if free_spots == 0:
            return True
        return False

    def get_random(self, player):
        """Tic-Tac-Toe is of complete information. Return a copy of this state.

        Parameters
        -----------
        player: Player
            Not used

        Returns
        -------
        State
            A copy of this state"""
        new = TicTacToeState(self.players)
        new.copy(self)
        return new

    def get_actor(self):
        """Return the actor that must perform an action in this state.

        Cycles between the first player and the second player

        Parameters
        ----------

        Returns
        -------
        Actor
            The player that must perform an action in this state."""
        return self.players[self.pi]

    def get_players(self):
        """Return a list of all the players in the game.

        Parameters
        ----------

        Returns
        -------
        List<Player>
            A list of all the players in the game."""
        return self.players

    def get_legal_actions(self, player):
        """Return the legal actions a player can take in this state.

        Parameters
        ----------
        player: Player
            the player who wants to know which actions he can take

        Returns
        -------
        actions: List
            a list of Actions"""
        symbol = [
         'O', 'X'][self.players.index(player)]
        legal_actions = []
        for j, row in enumerate(self.board):
            for k, item in enumerate(row):
                if item == '-':
                    legal_actions.append(TicTacToeAction(symbol=symbol, where=(
                     j, k)))
                    continue

        return legal_actions

    def get_utility(self, player):
        """Return +1 if player won, -1 if player lost, 0 if draw.

        If the state is final, returns the utility, else returns None

        Parameters
        ----------
        player: Player
            The player for which to find the utility

        Returns
        -------
        utility: int
            The utility received by the player, or None"""
        if not self.is_final():
            return
        success = self._find_success()
        if success:
            aim = [
             'O', 'X'][self.players.index(player)]
            if success[0] == aim:
                return 1
            else:
                return -1
        return 0

    def str(self, player):
        """Returns a string containing the board, and the current player

        Parameters
        ----------

        Returns
        -------
        str
            String representation of this state."""
        s = ''
        for row in self.board:
            s += '\t' + ' '.join(row) + '\n'

        s += "Player {}'s turn".format(self.pi)
        return s

    def __str__(self):
        return 'TicTacToe'
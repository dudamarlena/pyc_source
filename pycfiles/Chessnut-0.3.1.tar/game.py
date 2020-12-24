# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/chessmind/core/game.py
# Compiled at: 2008-04-25 19:01:29
import board
from definitions import CHESS_BOARD

class ChessGame(object):
    """Class that holds info about a game.

    This can be used to take back moves.
    """
    __module__ = __name__

    def __init__(self, diagram=CHESS_BOARD):
        self.start_diagram = diagram
        self.board = board.ChessBoard(self.start_diagram)
        self.moves = []
        self.undone = []

    def listMoves(self):
        return self.moves

    def addMove(self, start, target, promotion=False):
        self.moves.append({'start': start, 'target': target, 'promotion': promotion})

    def move(self, start, target, promotion=False, redo=False):
        """Make a move
        """
        self.board.move(start, target, promotion=promotion)
        self.addMove(start, target, promotion)
        if not redo:
            self.undone = []

    def undoPossible(self):
        """Can a move be undone?
        """
        return len(self.moves) > 0

    def redoPossible(self):
        """Can a move be undone?
        """
        return len(self.undone) > 0

    def undo(self):
        """Undo a move.

        Easiest is to start over and redo all moves except that last
        one.
        """
        self.board = board.ChessBoard(self.start_diagram)
        if not self.undoPossible():
            raise Exception, 'No further undo info'
        self.undone.append(self.moves[(-1)])
        self.moves = self.moves[:-1]
        for move in self.moves:
            self.board.move(move['start'], move['target'], promotion=move['promotion'])

    def redo(self):
        """Redo a move.
        """
        if not self.redoPossible():
            raise Exception, 'No further redo info'
        move = self.undone[(-1)]
        self.move(move['start'], move['target'], promotion=move['promotion'], redo=True)
        self.undone = self.undone[:-1]
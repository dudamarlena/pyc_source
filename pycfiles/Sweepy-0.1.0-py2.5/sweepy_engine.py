# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sweepy/model/sweepy_engine.py
# Compiled at: 2009-10-21 16:34:35
"""Minesweeper engine - defines classes and exceptions needed"""
import random

class UncoveredBomb(Exception):
    """Raised when uncover a bomb"""
    pass


class AlreadyUncovered(Exception):
    """Raised when uncover a cell that is already uncovered"""
    pass


class GameOver(Exception):
    """Raised if uncover or flag a cell when the game is already over"""
    pass


class Grid(object):
    """ Defines the minesweeper grid and its operations """

    def __init__(self, rows, cols, probability=0.2, bombs=None):
        """ Setup the minesweeper grid
            
            rows: number of rows
            cols: number of columns
            probability: probability that any grid square is a bomb > 0 and < 1. Default 0.2
            bombs: set of points in the grid that contain bombs. Use if want to override
            the random bomb placement. Ignores any points that are outside grid bounds.
            Only the points specified in this set are bombs.
            
            If both probability and bombs are given, the bombs take precedence
        """
        if rows < 0 or cols < 0:
            raise ValueError, 'rows and cols must be greater than 0'
        if probability and (probability <= 0 or probability >= 1):
            raise ValueError, 'probability must be greater than 0 and less than 1'
        self._num_rows = rows
        self._num_cols = cols
        self._num_cells_to_uncover = rows * cols
        self._bombs = []
        self._guesses = []
        for row in range(0, rows):
            self._bombs.append([])
            self._guesses.append([])
            for col in range(0, cols):
                self._guesses[row].append('?')
                if bombs:
                    if (row, col) not in bombs:
                        self._bombs[row].append('.')
                    else:
                        self._bombs[row].append('B')
                        self._num_cells_to_uncover -= 1
                elif random.random() >= probability:
                    self._bombs[row].append('.')
                else:
                    self._bombs[row].append('B')
                    self._num_cells_to_uncover -= 1

        self._gameover = False

    def game_state(self):
        """Returns a tuple containing the game's current state

           Tuple of (array of guesses, number of cells left to uncover,
           GameOver boolean)
        """
        return (
         self._guesses, self._num_cells_to_uncover, self._gameover)

    def flag(self, row, col):
        """Toggle a cell's flag from ? to F or vice-versa. 
    
            row and col are 0-indexed and must be less than rows/cols passed into the init
            Must not be an uncovered cell, or AlreadyUncovered is thrown
        """
        if self._gameover:
            raise GameOver
        if not self._valid_cell_index(row, col):
            raise ValueError, '%s,%s is not a valid Grid coordinate' % (row, col)
        if self._guesses[row][col] == '?':
            self._guesses[row][col] = 'F'
        elif self._guesses[row][col] == 'F':
            self._guesses[row][col] = '?'
        else:
            raise AlreadyUncovered

    def uncover(self, row, col):
        """Uncover a cell. 
        
            If the cell contains a bomb, raise UncoveredBomb
            If the cell is already uncovered, raise AlreadyUncovered
            If the cell does not contain a bomb, calc. no. of bomb neighbours
            
            A common feature of minesweeper games is that if you uncover 
            a cell with 0 bomb neighbours, the game auto-uncovers all that 
            cell's neighbours, recursively, until no more 0-bomb-neighbour cells
            are found.
        """
        if self._gameover:
            raise GameOver
        if not self._valid_cell_index(row, col):
            raise ValueError, '%s,%s is not a valid Grid coordinate' % (
             row, col)
        if self._bombs[row][col] == 'B':
            self._gameover = True
            raise UncoveredBomb
        try:
            dummy = int(self._guesses[row][col])
            raise AlreadyUncovered
        except ValueError:
            pass

        num_bombs = 0
        neighbours = [
         (-1, -1), (-1, 0), (-1, +1), (0, -1), (0, +1), (+1, -1), (+1, 0), (+1, +1)]
        for (x, y) in neighbours:
            xoff = row + x
            yoff = col + y
            if self._valid_cell_index(xoff, yoff):
                if self._bombs[xoff][yoff] == 'B':
                    num_bombs += 1

        self._guesses[row][col] = str(num_bombs)
        self._num_cells_to_uncover -= 1
        if self._num_cells_to_uncover < 1:
            self._gameover = True
            raise GameOver
        if num_bombs == 0:
            for (x, y) in neighbours:
                try:
                    self.uncover(row + x, col + y)
                except (AlreadyUncovered, ValueError):
                    pass

    def cheat(self):
        """Allows you to, well, cheat, by returning a set containing 
            the grid refs of all bombs.
        
            This set can also be used to initialise a new Grid via the optional <bombs> argument.
            The primary motivation for providing this method is to increase testability by allowing
            a given grid to be reinstantiated (i.e. for test fixtures)
            
            >>> from minesweeper.engine import Grid
            >>> mybombs = set([(0,0),(1,1),(2,2),(3,3),(0,1)])
            >>> g = Grid(4,4,bombs=mybombs)
            >>> c = g.cheat()
            >>> c == mybombs
            True

        """
        retval = []
        for row in range(0, self._num_rows):
            for col in range(0, self._num_cols):
                if self._bombs[row][col] == 'B':
                    retval.append((row, col))

        return set(retval)

    def _valid_cell_index(self, row, col):
        """ Check if the grid coordinate is valid
        
            Returns True if the given row, col refer to a cell within the bounds 
            of the Grid, otherwise returns False
        """
        if row < 0 or row >= self._num_rows or col < 0 or col >= self._num_cols:
            return False
        return True

    def cols(self):
        """Return the number of columns in the grid."""
        return self._num_cols

    def rows(self):
        """Return the number of rows in the grid."""
        return self._num_rows
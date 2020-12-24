# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmiller/Runestone/RunestoneComponents/runestone/codelens/ttt_module.py
# Compiled at: 2019-11-02 08:12:59
# Size of source mod 2**32: 5763 bytes
"""
Tic Tac Toe (and more generally, 2-D grid environments) that display in browser.

Created by Peter Norvig

NB: need to work on both Python 2 and 3
"""

def tagger(tagname):
    """Make a function that can be used to generate HTML."""

    def tagfn(*content, **kwargs):
        args = '' if not kwargs else ' ' + ' '.join(('{}={!r}'.format(k, kwargs[k]) for k in kwargs))
        return '<{}{}>{}</{}>'.format(tagname, args, join(content), tagname)

    return tagfn


A, B, I, P, TABLE, TR, TD, TH = list(map(tagger, 'A B I P, TABLE TR TD TH'.split()))

def join(content):
    """Like ' '.join(content), but recurses into nested lists."""
    if isinstance(content, str):
        return content
    if isinstance(content, (list, tuple)):
        return ' '.join(map(join, content))
    return str(content)


try:
    _ = xrange
except NameError:
    xrange = range

def table(matrix, **kwargs):
    """Given [[a, b, c], [d, e, f]], lay it out as a table.
    Each cell gets an id number, starting at 0.  Table can have kwargs."""
    ints = iter(range(1000000))
    return TABLE([TR([TD(c, id=(next(ints))) for c in row]) for row in matrix], **kwargs)


css = '#htmlOutputDiv table, #htmlOutputDiv td, #htmlOutputDiv th {\n  background-color: white;\n  border-collapse: collapse;\n  border: 2px solid black; }\n#htmlOutputDiv td, #htmlOutputDiv th {\n  width: 30px;\n  height: 30px;\n  font-family: sans-serif;\n  text-align: center; }'

class Game(object):
    __doc__ = 'Move stuff here later'


class TTTGame(Game):

    def __init__(self, player1, player2, verbose=True):
        print('Initializing TTTGame')
        self.board = [' '] * 9
        self.tomove = 0
        self.symbols = ['X', 'O']
        self.players = [player1, player2]
        self.lines = [
         (0, 1, 2),
         (3, 4, 5),
         (6, 7, 8),
         (0, 3, 6),
         (1, 4, 7),
         (2, 5, 8),
         (0, 4, 8),
         (2, 4, 6)]
        self.winner = None
        self.verbose = verbose
        setJS("$('#htmlOutputDiv table td').click(function(){myVisualizer.executeCodeWithRawInputFunc($(this).attr('id'), myVisualizer.curInstr)})")

    def draw(self):
        setCSS(css)
        s = table([[self.board[(3 * r + c)] for c in range(3)] for r in range(3)])
        if self.over():
            s += P('Game over; ', 'nobody' if self.winner is None else self.symbols[self.winner], ' wins')
        else:
            s += P(self.symbols[self.tomove] + ' to play')
        if self.verbose:
            print(s)
        setHTML(s)
        return s

    def play(self):
        self.draw()
        for i in range(2):
            p = self.tomove
            move = self.players[p](list(self.board), self.symbols[p])
            self.makemove(move)
            self.draw()

    def displayWarning(self, msg):
        print('WARNING! ' + msg)

    def makemove(self, move):
        player = self.tomove
        print('making move ' + str(move) + ' for player ' + str(player))
        if self.over():
            self.displayWarning('game over, no more moves')
        else:
            if move not in list(range(9)):
                self.displayWarning('not a legal square ' + str(move))
                return
            if self.board[move] != ' ':
                self.displayWarning('not an empty square ' + str(move))
                return
            self.board[move] = self.symbols[player]
            self.tomove = other(player)
            return move

    def legal(self, move):
        """A legal move is an index to a blank square."""
        return move in range(9) and self.board[move] == ' '

    def over(self):
        """Return True when game is over."""
        if ' ' not in self.board:
            winner = None
            return True
        for player in (0, 1):
            for line in self.lines:
                if self.linecount(line, player) == 3:
                    self.winner = player
                    return True

        return False

    def playgame(self):
        while not self.over():
            self.makemove()

    def linecount(self, line, player):
        """Return the number of pieces that player (0 or 1) has on this line."""
        return [self.board[i] for i in line].count(self.symbols[player])

    def illegalmove(self, move):
        """Report that move is illegal; decrement remaining count for player."""
        self.allowed_illegal_moves[self.tomove] -= 1
        if self.allowed_illegal_moves[self.tomove] < 0:
            self.winner = other(self.tomove)

    def copystate(self):
        clone = TTTGame(*self.players)
        clone.tomove = self.tomove
        clone.board = list(self.board)
        return clone


def other(player):
    return 1 - player
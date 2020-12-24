# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/chessmind/grok/cm.py
# Compiled at: 2008-04-25 19:35:15
import grok
from chessmind.core.game import ChessGame
from chessmind.core.definitions import WHITE, BLACK
from chessmind.core.position import ChessException, PromotionException
from chessmind.core.position import positionColour, squarify
from chessmind.core.piece import promotionmap

class Chessminder(grok.Application, grok.Model):
    __module__ = __name__

    def __init__(self):
        self.reset()

    def reset(self):
        self.game = ChessGame()
        self.discussion = []


def square_dict(backcolour=None, src=None, value='', selected=False):
    """Return a dictionary that a page template can use.
    """
    if src:
        klass = 'square'
    else:
        klass = 'empty'
    if backcolour:
        klass += '-' + backcolour
    if selected:
        klass += ' selected'
    data = {'backcolour': backcolour, 'src': src, 'value': value, 'class': klass, 'selected': selected}
    return data


def parseSquare(square, rowindex, colindex, selectedSquare):
    if square.colour == WHITE:
        colour = 'white'
    elif square.colour == BLACK:
        colour = 'black'
    else:
        colour = None
    if colour is None:
        src = ''
    else:
        piecename = square.name.lower()
        src = '++resource++chessmind.grok/' + piecename + '-' + colour + '.png'
    if positionColour(rowindex, colindex) == WHITE:
        backcolour = 'white'
    else:
        backcolour = 'black'
    value = squarify(rowindex, colindex)
    if value == selectedSquare:
        selected = True
    else:
        selected = False
    return square_dict(value=value, backcolour=backcolour, src=src, selected=selected)


class Index(grok.View):
    __module__ = __name__

    def update(self, promotion=False, want_hint=False, reset=None, undo=None, redo=None, start=None, target=None, square=None, show_diagram=False, white=None, black=None, discuss=None):
        """Update the board by making a move.
        """
        self.error = self.start = self.target = None
        self.promotion = promotion
        self.want_hint = want_hint
        self.reset = reset
        self.undo = undo
        self.redo = redo
        self.start = start
        self.target = target
        self.square = square
        self.show_diagram = show_diagram
        self.white = white
        self.black = black
        if discuss:
            self.context.discussion.insert(0, discuss)
            self.context._p_changed = True
        self.discussion = self.context.discussion[:4]
        self.do_requested_actions()
        self.mate = self.context.game.board.isMate()
        if self.mate:
            self.stalemate = self.context.game.board.isStaleMate()
            self.checkmate = self.context.game.board.isCheckMate()
            if self.checkmate:
                if self.context.game.board.player == WHITE:
                    self.winner = 'black'
                else:
                    self.winner = 'white'
        self.undo = self.context.game.undoPossible()
        self.redo = self.context.game.redoPossible()
        self.value = self.context.game.board.value()
        if self.want_hint:
            self.hint = self.context.game.board.hint()
        if self.context.game.board.player == WHITE:
            self.player = 'white'
        else:
            self.player = 'black'
        if self.show_diagram:
            self.printed_board = '%s' % self.context.game.board.export()
        return

    def do_requested_actions(self):
        """Do the actions requested by the player.
        """
        if self.reset:
            self.context.reset()
            self.white = ''
            self.black = ''
            return
        if self.undo:
            self.context.game.undo()
            self.context._p_changed = True
            return
        if self.redo:
            self.context.game.redo()
            self.context._p_changed = True
            return
        if self.square:
            self.target = self.square
        if self.target:
            if self.start:
                if self.start == self.target:
                    self.start = None
                    return
                try:
                    self.context.game.move(self.start, self.target, promotion=self.promotion)
                    self.context._p_changed = True
                    self.promotion = False
                    self.start = None
                except PromotionException, e:
                    self.error = e
                    self.promotion = True
                except ChessException, e:
                    self.error = e

            else:
                self.start = self.square
        return

    def promotion_row(self):
        """Return Queen, Rook, Bishop and Knight as promotion candidates.
        """
        pieces = []
        colour = self.player
        piecesigns = promotionmap.keys()
        for sign in piecesigns:
            piecename = promotionmap.get(sign)
            src = '++resource++chessmind.grok/' + piecename + '-' + colour + '.png'
            if colour == 'black':
                sign = sign.lower()
            pieces.append(square_dict(src=src, value=sign))

        return pieces

    def board(self):
        """Display a board in the browser.
        """
        rows = []
        for rowindex in range(len(self.context.game.board.rows)):
            rows.append([])
            row = rows[rowindex]
            colindex = 0
            for square in self.context.game.board.rows[rowindex]:
                info = parseSquare(square, rowindex, colindex, self.start)
                row.append(info)
                colindex += 1

        rows.reverse()
        return rows
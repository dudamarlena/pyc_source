# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sweepy/controllers/game.py
# Compiled at: 2009-10-21 16:37:05
import logging, sweepy.lib.helpers as h
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from sweepy.lib.base import BaseController, render
from sweepy.model.sweepy_engine import Grid, UncoveredBomb, AlreadyUncovered, GameOver
log = logging.getLogger(__name__)

class GameController(BaseController):

    def start(self, row, col, probability):
        g = Grid(int(row), int(col), probability=float(probability))
        session['grid'] = g
        session.save()
        (c.grid, c.num_left, c.gameover) = g.game_state()
        c.rows = g.rows()
        c.cols = g.cols()
        return render('/grid.html')

    def flag(self, row, col):
        try:
            session['grid'].flag(int(row), int(col))
        except (UncoveredBomb, AlreadyUncovered, GameOver):
            pass

        session.save()
        (c.grid, c.num_left, c.gameover) = session['grid'].game_state()
        c.rows = session['grid'].rows()
        c.cols = session['grid'].cols()
        return render('/grid.html')

    def uncover(self, row, col):
        try:
            session['grid'].uncover(int(row), int(col))
        except (UncoveredBomb, GameOver):
            c.bombs = session['grid'].cheat()
        except AlreadyUncovered:
            pass

        session.save()
        (c.grid, c.num_left, c.gameover) = session['grid'].game_state()
        c.rows = session['grid'].rows()
        c.cols = session['grid'].cols()
        return render('/grid.html')
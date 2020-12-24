# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\src\abs\game.py
# Compiled at: 2018-08-23 04:17:51
import threading
from colorama import Fore
from unit import E
from cell import Cell, Board
import random, click

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


BASE_BOARD = [
 [
  3, 2, 9, 6, 5, 7, 8, 4, 1],
 [
  7, 4, 5, 8, 3, 1, 2, 9, 6],
 [
  6, 1, 8, 2, 4, 9, 3, 7, 5],
 [
  1, 9, 3, 4, 6, 8, 5, 2, 7],
 [
  2, 7, 6, 1, 9, 5, 4, 8, 3],
 [
  8, 5, 4, 3, 7, 2, 6, 1, 9],
 [
  4, 3, 2, 7, 1, 6, 9, 5, 8],
 [
  5, 8, 7, 9, 2, 3, 1, 6, 4],
 [
  9, 6, 1, 5, 8, 4, 7, 3, 2]]

class Game(object):
    _instance_lock = threading.Lock()
    difficulties = {'easy': (9, 0), 
       'medium': (45, 0), 
       'hard': (45, 0), 
       'extreme': (54, 0)}

    def __init__(self, with_coordinate, step_check, mode, random, mutiple, lmutiple):
        self.with_coordinate = with_coordinate
        self.step_check = step_check
        self.mode = mode
        self.random = random
        self.mutiple = mutiple
        self.lmutiple = lmutiple
        self.numList = BASE_BOARD
        self.coords = self.coordinate()
        self.board = None
        return

    def __new__(cls, *args, **kwargs):
        if not hasattr(Game, '_instance'):
            with Game._instance_lock:
                if not hasattr(Game, '_instance'):
                    Game._instance = object.__new__(cls)
        return Game._instance

    def coordinate(self):

        def blank(i):
            if i == 8:
                return ''
            if (i + 1) % 3 == 0:
                return '  '
            return ''

        if self.with_coordinate:
            return [[ Fore.BLUE + '>' + str(i + 1) + Fore.RESET + ' ' for i in range(9) ],
             '   ' + Fore.BLUE + (' ').join([ 'v' + blank(i) for i in range(9) ]) + Fore.RESET + '\n   ' + Fore.BLUE + (' ').join([ str(i + 1) + blank(i) for i in range(9) ]) + Fore.RESET]
        else:
            return [[ '' for i in range(9) ],
             False]

    def fill_random(self):
        difficulty = Game.difficulties[self.mode]
        matrixs = E.batch_generate(self.random, self.mutiple)
        for i in range(self.lmutiple):
            self.numList = E.multiple(self.numList, matrixs[i], 9)

        for i in range(self.mutiple - self.lmutiple):
            self.numList = E.multiple(matrixs[(i + self.lmutiple)], self.numList, 9)

        self.board = Board(map(lambda x: Cell(x), [ cell for row in self.numList for cell in row ]), difficulty[0] + difficulty[1])
        self.reduce_cell(difficulty[0], difficulty[1])
        self.numList = list(chunks(self.board.cells, 9))

    def reduce_cell(self, init, addtion):
        for i in range(9):
            for j in range(init / 9):
                r = random.randint(3 * (i / 3), 3 * (i / 3) + 2)
                c = random.randint(3 * (i % 3), 3 * (i % 3) + 2)
                ind = r * 9 + c
                while self.board.cells[ind].visible == False:
                    r = random.randint(3 * (i / 3), 3 * (i / 3) + 2)
                    c = random.randint(3 * (i % 3), 3 * (i % 3) + 2)
                    ind = r * 9 + c

                self.board.cells[ind].set_visible(False)

    def game_over(self):
        return self.board.over()

    def flush(self):
        prefix = ''
        if self.with_coordinate:
            prefix = '   '
        if self.with_coordinate:
            print self.coords[1]
        for i in range(0, 9):
            _str = self.coords[0][i] + (' | ').join(map(lambda x: (' ').join(map(lambda y: str(y.get_value()), x)), list(chunks(self.numList[i], 3))))
            print _str
            if i != 0 and (i + 1) % 3 == 0:
                print prefix + '-' * 22

    def gloop(self):
        while not self.game_over():
            x = click.prompt('Please enter a valid integer [i] (1 - 9)', type=int)
            y = click.prompt('Please enter a valid integer [j] (1 - 9)', type=int)
            while x > 9 or x < 1 or y > 9 or y < 1:
                self.flush()
                print Fore.RED + 'You enter an invalid integer, think more and enter again!' + Fore.RESET
                x = click.prompt('Please enter a valid integer [i] (1 - 9)', type=int)
                y = click.prompt('Please enter a valid integer [j] (1 - 9)', type=int)

            while self.board.get_cell(x, y).visible:
                self.flush()
                print Fore.RED + 'Cells[%d][%d] need not to be covered, think more and enter again!' % (x, y) + Fore.RESET
                x = click.prompt('Please enter a valid integer [i] (1 - 9)', type=int)
                y = click.prompt('Please enter a valid integer [j] (1 - 9)', type=int)

            value = click.prompt('Please enter a valid integer (1 - 9) to cover the original integer Cells[%d][%d]' % (x, y), type=int)
            if value > 9 or value < 1:
                self.flush()
                print Fore.RED + 'Sorry you enter an invalid value %d, Try again!' % value + Fore.RESET
            elif self.step_check:
                if self.board.check(x, y, value):
                    self.board.set_cell(x, y, value)
                    self.flush()
                else:
                    self.flush()
                    print Fore.RED + 'Sorry you enter an invalid value %d, Try again!' % value + Fore.RESET
            else:
                self.board.set_cell(x, y, value)

        print 'You Got IT'
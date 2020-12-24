# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/iii/Documents/projects/ahorn/venv/lib/python3.4/site-packages/ahorn/run.py
# Compiled at: 2016-06-01 16:18:28
# Size of source mod 2**32: 309 bytes
from ahorn import Controller
from ahorn.TicTacToe import TTTState
from ahorn.Actors import RandomPlayer
if __name__ == '__main__':
    players = [
     RandomPlayer(), RandomPlayer()]
    initial_state = TTTState(players)
    controller = Controller(initial_state, verbose=True)
    end_state = controller.play()
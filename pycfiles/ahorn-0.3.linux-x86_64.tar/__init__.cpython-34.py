# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/iii/Documents/projects/ahorn/venv/lib/python3.4/site-packages/ahorn/__init__.py
# Compiled at: 2016-08-01 04:00:19
# Size of source mod 2**32: 1122 bytes
"""
Ahorn
===================

A game description framework and game playing AI library,
written entirely in Python.

Quickstart
==========
    import ahorn, ahorn.Actors, ahorn.TicTacToe
    player_a, player_b = ahorn.Actors.MCTSPlayer(), ahorn.Actors.MCTSPlayer()
    starting_state = ahorn.TicTacToe.TicTacToeState([player_a, player_b])
    controller = ahorn.Controller(starting_state, verbose=True)
    controller.play()

Installation
============
    pip3 install -r requirements.txt
    python3 setup.py install
    python3 run.py  # should start playing a game

Running the tests
=================
    python3 -m pytest tests

Adding a new game
=================

A game is described by states and actions.
To describe a new game, subclass ahorn.GameBase.State and ahorn.GameBase.Action.
Take a look at the example: ahorn.TicTacToe.

Adding new AI
=============

Ahorn comes with a generic AI based on the Monte Carlo Tree Search algorithm:
 ahorn.Actors.MCTSPlayer.
To create a new AI, subclass ahorn.GameBase.Player. Take a look at the
example: ahorn.Actors.RandomPlayer.

"""
from .Controller import Controller
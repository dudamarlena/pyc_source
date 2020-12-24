# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\game_hero\main_game.py
# Compiled at: 2020-01-24 07:34:21
# Size of source mod 2**32: 2128 bytes
"""
Game's main module.

The project developed covers a story game based on turn based combat,
where the game hero encounters a wild beast in the forest.

Game character's stats are taken into consideration on each turn,
whilst the hero also possesses some additional skills to help him in battle.
"""
import io
from contextlib import redirect_stdout
from tkinter import messagebox
from game_hero import game_characters
from game_hero import gameplay_mechanics

class HeroGame(metaclass=gameplay_mechanics.Singleton):
    __doc__ = '\n    Hero Game instance.\n    '

    def __init__(self):
        """
        This instance of the game is used in order to access the game,
        as well as simulate a fight between two characters.

        Exposes the `start_game()` method, which outputs the rounds
        of a turn based fight between the Game's Hero and a Wild Beast.
        """
        self._gameplay_functionality = gameplay_mechanics.Gameplay()

    def start_game(self):
        """
        Start of the game, therefore execution of the fight rounds
        between the Game's Hero and the encountered Wild Beast.

        Both of the Game's characters have their stats pre-initialized
        at the start of the game, with each turn subtracting health from
        the defender, based on attacker's strength and defender's defence stats

        The game ends when one of the player's health reaches zero.

        :return: Output of the game, with information from each turn.
        """
        with io.StringIO() as (buffer):
            with redirect_stdout(buffer):
                self._gameplay_functionality.simulate_fight(game_hero=(game_characters.Orderus()),
                  magical_beast=(game_characters.WildBeast()))
                game_output = buffer.getvalue()
        print(game_output)
        messagebox.showinfo('Hero Game', game_output)
        return game_output
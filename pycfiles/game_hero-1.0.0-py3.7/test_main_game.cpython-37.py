# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\test_main_game.py
# Compiled at: 2020-01-24 08:42:11
# Size of source mod 2**32: 543 bytes
from game_hero.main_game import HeroGame

def test_start_game():
    """
    Tests output of the game as string
    """
    game_instance = HeroGame()
    game_output = game_instance.start_game()
    assert isinstance(game_output, str), 'Output of the game is not string!'


def test_game_instance():
    """
    Tests singleton implementation for the HeroGame instances.
    """
    first_instance = HeroGame()
    second_instance = HeroGame()
    assert first_instance is second_instance, 'Different instances for game!'
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\joysticks.py
# Compiled at: 2020-03-29 13:19:23
# Size of source mod 2**32: 432 bytes
import pyglet.input

def get_joysticks():
    """
    Get a list of all the game controllers

    This is an alias of ``get_game_controllers``, which is better worded.

    :return: List of game controllers
    """
    return pyglet.input.get_joysticks()


def get_game_controllers():
    """
    Get a list of all the game controllers

    :return: List of game controllers
    """
    return get_joysticks()
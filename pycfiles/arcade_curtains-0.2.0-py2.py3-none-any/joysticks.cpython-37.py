# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
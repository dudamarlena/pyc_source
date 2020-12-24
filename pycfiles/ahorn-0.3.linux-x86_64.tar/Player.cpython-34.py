# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/iii/Documents/projects/ahorn/venv/lib/python3.4/site-packages/ahorn/GameBase/Player.py
# Compiled at: 2016-08-01 05:03:52
# Size of source mod 2**32: 164 bytes
from .Actor import Actor
import abc

class Player(Actor, metaclass=abc.ABCMeta):
    __doc__ = 'A player is an actor that actively decides which action to take'
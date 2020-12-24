# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python27\Lib\site-packages\milight\white.py
# Compiled at: 2015-03-18 21:01:11
from . import Command
from math import floor
import colorsys
COMMANDS = {'ON': (
        Command(53, wait=True),
        Command(56, wait=True),
        Command(61, wait=True),
        Command(55, wait=True),
        Command(50, wait=True)), 
   'OFF': (
         Command(57),
         Command(59),
         Command(51),
         Command(58),
         Command(54)), 
   'BRIGHTER': Command(60), 
   'DARKER': Command(52), 
   'WARMER': Command(62), 
   'COOLER': Command(63)}
COMMANDS['WHITE'] = (
 (
  COMMANDS['ON'][0], Command(181)),
 (
  COMMANDS['ON'][1], Command(184)),
 (
  COMMANDS['ON'][2], Command(189)),
 (
  COMMANDS['ON'][3], Command(183)),
 (
  COMMANDS['ON'][4], Command(178)))
COMMANDS['NIGHT'] = (
 (
  COMMANDS['OFF'][0], Command(185)),
 (
  COMMANDS['OFF'][1], Command(187)),
 (
  COMMANDS['OFF'][2], Command(179)),
 (
  COMMANDS['OFF'][3], Command(186)),
 (
  COMMANDS['OFF'][4], Command(182)))

def brightest(group=0):
    commands = [COMMANDS['ON'][group]]
    for i in range(0, 10):
        commands.append(COMMANDS['BRIGHTER'])

    return tuple(commands)


def darkest(group=0):
    commands = [COMMANDS['ON'][group]]
    for i in range(0, 10):
        commands.append(COMMANDS['DARKER'])

    return tuple(commands)


def warmest(group=0):
    commands = [COMMANDS['ON'][group]]
    for i in range(0, 10):
        commands.append(COMMANDS['WARMER'])

    return tuple(commands)


def coolest(group=0):
    commands = [COMMANDS['ON'][group]]
    for i in range(0, 10):
        commands.append(COMMANDS['COOLER'])

    return tuple(commands)


def fade_up(group=0):
    commands = list(darkest(group))
    for i in range(0, 10):
        commands.append(Command(60, wait=True))

    return tuple(commands)


COMMANDS['FADEUP'] = fade_up

def fade_down(group=0):
    commands = []
    for i in range(0, 10):
        commands.append(Command(60, wait=True))

    return brightest(group) + tuple(reversed(commands))


COMMANDS['FADEDOWN'] = fade_down

def brightness(level=100, group=0):
    """ Assumes level is out of 100 """
    if level not in range(0, 101):
        raise Exception('Brightness must be value between 0 and 100')
    b = int(floor(level / 10.0))
    commands = list(darkest(group))
    for i in range(0, b):
        commands.append(COMMANDS['BRIGHTER'])

    return tuple(commands)


COMMANDS['BRIGHTNESS'] = brightness

def warmness(level=100, group=0):
    """ Assumes level is out of 100 """
    if level not in range(0, 101):
        raise Exception('Warmness must be value between 0 and 100')
    b = int(floor(level / 10.0))
    commands = list(coolest(group))
    for i in range(0, b):
        commands.append(COMMANDS['WARMER'])

    return tuple(commands)


COMMANDS['WARMNESS'] = warmness
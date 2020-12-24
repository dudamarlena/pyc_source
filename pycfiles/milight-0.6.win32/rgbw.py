# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python27\Lib\site-packages\milight\rgbw.py
# Compiled at: 2015-03-18 21:01:11
from . import Command
from math import floor
COMMANDS = {'ON': (
        Command(66, wait=True),
        Command(69, wait=True),
        Command(71, wait=True),
        Command(73, wait=True),
        Command(75, wait=True)), 
   'OFF': (
         Command(65),
         Command(70),
         Command(72),
         Command(74),
         Command(76)), 
   'DISCO': Command(77), 
   'SLOWER': Command(67), 
   'FASTER': Command(68)}
COMMANDS['WHITE'] = (
 (
  COMMANDS['ON'][0], Command(194)),
 (
  COMMANDS['ON'][1], Command(197)),
 (
  COMMANDS['ON'][2], Command(199)),
 (
  COMMANDS['ON'][3], Command(201)),
 (
  COMMANDS['ON'][4], Command(203)))
COMMANDS['SYNC'] = (
 None,
 COMMANDS['ON'][1].with_repeat(5),
 COMMANDS['ON'][2].with_repeat(5),
 COMMANDS['ON'][3].with_repeat(5),
 COMMANDS['ON'][4].with_repeat(5))
PARTIES = {'white': 1, 
   'rainbow_swirl': 2, 
   'white_fade': 3, 
   'rgbw_fade': 4, 
   'rainbow_jump': 5, 
   'random': 6, 
   'red_twinkle': 7, 
   'green_twinkle': 8, 
   'blue_twinkle': 9}

def fade_up(group=0):
    commands = []
    for i in range(2, 28):
        commands.append(Command(78, i, True))

    return tuple(commands)


COMMANDS['FADEUP'] = fade_up

def fade_down(group=0):
    return reversed(fade_up(group))


COMMANDS['FADEDOWN'] = fade_down

def brightness(level=100, group=0):
    """ Assumes level is out of 100 """
    if level not in range(0, 101):
        raise Exception('Brightness must be value between 0 and 100')
    b = int(floor(level / 4.0) + 2)
    return (COMMANDS['ON'][group], Command(78, b))


COMMANDS['BRIGHTNESS'] = brightness

def color(hue=0, group=0):
    if hue not in range(0, 256):
        raise Exception('Color must be value between 0 and 255')
    return (
     COMMANDS['ON'][group], Command(64, hue))


COMMANDS['COLOR'] = color

def partay(mode, group=0):
    if mode not in PARTIES:
        raise Exception("Party Mode %s doesn't exist" % mode)
    number = PARTIES[mode]
    commands = list(COMMANDS['WHITE'][group])
    for i in range(1, number):
        commands.append(COMMANDS['DISCO'])

    return tuple(commands)


COMMANDS['PARTY'] = partay
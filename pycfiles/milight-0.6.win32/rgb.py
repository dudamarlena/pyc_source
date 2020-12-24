# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python27\Lib\site-packages\milight\rgb.py
# Compiled at: 2015-03-18 21:01:11
from . import Command
from math import floor
COMMANDS = {'ON': (
        Command(34, wait=True),
        Command(34, wait=True),
        Command(34, wait=True),
        Command(34, wait=True),
        Command(34, wait=True)), 
   'OFF': (
         Command(33),
         Command(33),
         Command(33),
         Command(33),
         Command(33)), 
   'BRIGHTER': Command(35), 
   'DARKER': Command(36), 
   'DISCOUP': Command(39), 
   'DISCODOWN': Command(40), 
   'SLOWER': Command(38), 
   'FASTER': Command(37)}
PARTIES = {'white': 1, 
   'rainbow_swirl': 2, 
   'white_fade': 3, 
   'rgbw_fade': 4, 
   'rainbow_jump': 5, 
   'random': 6, 
   'red_twinkle': 7, 
   'green_twinkle': 8, 
   'blue_twinkle': 9}

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


def fade_up(group=0):
    commands = list(darkest(group))
    for i in range(0, 10):
        commands.append(COMMANDS['BRIGHTER'].with_wait(True))

    return tuple(commands)


COMMANDS['FADEUP'] = fade_up

def fade_down(group=0):
    commands = list(brightest(group))
    for i in range(0, 10):
        commands.append(COMMANDS['DARKER'].with_wait(True))

    return tuple(commands)


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

def color(hue=0, group=0):
    if hue not in range(0, 256):
        raise Exception('Color must be value between 0 and 255')
    return (
     COMMANDS['ON'][group], Command(32, hue))


COMMANDS['COLOR'] = color

def partay(mode, group=0):
    if mode not in PARTIES:
        raise Exception("Party Mode %s doesn't exist" % mode)
    number = PARTIES[mode]
    commands = [
     COMMANDS['ON'][group]]
    for i in range(1, number):
        commands.append(COMMANDS['DISCOUP'])

    return tuple(commands)


COMMANDS['PARTY'] = partay
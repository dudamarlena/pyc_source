# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/bashplotlib/utils/helpers.py
# Compiled at: 2015-09-12 14:46:38
"""
Various helpful function for bashplotlib
"""
import sys
isiterable = lambda x: hasattr(x, '__iter__') or hasattr(x, '__getitem__')
bcolours = {'white': '\x1b[97m', 
   'aqua': '\x1b[96m', 
   'pink': '\x1b[95m', 
   'blue': '\x1b[94m', 
   'yellow': '\x1b[93m', 
   'green': '\x1b[92m', 
   'red': '\x1b[91m', 
   'grey': '\x1b[90m', 
   'black': '\x1b[30m', 
   'default': '\x1b[39m', 
   'ENDC': '\x1b[39m'}
colour_help = (', ').join([ colour for colour in bcolours if colour != 'ENDC' ])

def get_colour(colour):
    """
    Get the escape code sequence for a colour
    """
    return bcolours.get(colour, bcolours['ENDC'])


def printcolour(text, sameline=False, colour=get_colour('ENDC')):
    """
    Print color text using escape codes
    """
    if sameline:
        sep = ''
    else:
        sep = '\n'
    sys.stdout.write(get_colour(colour) + text + bcolours['ENDC'] + sep)


def drange(start, stop, step=1.0, include_stop=False):
    """
    Generate between 2 numbers w/ optional step, optionally include upper bound
    """
    if step == 0:
        step = 0.01
    r = start
    if include_stop:
        while r <= stop:
            yield r
            r += step
            r = round(r, 10)

    else:
        while r < stop:
            yield r
            r += step
            r = round(r, 10)


def box_text(text, width, offset=0):
    """
    Return text inside an ascii textbox
    """
    box = ' ' * offset + '-' * (width + 2) + '\n'
    box += ' ' * offset + '|' + text.center(width) + '|' + '\n'
    box += ' ' * offset + '-' * (width + 2)
    return box
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/lib/color.py
# Compiled at: 2011-04-22 06:35:42
colormap = {'white': 0, 
   'black': 1, 
   'navy': 2, 
   'green': 3, 
   'red': 4, 
   'brown': 5, 
   'purple': 6, 
   'orange': 7, 
   'yellow': 8, 
   'light_green': 9, 
   'teal': 10, 
   'cyan': 11, 
   'blue': 12, 
   'pink': 13, 
   'grey': 14, 
   'light_grey': 15}

def filtercolors(input):
    """
        Filters all irc colors out of a given string
    """
    for i in xrange(1, 16):
        input = input.replace(chr(3) + str(i), '')

    return input


def changecolor(fgcolor, bgcolor=None):
    """
        Returns a string that with the current irc color set to something
        different.
        Expects both arguments to be one of the strings defined in colormap:
        "white, black, navy, green, red, brown, purple, orange, yellow,
        light_green, teal, cyan, blue, pink, grey, light_grey"
        The background color is optional
    """
    if fgcolor not in colormap:
        raise ValueError('Unknown foreground color: "' + str(fgcolor) + '"')
    if bgcolor is not None and bgcolor not in colormap:
        raise ValueError('Unknown background color: "' + str(bgcolor) + '"')
    colorstring = chr(3) + str(colormap[fgcolor])
    if bgcolor is not None:
        colorstring += ',' + str(colormap[bgcolor])
    return colorstring


def resetcolors():
    """
        Returns a string that will reset all currently active irc colors.
    """
    return chr(3)
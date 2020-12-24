# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Apps/Whiteboard/Palette.py
# Compiled at: 2008-10-19 12:19:52
from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.Chassis.Graphline import Graphline
colours = {'black': (0, 0, 0), 'red': (192, 0, 0), 
   'orange': (192, 96, 0), 
   'yellow': (160, 160, 0), 
   'green': (0, 192, 0), 
   'turquoise': (0, 160, 160), 
   'blue': (0, 0, 255), 
   'purple': (192, 0, 192), 
   'darkgrey': (96, 96, 96), 
   'lightgrey': (192, 192, 192)}

def buildPalette(cols, order, topleft=(0, 0), size=32):
    buttons = {}
    links = {}
    pos = topleft
    i = 0
    for col in order:
        buttons[col] = Button(caption='', position=pos, size=(size, size), bgcolour=cols[col], msg=cols[col])
        links[(col, 'outbox')] = ('self', 'outbox')
        pos = (pos[0] + size, pos[1])
        i = i + 1

    return Graphline(linkages=links, **buttons)
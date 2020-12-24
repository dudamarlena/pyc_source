# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Apps/Games4Kids/MyGamesEventsComponent.py
# Compiled at: 2008-10-19 12:19:52
from Kamaelia.UI.Pygame.EventHandler import EventHandler
from Axon.Component import component
import pygame
from Kamaelia.UI.Pygame.KeyEvent import KeyEvent

def MyGamesEventsComponent(up='p', down='l', left='a', right='s'):
    if len(left) > 1:
        left = left.upper()
    else:
        left = left.lower()
    if len(right) > 1:
        right = right.upper()
    else:
        right = right.lower()
    if len(up) > 1:
        up = up.upper()
    else:
        up = up.lower()
    if len(down) > 1:
        down = down.upper()
    else:
        down = down.lower()
    return KeyEvent(outboxes={'outbox': 'Normal place for message', 'signal': 'Normal place for message'}, key_events={eval('pygame.K_' + up): ('start_up', 'outbox'), 
       eval('pygame.K_' + down): ('start_down', 'outbox'), 
       eval('pygame.K_' + left): ('start_left', 'outbox'), 
       eval('pygame.K_' + right): ('start_right', 'outbox')}, key_up_events={eval('pygame.K_' + up): ('stop_up', 'outbox'), 
       eval('pygame.K_' + down): ('stop_down', 'outbox'), 
       eval('pygame.K_' + left): ('stop_left', 'outbox'), 
       eval('pygame.K_' + right): ('stop_right', 'outbox')})
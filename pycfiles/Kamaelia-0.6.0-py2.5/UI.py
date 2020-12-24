# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Apps/Whiteboard/UI.py
# Compiled at: 2008-10-19 12:19:52
from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.Chassis.Graphline import Graphline

def PagingControls(left, top):
    return Graphline(PREV=Button(caption='<<', size=(63, 32), position=(
     left, top), msg='prev'), NEXT=Button(caption='>>', size=(63, 32), position=(
     left + 64, top), msg='next'), CHECKPOINT=Button(caption='checkpoint', size=(63,
                                                                                 32), position=(
     left + 128, top), msg='checkpoint'), NEWPAGE=Button(caption='new page', size=(63,
                                                                                   32), position=(
     left + 192, top), msg='new'), linkages={('PREV', 'outbox'): ('', 'outbox'), 
       ('NEXT', 'outbox'): ('', 'outbox'), 
       ('CHECKPOINT', 'outbox'): ('', 'outbox'), 
       ('NEWPAGE', 'outbox'): ('', 'outbox')})


def LocalPagingControls(left, top):
    return Graphline(REMOTEPREV=Button(caption='~~<<~~', size=(63, 32), position=(
     left, top), msg=[
     [
      'prev']]), REMOTENEXT=Button(caption='~~>>~~', size=(63, 32), position=(
     left + 64, top), msg=[
     [
      'next']]), linkages={('REMOTEPREV', 'outbox'): ('', 'outbox'), 
       ('REMOTENEXT', 'outbox'): ('', 'outbox')})


def Eraser(left, top):
    return Button(caption='Eraser', size=(64, 32), position=(left, top))


def ClearPage(left, top):
    return Button(caption='clear', size=(63, 32), position=(left, top), msg=[['clear']])
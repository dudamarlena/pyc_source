# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\研发资料\瓦力课程\试听课\代码\dianyi\events.py
# Compiled at: 2019-08-09 06:19:00
# Size of source mod 2**32: 2494 bytes
from .config import *

def get_mouse_pos():
    return pygame2Cartesian(pygame.mouse.get_pos())


def get_mouse_rel():
    """
    x, y = pygame.mouse.get_rel()
    return vec(x, -y)
    """
    for event in global_var.EVENTS:
        if event.type == MOUSEMOTION:
            x, y = event.rel
            return vec(x, -y)
    else:
        return vec(0, 0)


def get_mouse_clicked():
    for event in global_var.EVENTS:
        if event and event.type == MOUSEBUTTONDOWN:
            global_var.GET_CLICKED = True

    get_mouse_just_released()
    if global_var.GET_CLICKED:
        return True
    else:
        return False


def get_mouse_just_clicked():
    for event in global_var.EVENTS:
        if event:
            if event.type == MOUSEBUTTONDOWN:
                global_var.GET_CLICKED = True
                return True
    else:
        return False


def get_mouse_just_released():
    if global_var.JUST_RELEASED:
        return True
    else:
        get_mouse_just_clicked()
        if global_var.GET_CLICKED:
            for event in global_var.EVENTS:
                if event and event.type == MOUSEBUTTONUP:
                    global_var.GET_CLICKED = False
                    global_var.JUST_RELEASED = True

            if global_var.GET_CLICKED:
                return False
            else:
                return True
        else:
            return False


def key_pressed(key=None):
    if not key:
        if 1 in pygame.key.get_pressed():
            return True
        return False
    else:
        if pygame.key.get_pressed()[key]:
            return True
        return False


def key_just_pressed(*keys):
    keyEvents = []
    for event in global_var.EVENTS:
        if event.type == KEYDOWN:
            keyEvents.append(event.key)

    if not keys:
        return keyEvents
    else:
        for key in keys:
            if key not in keyEvents:
                break
        else:
            return True

        return False


def key_released(*keys):
    keyEvents = []
    for event in global_var.EVENTS:
        if event.type == KEYUP:
            keyEvents.append(event.key)

    if not keys:
        return keyEvents
    else:
        for key in keys:
            if key not in keyEvents:
                break
        else:
            return True

        return False
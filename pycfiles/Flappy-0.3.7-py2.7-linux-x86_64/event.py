# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flappy/events/event.py
# Compiled at: 2014-03-13 10:09:15


class EventPhase(object):
    CAPTURING_PHASE = 0
    AT_TARGET = 1
    BUBBLING_PHASE = 2


class Event(object):
    ACTIVATE = 'activate'
    ADDED = 'added'
    ADDED_TO_STAGE = 'addedToStage'
    CANCEL = 'cancel'
    CHANGE = 'change'
    CLOSE = 'close'
    COMPLETE = 'complete'
    CONNECT = 'connect'
    CONTEXT3D_CREATE = 'context3DCreate'
    DEACTIVATE = 'deactivate'
    ENTER_FRAME = 'enterFrame'
    ID3 = 'id3'
    INIT = 'init'
    OPEN = 'open'
    REMOVED = 'removed'
    REMOVED_FROM_STAGE = 'removedFromStage'
    RENDER = 'render'
    RESIZE = 'resize'
    SCROLL = 'scroll'
    SELECT = 'select'
    SOUND_COMPLETE = 'soundComplete'
    TAB_CHILDREN_CHANGE = 'tabChildrenChange'
    TAB_ENABLED_CHANGE = 'tabEnabledChange'
    TAB_INDEX_CHANGE = 'tabIndexChange'
    UNLOAD = 'unload'

    def __init__(self, etype, bubbles=False, cancelable=False):
        self.type = etype
        self.bubbles = bubbles
        self.cancelable = cancelable
        self.isCancelled = False
        self.isCancelledNow = False
        self.target = None
        self.currentTarget = None
        self.eventPhase = EventPhase.AT_TARGET
        return

    def clone(self):
        return Event(self.type, self.bubbles, self.cancelable)

    def stopImmediatePropagation(self):
        if self.cancelable:
            self.isCancelled = self.isCancelledNow = True

    def stopPropagation(self):
        if self.cancelable:
            self.isCancelled = True

    def __str__(self):
        return '[Event type=%s bubbles=%s cancelable=%s]' % (
         self.type, str(self.bubbles), str(self.cancelable))
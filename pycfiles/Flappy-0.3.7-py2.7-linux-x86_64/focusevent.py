# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flappy/events/focusevent.py
# Compiled at: 2014-03-13 10:09:15
from event import Event

class FocusEvent(Event):
    FOCUS_IN = 'focusIn'
    FOCUS_OUT = 'focusOut'
    KEY_FOCUS_CHANGE = 'keyFocusChange'
    MOUSE_FOCUS_CHANGE = 'mouseFocusChange'

    def __init__(self, etype, bubbles=True, cancelable=False, relatedObject=None, shiftKey=None, keyCode=0, direction='none'):
        Event.__init__(self, etype, bubbles, cancelable)
        self.relatedObject = relatedObject
        self.keyCode = keyCode
        self.shiftKey = shiftKey

    def clone(self):
        return FocusEvent(self.type, self.bubbles, self.cancelable, self.relatedObject, self.shiftKey, self.keyCode)

    def __str__(self):
        s = '[FocusEvent type=%s bubbles=%s cancelable=%srelatedObject=%s shiftKey=%s keyCode=%s]' % (
         self.type, str(self.bubbles), str(self.cancelable),
         str(self.relatedObject), str(self.shiftKey),
         str(self.keyCode))
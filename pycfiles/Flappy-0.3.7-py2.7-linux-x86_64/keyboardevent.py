# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flappy/events/keyboardevent.py
# Compiled at: 2014-03-13 10:09:15
from event import Event

class KeyboardEvent(Event):
    KEY_DOWN = 'keyDown'
    KEY_UP = 'keyUp'

    def __init__(self, etype, bubbles=False, cancelable=False, charCodeValue=0, keyCodeValue=0, keyLocationValue=0, ctrlKeyValue=False, altKeyValue=False, shiftKeyValue=False, controlKeyValue=False, commandKeyValue=False):
        Event.__init__(self, etype, bubbles, cancelable)
        self.keyCode = keyCodeValue
        self.keyLocation = keyLocationValue
        self.charCode = charCodeValue
        self.shiftKey = shiftKeyValue
        self.altKey = altKeyValue
        self.controlKey = controlKeyValue
        self.commandKey = commandKeyValue
        self.ctrlKey = ctrlKeyValue or self.controlKey or self.commandKey

    def clone(self):
        return KeyboardEvent(self.type, self.bubbles, self.cancelable, self.charCode, self.keyCode, self.keyLocation, self.ctrlKey, self.altKey, self.shiftKey, self.controlKey, self.commandKey)

    def __str__(self):
        s = '[KeyboardEvent type=%s bubbles=%s cancelable=%s' % (
         self.type, str(self.bubbles), str(self.cancelable))
        s += 'charCode=%s keyCode=%s keyLocation=%s ' % (
         str(self.charCode), str(self.keyCode), str(self.keyLocation))
        s += 'ctrlKey=%s altKey=%s shiftKey=%s]' % (
         str(self.ctrlKey), str(self.altKey), str(self.shiftKey))
        return s
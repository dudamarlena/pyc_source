# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/gwt/client/mouse_event_details.py
# Compiled at: 2013-04-04 15:36:36
"""Helper class to store and transfer mouse event details."""

class MouseEventDetails(object):
    """Helper class to store and transfer mouse event details."""
    BUTTON_LEFT = 1
    BUTTON_MIDDLE = 4
    BUTTON_RIGHT = 2

    def __init__(self, evt=None, relativeToElement=None):
        self._DELIM = ','
        self._button = None
        self._clientX = None
        self._clientY = None
        self._altKey = None
        self._ctrlKey = None
        self._metaKey = None
        self._shiftKey = None
        self._type = None
        self._relativeX = -1
        self._relativeY = -1
        if evt is None:
            pass
        elif relativeToElement is None:
            MouseEventDetails.__init__(self, evt, None)
        else:
            raise NotImplementedError
            self._button = evt.getButton()
            self._altKey = evt.getAltKey()
            self._ctrlKey = evt.getCtrlKey()
            self._metaKey = evt.getMetaKey()
            self._shiftKey = evt.getShiftKey()
            if relativeToElement is not None:
                self._relativeX = self.getRelativeX(self._clientX, relativeToElement)
                self._relativeY = self.getRelativeY(self._clientY, relativeToElement)
        return

    def __str__(self):
        return self.serialize()

    def serialize(self):
        return self._button + self._DELIM + self._clientX + self._DELIM + self._clientY + self._DELIM + str(self._altKey).lower() + self._DELIM + str(self._ctrlKey).lower() + self._DELIM + str(self._metaKey).lower() + self._DELIM + str(self._shiftKey).lower() + self._DELIM + self._type + self._DELIM + self._relativeX + self._DELIM + self._relativeY

    @classmethod
    def deSerialize(cls, serializedString):
        instance = MouseEventDetails()
        fields = serializedString.split(',')
        instance._button = int(fields[0])
        instance._clientX = int(fields[1])
        instance._clientY = int(fields[2])
        instance._altKey = fields[3].lower() == 'true'
        instance._ctrlKey = fields[4].lower() == 'true'
        instance._metaKey = fields[5].lower() == 'true'
        instance._shiftKey = fields[6].lower() == 'true'
        instance._type = int(fields[7])
        instance._relativeX = int(fields[8])
        instance._relativeY = int(fields[9])
        return instance

    def getButtonName(self):
        if self._button == self.BUTTON_LEFT:
            return 'left'
        if self._button == self.BUTTON_RIGHT:
            return 'right'
        if self._button == self.BUTTON_MIDDLE:
            return 'middle'
        return ''

    def getRelativeX(self, clientX=None, target=None):
        if clientX is None:
            return self._relativeX
        else:
            return clientX - target.getAbsoluteLeft() + target.getScrollLeft() + target.getOwnerDocument().getScrollLeft()
            return

    def getRelativeY(self, clientY=None, target=None):
        if clientY is None:
            return self._relativeY
        else:
            return clientY - target.getAbsoluteTop() + target.getScrollTop() + target.getOwnerDocument().getScrollTop()
            return

    def getType(self):
        return MouseEventDetails

    def isDoubleClick(self):
        return self._type == 2

    def getButton(self):
        return self._button

    def getClientX(self):
        return self._clientX

    def getClientY(self):
        return self._clientY

    def isAltKey(self):
        return self._altKey

    def isCtrlKey(self):
        return self._ctrlKey

    def isMetaKey(self):
        return self._metaKey

    def isShiftKey(self):
        return self._shiftKey
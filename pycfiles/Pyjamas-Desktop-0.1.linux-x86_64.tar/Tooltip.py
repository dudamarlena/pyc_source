# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjamas/Tooltip.py
# Compiled at: 2008-09-03 09:02:13
from ui import PopupPanel, HTML, RootPanel
from Timer import Timer
tooltip_hide_timer = None

class Tooltip(PopupPanel):

    def __init__(self, sender, offsetX, offsetY, text, show_delay, hide_delay, styleName):
        global tooltip_hide_timer
        PopupPanel.__init__(self, True)
        self.show_delay = show_delay
        self.hide_delay = hide_delay
        contents = HTML(text)
        self.add(contents)
        left = sender.getAbsoluteLeft() + offsetX
        top = sender.getAbsoluteTop() + offsetY
        self.setPopupPosition(left, top)
        self.setStyleName(styleName)
        if tooltip_hide_timer:
            self.tooltip_show_timer = Timer(1, self)
        else:
            self.tooltip_show_timer = Timer(self.show_delay, self)

    def show(self):
        global tooltip_hide_timer
        tooltip_hide_timer = Timer(self.hide_delay, self)
        PopupPanel.show(self)

    def hide(self):
        self.tooltip_show_timer.cancel()
        PopupPanel.hide(self)

    def onTimer(self, id):
        global tooltip_hide_timer
        if tooltip_hide_timer and id == tooltip_hide_timer.getID():
            tooltip_hide_timer = None
        if id == self.tooltip_show_timer.getID():
            self.show()
        else:
            self.hide()
        return


class TooltipListener:
    DEFAULT_TOOLTIP_STYLE = 'TooltipPopup'
    DEFAULT_OFFSET_X = 10
    DEFAULT_OFFSET_Y = 35

    def __init__(self, text, show_delay=1000, hide_delay=5000, styleName=''):
        if not styleName:
            styleName = TooltipListener.DEFAULT_TOOLTIP_STYLE
        self.tooltip = None
        self.text = text
        self.styleName = styleName
        self.show_delay = show_delay
        self.hide_delay = hide_delay
        self.offsetX = TooltipListener.DEFAULT_OFFSET_X
        self.offsetY = TooltipListener.DEFAULT_OFFSET_Y
        return

    def onMouseEnter(self, sender):
        if self.tooltip != None:
            self.tooltip.hide()
        self.tooltip = Tooltip(sender, self.offsetX, self.offsetY, self.text, self.show_delay, self.hide_delay, self.styleName)
        return

    def onMouseLeave(self, sender):
        if self.tooltip != None:
            self.tooltip.hide()
        return

    def onMouseMove(self, sender, x, y):
        pass

    def onMouseDown(self, sender, x, y):
        pass

    def onMouseUp(self, sender, x, y):
        pass

    def getStyleName(self):
        return self.styleName

    def setStyleName(self, styleName):
        self.styleName = styleName

    def getOffsetX(self):
        return self.offsetX

    def setOffsetX(self, offsetX):
        self.offsetX = offsetX

    def getOffsetY(self):
        return self.offsetY

    def setOffsetY(self, offsetY):
        self.offsetY = offsetY
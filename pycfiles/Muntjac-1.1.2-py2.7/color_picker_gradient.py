# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/addon/colorpicker/color_picker_gradient.py
# Compiled at: 2013-04-04 15:36:36
from muntjac.ui.abstract_component import AbstractComponent
from muntjac.addon.colorpicker.color_change_event import ColorChangeEvent
from muntjac.addon.colorpicker.color_picker import IColorChangeListener
from muntjac.addon.colorpicker.color_selector import IColorSelector
_COLOR_CHANGE_METHOD = getattr(IColorChangeListener, 'colorChanged')

class ColorPickerGradient(AbstractComponent, IColorSelector):
    """The Class ColorPickerGradient.

    @author: John Ahlroos
    @author: Richard Lincoln
    """
    CLIENT_WIDGET = None
    TYPE_MAPPING = 'com.vaadin.addon.colorpicker.ColorPickerGradient'

    def __init__(self, Id, converter):
        """Instantiates a new color picker gradient.

        @param id:
                   the id
        @param converter:
                   the converter
        """
        super(ColorPickerGradient, self).__init__()
        self._id = Id
        self._converter = converter
        self._color = None
        self._x = 0
        self._y = 0
        self._backgroundColor = None
        self.requestRepaint()
        return

    def setColor(self, c):
        self._color = c
        coords = self._converter.calculate(c)
        self._x = coords[0]
        self._y = coords[1]
        self.requestRepaint()

    def paintContent(self, target):
        target.addAttribute('cssid', self._id)
        if self._color is not None:
            target.addAttribute('cursorX', self._x)
            target.addAttribute('cursorY', self._y)
        if self._backgroundColor is not None:
            bgRed = '%.2x' % self._backgroundColor.getRed()
            bgGreen = '%.2x' % self._backgroundColor.getGreen()
            bgBlue = '%.2x' % self._backgroundColor.getBlue()
            target.addAttribute('bgColor', '#' + bgRed + bgGreen + bgBlue)
        return

    def changeVariables(self, source, variables):
        if 'cursorX' in variables and 'cursorY' in variables:
            self._x = variables['cursorX']
            self._y = variables['cursorY']
            self._color = self._converter.calculate(self._x, self._y)
            self.fireColorChanged(self._color)

    def addListener(self, listener, iface=None):
        if isinstance(listener, IColorChangeListener) and (iface is None or issubclass(iface, IColorChangeListener)):
            self.registerListener(ColorChangeEvent, listener, _COLOR_CHANGE_METHOD)
        super(ColorPickerGradient, self).addListener(listener, iface)
        return

    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, ColorChangeEvent):
            self.registerCallback(ColorChangeEvent, callback, None, *args)
        else:
            super(ColorPickerGradient, self).addCallback(callback, eventType, *args)
        return

    def removeListener(self, listener, iface=None):
        if isinstance(listener, IColorChangeListener) and (iface is None or issubclass(iface, IColorChangeListener)):
            self.withdrawListener(ColorChangeEvent, listener)
        super(ColorPickerGradient, self).removeListener(listener, iface)
        return

    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, ColorChangeEvent):
            self.withdrawCallback(ColorChangeEvent, callback)
        else:
            super(ColorPickerGradient, self).removeCallback(callback, eventType)
        return

    def setBackgroundColor(self, color):
        """Sets the background color.

        @param color:
                   the new background color
        """
        self._backgroundColor = color
        self.requestRepaint()

    def getColor(self):
        return self._color

    def fireColorChanged(self, color):
        """Notifies the listeners that the color has changed

        @param color:
                   The color which it changed to
        """
        self.fireEvent(ColorChangeEvent(self, color))
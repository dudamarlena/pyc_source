# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/addon/colorpicker/color_picker_preview.py
# Compiled at: 2013-04-04 15:36:36
from muntjac.addon.colorpicker.color import Color
from muntjac.ui.css_layout import CssLayout
from muntjac.ui.text_field import TextField
from muntjac.data.property import IValueChangeListener
from muntjac.addon.colorpicker.color_change_event import ColorChangeEvent
from muntjac.addon.colorpicker.color_picker import IColorChangeListener
from muntjac.addon.colorpicker.color_selector import IColorSelector
from muntjac.data.validators.regexp_validator import RegexpValidator
_COLOR_CHANGE_METHOD = getattr(IColorChangeListener, 'colorChanged')

class ColorPickerPreview(CssLayout, IColorSelector, IValueChangeListener):
    """The Class ColorPickerPreview.

    @author: John Ahlroos / ITMill Oy 2010
    @author: Richard Lincoln
    """
    _STYLE_DARK_COLOR = 'v-textfield-dark'
    _STYLE_LIGHT_COLOR = 'v-textfield-light'

    def __init__(self, color):
        """Instantiates a new color picker preview."""
        super(ColorPickerPreview, self).__init__()
        self.setStyleName('v-colorpicker-preview')
        self.setImmediate(True)
        self._color = color
        self._field = TextField()
        self._field.setReadOnly(True)
        self._field.setImmediate(True)
        self._field.setSizeFull()
        self._field.setStyleName('v-colorpicker-preview-textfield')
        self._field.setData(self)
        self._field.addListener(self, IValueChangeListener)
        self._field.addValidator(RegexpValidator('#[0-9a-fA-F]{6}', True, ''))
        self._oldValue = None
        self.addComponent(self._field)
        self.setColor(color)
        return

    def setColor(self, color):
        self._color = color
        red = '%.2x' % color.getRed()
        green = '%.2x' % color.getGreen()
        blue = '%.2x' % color.getBlue()
        self._field.removeListener(self, IValueChangeListener)
        self._field.setReadOnly(False)
        self._field.setValue('#' + red + green + blue)
        if self._field.isValid():
            self._oldValue = '#' + red + green + blue
        else:
            self._field.setValue(self._oldValue)
        self._field.setReadOnly(True)
        self._field.addListener(self, IValueChangeListener)
        self._field.removeStyleName(self._STYLE_DARK_COLOR)
        self._field.removeStyleName(self._STYLE_LIGHT_COLOR)
        if self._color.getRed() + self._color.getGreen() + self._color.getBlue() < 384:
            self._field.addStyleName(self._STYLE_DARK_COLOR)
        else:
            self._field.addStyleName(self._STYLE_LIGHT_COLOR)
        self.requestRepaint()

    def getColor(self):
        return self._color

    def addListener(self, listener, iface=None):
        """Adds a color change listener

        @param listener:
                   The color change listener
        """
        if isinstance(listener, IColorChangeListener) and (iface is None or issubclass(iface, IColorChangeListener)):
            self.registerListener(ColorChangeEvent, listener, _COLOR_CHANGE_METHOD)
        super(ColorPickerPreview, self).addListener(listener, iface)
        return

    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, ColorChangeEvent):
            self.registerCallback(ColorChangeEvent, callback, None, *args)
        else:
            super(ColorPickerPreview, self).addCallback(callback, eventType, *args)
        return

    def removeListener(self, listener, iface=None):
        """Removes a color change listener

        @param listener:
                   The listener
        """
        if isinstance(listener, IColorChangeListener) and (iface is None or issubclass(iface, IColorChangeListener)):
            self.withdrawListener(ColorChangeEvent, listener)
        super(ColorPickerPreview, self).removeListener(listener, iface)
        return

    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, ColorChangeEvent):
            self.withdrawCallback(ColorChangeEvent, callback)
        else:
            super(ColorPickerPreview, self).removeCallback(callback, eventType)
        return

    def valueChange(self, event):
        value = event.getProperty().getValue()
        if not self._field.isValid():
            self._field.setValue(self._oldValue)
            return
        else:
            self._oldValue = value
            if value is not None and len(value) == 7:
                red = int(value[1:3], 16)
                green = int(value[3:5], 16)
                blue = int(value[5:7], 16)
                self._color = Color(red, green, blue)
                evt = ColorChangeEvent(self._field.getData(), self._color)
                self.fireEvent(evt)
            return

    def getCss(self, c):
        """Called when the component is refreshing"""
        red = '%.2x' % self._color.getRed()
        green = '%.2x' % self._color.getGreen()
        blue = '%.2x' % self._color.getBlue()
        css = 'background: #' + red + green + blue
        return css
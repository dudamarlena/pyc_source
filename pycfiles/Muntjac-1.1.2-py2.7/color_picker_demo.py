# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/addon/colorpicker/color_picker_demo.py
# Compiled at: 2013-04-04 15:36:36
from muntjac.api import Application, Window, Label
from muntjac.addon.colorpicker.color import Color
from muntjac.addon.colorpicker.color_picker import ColorPicker

class ColorPickerDemo(Application):

    def init(self):
        mainWindow = Window('Color Picker Demo Application')
        label = Label('Hello Muntjac user')
        mainWindow.addComponent(label)
        self.setMainWindow(mainWindow)
        cp = ColorPicker('Our ColorPicker', Color.RED)
        mainWindow.addComponent(cp)
        cp.setButtonCaption('Our color')

    def colorChanged(self, event):
        self.getMainWindow().showNotification('Color changed!')


if __name__ == '__main__':
    from muntjac.main import muntjac
    muntjac(ColorPickerDemo, nogui=True, forever=True, debug=True)
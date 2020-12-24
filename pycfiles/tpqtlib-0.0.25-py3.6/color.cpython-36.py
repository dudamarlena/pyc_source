# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpQtLib/widgets/color.py
# Compiled at: 2020-01-16 21:52:29
# Size of source mod 2**32: 4504 bytes
"""
Module that contains widgets for colors
"""
from __future__ import print_function, division, absolute_import
from functools import partial
from Qt.QtCore import *
from Qt.QtWidgets import *
from Qt.QtGui import *
from tpQtLib.core import color as core_color

class ColorButton(QPushButton, object):

    def __init__(self, *args, **kwargs):
        (super(ColorButton, self).__init__)(*args, **kwargs)


class ColorPicker(QFrame, object):
    COLOR_BUTTON_CLASS = ColorButton
    colorChanged = Signal(object)

    def __init__(self, *args):
        (super(ColorPicker, self).__init__)(*args)
        self._buttons = list()
        self._current_color = None
        self._browser_colors = None
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

    def current_color(self):
        """
        Returns the current color
        :return: QColor
        """
        return self._current_color

    def set_current_color(self, color):
        """
        Sets the current color
        :param color: QColor
        """
        self._current_color = color

    def browser_colors(self):
        """
        Returns the colors to be displayed in the browser
        :return: list(Color)
        """
        return self._browser_colors

    def set_browser_colors(self, colors):
        """
        Sets the colors to be displayed in the browser
        :param colors: list(Color)
        """
        self._browser_colors = colors

    def delete_buttons(self):
        """
        Deletes all color buttons
        """
        layout = self.layout()
        while layout.count():
            item = layout.takeAt(0)
            item.widget().deleteLater()

    def set_colors(self, colors):
        """
        Sets the colors for the color bar
        :param colors: list(str) or list(Color)
        """
        self.delete_buttons()
        first = True
        last = False
        for i, color in enumerate(colors):
            if i == len(colors) - 1:
                last = True
            if not isinstance(color, str):
                color = core_color.Color(color)
                color = color.to_string()
            callback = partial(self._on_color_changed, color)
            css = 'background-color: {}'.format(color)
            btn = self.COLOR_BUTTON_CLASS(self)
            btn.setObjectName('colorButton')
            btn.setStyleSheet(css)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            btn.setProperty('first', first)
            btn.setProperty('last', last)
            btn.clicked.connect(callback)
            self.layout().addWidget(btn)
            first = False

        browse_btn = QPushButton('...', self)
        browse_btn.setObjectName('menuButton')
        browse_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        browse_btn.clicked.connect(self._on_browse_color)
        self.layout().addWidget(browse_btn)

    def _on_browse_color(self):
        """
        Internal callback function that is triggered when the user clicks on browse button
        """
        current_color = self.current_color()
        d = QColorDialog(self)
        d.setCurrentColor(current_color)
        standard_colors = self.browser_colors()
        if standard_colors:
            index = -1
            for standard_color in standard_colors:
                index += 1
                try:
                    standard_color = QColor(standard_color)
                    d.setStandardColor(index, standard_color)
                except Exception:
                    standard_color = QColor(standard_color).rgba()
                    d.setStandardColor(index, standard_color)

        else:
            d.currentColorChanged.connect(self._on_color_changed)
            if d.exec_():
                self._on_color_changed(d.selectedColor())
            else:
                self._on_color_changed(current_color)

    def _on_color_changed(self, color):
        """
        Internal callback function that is triggered when the user clcks or browse for a color
        :param color: QColor
        """
        self._current_color = color
        self.colorChanged.emit(color)

    @Slot()
    def blandSlot(self):
        """
        Blank slot to fix issue with PySide2.QColorDialog.open()
        """
        pass
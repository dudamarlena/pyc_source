# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/stareditor.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from customeditor import CustomEditor
from camelot.view.art import Icon

class StarEditor(CustomEditor):
    star_icon = Icon('tango/16x16/status/weather-clear.png')
    no_star_icon = Icon('tango/16x16/status/weather-clear-noStar.png')

    def __init__(self, parent, maximum=5, editable=True, field_name='star', **kwargs):
        CustomEditor.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        self.setObjectName(field_name)
        self.setFocusPolicy(Qt.StrongFocus)
        layout = QtGui.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.maximum = maximum
        self.buttons = []
        for i in range(self.maximum):
            button = QtGui.QToolButton(self)
            button.setIcon(self.no_star_icon.getQIcon())
            button.setFocusPolicy(Qt.ClickFocus)
            if editable:
                button.setAutoRaise(True)
            else:
                button.setAutoRaise(True)
                button.setDisabled(True)
            button.setFixedHeight(self.get_height())
            self.buttons.append(button)

        def createStarClick(i):
            return lambda : self.starClick(i + 1)

        for i in range(self.maximum):
            self.buttons[i].clicked.connect(createStarClick(i))

        for i in range(self.maximum):
            layout.addWidget(self.buttons[i])

        layout.addStretch()
        self.setLayout(layout)

    def get_value(self):
        return CustomEditor.get_value(self) or self.stars

    def set_enabled(self, editable=True):
        for button in self.buttons:
            button.setEnabled(editable)
            button.update()

        self.set_value(self.stars)

    def starClick(self, value):
        if self.stars == value:
            self.stars -= 1
        else:
            self.stars = int(value)
        for i in range(self.maximum):
            if i + 1 <= self.stars:
                self.buttons[i].setIcon(self.star_icon.getQIcon())
            else:
                self.buttons[i].setIcon(self.no_star_icon.getQIcon())

        self.editingFinished.emit()

    def set_value(self, value):
        value = CustomEditor.set_value(self, value) or 0
        self.stars = int(value)
        for i in range(self.maximum):
            if i + 1 <= self.stars:
                self.buttons[i].setIcon(self.star_icon.getQIcon())
            else:
                self.buttons[i].setIcon(self.no_star_icon.getQIcon())

    def set_background_color(self, background_color):
        return False
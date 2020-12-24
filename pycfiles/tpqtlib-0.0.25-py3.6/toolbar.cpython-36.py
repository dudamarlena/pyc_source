# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpQtLib/widgets/toolbar.py
# Compiled at: 2020-01-16 21:52:29
# Size of source mod 2**32: 4933 bytes
"""
Module that contains classes that extend QToolBar functionality
"""
from __future__ import print_function, division, absolute_import
from Qt.QtCore import *
from Qt.QtWidgets import *
from tpQtLib.core import icon

class ToolBar(QToolBar, object):
    __doc__ = '\n    Class that adds functionality to expand/collapse QToolBars\n    '
    DEFAULT_EXPANDED_HEIGHT = 34
    DEFAULT_COLLAPSED_HEIGHT = 10

    def __init__(self, *args):
        (super(ToolBar, self).__init__)(*args)
        self._is_expanded = True
        self._expanded_height = self.DEFAULT_EXPANDED_HEIGHT
        self._collapsed_height = self.DEFAULT_COLLAPSED_HEIGHT

    def mousePressEvent(self, event):
        if not self.is_expanded():
            self.expand()

    def setFixedHeight(self, value):
        self.set_children_height(value)
        super(QToolBar, self).setFixedHeight(value)

    def insertAction(self, before, action):
        action.setParent(self)
        if isinstance(before, (unicode, str)):
            before = self.find_action(before)
        action = super(ToolBar, self).insertAction(before, action)
        return action

    def actions(self):
        """
        Overrides base QToolBar actions function
        Returns all the widgets that are a child of the menu bar widget
        :return: list(QWidget)
        """
        widgets = list()
        for i in range(self.layout().count()):
            w = self.layout().itemAt(i).widget()
            if isinstance(w, QWidget):
                widgets.append(w)

        return widgets

    def widgets(self):
        """
        Returns all the widgets that are a child of the menu bar widget
        :return: list(QWidget)
        """
        widgets = list()
        for i in range(self.layout().count()):
            w = self.layout().itemAt(i).widget()
            if isinstance(w, QWidget):
                widgets.append(w)

        return widgets

    def is_expanded(self):
        """
        Returns whether the menu bar is expanded or not
        :return: bool
        """
        return self._is_expanded

    def expand_height(self):
        """
        Returns the height of menu bar when is expanded
        :return: float
        """
        return self._expanded_height

    def collapse_height(self):
        """
        Returns the height of widget when collapsed
        :return: int
        """
        return self._collapsed_height

    def set_children_hidden(self, flag):
        """
        Hide/Show all child widgets
        :param flag: bool
        """
        for w in self.widgets():
            w.setHidden(flag)

    def set_children_height(self, height):
        """
        Set the height of all the child widgets to the given height
        :param height: int
        """
        for w in self.widgets():
            w.setFixedHeight(height)

    def expand(self):
        """
        Expand the menu bar to the expand height
        """
        self._is_expanded = True
        height = self.expand_height()
        self.setFixedHeight(height)
        self.set_children_hidden(False)
        self.setIconSize(QSize(height, height))

    def collapse(self):
        """
        Collapse the menu bar to the collapse height
        """
        self._is_expanded = False
        height = self.collapse_height()
        self.setFixedHeight(height)
        self.set_children_height(0)
        self.set_children_hidden(True)
        self.setIconSize(QSize(0, 0))

    def set_icon_color(self, color):
        """
        Set the icon colors to the current foregroundRole
        :param color: QColor
        """
        for action in self.actions():
            action_icon = action.icon()
            action_icon = icon.Icon(action_icon)
            action_icon.set_color(color)
            action.setIcon(action_icon)

    def find_action(self, text):
        """
        Find the action with the given text
        :param text: str
        :return: QAction or None
        """
        for child in self.children():
            if isinstance(child, QAction):
                if child.text() == text:
                    return child

    def find_tool_button(self, text):
        """
        Find the QToolButton with the given text
        :param text: str
        :return: QToolButton or None
        """
        for child in self.children():
            if isinstance(child, QAction):
                if child.text() == text:
                    return self.widgetForAction(child)
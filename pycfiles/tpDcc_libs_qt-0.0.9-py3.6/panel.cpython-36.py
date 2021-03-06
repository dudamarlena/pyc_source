# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/widgets/panel.py
# Compiled at: 2020-04-24 23:12:07
# Size of source mod 2**32: 8657 bytes
"""
Module that contains implementation for panel widgets
"""
from __future__ import print_function, division, absolute_import
from Qt.QtCore import *
from Qt.QtWidgets import *
import tpDcc as tp
from tpDcc.libs.qt.core import base
from tpDcc.libs.qt.widgets import label, buttons, dividers

class SliderPanelPositions(object):
    LEFT = 'left'
    RIGHT = 'right'
    TOP = 'top'
    BOTTOM = 'bottom'


class SliderPanel(base.BaseWidget, object):
    __doc__ = '\n    Panel that slides in from the edge of the window\n    '
    closed = Signal()

    def __init__(self, title, position=SliderPanelPositions.RIGHT, closable=True, parent=None):
        self._title = title
        self._position = position
        self._closable = closable
        self._is_first_close = True
        super(SliderPanel, self).__init__(parent)
        self.setObjectName('sliderPanel')
        self.setWindowFlags(Qt.Popup)
        self.setAttribute(Qt.WA_StyledBackground)
        self._close_timer = QTimer(self)
        self._close_timer.setInterval(300)
        self._close_timer.setSingleShot(True)
        self._close_timer.timeout.connect(self.close)
        self._close_timer.timeout.connect(self.closed.emit)
        self._pos_anim = QPropertyAnimation(self)
        self._pos_anim.setTargetObject(self)
        self._pos_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._pos_anim.setDuration(300)
        self._pos_anim.setPropertyName('pos')
        self._opacity_anim = QPropertyAnimation()
        self._opacity_anim.setTargetObject(self)
        self._opacity_anim.setDuration(300)
        self._opacity_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._opacity_anim.setPropertyName('windowOpacity')
        self._opacity_anim.setStartValue(0.0)
        self._opacity_anim.setEndValue(1.0)

    @property
    def position(self):
        """
        Returns the placement of the panel in parent window
        :return: str
        """
        return self._position

    @position.setter
    def position(self, value):
        """
        Sets the position of the panel in parent window ('top', 'right', 'bottom' or 'left').
        :param value: str
        """
        self._position = value
        if value in [SliderPanelPositions.BOTTOM, SliderPanelPositions.TOP]:
            self.setFixedHeight(200)
        else:
            self.setFixedWidth(200)

    def ui(self):
        super(SliderPanel, self).ui()
        self._title_label = label.BaseLabel(parent=self).h4()
        self._title_label.setText(self._title)
        self._close_btn = buttons.BaseToolButton(parent=self).icon_only().image('close', theme='window').small()
        self._close_btn.setVisible(self._closable or False)
        title_layout = QHBoxLayout()
        title_layout.addWidget(self._title_label)
        title_layout.addStretch()
        title_layout.addWidget(self._close_btn)
        self._button_layout = QHBoxLayout()
        self._button_layout.addStretch()
        self._scroll_area = QScrollArea()
        self.main_layout.addLayout(title_layout)
        self.main_layout.addWidget(dividers.Divider())
        self.main_layout.addWidget(self._scroll_area)
        self.main_layout.addWidget(dividers.Divider())
        self.main_layout.addLayout(self._button_layout)

    def setup_signals(self):
        self._close_btn.clicked.connect(self.close)

    def show(self):
        self._update_position()
        self._fade_in()
        return super(SliderPanel, self).show()

    def closeEvent(self, event):
        if self._is_first_close:
            self._is_first_close = False
            self._close_timer.stop()
            self._fade_out()
            event.ignore()
        else:
            event.accept()

    def set_widget(self, widget):
        """
        Sets the widget that will be contained inside the panel
        :param widget: QWidget
        """
        self._scroll_area.setWidget(widget)

    def add_button(self, button):
        """
        Adds a new button to the bottom part of the panel
        :param button: QPushButton
        """
        self._button_layout.addWidget(button)

    def left(self):
        """
        Sets the panel's placement to left
        :return: SliderPanel
        """
        self.position = SliderPanelPositions.LEFT
        return self

    def right(self):
        """
        Sets the panel's placement to right
        :return: SliderPanel
        """
        self.position = SliderPanelPositions.RIGHT
        return self

    def top(self):
        """
        Sets the panel's placement to top
        :return: SliderPanel
        """
        self.position = SliderPanelPositions.TOP
        return self

    def bottom(self):
        """
        Sets the panel's placement to bottom
        :return: SliderPanel
        """
        self.position = SliderPanelPositions.BOTTOM
        return self

    def _fade_in(self):
        """
        Internal function that fades in the panel
        """
        self._pos_anim.start()
        self._opacity_anim.start()

    def _fade_out(self):
        """
        Internal function that fades out the panel
        """
        self._pos_anim.setDirection(QAbstractAnimation.Backward)
        self._pos_anim.start()
        self._opacity_anim.setDirection(QAbstractAnimation.Backward)
        self._opacity_anim.start()

    def _update_position(self):
        """
        Internal function that makes sure that panel is positioned in the proper place
        """
        parent = self.parent()
        parent_parent = parent.parent()
        dcc_win = tp.Dcc.get_main_window()
        dcc_window = parent_parent == dcc_win
        if parent_parent:
            dcc_window = dcc_window or parent_parent.objectName() == dcc_win.objectName()
        parent_geo = parent.geometry()
        if self._position == SliderPanelPositions.LEFT:
            pos = parent_geo.topLeft() if dcc_window else parent.mapToGlobal(parent_geo.topLeft())
            target_x = pos.x()
            target_y = pos.y()
            self.setFixedHeight(parent_geo.height())
            self._pos_anim.setStartValue(QPoint(target_x - self.width(), target_y))
            self._pos_anim.setEndValue(QPoint(target_x, target_y))
        if self._position == SliderPanelPositions.RIGHT:
            pos = parent_geo.topRight() if dcc_window else parent.mapToGlobal(parent_geo.topRight())
            self.setFixedHeight(parent_geo.height())
            target_x = pos.x() - self.width()
            target_y = pos.y()
            self._pos_anim.setStartValue(QPoint(target_x + self.width(), target_y))
            self._pos_anim.setEndValue(QPoint(target_x, target_y))
        if self._position == SliderPanelPositions.TOP:
            pos = parent_geo.topLeft() if dcc_window or parent_parent is None else parent.mapToGlobal(parent_geo.topLeft())
            self.setFixedWidth(parent_geo.width())
            target_x = pos.x()
            target_y = pos.y()
            self._pos_anim.setStartValue(QPoint(target_x, target_y - self.height()))
            self._pos_anim.setEndValue(QPoint(target_x, target_y))
        if self._position == SliderPanelPositions.BOTTOM:
            pos = parent_geo.bottomLeft() if dcc_window else parent.mapToGlobal(parent_geo.bottomLeft())
            self.setFixedWidth(parent_geo.width())
            target_x = pos.x()
            target_y = pos.y() - self.height()
            self._pos_anim.setStartValue(QPoint(target_x, target_y + self.height()))
            self._pos_anim.setEndValue(QPoint(target_x, target_y))
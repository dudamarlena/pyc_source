# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/widgets/toast.py
# Compiled at: 2020-04-15 12:12:43
# Size of source mod 2**32: 3644 bytes
"""
Module that contains toast widget implementation
"""
from __future__ import print_function, division, absolute_import
from Qt.QtCore import *
from Qt.QtWidgets import *
from Qt.QtGui import *
from tpDcc.libs.qt.core import animation

class ToastWidget(QLabel, object):
    __doc__ = '\n    Toast widget used to show quick messages to user\n    '
    DEFAULT_DURATION = 500
    DEFAULT_PADDING = 30

    def __init__(self, *args):
        (super(ToastWidget, self).__init__)(*args)
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._on_fade_out)
        self._duration = self.DEFAULT_DURATION
        self.setMouseTracking(True)
        self.setAlignment(Qt.AlignCenter)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        if self.parent():
            self.parent().installEventFilter(self)

    def updateGeometry(self):
        """
        Overrides base QLabel updateGeometry function
        Updates and aligns the geometry to the parent widget
        """
        padding = self.DEFAULT_PADDING
        widget = self.parent()
        width = self.text_width() + padding
        height = self.text_height() + padding
        x = widget.width() * 0.5 - width * 0.5
        y = (widget.height() - height) / 1.2
        self.setGeometry(x, y, width, height)

    def setText(self, *args, **kwargs):
        (super(ToastWidget, self).setText)(*args, **kwargs)
        self.updateGeometry()

    def show(self):
        duration = self.duration()
        self._timer.stop()
        self._timer.start(duration)
        if not self.isVisible():
            animation.fade_in_widget(self, duration=0)
            super(ToastWidget, self).show()

    def duration(self):
        """
        Returns duration
        :return: int
        """
        return self._duration

    def set_duration(self, duration):
        """
        Sets how long to show the toast (in milliseconds)
        :param duration: int
        """
        self._duration = duration

    def text_rect(self):
        """
        Returns the bounding box rect for the text
        :return: QRect
        """
        text = self.text()
        font = self.font()
        metrics = QFontMetricsF(font)
        return metrics.boundingRect(text)

    def text_width(self):
        """
        Returns the width of the text
        :return: int
        """
        text_width = self.text_rect().width()
        return max(0, text_width)

    def text_height(self):
        """
        Returns the height of the text
        :return: int
        """
        text_height = self.text_rect().height()
        return max(0, text_height)

    def _on_fade_out(self, duration=250):
        """
        Internal callback function that fades out the toast message
        :param duration: int
        """
        animation.fade_out_widget(self, duration=duration, on_finished=(self.hide))
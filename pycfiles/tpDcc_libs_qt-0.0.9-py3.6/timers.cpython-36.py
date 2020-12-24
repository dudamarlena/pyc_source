# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/core/timers.py
# Compiled at: 2020-04-24 23:12:07
# Size of source mod 2**32: 1603 bytes
"""
Module that contains different types of Qt timers
"""
from __future__ import print_function, division, absolute_import
from Qt.QtCore import *

class ClickTimer(QObject, object):
    EXECUTE = Signal()

    def __init__(self):
        super(ClickTimer, self).__init__()
        self.timer_id = None
        self.init_data()

    def set_data(self, button, modifier, pos, selected):
        self.button = button
        self.modifier = modifier
        self.pos = pos
        self.isSelected = selected

    def init_data(self):
        self.button = None
        self.modifier = None
        self.pos = None
        self.isSelected = False

    def start(self, interval):
        self.timer_id = self.startTimer(interval)

    def remove_timer(self):
        if self.timer_id:
            self.killTimer(self.timer_id)
        self.timer_id = None

    def timerEvent(self, event):
        if self.timer_id == event.timerId():
            self.EXECUTE.emit()
        self.remove_timer()


def defer(delay, fn, default_delay=1):
    """
    Append artificial delay to `func`
    This aids in keeping the GUI responsive, but complicates logic
    when producing tests. To combat this, the environment variable ensures
    that every operation is synchronous.
    :param delay: float, Delay multiplier; default 1, 0 means no delay
    :param fn: callable, Any callable
    :param default_delay: float
    """
    delay *= float(default_delay)
    if delay > 0:
        return QTimer.singleShot(delay, fn)
    else:
        return fn()
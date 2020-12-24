# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/busy_widget.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from camelot.view.art import Pixmap
from camelot.view.model_thread import get_model_thread
working_pixmap = Pixmap('tango/32x32/animations/process-working.png')

class BusyWidget(QtGui.QLabel):
    """A widget indicating the application is performing some background task.
    The widget acts as an overlay of its parent widget and displays animating
    orbs"""

    def __init__(self, parent=None):
        super(BusyWidget, self).__init__(parent)
        palette = QtGui.QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        pixmap = working_pixmap.getQPixmap()
        rows = 4
        self.cols = 8
        self.frame_height = pixmap.height() / rows
        self.frame_width = pixmap.width() / self.cols
        self.orbs = rows * self.cols
        self.highlighted_orb = 0
        self.timer = None
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        mt = get_model_thread()
        mt.thread_busy_signal.connect(self.set_busy)
        self.set_busy(mt.busy())
        return

    @QtCore.pyqtSlot(bool)
    def set_busy(self, busy_state):
        """start/stop the animation
        :arg busy_state: True or False
        """
        if busy_state and self.timer == None:
            self.timer = self.startTimer(200)
        else:
            if self.timer:
                self.killTimer(self.timer)
                self.timer = None
            self.highlighted_orb = 0
        self.update()
        return

    def paintEvent(self, event):
        """custom paint, painting the orbs"""
        painter = QtGui.QPainter()
        painter.begin(self)
        pixmap = working_pixmap.getQPixmap()
        row, col = divmod(self.highlighted_orb, self.cols)
        painter.drawPixmap(self.width() - self.frame_width, self.height() - self.frame_height, pixmap, self.frame_width * col, self.frame_height * row, self.frame_width, self.frame_height)
        painter.end()

    def timerEvent(self, event):
        """custom timer event, updating the animation"""
        self.update()
        self.highlighted_orb += 1
        if self.highlighted_orb > self.orbs:
            self.highlighted_orb = 0
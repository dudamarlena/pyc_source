# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/QueueLogHandler.py
# Compiled at: 2019-12-11 16:37:47
"""LogHandler to capture logs for display in the gui.

   This is a simple finite-length queue of formatted log messages, but
   we also track the level to support filtering the recorded log messages."""
from collections import deque
from logging import Handler, Formatter, DEBUG
QUEUE_LENGTH = 500

class QueueLogHandler(Handler, object):
    """Simple log handler that adds messages to a queue"""

    def __init__(self):
        super(QueueLogHandler, self).__init__()
        self.aQueue = deque([], QUEUE_LENGTH)
        self.setLevel(DEBUG)
        self.formatter = Formatter('%(asctime)s - %(levelname)s - %(module)s.%(funcName)s: %(message)s')
        self._oLogWidget = None
        return

    def set_widget(self, oLogWidget):
        """Associate with the correct display widget"""
        self._oLogWidget = oLogWidget
        oLogWidget.queue_reload()

    def unset_widget(self):
        """Remove the widget association"""
        self._oLogWidget = None
        return

    def emit(self, oRecord):
        """Add message to the queue"""
        self.aQueue.append((oRecord.levelno, self.format(oRecord)))
        if self._oLogWidget:
            self._oLogWidget.queue_reload()
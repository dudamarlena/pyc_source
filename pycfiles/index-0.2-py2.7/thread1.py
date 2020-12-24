# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\index\mainframe\thread1.py
# Compiled at: 2013-08-05 10:21:11
from __future__ import division, absolute_import, print_function, unicode_literals
import logging
from PySide import QtCore

class Thread(QtCore.QThread):

    def __init__(self):
        super(Thread, self).__init__()
        self.timer = None
        self.message = b''
        return

    def set_callback(self, update_func, ending_func, interval=1000):
        self.timer = QtCore.QTimer(self)
        self.update_func = update_func
        self.ending_func = ending_func
        self.interval = interval
        self.timer.timeout.connect(self.update)

    def update(self):
        if self.isRunning():
            self.secs += self.interval
            if self.update_func:
                self.update_func(self.secs)
        else:
            self.timer.stop()
            if self.ending_func:
                self.ending_func(self.secs, self.message)

    def start(self, func, *args, **kargs):
        if self.timer:
            self.secs = 0
            self.timer.start(self.interval)
        self.func = func
        self.args = args
        self.kargs = kargs
        super(Thread, self).start()

    def run(self):
        if self.func:
            try:
                self.message = self.func(*self.args, **self.kargs)
            except Exception as e:
                msg = (b"Завершено с ошибкой: '{0}'").format(e)
                logging.exception(msg)
                self.message = msg


th = Thread()
# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.6/site-packages/PyLAF/thread.py
# Compiled at: 2011-04-15 05:00:24
import Tkinter
from core import Component, Port, Output

class StateCanceled(Exception):
    pass


class Buffer(Component):

    def __init__(self, master=None, name=None):
        Component.__init__(self, master, name)
        self.receive = Port(None).bind(self._set)
        self.send = Output(None).bind(self.flush)
        self._last = None
        return

    def _set(self):
        self._last = self.receive.get()

    def flush(self):
        if not self._last == None:
            self.send.set_now(self._last)
            self._last = None
        return


class Polling(Tkinter.Frame):

    def __init__(self, master=None, interval=200, cnf={}, **kw):
        Tkinter.Frame.__init__(self, master, cnf, **kw)
        self.interval = interval
        self.value = Port(None)
        self._id = None
        self._polling()
        return

    def start(self):
        self._polling()

    def stop(self):
        if not self._id == None:
            self.after_cancel(self._id)
        return

    def _polling(self):
        self.value.set_now(None)
        self._id = self.after(self.interval, self._polling)
        return
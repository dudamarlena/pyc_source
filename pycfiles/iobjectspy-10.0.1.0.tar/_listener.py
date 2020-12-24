# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\data\_listener.py
# Compiled at: 2019-12-31 04:08:57
# Size of source mod 2**32: 1413 bytes
import datetime, threading

class PythonListenerBase(object):

    def __init__(self, name, func):
        self._name = name
        self._func = func
        self._code = hash((name, func, datetime.datetime.now(), threading.get_ident()))

    @property
    def name(self):
        return self._name

    @property
    def func(self):
        return self._func

    @property
    def code(self):
        return self._code

    def equals(self, obj):
        return self.toString() == obj.toString()

    def hashCode(self):
        return self.code

    def toString(self):
        return '%s, %s' % (self.name, str(self.code))


class ProgressListener(PythonListenerBase):

    def __init__(self, progress_fun, name):
        from .step import StepEvent
        self._stepped = StepEvent()
        PythonListenerBase.__init__(self, 'Progress:' + name, progress_fun)

    def stepped(self, event):
        if self.func is not None:
            self._stepped._title = event.getTitle()
            self._stepped._message = event.getMessage()
            self._stepped._percent = event.getPercent()
            self._stepped._is_cancel = event.getCancel()
            self._stepped._remain_time = event.getRemainTime()
            self.func(self._stepped)
            if self._stepped.is_cancel:
                event.setCancle(True)

    class Java:
        implements = ['com.supermap.data.SteppedListener']
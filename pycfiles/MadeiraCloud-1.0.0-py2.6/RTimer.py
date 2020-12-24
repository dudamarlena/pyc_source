# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/madeiracloud/RTimer.py
# Compiled at: 2011-12-16 02:01:38
import threading

class RTimer(object):

    def __init__(self, interval, callback, args=[], kwargs={}):
        self.__interval = interval
        self.__callback = callback
        self.__args = args
        self.__kwargs = kwargs
        self.__event = threading.Event()
        self.__timer = threading.Thread(target=self.__serve)

    def __serve(self):
        while not self.__event.is_set():
            self.__event.wait(self.__interval)
            if not self.__event.is_set():
                self.__callback(*self.__args, **self.__kwargs)

    def run(self):
        self.__timer.start()

    def cancel(self):
        self.__event.set()
        self.__timer.join()
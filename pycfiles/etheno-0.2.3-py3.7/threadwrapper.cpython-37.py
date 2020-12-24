# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/etheno/threadwrapper.py
# Compiled at: 2019-06-27 23:49:12
# Size of source mod 2**32: 4076 bytes
import threading
from threading import Condition

def is_main_thread():
    return isinstance(threading.current_thread(), threading._MainThread)


class MainThreadController(object):

    def __init__(self):
        if not is_main_thread():
            raise Exception('A controller can only be created from the main thread')
        self._main_wake_up = Condition()
        self._main_wake_up.acquire()
        self._obj = None
        self._caller_wake_up = None
        self._args = None
        self._kwargs = None
        self._return = None
        self._quit = False

    def invoke(self, obj, *args, **kwargs):
        if is_main_thread():
            return (obj.__call__)(*args, **kwargs)
        released = False
        self._main_wake_up.acquire()
        try:
            self._caller_wake_up = Condition()
            with self._caller_wake_up:
                self._obj = obj
                self._args = args
                self._kwargs = kwargs
                self._main_wake_up.notify_all()
                self._main_wake_up.release()
                released = True
                self._caller_wake_up.wait()
                self._caller_wake_up.notify_all()
                ret = self._return
                return ret
        finally:
            self._obj = None
            self._args = None
            self._kwargs = None
            self._caller_wake_up = None
            self._return = None
            if not released:
                self._main_wake_up.release()

    def quit(self):
        self._main_wake_up.acquire()
        try:
            self._quit = True
            self._main_wake_up.notify_all()
        finally:
            self._main_wake_up.release()

    def run(self):
        if not is_main_thread():
            raise Exception('run can only be called from the main thread!')
        from . import signals

        def signal_handler(signal, frame):
            self._quit = True

        signals.add_sigint_handler(signal_handler)
        while True:
            try:
                self._main_wake_up.wait(1.0)
            except KeyboardInterrupt:
                self._quit = True

            if self._quit:
                return
            if self._caller_wake_up is None:
                continue
            with self._caller_wake_up:
                self._return = (self._obj.__call__)(*self._args, **self._kwargs)
                self._caller_wake_up.notify_all()
                while not self._caller_wake_up.wait(1.0):
                    if self._quit:
                        return


class MainThreadWrapper(object):

    def __init__(self, mainobj, controller):
        self._main = mainobj
        self._controller = controller

    def __call__(self, *args, **kwargs):
        ret = (self._controller.invoke)(self._main, *args, **kwargs)
        if id(self._main) == id(ret):
            return MainThreadWrapper(ret, self._controller)
        return ret

    def __getattribute__(self, name):
        if name == '_main' or name == '_controller':
            return object.__getattribute__(self, name)
        if isinstance(getattr(type(self._main), name), property):
            return getattr(self._main, name)
        return MainThreadWrapper(getattr(self._main, name), self._controller)


if __name__ == '__main__':

    class MainThreadOnlyClass(object):

        def do_stuff(self):
            if not is_main_thread():
                raise Exception('ERROR!')
            return 1337


    main_thread_only = MainThreadOnlyClass()
    controller = MainThreadController()

    def dostuff(mtoc):
        print(mtoc.do_stuff())


    from threading import Thread
    thread = Thread(target=dostuff, args=(MainThreadWrapper(main_thread_only, controller),))
    thread.start()
    controller.run()
    thread.join()
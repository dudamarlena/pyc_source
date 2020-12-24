# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/Cellar/python/3.7.6_1/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/NEMbox/kill_thread.py
# Compiled at: 2020-03-14 16:24:02
# Size of source mod 2**32: 1033 bytes
import threading, time, inspect, ctypes
__all__ = [
 'stop_thread']

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    else:
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError('invalid thread id')
        else:
            if res != 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                raise SystemError('PyThreadState_SetAsyncExc failed')


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def test():
    while True:
        print('-------')
        time.sleep(0.5)


if __name__ == '__main__':
    t = threading.Thread(target=test)
    t.start()
    time.sleep(5.2)
    print('main thread sleep finish')
    stop_thread(t)
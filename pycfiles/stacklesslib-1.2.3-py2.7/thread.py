# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\stacklesslib\replacements\thread.py
# Compiled at: 2017-12-11 20:12:50
from __future__ import absolute_import
import traceback, stackless, stacklesslib.locks

class error(RuntimeError):
    pass


def _count():
    return Thread.thread_count


class Thread(stackless.tasklet):
    __slots__ = [
     '__dict__']
    thread_count = 0

    def __new__(cls, function, args, kwargs):
        return stackless.tasklet.__new__(cls, cls.thread_main)

    def __init__(self, function, args, kwargs):
        super(Thread, self).__init__(self.thread_main)
        self(function, args, kwargs)
        self.__class__.thread_count += 1

    @classmethod
    def thread_main(cls, func, args, kwargs):
        try:
            try:
                try:
                    func(*args, **kwargs)
                except SystemExit:
                    raise TaskletExit

            except Exception:
                traceback.print_exc()

        finally:
            cls.thread_count -= 1


def start_new_thread(function, args, kwargs={}):
    t = Thread(function, args, kwargs)
    return id(t)


def interrupt_main():
    pass


def exit():
    stackless.getcurrent().kill()


def get_ident():
    return id(stackless.getcurrent())


_stack_size = 0

def stack_size(size=None):
    global _stack_size
    old = _stack_size
    if size is not None:
        _stack_size = size
    return old


def allocate_lock(self=None):
    return LockType()


class LockType(stacklesslib.locks.Lock):
    """
    Check if the lock is held by someone
    """

    def locked(self):
        success = self.acquire(False)
        if not success:
            return True
        self.release()
        return False
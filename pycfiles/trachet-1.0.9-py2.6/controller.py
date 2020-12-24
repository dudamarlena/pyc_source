# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/trachet/controller.py
# Compiled at: 2014-07-01 10:29:06
_DEBUG_MODE_NONE = 0
_DEBUG_MODE_NORMAL_STEP = 1
_DEBUG_MODE_FUZZY_STEP = 2
_DEBUG_MODE_STOP = 3
import constant, time

class ActionController(object):
    __mode = _DEBUG_MODE_NONE
    __actions = None
    __accel = 1.0
    __lastcalltime = 0

    def __init__(self, tty):
        self.__mode = _DEBUG_MODE_NONE
        self.__actions = []
        self.__tty = tty
        self.__accel = 1.0

    def is_suspended(self):
        return self.__mode != _DEBUG_MODE_NONE

    def append(self, action):
        return self.__actions.append(action)

    def resume(self):
        self.__mode = _DEBUG_MODE_NONE

    def set_normal_step(self):
        self.__mode = _DEBUG_MODE_NORMAL_STEP

    def set_fuzzy_step(self):
        self.__mode = _DEBUG_MODE_FUZZY_STEP

    def set_break(self):
        self.__mode = _DEBUG_MODE_STOP

    def _get_repeat_count(self):
        now = time.time()
        if now - self.__lastcalltime < 0.1:
            self.__accel *= 1.2
        else:
            self.__accel = 1
        self.__lastcalltime = now
        repeat = max(1, self.__accel)
        return repeat

    def tick(self):
        if self.__mode == _DEBUG_MODE_NONE:
            while self.__actions:
                action = self.__actions.pop(0)
                result = action()

        elif self.__mode == _DEBUG_MODE_NORMAL_STEP:
            self.__mode = _DEBUG_MODE_STOP
            repeat = self._get_repeat_count()
            while repeat > 0 and self.__actions:
                repeat -= 1
                action = self.__actions.pop(0)
                result = action()

        elif self.__mode == _DEBUG_MODE_FUZZY_STEP:
            self.__mode = _DEBUG_MODE_STOP
            repeat = self._get_repeat_count()
            while repeat > 0:
                repeat -= 1
                while self.__actions:
                    action = self.__actions.pop(0)
                    result = action()
                    if result != constant.SEQ_TYPE_CHAR:
                        break
                else:
                    return


if __name__ == '__main__':
    import doctest
    doctest.testmod()
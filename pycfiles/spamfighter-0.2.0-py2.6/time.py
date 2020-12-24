# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/utils/time.py
# Compiled at: 2009-01-30 08:10:10
"""
Модуль подсчета "неточного" времени (разрешение одна секунда). Доступен
вариант для использования в unit-тестах.

Модуль экспортирует функцию C{time()}, которая возвращает целое число
секунд, начиная с некоторой даты. В production - это переменная, которая
обновляется (осуществляется системный вызов) не чаще, чем раз в секунду.

При использовании в тестах можно подменить реальное время модельным.
После вызова функции startUpTestTimer функция time() буде возвращать таймер,
значение которого можно корректировать
"""
import sys
from ..time import time as sys_time
from twisted.internet import reactor

def _inaccurate_time():
    global _inaccurate_timer
    return _inaccurate_timer


_timer_func = _inaccurate_time
_inaccurate_timer = int(sys_time())

def time():
    global _timer_func
    return _timer_func()


def _inaccurate_timer_tick():
    global _inaccurate_timer
    _inaccurate_timer = int(sys_time())
    _start_inaccurate_timer()


def _start_inaccurate_timer():
    if not sys.modules.has_key('twisted.trial.runner'):
        reactor.callLater(1, _inaccurate_timer_tick)


_start_inaccurate_timer()
_test_timer = 0

def _test_time():
    global _test_timer
    return _test_timer


def startUpTestTimer(initial=0):
    global _test_timer
    global _timer_func
    _test_timer = initial
    _timer_func = _test_time


def advanceTestTimer(step):
    global _test_timer
    _test_timer += step


def setTestTimer(value):
    global _test_timer
    _test_timer = value


def tearDownTestTimer():
    global _timer_func
    _timer_func = _inaccurate_time


__all__ = [
 'time', 'startUpTestTimer', 'advanceTestTimer', 'setTestTimer', 'tearDownTestTimer']
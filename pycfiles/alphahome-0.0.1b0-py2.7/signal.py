# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/alphahome/signal.py
# Compiled at: 2017-08-07 12:33:16
import uuid, threading
_pool = dict()

class SignalError(Exception):
    """
    信号池错误
    """

    def __init__(self, msg):
        self.message = msg

    def print_exception(self):
        print self.message


class Signal(object):
    """
    信号，作为信号池必须组件
    """

    def __init__(self, sig, func):
        if not isinstance(sig, (str,)):
            raise SignalError('[Parameter error] "sig" must be str')
        if not callable(func):
            raise SignalError('[Parameter error] "func" must be callable')
        self.__sig = sig
        self.__func = func
        self.__uuid = uuid.uuid1().__str__()

    @property
    def uuid(self):
        return self.__uuid

    @property
    def sig(self):
        return self.__sig

    @property
    def func(self):
        return self.__func


def register(signal):
    u"""
    注册新信号
    :param signal:
    :return:
    """
    if not isinstance(signal, (Signal,)):
        raise SignalError('[Parameter error] "signal" must be SignalPool.Signal ')
    _pool.setdefault(signal.sig, [])
    _pool[signal.sig].append(signal)
    return signal.uuid


def call(sig, params=tuple()):
    u"""
    放入新信号
    :param params:
    :param sig:
    :return:
    """
    if not isinstance(sig, (str,)):
        raise SignalError('[Parameter error] "sig" must be str')
    if not isinstance(params, (tuple,)):
        raise SignalError('[Parameter error] "parameters" must be tuple ')
    signal_set = _pool.get(sig)
    if signal_set is None:
        return
    else:
        for signal in signal_set:
            t = threading.Thread(target=signal.func, args=params)
            t.start()

        return


def remove(sig, id):
    u"""
    移除信号
    :param id:
    :param sig:
    :return:
    """
    signal_set = _pool.get(sig)
    if signal_set is None:
        return
    else:
        for signal in signal_set:
            if signal.uuid == id:
                signal_set.remove(signal)
                break

        return
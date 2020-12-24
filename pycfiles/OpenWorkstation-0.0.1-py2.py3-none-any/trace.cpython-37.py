# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/l0/ss9rqt5j7xbg0x2bpvmjx_k40000gp/T/pip-install-n2xwwglt/workstation/workstation/util/trace.py
# Compiled at: 2019-09-24 08:15:55
# Size of source mod 2**32: 1922 bytes
from functools import wraps
import inspect

def traceable(*args):

    def _traceable(f):

        @wraps(f)
        def decorated(*args, **kwargs):
            res = f(*args, **kwargs)
            broker = EventBroker.get_instance()
            args_dict = {}
            if inspect.getargspec(f).defaults:
                args_dict = dict(zip(reversed(inspect.getargspec(f).args), reversed(inspect.getargspec(f).defaults)))
            args_dict.update(dict(zip(inspect.getargspec(f).args, args)))
            args_dict.update(kwargs)
            broker.notify({'name':name, 
             'function':f.__qualname__, 
             'arguments':args_dict, 
             'result':res})
            return res

        return decorated

    if len(args) == 1:
        if callable(args[0]):
            f, = args
            name = f.__qualname__
            return _traceable(f)
    name, = args
    return _traceable


class EventBroker(object):
    _instance = None

    def __init__(self):
        self.listeners = []

    def add(self, f):
        self.listeners.append(f)

    def remove(self, f):
        self.listeners.remove(f)

    def notify(self, arguments):
        for listener in self.listeners:
            listener(arguments)

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = EventBroker()
        return cls._instance
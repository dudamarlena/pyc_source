# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/core/utils/designpattern.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 1815 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '26/06/2019'

class Borg:
    _Borg__shared_state = {}
    _Borg__register = {}

    def __init__(self):
        self.__dict__ = self._Borg__shared_state
        if not self._Borg__register:
            self._init_default_register()


def singleton(class_):
    instances = {}

    def wrapper(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return wrapper
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mico/lib/python2.7/site-packages/mico/util/switch.py
# Compiled at: 2013-02-18 09:26:02


class Switcher(object):
    """Switch a global status using the environment as critical region, and
    setted using class constructor.
    """
    _switch = (None, None)

    def __init__(self, init_value=None):
        self._old_value = env.get(self._switch[0], None)
        env[self._switch[0]] = self._switch[1] if init_value is None else init_value
        return

    def __enter__(self):
        pass

    def __exit__(self, t, v, tr):
        if self._old_value is None:
            del env[self._switch[0]]
        else:
            env[self._switch[0]] = self._old_value
        return

    @staticmethod
    def getValue(key):
        return env.get(key, None)

    @classmethod
    def from_key(cls, key, value):
        return type.__new__(type, 'switch_%s' % key, (Switcher,), {'_switch': (key, value)})
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/socek/projects/impaf/example/venv_impex/lib/python3.5/site-packages/impaf/utils.py
# Compiled at: 2015-11-29 15:37:02
# Size of source mod 2**32: 328 bytes


def cached(fun):
    name = fun.__name__

    def wrapper(self, *args, **kwargs):
        try:
            self._cache
        except AttributeError:
            self._cache = {}

        if name not in self._cache:
            self._cache[name] = fun(self, *args, **kwargs)
        return self._cache[name]

    return wrapper
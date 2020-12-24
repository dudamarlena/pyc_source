# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tyrs/container.py
# Compiled at: 2011-07-04 17:37:11


class Container(object):
    """
    Contain main classes that we need thought all the programm
    such as conf, api and ui
    """
    _container = {}

    def __setitem__(self, key, value):
        self._container[key] = value

    def __getitem__(self, key):
        return self._container[key]

    def add(self, name, dependency):
        self[name] = dependency
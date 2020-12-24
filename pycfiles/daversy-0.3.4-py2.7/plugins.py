# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\daversy\plugins.py
# Compiled at: 2016-01-14 15:12:15
import os, sys, optparse, textwrap

class Plugin(object):
    """A very simple plugin system."""

    @classmethod
    def _load_plugins(cls):
        cls._list = []
        if not hasattr(cls, '__plugins__'):
            return
        try:
            module = __import__(cls.__plugins__, {}, {}, [''])
            for name in module.__all__:
                __import__('%s.%s' % (cls.__plugins__, name), {}, {}, ['*'])

            for subclass in cls.__subclasses__():
                cls._list.append(subclass)

        except Exception as e:
            print 'Exception', e

    @classmethod
    def list(cls):
        if not hasattr(cls, '_list'):
            cls._load_plugins()
        return cls._list
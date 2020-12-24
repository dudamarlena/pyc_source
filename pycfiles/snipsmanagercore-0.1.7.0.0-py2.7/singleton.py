# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/snipsmanagercore/singleton.py
# Compiled at: 2017-08-07 05:06:11
""" Singleton class. """

class Singleton(object):
    """ Singleton class. """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """ Initialisation. """
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance
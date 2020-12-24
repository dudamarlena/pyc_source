# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/singleton.py
# Compiled at: 2019-08-19 15:09:29
"""This module contains a class which can be used as a super class for all
classes that need to implement the Singleton design pattern."""
from builtins import object
__all__ = [
 'Singleton']
__docformat__ = 'restructuredtext'

class Singleton(object):
    """ This class allows Singleton objects
    The __new__ method is overriden to force Singleton behaviour.
    The Singleton is created for the lowest subclass.
    Usage::

        from taurus.core.util.singleton import Singleton

        class MyManager(Singleton):

            def init(self, *args, **kwargs):
                print "Singleton initialization"

    command line::

        >>> manager1 = MyManager()
        Singleton initialization

        >>> manager2 = MyManager()

        >>> print(manager1,manager2)
        <__main__.MyManager object at 0x9c2a0ec>
        <__main__.MyManager object at 0x9c2a0ec>

    Notice that the two instances of manager point to the same object even
    though you *tried* to construct two instances of MyManager.

    .. warning::

        although __new__ is overriden __init__ is still being called for
        each instance=Singleton()
    """
    _the_instance = None

    def __new__(cls, *p, **k):
        if cls != type(cls._the_instance):
            cls._the_instance = object.__new__(cls)
            if 'init_single' in cls.__dict__:
                cls._the_instance.init_single(*p, **k)
            else:
                cls._the_instance.init(*p, **k)
        return cls._the_instance

    def init(self, *p, **k):
        pass
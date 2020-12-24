# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/utils/registrator.py
# Compiled at: 2009-01-30 08:10:10
"""
Декоратор регистрации, позволяющий получить текущий класс в функции,
вызванной в теле класса.
"""

def registrator(f):
    u"""Декоратор регистраторов

    оборачивает методы которые затем могут вызываться в определении классов.
    При этом первым параметром в оборачиваемую функцию передается класс в определении которого она вызвана

    Пример::

        @registrator
        def register(cls, *args, **kw):
            print "Class:", cls

        class Test(object):
            register()

    выведет на экран 
    <class '__main__.Test'>
    """

    def registration(*args, **kw):
        _implements(f.__name__, args, kw, f)

    return registration


import sys
from zope.interface.advice import addClassAdvisor

def _implements(name, args, kw, classImplements):

    def _implements_advice(cls):
        classImplements(cls, *args, **kw)
        return cls

    frame = sys._getframe(2)
    locals = frame.f_locals
    if locals is frame.f_globals or '__module__' not in locals and sys.version_info[:3] > (2,
                                                                                           2,
                                                                                           0):
        raise TypeError(name + ' can be used only from a class definition.')
    if str(classImplements) in locals:
        raise TypeError(name + ' can be used only once in a class definition.')
    locals[str(classImplements)] = (
     args, kw, classImplements)
    addClassAdvisor(_implements_advice, depth=3)
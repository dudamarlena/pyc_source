# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/linjiao/dv/beim/beim/paths/SingletonByName.py
# Compiled at: 2013-12-08 21:45:16


class SingletonByName(object):

    def __new__(cls, name, *args, **kwds):
        its = cls.__dict__.get('__its__')
        if its is None:
            its = cls.__its__ = {}
        try:
            return its[name]
        except KeyError:
            new_inst = object.__new__(cls)
            its[name] = new_inst
            return its[name]

        return

    def getSingleton(self, name):
        return self.__class__.__dict__.get('__its__')[name]


__id__ = '$Id: SingletonByName.py 135 2005-08-06 16:31:39Z linjiao $'
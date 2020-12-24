# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/skeletool/controller.py
# Compiled at: 2012-08-31 11:30:16
from new import instancemethod
from container import Container

class Controllers(Container):

    def command(self, commandid):
        for controller in self._items:
            if 'usage' not in dir(controller):
                continue
            if commandid in controller.usage['command']:
                return self._items[controller]

        return


class Controller(object):

    @staticmethod
    def __new__(cls):
        if cls is Controller:
            raise TypeError('Cannot directly instanciate ' + repr(cls))
        if '_instance' not in dir(cls):
            cls._instance = super(Controller, cls).__new__(cls)
            Controllers().set(cls._instance)
        return cls._instance

    def actions(self):
        lst = []
        for methodname in dir(self):
            method = eval('self.' + methodname)
            if isinstance(method, instancemethod) and not methodname.startswith('_'):
                lst.append(method)

        return lst

    def default(self, *kargs, **kwargs):
        return
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/mvc/model_and_view.py
# Compiled at: 2018-05-30 05:31:20
__all__ = [
 'ModelAndView', 'Model']
__authors__ = ['Tim Chow']

class ModelAndView(object):

    def __init__(self):
        self._model = Model()
        self._view = None
        return

    @property
    def model(self):
        return self._model

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, value):
        self._view = value

    def merge(self, mv):
        if mv.view is not None:
            self.view = mv.view
        self.model.merge(mv.model)
        return

    def __str__(self):
        return '%s{view=%s, model=%s}' % (self.__class__.__name__,
         self.view, self.model)

    def clear(self):
        self.model.clear()


class Model(object):

    def __init__(self):
        self._map = {}

    def add_attribute(self, attr, value):
        self._map[attr] = value

    def set_attribute(self, attr, value):
        if attr in self._map:
            self._map[attr] = value

    def get_attribute(self, attr):
        return self._map[attr]

    def iteritems(self):
        for item in self._map.iteritems():
            yield item

    def merge(self, model):
        for k, v in model.iteritems():
            self.add_attribute(k, v)

    def asmap(self):
        return self._map

    def __str__(self):
        return '%s%s' % (self.__class__.__name__, self._map)

    def clear(self):
        self._map.clear()
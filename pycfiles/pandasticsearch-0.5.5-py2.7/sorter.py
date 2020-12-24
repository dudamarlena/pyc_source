# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/pandasticsearch/operators/sorter.py
# Compiled at: 2018-09-25 01:28:44
_sort_mode = ('min', 'max', 'sum', 'avg', 'median')

class Sorter(object):

    def __init__(self, field, order='desc', mode=None):
        self._field = field
        self._order = order
        self._mode = mode

    def build(self):
        sort = {}
        if self._mode is not None:
            if self._mode not in _sort_mode:
                raise Exception(('Not support sort mode: {0}').format(self._mode))
            sort['mode'] = self._mode
        sort['order'] = self._order
        return {self._field: sort}


class ScriptSorter(object):

    def __init__(self, script, order='desc', type='number', params=None):
        self._order = order
        self._script = script
        self._params = params
        self._type = type

    def build(self):
        script = {'script': self._script, 'type': self._type, 'order': self._order}
        if self._params:
            script['params'] = self._params
        return {'_script': script}
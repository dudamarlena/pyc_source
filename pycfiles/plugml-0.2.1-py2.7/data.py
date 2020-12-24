# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\plugml\data.py
# Compiled at: 2015-02-03 10:29:22
import numpy as np

class Data:

    def __init__(self, data, colDef):
        self._map = {col:idx for col, idx in zip(colDef, range(len(colDef)))}
        self._samples = len(data)
        self._data = data
        self._cols = dict()
        self._names = []

    def __len__(self):
        return self._samples

    def __getitem__(self, key):
        if isinstance(key, basestring):
            return self._cols[key]
        else:
            if isinstance(key, (int, long, np.int64)):
                return [ self[col][key] for col in self._names ]
            row, col = key
            if isinstance(col, basestring):
                return self[col][row]
            return self[self._names[col]][row]

    def use(self, cols, name=None, reducer=None):
        if not isinstance(cols, list):
            cols = [
             cols]
        l = []
        reducer = reducer or (lambda x: x[cols[0]])
        for i in range(self._samples):
            inp = {col:self._data[i][self._map[col]] for col in cols}
            l.append(reducer(inp))

        name = name or ('##').join(cols)
        if name in self._cols:
            raise 'name already used: ' + name
        self._cols[name] = np.array(l)
        self._names.append(name)

    def filter(self, col, cond):
        if len(self._cols) > 0:
            raise 'cannot filter after use'
        self._data = [ row for row in self._data if not cond(row[self._map[col]]) ]
        self._samples = len(self._data)
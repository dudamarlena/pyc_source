# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/LineMetaInfo.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 2954 bytes
from vaitk import core
import collections, copy

class LineMetaInfo:

    def __init__(self, meta_type, document):
        self._meta_type = meta_type
        self._document = document
        self.resetLines()
        self.contentChanged = core.VSignal(self)

    def numLines(self):
        return len(self._data)

    def addLines(self, line_number, how_many):
        for i in range(how_many):
            self._data.insert(line_number - 1, None)

    def deleteLines(self, line_number, how_many):
        for i in range(how_many):
            self._data.pop(line_number - 1)

        if len(self._data) == 0:
            self._data = [
             None]

    def resetLines(self):
        self._data = [
         None] * self._document.numLines()

    def setData(self, data, from_line=1):
        if not isinstance(data, collections.Iterable) or isinstance(data, str):
            data = [
             data]
        try:
            for idx, d in enumerate(data):
                self._data[from_line - 1 + idx] = d

        except IndexError:
            pass

        self.notifyObservers()

    def setDataForLines(self, data_dict):
        for k, v in data_dict.items():
            self._data[k - 1] = v

        self.notifyObservers()

    def data(self, from_line=None, how_many=None):
        if from_line is not None:
            if how_many is None:
                return self._data[(from_line - 1)]
            else:
                return self._data[from_line - 1:from_line - 1 + how_many]
        else:
            if how_many is None:
                return self._data
            else:
                return self._data[:how_many]

    def notNoneData(self):
        return self.findWhere(lambda x: x is not None)

    def findWhere(self, condition):
        return {i + 1:v for i, v in enumerate(self._data) if condition(v)}

    def dataForLines(self, lines):
        return {i:self._data[(i - 1)] for i in lines}

    def clear(self):
        self._data = [
         None] * self._document.numLines()
        self.notifyObservers()

    def notifyObservers(self):
        self.contentChanged.emit()

    @property
    def meta_type(self):
        return self._meta_type

    @property
    def document(self):
        return self._document

    def memento(self, line):
        return copy.deepcopy(self._data[(line - 1)])

    def insertFromMemento(self, line, memento):
        self._data.insert(line - 1, copy.deepcopy(memento))

    def replaceFromMemento(self, line, memento):
        self._data[line - 1] = copy.deepcopy(memento)

    def __str__(self):
        return str(self._data)
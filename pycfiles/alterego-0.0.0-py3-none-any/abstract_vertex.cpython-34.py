# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alteraparser/syntaxgraph/abstract_vertex.py
# Compiled at: 2015-12-30 04:57:43
# Size of source mod 2**32: 1553 bytes
from .processor import ProcessingResult
from .clonable import Clonable

class AbstractVertex(Clonable):

    def __init__(self):
        Clonable.__init__(self)

    def num_successors(self):
        raise NotImplemented

    def nth_successor(self, idx):
        raise NotImplemented

    def walk(self, processor):
        path = []
        current = self
        result = None
        while True:
            result = processor.process(current, path)
            if result in [ProcessingResult.CONTINUE, None]:
                next = self._AbstractVertex__continue(current, path)
                if not next:
                    next = self._AbstractVertex__back(path, processor)
            else:
                if result == ProcessingResult.GO_BACK:
                    next = self._AbstractVertex__back(path, processor)
                else:
                    break
                if next is None:
                    break
            current = next

        return result

    @staticmethod
    def __continue(current, path):
        if current.num_successors() > 0:
            next = current.nth_successor(0)
            path.append((current, 0))
        else:
            next = None
        return next

    @staticmethod
    def __back(path, processor):
        next_vertex = None
        while path:
            vertex, idx = path.pop()
            if idx < vertex.num_successors() - 1:
                next_vertex = vertex.nth_successor(idx + 1)
                path.append((vertex, idx + 1))
                return next_vertex
            processor.undo(vertex, path)

        return next_vertex
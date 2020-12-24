# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alteraparser/syntaxgraph/vertex_group.py
# Compiled at: 2015-12-30 04:57:43
# Size of source mod 2**32: 4646 bytes
from .dockable import Dockable
from .clonable import Clonable
from .vertex import Vertex, VertexCategory

class StartVertex(Vertex):

    def __init__(self, vertex_group):
        Vertex.__init__(self, VertexCategory.GROUP_START)
        self._StartVertex__group = vertex_group
        self.name = None
        self.id = None

    def num_successors(self):
        if not self._StartVertex__group._VertexGroup__expanded:
            self._StartVertex__group.expand()
        return Vertex.num_successors(self)

    def nth_successor(self, idx):
        if not self._StartVertex__group._VertexGroup__expanded:
            self._StartVertex__group.expand()
        return Vertex.nth_successor(self, idx)


class EndVertex(Vertex):

    def __init__(self):
        Vertex.__init__(self, VertexCategory.GROUP_END)
        self.name = None
        self.id = None
        self.ignore = False
        self.transform_ast_fn = lambda ast: ast
        self.is_rule_end = False


class VertexGroup(Dockable, Clonable):

    def __init__(self):
        self._VertexGroup__expanded = False
        self._VertexGroup__start = StartVertex(self)
        self._VertexGroup__end = EndVertex()

    def set_name(self, name):
        res = self.clone()
        res._VertexGroup__start.name = name
        res._VertexGroup__end.name = name
        return res

    def get_name(self):
        return self._VertexGroup__start.name

    name = property(get_name, set_name)

    def set_id(self, id):
        res = self.clone()
        res._VertexGroup__start.id = id
        res._VertexGroup__end.id = id
        return res

    def get_id(self):
        return self._VertexGroup__start.id

    id = property(get_id, set_id)

    def set_ignore(self, ignore=True):
        self._VertexGroup__end.ignore = ignore
        return self

    def transform_ast(self, transformer_fn):
        res = self.clone()
        res._VertexGroup__end.transform_ast_fn = transformer_fn
        return res

    def set_unique(self, is_unique=True):
        res = self.clone()
        res._VertexGroup__end.is_rule_end = is_unique
        return res

    def connect(self, dockable):
        self._VertexGroup__end.connect(dockable)
        return dockable

    def get_dock_vertex(self):
        return self._VertexGroup__start

    def expand(self):
        if not self._VertexGroup__expanded:
            start = Vertex()
            end = Vertex()
            self._VertexGroup__start.connect(start)
            end.connect(self._VertexGroup__end)
            self._on_expand(start, end)
            self._VertexGroup__expanded = True

    def _on_expand(self, start, end):
        pass

    def _on_clone_creation(self, original):
        self._VertexGroup__start.name = self._VertexGroup__end.name = original._VertexGroup__start.name
        self._VertexGroup__start.id = self._VertexGroup__end.id = original._VertexGroup__start.id
        self._VertexGroup__end.ignore = original._VertexGroup__end.ignore
        self._VertexGroup__end.transform_ast_fn = original._VertexGroup__end.transform_ast_fn
        self._VertexGroup__end.is_rule_end = original._VertexGroup__end.is_rule_end


class Multiples(VertexGroup):

    def __init__(self, element=None, min_occur=0, max_occur=None):
        VertexGroup.__init__(self)
        if element:
            self._Multiples__element = element.clone()
        else:
            self._Multiples__element = None
        self._Multiples__min_occur = min_occur
        self._Multiples__max_occur = max_occur

    def _on_expand(self, start, end):
        current = start
        for _ in range(self._Multiples__min_occur):
            current = current.connect(self._Multiples__element.clone())

        min_end = current
        if self._Multiples__max_occur is None:
            if current is not start:
                current.connect(current)
            else:
                elem = self._Multiples__element.clone()
                start.connect(elem).connect(start)
                elem.connect(end)
        else:
            delta = self._Multiples__max_occur - self._Multiples__min_occur
            for _ in range(delta):
                current = current.connect(self._Multiples__element.clone())
                current.connect(end)

        min_end.connect(end)

    def _on_clone_creation(self, original):
        VertexGroup._on_clone_creation(self, original)
        self._Multiples__element = original._Multiples__element.clone()
        self._Multiples__min_occur = original._Multiples__min_occur
        self._Multiples__max_occur = original._Multiples__max_occur


class Branches(VertexGroup):

    def __init__(self):
        VertexGroup.__init__(self)
        self._Branches__branches = []

    def add_branch(self, elements):
        self._Branches__branches.append([el.clone() for el in elements])

    def _on_expand(self, start, end):
        for branch in self._Branches__branches:
            curr = start
            for elem in branch:
                curr = curr.connect(elem)

            curr.connect(end)

    def _on_clone_creation(self, original):
        VertexGroup._on_clone_creation(self, original)
        self._Branches__branches = [[el.clone() for el in orig_branch] for orig_branch in original._Branches__branches]
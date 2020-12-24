# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spodgi/term.py
# Compiled at: 2020-04-09 17:21:56
# Size of source mod 2**32: 7727 bytes
"""
This module defines the specific IRI objects that are used to avoid joins/refetching by
passing references.

* :class:`Step IRI reference <rdflib.term.URIRef>`
* :class:`Step IRI to end References <rdflib.term.URIRef>`
* :class:`Step IRI to begin References <rdflib.term.URIRef>`
* :class:`Node IRI References <rdflib.term.URIRef>`
"""
from rdflib.term import URIRef
__all__ = [
 'NodeIriRef',
 'StepIriRef',
 'StepEndIriRef',
 'StepBeginIriRef']

class StepIriRef(URIRef):
    __slots__ = ('_stepHandle', '_base', '_odgi', '_position', '_rank')

    def __new__(cls, stepHandle, base, odgi, position, rank):
        inst = str.__new__(cls)
        inst._stepHandle = stepHandle
        inst._base = base
        inst._odgi = odgi
        inst._rank = rank
        inst._position = position
        return inst

    def __eq__(self, other):
        if type(self) == type(other):
            return self._stepHandle == other._stepHandle and self._base == other._base
        if isinstance(other, URIRef):
            return URIRef(self.unicode()) == other
        return False

    def __gt__(self, other):
        if other is None:
            return True
            if type(self) == type(other):
                if self._base > other._base:
                    return True
                if self._base < other._base:
                    return False
                return self._rank > other._rank
        else:
            if isinstance(other, URIRef):
                return URIRef(self.unicode()) > other
            return str(type(self)) > str(type(other))

    def __lt__(self, other):
        return not self.__gt__(other)

    def n3(self, namespace_manager=None):
        if namespace_manager:
            return namespace_manager.normalizeUri(self)
        return f"<{self.unicode()}>"

    def stepHandle(self):
        return self._stepHandle

    def rank(self):
        return self._rank

    def position(self):
        return self._position

    def path(self):
        return self._odgi.get_path_handle_of_step(self.stepHandle())

    def toPython(self):
        return self.unicode()

    def unicode(self):
        return f"{self._base}path/{self._odgi.get_path_name(self._odgi.get_path_handle_of_step(self._stepHandle))}/step/{self._rank}"

    def __str__(self):
        return self.unicode()

    def __repr__(self):
        return "odgi.StepIriRef('" + self.unicode() + "')"

    def __hash__(self):
        return hash(self._stepHandle)


class NodeIriRef(URIRef):
    __slots__ = ('_nodeHandle', '_base', '_odgi')

    def __new__(cls, node_handle, base=None, odgi=None):
        inst = str.__new__(cls)
        inst._nodeHandle = node_handle
        inst._base = base
        inst._odgi = odgi
        return inst

    def __eq__(self, other):
        if type(self) == type(other):
            return self._odgi.get_id(self._nodeHandle) == other._odgi.get_id(other._nodeHandle) and self._base == other._base
        if type(other) == URIRef:
            return URIRef(self.unicode()) == other
        return False

    def __gt__(self, other):
        if other is None:
            return True
            if type(self) == type(other):
                if self._base > other._base:
                    return True
                if self._base < other._base:
                    return False
                return self._odgi.get_id(self._nodeHandle) > self._odgi.get_id(other._nodeHandle)
        else:
            return type(self) > type(other)

    def n3(self, namespace_manager=None):
        if namespace_manager:
            return namespace_manager.normalizeUri(self)
        return f"<{self.unicode()}>"

    def toPython(self):
        return self.unicode()

    def unicode(self):
        nid = self._odgi.get_id(self._nodeHandle)
        return f"{self._base}{nid}"

    def __str__(self):
        return self.unicode()

    def __repr__(self):
        return "odgi.NodeIriRef('" + self.unicode() + "')"

    def __hash__(self):
        return self._odgi.get_id(self._nodeHandle)


class StepBeginIriRef(URIRef):
    __slots__ = '_stepIri'

    def __new__(cls, stepIri):
        inst = str.__new__(cls)
        inst._stepIri = stepIri
        return inst

    def __eq__(self, other):
        if type(self) == type(other):
            return self._stepIri == other._stepIri
        if type(other) == URIRef:
            return URIRef(self.unicode()) == other
        return False

    def __gt__(self, other):
        if other is None:
            return True
        if type(self) == type(other):
            return self._stepIri > other._stepIri
        return type(self) > type(other)

    def n3(self, namespace_manager=None):
        if namespace_manager:
            return namespace_manager.normalizeUri(self)
        return f"<{self.unicode()}>"

    def stepHandle(self):
        return self._stepIri._stepHandle

    def rank(self):
        return self._stepIri._rank

    def position(self):
        return self._stepIri._position

    def path(self):
        return self._stepIri.path()

    def toPython(self):
        return self.unicode()

    def unicode(self):
        return f"{self._stepIri._base}path/{self._stepIri._odgi.get_path_name(self._stepIri._odgi.get_path_handle_of_step(self._stepIri._stepHandle))}/step/{self._stepIri._rank}/begin/{self._stepIri._position}"

    def __str__(self):
        return self.unicode()

    def __repr__(self):
        return "odgi.StepBeginIriRef('" + self.unicode() + "')"

    def __hash__(self):
        return hash(self._stepIri)


class StepEndIriRef(URIRef):
    __slots__ = '_stepIri'

    def __new__(cls, step_iri):
        inst = str.__new__(cls)
        inst._stepIri = step_iri
        return inst

    def __eq__(self, other):
        if type(self) == type(other):
            return self._stepIri == other._stepIri
        if type(other) == URIRef:
            return URIRef(self.unicode()) == other
        return False

    def __gt__(self, other):
        if other is None:
            return True
        if type(self) == type(other):
            return self._stepIri > other._stepIri

    def n3(self, namespace_manager=None):
        if namespace_manager:
            return namespace_manager.normalizeUri(self)
        return f"<{self.unicode()}>"

    def stepHandle(self):
        return self._stepIri._stepHandle

    def rank(self):
        return self._stepIri._rank

    def position(self):
        return self._stepIri._position + self._stepIri._odgi.get_length(self._stepIri._odgi.get_handle_of_step(self._stepIri._stepHandle))

    def path(self):
        return self._stepIri.path()

    def toPython(self):
        return self.unicode()

    def unicode(self):
        end = self.position()
        return f"{self._stepIri._base}path/{self._stepIri._odgi.get_path_name(self._stepIri._odgi.get_path_handle_of_step(self._stepIri._stepHandle))}/step/{self._stepIri._rank}/end/{end}"

    def __str__(self):
        return self.unicode()

    def __repr__(self):
        return "odgi.StepEndIriRef('" + self.unicode() + "')"

    def __hash__(self):
        return hash(self._stepIri)
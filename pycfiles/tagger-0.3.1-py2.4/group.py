# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-fat/egg/tagger/group.py
# Compiled at: 2006-10-10 17:32:29
from utils import any, all, nscollection, set_intersect, utcnow, implements
from dispatch_predicates import IS_GROUP
from tagger.tag import Tagger

class TaggerContrained(Tagger):
    __module__ = __name__
    ns = nscollection()
    isgroup = ns.tagger['taggroup']
    groupedby = ns.tagger['groupedBy']
    isrule = ns.tagger['Rule']

    def __init__(self, graph):
        self.graph = graph
        self.ns.bindAll(graph)

    @dispatch.generic()
    def isGroup(self, id_):
        """See tagger.interfaces.ITagger"""
        pass

    @dispatch.generic()
    def createRule(self, spec):
        """See tagger.interfaces.ITagger"""
        pass

    @getGroupsFor.when(strategy.default)
    def _getGroupsForAssociations(self, subject):
        """handles straight node ids"""
        node = self.get(subject)
        return self.graph.subjects(predicate=self.associated, object=node)

    @createRule.when('isinstance(spec, dict)')
    def _dict_createRule(self, spec):
        subject = self.get_create(spec[RDF.ID])
        triples = self._to_triples(spec, subject=subject)
        if subject:
            self._addTriples(triples, set=True)
        else:
            self._addTriples(triples)
            subject = triples[0][0]
        return subject

    @dispatch.generic()
    def getGroupsFor(self, subject):
        """See tagger.interfaces.ITagger"""
        pass
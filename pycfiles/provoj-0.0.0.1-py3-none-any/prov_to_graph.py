# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/provneo4j/prov_to_graph.py
# Compiled at: 2016-10-26 07:49:18
__author__ = 'Trung Dong Huynh'
__email__ = 'trungdong@donggiang.com'
import networkx as nx
from prov.model import ProvEntity, ProvActivity, ProvAgent, ProvElement, ProvRelation, PROV_ATTR_ENTITY, PROV_ATTR_ACTIVITY, PROV_ATTR_AGENT, PROV_ATTR_TRIGGER, PROV_ATTR_GENERATED_ENTITY, PROV_ATTR_USED_ENTITY, PROV_ATTR_DELEGATE, PROV_ATTR_RESPONSIBLE, PROV_ATTR_SPECIFIC_ENTITY, PROV_ATTR_GENERAL_ENTITY, PROV_ATTR_ALTERNATE1, PROV_ATTR_ALTERNATE2, PROV_ATTR_COLLECTION, PROV_ATTR_INFORMED, PROV_ATTR_INFORMANT
INFERRED_ELEMENT_CLASS = {PROV_ATTR_ENTITY: ProvEntity, 
   PROV_ATTR_ACTIVITY: ProvActivity, 
   PROV_ATTR_AGENT: ProvAgent, 
   PROV_ATTR_TRIGGER: ProvEntity, 
   PROV_ATTR_GENERATED_ENTITY: ProvEntity, 
   PROV_ATTR_USED_ENTITY: ProvEntity, 
   PROV_ATTR_DELEGATE: ProvAgent, 
   PROV_ATTR_RESPONSIBLE: ProvAgent, 
   PROV_ATTR_SPECIFIC_ENTITY: ProvEntity, 
   PROV_ATTR_GENERAL_ENTITY: ProvEntity, 
   PROV_ATTR_ALTERNATE1: ProvEntity, 
   PROV_ATTR_ALTERNATE2: ProvEntity, 
   PROV_ATTR_COLLECTION: ProvEntity, 
   PROV_ATTR_INFORMED: ProvActivity, 
   PROV_ATTR_INFORMANT: ProvActivity}

def prov_to_graph_flattern(prov_document):
    """ Convert a :class:`~prov.model.ProvDocument` to a `MultiDiGraph
    <http://networkx.github.io/documentation/latest/reference/classes.multidigraph.html>`_
    instance of the `NetworkX <https://networkx.github.io/>`_ library.

    :param prov_document: The :class:`~prov.model.ProvDocument` instance to
    convert.
    """
    g = nx.MultiDiGraph()
    unified = prov_document.unified()
    node_map = dict((element.identifier, element) for element in unified.get_records(ProvElement))
    unknown_count = 0
    for relation in unified.get_records(ProvRelation):
        attr_pair_1, attr_pair_2 = relation.formal_attributes[:2]
        qn1, qn2 = attr_pair_1[1], attr_pair_2[1]
        if not qn1:
            unknown_count = unknown_count + 1
            identifier = 'Unknown_%s' % unknown_count
            node_map[identifier] = ProvEntity(bundle=prov_document, identifier=identifier)
            qn1 = identifier
        if not qn2:
            unknown_count = unknown_count + 1
            identifier = 'Unknown_%s' % unknown_count
            node_map[identifier] = ProvEntity(bundle=prov_document, identifier=identifier)
            qn2 = identifier
        try:
            if qn1 not in node_map:
                node_map[qn1] = INFERRED_ELEMENT_CLASS[attr_pair_1[0]](None, qn1)
            if qn2 not in node_map:
                node_map[qn2] = INFERRED_ELEMENT_CLASS[attr_pair_2[0]](None, qn2)
        except KeyError:
            continue

        g.add_edge(node_map[qn1], node_map[qn2], relation=relation)

    return g
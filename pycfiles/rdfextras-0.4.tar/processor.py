# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/rdfextras/sparql/processor.py
# Compiled at: 2012-04-24 09:28:08
import rdfextras.sparql.parser
from rdfextras.sparql.algebra import TopEvaluate
from rdflib import RDFS, RDF, OWL
from rdflib.query import Processor
from rdfextras.sparql.components import Query, Prolog

class Processor(Processor):

    def __init__(self, graph):
        self.graph = graph

    def query(self, strOrQuery, initBindings={}, initNs={}, DEBUG=False, PARSE_DEBUG=False, dataSetBase=None, extensionFunctions={}, USE_PYPARSING=False, dSCompliance=False, loadContexts=False):
        initNs.update({'rdfs': RDFS.uri, 'owl': str(OWL), 'rdf': RDF.uri})
        if not isinstance(strOrQuery, (basestring, Query)):
            raise AssertionError('%s must be a string or an rdfextras.sparql.components.Query instance' % strOrQuery)
            if isinstance(strOrQuery, basestring):
                strOrQuery = rdfextras.sparql.parser.parse(strOrQuery)
            strOrQuery.prolog = strOrQuery.prolog or Prolog(None, [])
            strOrQuery.prolog.prefixBindings.update(initNs)
        else:
            for prefix, nsInst in initNs.items():
                if prefix not in strOrQuery.prolog.prefixBindings:
                    strOrQuery.prolog.prefixBindings[prefix] = nsInst

        return TopEvaluate(strOrQuery, self.graph, initBindings, DEBUG=DEBUG, dataSetBase=dataSetBase, extensionFunctions=extensionFunctions, dSCompliance=dSCompliance, loadContexts=loadContexts)
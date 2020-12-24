# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/n3p/parser.py
# Compiled at: 2008-04-06 12:20:54
from rdf.parser import Parser
from rdf.term import URIRef, BNode, Literal, Variable
from rdf.graph import Graph, QuotedGraph, ConjunctiveGraph
from rdf.plugins.parsers.n3p.n3proc import N3Processor

class N3(Parser):

    def __init__(self):
        pass

    def parse(self, source, graph):
        assert graph.store.context_aware, 'graph not context aware as required'
        assert graph.store.formula_aware, 'graph not formula aware as required'
        conj_graph = ConjunctiveGraph(store=graph.store)
        conj_graph.default_context = graph
        sink = Sink(conj_graph)
        if False:
            sink.quantify = lambda *args: True
            sink.flatten = lambda *args: True
        baseURI = graph.absolutize(source.getPublicId() or source.getSystemId() or '')
        p = N3Processor('nowhere', sink, baseURI=baseURI)
        p.userkeys = True
        p.data = source.getByteStream().read()
        p.parse()
        for (prefix, namespace) in p.bindings.items():
            conj_graph.bind(prefix, namespace)


class Sink(object):

    def __init__(self, graph):
        self.graph = graph

    def start(self, root):
        pass

    def statement(self, s, p, o, f):
        f.add((s, p, o))

    def quantify(self, formula, var):
        pass
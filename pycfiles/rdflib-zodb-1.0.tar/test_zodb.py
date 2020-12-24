# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/s2616794/Documents/Projects/Uni/workspace_rdflib/rdflib-zodb/test/test_zodb.py
# Compiled at: 2014-02-26 17:10:12
try:
    import ZODB, transaction
except ImportError:
    ZODB = False

import logging
_logger = logging.getLogger(__name__)
import os
from rdflib import RDF, URIRef, BNode, ConjunctiveGraph, Graph
import graph_case, context_case

class ZODBGraphTestCase(graph_case.GraphTestCase):
    store_name = 'ZODB'
    storetest = True
    path = '/tmp/zodb_local2.fs'
    url = 'file:///tmp/zodb_local2.fs'
    conn = None

    def initConnection(self, clear=True):
        if not (self.conn and self.conn.opened):
            if self.url.endswith('.fs'):
                from ZODB.FileStorage import FileStorage
                if clear and os.path.exists(self.path):
                    os.unlink('/tmp/zodb_local2.fs')
                    os.unlink('/tmp/zodb_local2.fs.index')
                    os.unlink('/tmp/zodb_local2.fs.tmp')
                    os.unlink('/tmp/zodb_local2.fs.lock')
                openstr = os.path.abspath(os.path.expanduser(self.url[7:]))
                fs = FileStorage(openstr)
            else:
                from ZEO.ClientStorage import ClientStorage
                schema, opts = _parse_rfc1738_args(self.url)
                fs = ClientStorage((opts['host'], int(opts['port'])))
            self.zdb = ZODB.DB(fs)
            self.conn = self.zdb.open()
        root = self.conn.root()
        if 'rdflib' not in root:
            root['rdflib'] = ConjunctiveGraph(self.store_name)
        self.graph = self.g = root['rdflib']
        transaction.commit()

    def setUp(self):
        self.initConnection()
        self.michel = URIRef('michel')
        self.tarek = URIRef('tarek')
        self.bob = URIRef('bob')
        self.likes = URIRef('likes')
        self.hates = URIRef('hates')
        self.pizza = URIRef('pizza')
        self.cheese = URIRef('cheese')
        transaction.begin()

    def tearDown(self):
        self.graph.close()
        try:
            transaction.commit()
        except Exception as e:
            transaction.abort()

        self.conn.close()
        self.zdb.close()
        os.unlink('/tmp/zodb_local2.fs')
        os.unlink('/tmp/zodb_local2.fs.index')
        os.unlink('/tmp/zodb_local2.fs.tmp')
        os.unlink('/tmp/zodb_local2.fs.lock')

    def addStuff(self):
        tarek = self.tarek
        michel = self.michel
        bob = self.bob
        likes = self.likes
        hates = self.hates
        pizza = self.pizza
        cheese = self.cheese
        self.graph.add((tarek, likes, pizza))
        self.graph.add((tarek, likes, cheese))
        self.graph.add((michel, likes, pizza))
        self.graph.add((michel, likes, cheese))
        self.graph.add((bob, likes, cheese))
        self.graph.add((bob, hates, pizza))
        self.graph.add((bob, hates, michel))
        transaction.commit()

    def removeStuff(self):
        tarek = self.tarek
        michel = self.michel
        bob = self.bob
        likes = self.likes
        hates = self.hates
        pizza = self.pizza
        cheese = self.cheese
        self.graph.remove((tarek, likes, pizza))
        self.graph.remove((tarek, likes, cheese))
        self.graph.remove((michel, likes, pizza))
        self.graph.remove((michel, likes, cheese))
        self.graph.remove((bob, likes, cheese))
        self.graph.remove((bob, hates, pizza))
        self.graph.remove((bob, hates, michel))
        transaction.commit()

    def testAdd(self):
        self.addStuff()

    def testRemove(self):
        self.addStuff()
        self.removeStuff()

    def testTriples(self):
        tarek = self.tarek
        michel = self.michel
        bob = self.bob
        likes = self.likes
        hates = self.hates
        pizza = self.pizza
        cheese = self.cheese
        asserte = self.assertEquals
        triples = self.graph.triples
        Any = None
        self.addStuff()
        asserte(len(list(triples((Any, likes, pizza)))), 2)
        asserte(len(list(triples((Any, hates, pizza)))), 1)
        asserte(len(list(triples((Any, likes, cheese)))), 3)
        asserte(len(list(triples((Any, hates, cheese)))), 0)
        asserte(len(list(triples((michel, likes, Any)))), 2)
        asserte(len(list(triples((tarek, likes, Any)))), 2)
        asserte(len(list(triples((bob, hates, Any)))), 2)
        asserte(len(list(triples((bob, likes, Any)))), 1)
        asserte(len(list(triples((michel, Any, cheese)))), 1)
        asserte(len(list(triples((tarek, Any, cheese)))), 1)
        asserte(len(list(triples((bob, Any, pizza)))), 1)
        asserte(len(list(triples((bob, Any, michel)))), 1)
        asserte(len(list(triples((Any, hates, Any)))), 2)
        asserte(len(list(triples((Any, likes, Any)))), 5)
        asserte(len(list(triples((michel, Any, Any)))), 2)
        asserte(len(list(triples((bob, Any, Any)))), 3)
        asserte(len(list(triples((tarek, Any, Any)))), 2)
        asserte(len(list(triples((Any, Any, pizza)))), 3)
        asserte(len(list(triples((Any, Any, cheese)))), 3)
        asserte(len(list(triples((Any, Any, michel)))), 1)
        asserte(len(list(triples((Any, Any, Any)))), 7)
        self.removeStuff()
        asserte(len(list(triples((Any, Any, Any)))), 0)
        return

    def testStatementNode(self):
        graph = self.graph
        from rdflib.term import Statement
        c = URIRef('http://example.org/foo#c')
        r = URIRef('http://example.org/foo#r')
        s = Statement((self.michel, self.likes, self.pizza), c)
        graph.add((s, RDF.value, r))
        self.assertEquals(r, graph.value(s, RDF.value))
        self.assertEquals(s, graph.value(predicate=RDF.value, object=r))


class ZODBContextTestCase(context_case.ContextTestCase):
    store_name = 'ZODB'
    storetest = True
    path = '/tmp/zodb_local3.fs'
    url = 'file:///tmp/zodb_local3.fs'

    def setUp(self):
        if self.url.endswith('.fs'):
            from ZODB.FileStorage import FileStorage
            if os.path.exists(self.path):
                os.unlink('/tmp/zodb_local3.fs')
                os.unlink('/tmp/zodb_local3.fs.index')
                os.unlink('/tmp/zodb_local3.fs.tmp')
                os.unlink('/tmp/zodb_local3.fs.lock')
            openstr = os.path.abspath(os.path.expanduser(self.url[7:]))
            fs = FileStorage(openstr)
        else:
            from ZEO.ClientStorage import ClientStorage
            schema, opts = _parse_rfc1738_args(self.url)
            fs = ClientStorage((opts['host'], int(opts['port'])))
        self.zdb = ZODB.DB(fs)
        self.conn = self.zdb.open()
        root = self.conn.root()
        if 'rdflib' not in root:
            root['rdflib'] = ConjunctiveGraph(self.store_name)
        self.graph = self.g = root['rdflib']
        self.michel = URIRef('michel')
        self.tarek = URIRef('tarek')
        self.bob = URIRef('bob')
        self.likes = URIRef('likes')
        self.hates = URIRef('hates')
        self.pizza = URIRef('pizza')
        self.cheese = URIRef('cheese')
        transaction.commit()

    def tearDown(self):
        self.graph.close()
        transaction.commit()
        self.conn.close()
        self.zdb.close()
        os.unlink('/tmp/zodb_local3.fs')
        os.unlink('/tmp/zodb_local3.fs.index')
        os.unlink('/tmp/zodb_local3.fs.tmp')
        os.unlink('/tmp/zodb_local3.fs.lock')

    def get_context(self, identifier):
        assert isinstance(identifier, URIRef) or isinstance(identifier, BNode), type(identifier)
        return Graph(store=self.graph.store, identifier=identifier, namespace_manager=self)

    def addStuff(self):
        tarek = self.tarek
        michel = self.michel
        bob = self.bob
        likes = self.likes
        hates = self.hates
        pizza = self.pizza
        cheese = self.cheese
        c1 = self.c1
        graph = Graph(self.graph.store, c1)
        graph.add((tarek, likes, pizza))
        graph.add((tarek, likes, cheese))
        graph.add((michel, likes, pizza))
        graph.add((michel, likes, cheese))
        graph.add((bob, likes, cheese))
        graph.add((bob, hates, pizza))
        graph.add((bob, hates, michel))
        transaction.commit()

    def removeStuff(self):
        tarek = self.tarek
        michel = self.michel
        bob = self.bob
        likes = self.likes
        hates = self.hates
        pizza = self.pizza
        cheese = self.cheese
        c1 = self.c1
        graph = Graph(self.graph.store, c1)
        graph.remove((tarek, likes, pizza))
        graph.remove((tarek, likes, cheese))
        graph.remove((michel, likes, pizza))
        graph.remove((michel, likes, cheese))
        graph.remove((bob, likes, cheese))
        graph.remove((bob, hates, pizza))
        graph.remove((bob, hates, michel))
        transaction.commit()

    def addStuffInMultipleContexts(self):
        c1 = self.c1
        c2 = self.c2
        triple = (self.pizza, self.hates, self.tarek)
        self.graph.add(triple)
        graph = Graph(self.graph.store, c1)
        graph.add(triple)
        graph = Graph(self.graph.store, c2)
        graph.add(triple)

    def testConjunction(self):
        self.addStuffInMultipleContexts()
        triple = (self.pizza, self.likes, self.pizza)
        graph = Graph(self.graph.store, self.c1)
        graph.add(triple)
        self.assertEquals(len(self.graph), len(graph))

    def testAdd(self):
        self.addStuff()

    def testRemove(self):
        self.addStuff()
        self.removeStuff()

    def testLenInOneContext(self):
        c1 = self.c1
        self.graph.remove_context(self.get_context(c1))
        graph = Graph(self.graph.store, c1)
        oldLen = len(self.graph)
        for i in range(0, 10):
            graph.add((BNode(), self.hates, self.hates))

        self.assertEquals(len(graph), oldLen + 10)
        self.assertEquals(len(self.get_context(c1)), oldLen + 10)
        self.graph.remove_context(self.get_context(c1))
        self.assertEquals(len(self.graph), oldLen)
        self.assertEquals(len(graph), 0)

    def testLenInMultipleContexts(self):
        oldLen = len(self.graph)
        self.addStuffInMultipleContexts()
        self.assertEquals(len(self.graph), oldLen + 1)
        graph = Graph(self.graph.store, self.c1)
        self.assertEquals(len(graph), oldLen + 1)

    def testRemoveInMultipleContexts(self):
        c1 = self.c1
        c2 = self.c2
        triple = (self.pizza, self.hates, self.tarek)
        self.addStuffInMultipleContexts()
        self.assert_(triple in self.graph)
        graph = Graph(self.graph.store, c1)
        graph.remove(triple)
        self.assert_(triple in self.graph)
        graph = Graph(self.graph.store, c2)
        graph.remove(triple)
        self.assert_(triple in self.graph)
        self.graph.remove(triple)
        self.assert_(triple not in self.graph)
        self.addStuffInMultipleContexts()
        self.graph.remove(triple)
        self.assert_(triple not in self.graph)

    def testContexts(self):
        triple = (
         self.pizza, self.hates, self.tarek)
        self.addStuffInMultipleContexts()

        def cid(c):
            if not isinstance(c, basestring):
                return c.identifier
            return c

        self.assert_(self.c1 in map(cid, self.graph.contexts()))
        self.assert_(self.c2 in map(cid, self.graph.contexts()))
        contextList = map(cid, list(self.graph.contexts(triple)))
        self.assert_(self.c1 in contextList)
        self.assert_(self.c2 in contextList)

    def testRemoveContext(self):
        c1 = self.c1
        self.addStuffInMultipleContexts()
        self.assertEquals(len(Graph(self.graph.store, c1)), 1)
        self.assertEquals(len(self.get_context(c1)), 1)
        self.graph.remove_context(self.get_context(c1))
        self.assert_(self.c1 not in self.graph.contexts())

    def testRemoveAny(self):
        Any = None
        self.addStuffInMultipleContexts()
        self.graph.remove((Any, Any, Any))
        self.assertEquals(len(self.graph), 0)
        return

    def testTriples(self):
        tarek = self.tarek
        michel = self.michel
        bob = self.bob
        likes = self.likes
        hates = self.hates
        pizza = self.pizza
        cheese = self.cheese
        c1 = self.c1
        asserte = self.assertEquals
        triples = self.graph.triples
        graph = self.graph
        c1graph = Graph(self.graph.store, c1)
        c1triples = c1graph.triples
        Any = None
        self.addStuff()
        asserte(len(list(c1triples((Any, likes, pizza)))), 2)
        asserte(len(list(c1triples((Any, hates, pizza)))), 1)
        asserte(len(list(c1triples((Any, likes, cheese)))), 3)
        asserte(len(list(c1triples((Any, hates, cheese)))), 0)
        asserte(len(list(triples((Any, likes, pizza)))), 2)
        asserte(len(list(triples((Any, hates, pizza)))), 1)
        asserte(len(list(triples((Any, likes, cheese)))), 3)
        asserte(len(list(triples((Any, hates, cheese)))), 0)
        asserte(len(list(c1triples((michel, likes, Any)))), 2)
        asserte(len(list(c1triples((tarek, likes, Any)))), 2)
        asserte(len(list(c1triples((bob, hates, Any)))), 2)
        asserte(len(list(c1triples((bob, likes, Any)))), 1)
        asserte(len(list(triples((michel, likes, Any)))), 2)
        asserte(len(list(triples((tarek, likes, Any)))), 2)
        asserte(len(list(triples((bob, hates, Any)))), 2)
        asserte(len(list(triples((bob, likes, Any)))), 1)
        asserte(len(list(c1triples((michel, Any, cheese)))), 1)
        asserte(len(list(c1triples((tarek, Any, cheese)))), 1)
        asserte(len(list(c1triples((bob, Any, pizza)))), 1)
        asserte(len(list(c1triples((bob, Any, michel)))), 1)
        asserte(len(list(triples((michel, Any, cheese)))), 1)
        asserte(len(list(triples((tarek, Any, cheese)))), 1)
        asserte(len(list(triples((bob, Any, pizza)))), 1)
        asserte(len(list(triples((bob, Any, michel)))), 1)
        asserte(len(list(c1triples((Any, hates, Any)))), 2)
        asserte(len(list(c1triples((Any, likes, Any)))), 5)
        asserte(len(list(triples((Any, hates, Any)))), 2)
        asserte(len(list(triples((Any, likes, Any)))), 5)
        asserte(len(list(c1triples((michel, Any, Any)))), 2)
        asserte(len(list(c1triples((bob, Any, Any)))), 3)
        asserte(len(list(c1triples((tarek, Any, Any)))), 2)
        asserte(len(list(triples((michel, Any, Any)))), 2)
        asserte(len(list(triples((bob, Any, Any)))), 3)
        asserte(len(list(triples((tarek, Any, Any)))), 2)
        asserte(len(list(c1triples((Any, Any, pizza)))), 3)
        asserte(len(list(c1triples((Any, Any, cheese)))), 3)
        asserte(len(list(c1triples((Any, Any, michel)))), 1)
        asserte(len(list(triples((Any, Any, pizza)))), 3)
        asserte(len(list(triples((Any, Any, cheese)))), 3)
        asserte(len(list(triples((Any, Any, michel)))), 1)
        asserte(len(list(c1triples((Any, Any, Any)))), 7)
        asserte(len(list(triples((Any, Any, Any)))), 7)
        for c in [graph, self.get_context(c1)]:
            asserte(set(c.subjects(likes, pizza)), set((michel, tarek)))
            asserte(set(c.subjects(hates, pizza)), set((bob,)))
            asserte(set(c.subjects(likes, cheese)), set([tarek, bob, michel]))
            asserte(set(c.subjects(hates, cheese)), set())
            asserte(set(c.objects(michel, likes)), set([cheese, pizza]))
            asserte(set(c.objects(tarek, likes)), set([cheese, pizza]))
            asserte(set(c.objects(bob, hates)), set([michel, pizza]))
            asserte(set(c.objects(bob, likes)), set([cheese]))
            asserte(set(c.predicates(michel, cheese)), set([likes]))
            asserte(set(c.predicates(tarek, cheese)), set([likes]))
            asserte(set(c.predicates(bob, pizza)), set([hates]))
            asserte(set(c.predicates(bob, michel)), set([hates]))
            asserte(set(c.subject_objects(hates)), set([(bob, pizza), (bob, michel)]))
            asserte(set(c.subject_objects(likes)), set([(tarek, cheese), (michel, cheese), (michel, pizza), (bob, cheese), (tarek, pizza)]))
            asserte(set(c.predicate_objects(michel)), set([(likes, cheese), (likes, pizza)]))
            asserte(set(c.predicate_objects(bob)), set([(likes, cheese), (hates, pizza), (hates, michel)]))
            asserte(set(c.predicate_objects(tarek)), set([(likes, cheese), (likes, pizza)]))
            asserte(set(c.subject_predicates(pizza)), set([(bob, hates), (tarek, likes), (michel, likes)]))
            asserte(set(c.subject_predicates(cheese)), set([(bob, likes), (tarek, likes), (michel, likes)]))
            asserte(set(c.subject_predicates(michel)), set([(bob, hates)]))
            asserte(set(c), set([(bob, hates, michel), (bob, likes, cheese), (tarek, likes, pizza), (michel, likes, pizza), (michel, likes, cheese), (bob, hates, pizza), (tarek, likes, cheese)]))

        self.removeStuff()
        asserte(len(list(c1triples((Any, Any, Any)))), 0)
        asserte(len(list(triples((Any, Any, Any)))), 0)
        return


def load_tests(loader, tests, pattern):
    from unittest import TestSuite, TestLoader
    if not ZODB:
        from unittest import SkipTest
        raise SkipTest('ZODB not installed')
    suite = TestSuite()
    suite.addTests(TestLoader().loadTestsFromTestCase(ZODBGraphTestCase))
    suite.addTests(TestLoader().loadTestsFromTestCase(ZODBContextTestCase))
    return suite
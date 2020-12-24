# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_store/test_graph.py
# Compiled at: 2012-02-24 05:27:21
import unittest, BaseHTTPServer
from tempfile import mkdtemp
from tempfile import mkstemp
from rdflib import Graph
from rdflib import RDF
from rdflib import URIRef
import rdflib.plugin

class GraphTestCase(unittest.TestCase):
    store_name = 'default'
    path = None
    storetest = True
    create = True
    michel = URIRef('michel')
    tarek = URIRef('tarek')
    bob = URIRef('bob')
    likes = URIRef('likes')
    hates = URIRef('hates')
    pizza = URIRef('pizza')
    cheese = URIRef('cheese')

    def setUp(self):
        self.graph = Graph(store=self.store_name)
        self.graph.destroy(self.path)
        if isinstance(self.path, type(None)):
            if self.store_name == 'SQLite':
                self.path = mkstemp(prefix='test', dir='/tmp')
            else:
                self.path = mkdtemp(prefix='test', dir='/tmp')
        self.graph.open(self.path, create=self.create)
        return

    def tearDown(self):
        self.graph.destroy(self.path)
        try:
            self.graph.close()
        except:
            pass

        import os
        if hasattr(self, 'path') and self.path is not None:
            if os.path.exists(self.path):
                if os.path.isdir(self.path):
                    for f in os.listdir(self.path):
                        os.unlink(self.path + '/' + f)

                    os.rmdir(self.path)
                elif len(self.path.split(':')) == 1:
                    os.unlink(self.path)
                else:
                    os.remove(self.path)
        return

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
        self.graph.commit()

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

    def testGraphValue(self):
        from rdflib.graph import GraphValue
        graph = self.graph
        alice = URIRef('alice')
        bob = URIRef('bob')
        pizza = URIRef('pizza')
        cheese = URIRef('cheese')
        g1 = Graph()
        g1.add((alice, RDF.value, pizza))
        g1.add((bob, RDF.value, cheese))
        g1.add((bob, RDF.value, pizza))
        g2 = Graph()
        g2.add((bob, RDF.value, pizza))
        g2.add((bob, RDF.value, cheese))
        g2.add((alice, RDF.value, pizza))
        gv1 = GraphValue(store=graph.store, graph=g1)
        gv2 = GraphValue(store=graph.store, graph=g2)
        graph.add((gv1, RDF.value, gv2))
        v = graph.value(gv1)
        self.assertEquals(gv2, v)
        graph.remove((gv1, RDF.value, gv2))

    def testConnected(self):
        graph = self.graph
        self.addStuff()
        self.assertEquals(True, graph.connected())
        jeroen = URIRef('jeroen')
        unconnected = URIRef('unconnected')
        graph.add((jeroen, self.likes, unconnected))
        self.assertEquals(False, graph.connected())

    def testSub(self):
        g1 = Graph()
        g2 = Graph()
        tarek = self.tarek
        michel = self.michel
        bob = self.bob
        likes = self.likes
        hates = self.hates
        pizza = self.pizza
        cheese = self.cheese
        g1.add((tarek, likes, pizza))
        g1.add((bob, likes, cheese))
        g2.add((bob, likes, cheese))
        g3 = g1 - g2
        self.assertEquals(len(g3), 1)
        self.assertEquals((tarek, likes, pizza) in g3, True)
        self.assertEquals((tarek, likes, cheese) in g3, False)
        self.assertEquals((bob, likes, cheese) in g3, False)
        g1 -= g2
        self.assertEquals(len(g1), 1)
        self.assertEquals((tarek, likes, pizza) in g1, True)
        self.assertEquals((tarek, likes, cheese) in g1, False)
        self.assertEquals((bob, likes, cheese) in g1, False)

    def testGraphAdd(self):
        g1 = Graph()
        g2 = Graph()
        tarek = self.tarek
        michel = self.michel
        bob = self.bob
        likes = self.likes
        hates = self.hates
        pizza = self.pizza
        cheese = self.cheese
        g1.add((tarek, likes, pizza))
        g2.add((bob, likes, cheese))
        g3 = g1 + g2
        self.assertEquals(len(g3), 2)
        self.assertEquals((tarek, likes, pizza) in g3, True)
        self.assertEquals((tarek, likes, cheese) in g3, False)
        self.assertEquals((bob, likes, cheese) in g3, True)
        g1 += g2
        self.assertEquals(len(g1), 2)
        self.assertEquals((tarek, likes, pizza) in g1, True)
        self.assertEquals((tarek, likes, cheese) in g1, False)
        self.assertEquals((bob, likes, cheese) in g1, True)

    def testGraphIntersection(self):
        g1 = Graph()
        g2 = Graph()
        tarek = self.tarek
        michel = self.michel
        bob = self.bob
        likes = self.likes
        hates = self.hates
        pizza = self.pizza
        cheese = self.cheese
        g1.add((tarek, likes, pizza))
        g1.add((michel, likes, cheese))
        g2.add((bob, likes, cheese))
        g2.add((michel, likes, cheese))
        g3 = g1 * g2
        self.assertEquals(len(g3), 1)
        self.assertEquals((tarek, likes, pizza) in g3, False)
        self.assertEquals((tarek, likes, cheese) in g3, False)
        self.assertEquals((bob, likes, cheese) in g3, False)
        self.assertEquals((michel, likes, cheese) in g3, True)
        g1 *= g2
        self.assertEquals(len(g1), 1)
        self.assertEquals((tarek, likes, pizza) in g1, False)
        self.assertEquals((tarek, likes, cheese) in g1, False)
        self.assertEquals((bob, likes, cheese) in g1, False)
        self.assertEquals((michel, likes, cheese) in g1, True)

    def testFinalNewline(self):
        """
        http://code.google.com/p/rdflib/issues/detail?id=5
        """
        pass

    def testConNeg(self):
        pass


xmltestdoc = '<?xml version="1.0" encoding="UTF-8"?>\n<rdf:RDF\n   xmlns="http://example.org/"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n>\n  <rdf:Description rdf:about="http://example.org/a">\n    <b rdf:resource="http://example.org/c"/>\n  </rdf:Description>\n</rdf:RDF>\n'
n3testdoc = '@prefix : <http://example.org/> .\n\n:a :b :c .\n'
nttestdoc = '<http://example.org/a> <http://example.org/b> <http://example.org/c> .\n'

class TestHTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200, 'OK')
        acs = self.headers['Accept'].split(',')
        acq = [ x.split(';') for x in acs if ';' in x ]
        acn = [ (x, 'q=1') for x in acs if ';' not in x ]
        acs = [ (x[0], float(x[1].strip()[2:])) for x in acq + acn ]
        ac = sorted(acs, key=lambda x: x[1])
        ct = ac[(-1)]
        if 'application/rdf+xml' in ct:
            rct = 'application/rdf+xml'
            content = xmltestdoc
        elif 'text/n3' in ct:
            rct = 'text/n3'
            content = n3testdoc
        elif 'text/plain' in ct:
            rct = 'text/plain'
            content = nttestdoc
        self.send_header('Content-type', rct)
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, *args):
        pass


def runHttpServer(server_class=BaseHTTPServer.HTTPServer, handler_class=TestHTTPHandler):
    """Start a server than can handle 3 requests :)"""
    server_address = ('localhost', 12345)
    httpd = server_class(server_address, handler_class)
    httpd.handle_request()
    httpd.handle_request()
    httpd.handle_request()


if __name__ == '__main__':
    unittest.main()
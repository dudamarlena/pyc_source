# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/s2616794/Documents/Projects/Uni/workspace_rdflib/rdflib-zodb/test/test_store_performance.py
# Compiled at: 2014-02-26 17:10:12
import unittest, gc, os, itertools
from time import time
from random import random
from tempfile import mkdtemp
from rdflib import Graph
from rdflib import URIRef

def random_uri():
    return URIRef('%s' % random())


class StoreTestCase(unittest.TestCase):
    """
    Test case for testing store performance... probably should be
    something other than a unit test... but for now we'll add it as a
    unit test.
    """
    store = 'IOMemory'
    path = None
    storetest = True
    performancetest = True

    def setUp(self):
        self.gcold = gc.isenabled()
        gc.collect()
        gc.disable()
        self.graph = Graph(store=self.store)
        if not self.path:
            path = mkdtemp()
        else:
            path = self.path
        self.path = path
        self.graph.open(self.path, create=True)
        self.input = Graph()

    def tearDown(self):
        self.graph.close()
        if self.gcold:
            gc.enable()
        self.graph.close()
        del self.graph
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

    def testTime(self):
        print '"Load %s": [' % self.store
        for i in ['500triples', '1ktriples', '2ktriples',
         '3ktriples', '5ktriples', '10ktriples',
         '25ktriples']:
            inputloc = os.getcwd() + '/test/sp2b/%s.n3' % i
            self.input = Graph()
            self.graph.remove((None, None, None))
            res = self._testInput(inputloc)
            print 'Loaded %5d triples in %ss' % (len(self.graph), res.strip())

        print '],'
        print '"Read %s": [' % self.store
        t0 = time()
        for _i in self.graph.triples((None, None, None)):
            pass

        self.assertEqual(len(self.graph), 25161)
        t1 = time()
        print '%.3gs' % (t1 - t0)
        print '],'
        print '"Delete %s": [' % self.store
        t0 = time()
        self.graph.remove((None, None, None))
        self.assertEqual(len(self.graph), 0)
        t1 = time()
        print '%.3g ' % (t1 - t0)
        print '],'
        return

    def _testInput(self, inputloc):
        number = 1
        store = self.graph
        self.input.parse(location=inputloc, format='n3')

        def add_from_input():
            for t in self.input:
                store.add(t)

        it = itertools.repeat(None, number)
        t0 = time()
        for _i in it:
            add_from_input()

        t1 = time()
        return '%.3g ' % (t1 - t0)


class ZODBStoreTestCase(StoreTestCase):
    non_standard_dep = True
    store = 'ZODB'

    def setUp(self):
        self.store = 'ZODB'
        self.path = '/tmp/zodbtest'
        StoreTestCase.setUp(self)


if __name__ == '__main__':
    unittest.main()
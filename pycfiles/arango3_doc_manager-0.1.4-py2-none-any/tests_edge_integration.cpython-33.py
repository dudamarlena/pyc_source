# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/tests/tests_edge_integration.py
# Compiled at: 2013-03-08 14:06:20
# Size of source mod 2**32: 2290 bytes
import logging
from nose.tools import assert_equal, raises
from arango.collection import Collection
from .tests_integraion_base import TestsIntegration
logger = logging.getLogger(__name__)
__all__ = ('TestsEdge', )

class TestsEdge(TestsIntegration):

    def setUp(self):
        super(TestsEdge, self).setUp()
        self.c = self.conn.collection
        self.c.test.create(type=Collection.TYPE_EDGE)
        body = {'key': 1}
        self.from_doc = self.c.test.documents.create(body)
        self.to_doc = self.c.test.documents.create(body)

    def tearDown(self):
        super(TestsEdge, self).tearDown()
        c = self.conn
        c.collection.test.delete()

    @raises(NotImplementedError)
    def test_edge_creation(self):
        self.c.test.edges.create(self.from_doc, self.to_doc, {'custom': 1})
        result = self.c.test.edges(self.from_doc, direction='out').first
        assert_equal(result.to_document, self.to_doc)
        assert_equal(self.c.test.edges(self.from_doc, direction='in').first, None)
        return

    @raises(NotImplementedError)
    def test_edge_deletion(self):
        self.c.test.edges.create(self.from_doc, self.to_doc, {'custom': 1})
        self.c.test.edges(self.from_doc).first.delete()
        assert_equal(self.c.test.edges(self.from_doc).first, None)
        return

    @raises(NotImplementedError)
    def test_edge_update(self):
        self.c.test.edges.create(self.from_doc, self.to_doc, {'custom': 1})
        new_doc = self.c.test.documents.create({'value': 2})
        edge = self.c.test.edges(self.from_doc).first
        edge.update(edge.body, from_doc=edge.from_document, to_doc=new_doc, save=True)
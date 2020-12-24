# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/oort/test/test_rdfview_context.py
# Compiled at: 2007-10-07 09:19:29
from rdflib import Literal
from oort.rdfview import QueryContext
from oort.test.test_rdfview import T, testgraph, itemX, Item
from oort.test import test_rdfview

class TypedItem(Item):
    RDF_TYPE = T.Item


class TestQueryContext:

    def test_by_attr(self):
        context = QueryContext(testgraph, 'en', query_modules=[test_rdfview])
        item = context.Item(itemX)
        self.assert_item_stuff(item)

    def test_find_all(self):
        context = QueryContext(testgraph, 'en', queries=[TypedItem])
        items = context.TypedItem.find_all()
        assert itemX in [ item.uri for item in items ]

    def test_by_find(self):
        context = QueryContext(testgraph, 'en', queries=[Item, TypedItem])
        item = context.view_for(itemX)
        assert isinstance(item, TypedItem)
        self.assert_item_stuff(item)

    def test_by_attr_and_find_by(self):
        context = QueryContext(testgraph, 'en', queries=[Item])
        found = context.Item.find_by(name=Literal('Item X'))
        assert list(found)[0].uri == itemX

    def test_callable_lang(self):

        def getlang():
            return 'en'

        context = QueryContext(testgraph, getlang, queries=[Item])
        item = context.Item(itemX)
        self.assert_item_stuff(item)

    def assert_item_stuff(self, item):
        assert item.uri == itemX, 'Unexpected uri: %r' % item.uri
        assert item.title == Literal('Example Item', 'en'), 'Unexpected title: %r' % item.title
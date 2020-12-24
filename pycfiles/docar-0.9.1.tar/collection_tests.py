# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/crito/Work/docar/tests/collection_tests.py
# Compiled at: 2012-09-26 08:45:40
from nose.tools import eq_, assert_raises
from .factory import Newspaper, Article
from .factory import article_factory, collection_factory
from docar import Collection
from docar.exceptions import CollectionNotBound
import unittest

class when_you_instantiate_a_collection_of_documents(unittest.TestCase):
    """Users interact with collections using a defined API."""

    def it_needs_to_be_bound_to_a_document(self):
        """Not binding a collection to a document, raises an exception."""

        class Coll(Collection):
            pass

        assert_raises(CollectionNotBound, Coll)

    def it_can_take_a_list_of_documents_at_initialization_time(self):
        """Initialize a new collection with a list of documents."""
        article = article_factory()
        newspaper = Newspaper([article])
        eq_(1, len(newspaper.collection_set))

    def it_can_create_collections_from_a_dict(self):
        """Create a collection by feeding it a dict."""
        data = [{'id': 1, 'title': 'article title', 'slug': 'article-slug', 'editor': {'id': 1, 'name': 'Jules Vernes'}}, {'id': 1, 'title': 'article 2 title', 'slug': 'article-slug', 'editor': {'id': 1, 'name': 'Jules Vernes'}}, {'id': 1, 'title': 'article 3 title', 'slug': 'article-slug', 'editor': {'id': 1, 'name': 'H.G. Wells'}}]
        newspaper = Newspaper()
        newspaper.from_dict(data)
        eq_(3, len(newspaper.collection_set))

    def it_can_turn_itself_into_a_dict(self):
        """Serialize a collection into a dict."""
        newspaper = collection_factory()
        expected = [{'id': 1, 'title': 'article title', 'slug': 'article-slug', 'editor': {'id': 1, 'name': 'Jules Vernes'}}, {'id': 1, 'title': 'article 2 title', 'slug': 'article-slug', 'editor': {'id': 1, 'name': 'Jules Vernes'}}, {'id': 1, 'title': 'article 3 title', 'slug': 'article-slug', 'editor': {'id': 1, 'name': 'H.G. Wells'}}]
        eq_(expected, newspaper.to_dict())

    def it_normalizes_the_collection_when_rendering(self):
        """Normalize the collection when rendering."""
        newspaper = collection_factory()
        expected = [{'title': 'article title', 'slug': 'article-slug', 'editor': {'name': 'Jules Vernes'}}, {'title': 'article 2 title', 'slug': 'article-slug', 'editor': {'name': 'Jules Vernes'}}, {'title': 'article 3 title', 'slug': 'article-slug', 'editor': {'name': 'H.G. Wells'}}]
        eq_(expected, newspaper.render())

    def it_can_add_documents(self):
        """Add documents to a collection."""
        newspaper = Newspaper()
        eq_(0, len(newspaper.collection_set))
        article = article_factory()
        newspaper.add(article)
        eq_(1, len(newspaper.collection_set))

    def it_does_not_add_items_to_the_collection_that_are_not_documents(self):
        """Only documents can be added to a collection."""
        newspaper = Newspaper()
        eq_(0, len(newspaper.collection_set))
        newspaper.add(type('Klass', (), {}))
        eq_(0, len(newspaper.collection_set))

    def it_can_delete_documents(self):
        """Delete documents from the collection."""
        newspaper = Newspaper()
        newspaper.collection_set.append(Article({'id': 3}))
        newspaper.delete({'id': 3})
        eq_(0, len(newspaper.collection_set))

    def it_stores_documents_in_the_collection_set(self):
        """Internally the documents are stored in a list."""
        newspaper = Newspaper()
        eq_(0, len(newspaper.collection_set))
        eq_(True, isinstance(newspaper.collection_set, list))
        article = article_factory()
        newspaper.add(article)
        eq_(1, len(newspaper.collection_set))
        eq_(True, isinstance(newspaper.collection_set, list))
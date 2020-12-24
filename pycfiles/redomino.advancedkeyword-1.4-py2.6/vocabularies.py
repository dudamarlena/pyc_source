# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redomino/advancedkeyword/vocabularies.py
# Compiled at: 2013-05-08 04:41:18
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from Products.CMFCore.utils import getToolByName

class KeywordsVocabulary(object):
    """Vocabulary factory listing all catalog keywords from the "Subject" index

        >>> from redomino.advancedkeyword.tests.utils import DummyCatalog
        >>> from redomino.advancedkeyword.tests.utils import create_context
        >>> from redomino.advancedkeyword.tests.utils import DummyContent
        >>> from redomino.advancedkeyword.tests.utils import Request
        >>> from Products.PluginIndexes.KeywordIndex.KeywordIndex import KeywordIndex

        >>> context = create_context()

        >>> rids = ('/1234', '/2345', '/dummy/1234')
        >>> tool = DummyCatalog(rids)
        >>> context.portal_catalog = tool
        >>> index = KeywordIndex('Subject')
        >>> done = index._index_object(1,DummyContent('ob1', ['foo', 'bar', 'baz']), attr='Subject')
        >>> done = index._index_object(2,DummyContent('ob2', ['blee', 'bar']), attr='Subject')
        >>> tool.indexes['Subject'] = index
        >>> vocab = KeywordsVocabulary()
        >>> result = vocab(context)
        >>> result.by_token.keys()
        ['blee', 'baz', 'foo', 'bar']
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        self.context = context
        self.catalog = getToolByName(context, 'portal_catalog')
        if self.catalog is None:
            return SimpleVocabulary([])
        else:
            index = self.catalog._catalog.getIndex('Subject')
            items = [ SimpleTerm(i, i.decode('utf-8').encode('ascii', 'ignore'), i) for i in index._index ]
            return SimpleVocabulary(items)


KeywordsVocabularyFactory = KeywordsVocabulary()
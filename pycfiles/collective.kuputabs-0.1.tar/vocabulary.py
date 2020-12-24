# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/kss/flygui/vocabulary.py
# Compiled at: 2008-05-01 14:12:35
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.app.schema.vocabulary import IVocabularyFactory
from Products.CMFCore.utils import getToolByName

class PortalTypesVocabulary(object):
    """Vocabulary factory listig portal types
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        ttool = getToolByName(context, 'portal_types', None)
        items = [ SimpleTerm(t, t, '%s [%s]' % (ttool[t].Title(), ttool[t].getId())) for t in ttool.listContentTypes()
                ]
        return SimpleVocabulary(items)


PortalTypesVocabularyFactory = PortalTypesVocabulary()
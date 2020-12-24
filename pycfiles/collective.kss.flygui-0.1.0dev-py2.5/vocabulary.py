# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
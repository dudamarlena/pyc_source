# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fez/atcsv/vocabularies.py
# Compiled at: 2009-01-26 07:22:20
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.interface import implements

class AddableContentTypes(object):
    __module__ = __name__
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        omit = context
        items = [ ctype for ctype in context.getAllowedTypes() if ctype.id not in context.getNotAddableTypes() ]
        items.sort(lambda x, y: cmp(x.Title(), y.Title()))
        items = [ SimpleTerm(ctype, ctype.getId(), ctype.Title()) for ctype in items ]
        return SimpleVocabulary(items)


AddableContentTypesFactory = AddableContentTypes()
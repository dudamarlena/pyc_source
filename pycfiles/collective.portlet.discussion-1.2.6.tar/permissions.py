# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/collective/portlet/debuginfo/permissions.py
# Compiled at: 2009-02-05 06:53:22
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName

class PermissionsVocabulary(object):
    """Vocabulary factory for permissions.

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> name = 'collective.portlet.debuginfo.vocabularies.Permissions'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context1 = DummyContext()
      >>> context2 = DummyContext()
      >>> context1.context = context2

      >>> permissions = util(context1)
      >>> permissions
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(permissions.by_token) > 0
      True

      >>> perm = permissions.by_token['View']
      >>> perm.title, perm.token, perm.value
      ('View', 'View', 'View')
    """
    __module__ = __name__
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        items = context.possible_permissions()
        items.sort()
        items = [ SimpleTerm(i, i, i) for i in items ]
        return SimpleVocabulary(items)


PermissionsVocabularyFactory = PermissionsVocabulary()
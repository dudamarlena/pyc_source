# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simplon/plone/ldap/engine/vocabulary.py
# Compiled at: 2007-11-14 08:14:44
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.component import getUtility
from simplon.plone.ldap.engine.interfaces import ILDAPConfiguration
import ldap

class LDAPServerTypeVocabulary(object):
    """Vocabulary factory for LDAP server types.
    """
    __module__ = __name__
    implements(IVocabularyFactory)

    def __call__(self, context):
        return SimpleVocabulary([SimpleTerm('LDAP', 'LDAP'), SimpleTerm('AD', 'Active Directory')])


LDAPServerTypeVocabularyFactory = LDAPServerTypeVocabulary()

class LDAPConnectionTypeVocabulary(object):
    """Vocabulary factory for LDAP connection types.
    """
    __module__ = __name__
    implements(IVocabularyFactory)

    def __call__(self, context):
        return SimpleVocabulary([SimpleTerm(0, 'LDAP'), SimpleTerm(1, 'LDAP over SSL'), SimpleTerm(2, 'LDAP over IPC')])


LDAPConnectionTypeVocabularyFactory = LDAPConnectionTypeVocabulary()

class LDAPScopeVocabulary(object):
    """Vocabulary factory for LDAP search scopes.
    """
    __module__ = __name__
    implements(IVocabularyFactory)

    def __call__(self, context):
        return SimpleVocabulary([SimpleTerm(ldap.SCOPE_ONELEVEL, 'one level'), SimpleTerm(ldap.SCOPE_SUBTREE, 'subtree')])


LDAPScopeVocabularyFactory = LDAPScopeVocabulary()

class LDAPAttributesVocabulary(object):
    """Vocabulary factory for LDAP attributes.
    """
    __module__ = __name__
    implements(IVocabularyFactory)

    def __call__(self, context):
        config = getUtility(ILDAPConfiguration)
        attributes = [ (a.ldap_name, a.__name__) for a in config.schema.values() ]
        return SimpleVocabulary.fromItems(sorted(attributes))


LDAPAttributesVocabularyFactory = LDAPAttributesVocabulary()

class LDAPSinglueValueAttributesVocabulary(object):
    """Vocabulary factory for LDAP attributes.
    """
    __module__ = __name__
    implements(IVocabularyFactory)

    def __call__(self, context):
        config = getUtility(ILDAPConfiguration)
        attributes = [ (a.ldap_name, a.__name__) for a in config.schema.values() if not a.multi_valued ]
        return SimpleVocabulary.fromItems(sorted(attributes))


LDAPSingleValueAttributesVocabularyFactory = LDAPAttributesVocabulary()
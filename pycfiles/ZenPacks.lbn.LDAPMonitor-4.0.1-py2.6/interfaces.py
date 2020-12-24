# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/lbn/LDAPMonitor/interfaces.py
# Compiled at: 2013-02-02 18:23:57
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from Products.Zuul.interfaces import IBasicDataSourceInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t
PROTOS = SimpleVocabulary((SimpleTerm('ldap', 'ldap', 'ldap'),
 SimpleTerm('ldaps', 'ldaps', 'ldaps')))

class ILDAPDataSourceInfo(IBasicDataSourceInfo):
    """ connectivity info for a (remote) LDAP server """
    ldapProto = schema.Choice(title=_t('LDAP Protocol'), vocabulary=PROTOS)
    ldapPort = schema.Int(title=_t('LDAP Port (usually 389 or 636)'))
    ldapDN = schema.Text(title=_t('User (Distinguished Name)'))
    ldapPW = schema.Password(title=_t('Password'))
    timeout = schema.Int(title=_t('Connection Timeout (seconds)'))
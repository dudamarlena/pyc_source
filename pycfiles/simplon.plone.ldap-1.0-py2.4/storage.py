# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simplon/plone/ldap/engine/storage.py
# Compiled at: 2007-11-14 08:14:44
from Persistence import Persistent
from zope.interface import implements
from zope.app.container.ordered import OrderedContainer
from zope.app.container.interfaces import INameChooser
from simplon.plone.ldap.engine.interfaces import ILDAPServerStorage
from simplon.plone.ldap.engine.interfaces import ILDAPSchema
from simplon.plone.ldap.engine.interfaces import ILDAPConfiguration
from BTrees.OOBTree import OOBTree
from ldap import SCOPE_SUBTREE
from simplon.plone.ldap.engine.schema import LDAPProperty

class LDAPConfiguration(Persistent):
    __module__ = __name__
    implements(ILDAPConfiguration)
    ldap_type = 'LDAP'
    rdn_attribute = 'uid'
    userid_attribute = 'uid'
    login_attribute = 'uid'
    user_object_classes = 'pilotPerson'
    bind_dn = ''
    bind_password = ''
    user_base = ''
    user_scope = SCOPE_SUBTREE
    group_base = ''
    group_scope = SCOPE_SUBTREE

    def __init__(self):
        self.servers = LDAPServerStorage()
        self.schema = LDAPSchema()
        self.schema.addItem(LDAPProperty(ldap_name='uid', description='User id'))
        self.schema.addItem(LDAPProperty(ldap_name='mail', plone_name='email', description='Email address'))
        self.schema.addItem(LDAPProperty(ldap_name='cn', plone_name='fullname', description='Canonical Name'))
        self.schema.addItem(LDAPProperty(ldap_name='sn', description='Surname (unused)'))


class LDAPContainer(OrderedContainer):
    """Base class for our containers.
    """
    __module__ = __name__

    def __init__(self):
        OrderedContainer.__init__(self)
        self._data = OOBTree()

    def addItem(self, item):
        chooser = INameChooser(self)
        self[chooser.chooseName(None, item)] = item
        return


class LDAPServerStorage(LDAPContainer):
    """A container for LDAP servers.
    """
    __module__ = __name__
    implements(ILDAPServerStorage)


class LDAPSchema(LDAPContainer):
    """A container for LDAP properties.
    """
    __module__ = __name__
    implements(ILDAPSchema)
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simplon/plone/ldap/ploneldap/schema.py
# Compiled at: 2007-11-14 08:14:44
from zope.component import adapter
from simplon.plone.ldap.engine.interfaces import ILDAPProperty
from simplon.plone.ldap.ploneldap.util import guaranteePluginExists
from simplon.plone.ldap.ploneldap.util import getLDAPPlugin
from simplon.plone.ldap.ploneldap.util import configureLDAPSchema
from simplon.plone.ldap.ploneldap.util import addMandatorySchemaItems
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.app.container.interfaces import IObjectRemovedEvent

@adapter(ILDAPProperty, IObjectCreatedEvent)
def HandleCreated(property, event):
    if guaranteePluginExists():
        return
    luf = getLDAPPlugin()._getLDAPUserFolder()
    luf.manage_deleteLDAPSchemaItems([str(property.ldap_name)])
    luf.manage_addLDAPSchemaItem(ldap_name=str(property.ldap_name), friendly_name=property.description, public_name=str(property.plone_name), multivalued=property.multi_valued)


@adapter(ILDAPProperty, IObjectModifiedEvent)
def HandleModified(property, event):
    if guaranteePluginExists():
        return
    configureLDAPSchema()


@adapter(ILDAPProperty, IObjectRemovedEvent)
def HandleRemoved(property, event):
    if guaranteePluginExists():
        return
    luf = getLDAPPlugin()._getLDAPUserFolder()
    luf.manage_deleteLDAPSchemaItems([str(property.ldap_name)])
    addMandatorySchemaItems()
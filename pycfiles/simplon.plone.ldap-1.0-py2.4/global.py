# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simplon/plone/ldap/ploneldap/global.py
# Compiled at: 2007-11-14 08:14:44
from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from simplon.plone.ldap.engine.interfaces import ILDAPBinding
from simplon.plone.ldap.ploneldap.util import guaranteePluginExists
from simplon.plone.ldap.ploneldap.util import getLDAPPlugin

@adapter(ILDAPBinding, IObjectModifiedEvent)
def HandleModified(config, event):
    if guaranteePluginExists():
        return
    luf = getLDAPPlugin()._getLDAPUserFolder()
    luf.manage_edit(title='Plone managed LDAP', login_attr=str(config.schema[config.login_attribute].ldap_name), uid_attr=str(config.schema[config.userid_attribute].ldap_name), rdn_attr=str(config.schema[config.rdn_attribute].ldap_name), users_base=config.user_base or '', users_scope=config.user_scope, groups_base=config.group_base or '', groups_scope=config.group_scope, binduid=str(config.bind_dn) or '', bindpwd=str(config.bind_password) or '', roles='Member', obj_classes=config.user_object_classes)
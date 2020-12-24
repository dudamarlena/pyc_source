# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simplon/plone/ldap/ploneldap/server.py
# Compiled at: 2007-11-14 08:14:44
from zope.component import adapter
from simplon.plone.ldap.engine.interfaces import ILDAPServer
from simplon.plone.ldap.ploneldap.util import guaranteePluginExists
from simplon.plone.ldap.ploneldap.util import getLDAPPlugin
from simplon.plone.ldap.ploneldap.util import configureLDAPServers
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.app.container.interfaces import IObjectRemovedEvent

def FindServerIndex(luf, server):
    servers = luf.getServers()
    for i in range(len(servers)):
        if servers[i].host == server.server and servers[i].port == server.port:
            return i

    raise KeyError


@adapter(ILDAPServer, IObjectCreatedEvent)
def HandleCreated(server, event):
    if guaranteePluginExists():
        return
    if not server.enabled:
        return
    luf = getLDAPPlugin()._getLDAPUserFolder()
    luf.manage_addServer(host=server.server, port=server.port, use_ssl=server.connection_type, conn_timeout=server.connection_timeout, op_timeout=server.operation_timeout)


@adapter(ILDAPServer, IObjectModifiedEvent)
def HandleModified(server, event):
    if guaranteePluginExists():
        return
    configureLDAPServers()


@adapter(ILDAPServer, IObjectRemovedEvent)
def HandleRemoved(server, event):
    if guaranteePluginExists():
        return
    luf = getLDAPPlugin()._getLDAPUserFolder()
    servers = luf.getServers()
    for i in range(len(servers)):
        if servers[i].host == server.server and servers[i].port == server.port:
            luf.manage_deleteServers((i,))
            return
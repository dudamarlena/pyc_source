# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/iccommunity/mediawiki/preferences.py
# Compiled at: 2008-10-06 10:31:13
from string import strip
from Acquisition import aq_inner
from persistent import Persistent
from zope.interface import implements
from zope.component import getUtility
from OFS.SimpleItem import SimpleItem
from zope.schema.fieldproperty import FieldProperty
import interfaces

class icCommunityManagementMediawikiRolesMapper(SimpleItem):
    __module__ = __name__
    implements(interfaces.IicCommunityManagementMediawikiRolesMapper)
    rolemap = FieldProperty(interfaces.IicCommunityManagementMediawikiRolesMapper['rolemap'])

    def get_parsed_rolemap(self):
        """Returns a list of pairs containing a string for the Plone
        role and a string for the Mediawiki role.
        """
        pairs = []
        for item in self.rolemap:
            if item is not None:
                pairs += [tuple(map(strip, item.split(';')))]

        return pairs


def mediawiki_roles_form_adapter(context):
    return getUtility(interfaces.IicCommunityManagementMediawikiRolesMapper, name='iccommunity.configuration', context=context)


class icCommunityManagementMediawikiSQLServer(SimpleItem):
    __module__ = __name__
    implements(interfaces.IicCommunityManagementMediawikiSQLServer)
    hostname = FieldProperty(interfaces.IicCommunityManagementMediawikiSQLServer['hostname'])
    username = FieldProperty(interfaces.IicCommunityManagementMediawikiSQLServer['username'])
    password = FieldProperty(interfaces.IicCommunityManagementMediawikiSQLServer['password'])
    database = FieldProperty(interfaces.IicCommunityManagementMediawikiSQLServer['database'])
    dbprefix = FieldProperty(interfaces.IicCommunityManagementMediawikiSQLServer['dbprefix'])


def mediawiki_sql_server_adapter(context):
    return getUtility(interfaces.IicCommunityManagementMediawikiSQLServer, name='iccommunity.configuration', context=context)
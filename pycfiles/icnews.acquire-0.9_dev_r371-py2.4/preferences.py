# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icnews/acquire/preferences.py
# Compiled at: 2008-10-06 10:31:17
from Acquisition import aq_inner
from persistent import Persistent
from zope.interface import implements
from zope.component import getUtility
from OFS.SimpleItem import SimpleItem
from zope.schema.fieldproperty import FieldProperty
import interfaces

class icNewsManagementAcquireSQLServer(SimpleItem):
    __module__ = __name__
    implements(interfaces.IicNewsManagementAcquireSQLServer)
    hostname = FieldProperty(interfaces.IicNewsManagementAcquireSQLServer['hostname'])
    username = FieldProperty(interfaces.IicNewsManagementAcquireSQLServer['username'])
    password = FieldProperty(interfaces.IicNewsManagementAcquireSQLServer['password'])
    database = FieldProperty(interfaces.IicNewsManagementAcquireSQLServer['database'])
    dbprefix = FieldProperty(interfaces.IicNewsManagementAcquireSQLServer['dbprefix'])


def acquire_sql_server_adapter(context):
    return getUtility(interfaces.IicNewsManagementAcquireSQLServer, name='icnews.configuration', context=context)
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/lbn/LDAPMonitor/datasources/LDAPDataSource.py
# Compiled at: 2013-02-02 18:15:27
from Products.ZenModel.BasicDataSource import BasicDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import Permissions
from Products.ZenUtils.Utils import binPath
from ZenPacks.lbn.LDAPMonitor.config import MONITORED

class LDAPDataSource(ZenPackPersistence, BasicDataSource):
    """
    A command-plugin that calls munin-based Zope-agents on remote
    instance via wget

    This base class needs instantiations with munin_plugins, and uri 
    attributes
    """
    LDAP_MONITOR = 'LDAP'
    ZENPACKID = 'ZenPacks.lbn.LDAPMonitor'
    sourcetypes = (
     LDAP_MONITOR,)
    sourcetype = LDAP_MONITOR
    eventClass = '/Status/LDAP'
    hostname = '${dev/ip}'
    ipAddress = '${dev/manageIp}'
    ldapProto = '${dev/zLDAPProto}'
    ldapPort = '${dev/zLDAPPort}'
    ldapDN = '${dev/zLDAPDN}'
    ldapPW = '${dev/zLDAPPW}'
    timeout = 20
    searchFilter = 'cn=monitor'
    _properties = BasicDataSource._properties + ({'id': 'ldapProto', 'type': 'string', 'mode': 'w'}, {'id': 'ldapPort', 'type': 'int', 'mode': 'w'}, {'id': 'ldapDN', 'type': 'string', 'mode': 'w'}, {'id': 'ldapPW', 'type': 'string', 'mode': 'w'}, {'id': 'timeout', 'type': 'int', 'mode': 'w'}, {'id': 'searchFilter', 'type': 'string', 'mode': 'r'})
    _relations = BasicDataSource._relations

    def __init__(self, id, title=None, buildRelations=True):
        BasicDataSource.__init__(self, id, title, buildRelations)
        self.addDataPoints()

    def ldapURI(self, device):
        """
        LDAP server connection string - this is really the getCommand() function here
        """
        return self.getCommand(device, '%s://%s:%s' % (self.ldapProto, self.ipAddress, self.ldapPort))

    def getDescription(self):
        return '%s://%s:%s (%s)' % (self.ldapProto, self.hostname, self.ldapPort, self.searchFilter)

    def useZenCommand(self):
        return False

    def checkCommandPrefix(self, context, cmd):
        return cmd

    def addDataPoints(self):
        for tag in map(lambda x: x[0], MONITORED):
            if not hasattr(self.datapoints, tag):
                self.manage_addRRDDataPoint(tag)
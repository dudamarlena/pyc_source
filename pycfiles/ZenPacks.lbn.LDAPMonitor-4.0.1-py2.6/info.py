# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/lbn/LDAPMonitor/info.py
# Compiled at: 2013-02-02 18:07:01
from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.template import BasicDataSourceInfo
from interfaces import ILDAPDataSourceInfo

class LDAPDataSourceInfo(BasicDataSourceInfo):
    implements(ILDAPDataSourceInfo)
    ldapProto = ProxyProperty('ldapProto')
    ldapPort = ProxyProperty('ldapPort')
    ldapDN = ProxyProperty('ldapDN')
    ldapPW = ProxyProperty('ldapPW')
    timeout = ProxyProperty('timeout')

    @property
    def testable(self):
        """
        We can NOT test this datsource against a specific device
        """
        return False
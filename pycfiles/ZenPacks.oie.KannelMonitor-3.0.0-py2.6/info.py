# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/oie/KannelMonitor/info.py
# Compiled at: 2012-01-12 17:55:00
from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.template import BasicDataSourceInfo
from interfaces import IKannelDataSourceInfo

class KannelDataSourceInfo(BasicDataSourceInfo):
    implements(IKannelDataSourceInfo)
    secure = ProxyProperty('secure')
    password = ProxyProperty('password')
    port = ProxyProperty('port')
    timeout = ProxyProperty('timeout')

    @property
    def testable(self):
        """
        We can NOT test this datsource against a specific device
        """
        return False
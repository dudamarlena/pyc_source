# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/lbn/ZopeMonitor/info.py
# Compiled at: 2012-01-12 22:44:34
from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.template import BasicDataSourceInfo
from interfaces import IZopeThreadsDataSourceInfo, IZopeDBActivityDataSourceInfo, IZopeMemoryDataSourceInfo, IZopeCacheDataSourceInfo

class ZopeDataSourceInfo(BasicDataSourceInfo):
    zopeURI = ProxyProperty('zopeURI')
    timeout = ProxyProperty('timeout')

    @property
    def testable(self):
        """
        We can NOT test this datsource against a specific device
        """
        return False


class ZopeCacheDataSourceInfo(ZopeDataSourceInfo):
    implements(IZopeCacheDataSourceInfo)


class ZopeDBActivityDataSourceInfo(ZopeDataSourceInfo):
    implements(IZopeDBActivityDataSourceInfo)


class ZopeMemoryDataSourceInfo(ZopeDataSourceInfo):
    implements(IZopeMemoryDataSourceInfo)


class ZopeThreadsDataSourceInfo(ZopeDataSourceInfo):
    implements(IZopeThreadsDataSourceInfo)
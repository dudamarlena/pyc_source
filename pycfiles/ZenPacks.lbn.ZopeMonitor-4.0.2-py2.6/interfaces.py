# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/lbn/ZopeMonitor/interfaces.py
# Compiled at: 2012-01-12 22:41:23
from Products.Zuul.interfaces import IBasicDataSourceInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t

class IZopeDataSourceInfo(IBasicDataSourceInfo):
    zopeURI = schema.Text(title=_t('URI of Zope Server'))
    timeout = schema.Int(title=_t('Connection Timeout (seconds)'))


class IZopeThreadsDataSourceInfo(IZopeDataSourceInfo):
    pass


class IZopeDBActivityDataSourceInfo(IZopeDataSourceInfo):
    pass


class IZopeMemoryDataSourceInfo(IZopeDataSourceInfo):
    pass


class IZopeCacheDataSourceInfo(IZopeDataSourceInfo):
    pass
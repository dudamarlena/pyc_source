# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/lbn/ZopeMonitor/datasources/ZopeThreadsDataSource.py
# Compiled at: 2010-05-16 15:34:21
from DataSourceBase import DataSourceBase
from ZenPacks.lbn.ZopeMonitor.config import MUNIN_THREADS

class ZopeThreadsDataSource(DataSourceBase):
    """Zope Threads"""
    meta_type = 'ZopeThreadsDataSource'
    munin_tags = MUNIN_THREADS
    uri = 'zopethreads'
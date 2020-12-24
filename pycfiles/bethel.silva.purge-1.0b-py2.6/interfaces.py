# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bethel/silva/purge/interfaces.py
# Compiled at: 2012-05-16 08:59:56
from silva.core.interfaces import ISilvaLocalService

class IPurgingService(ISilvaLocalService):
    """A service to store purging configurations for frontend caching
       servers"""

    def set_caching_servers(hosts):
        """set the frontend caching servers"""
        pass

    def get_caching_servers():
        """return the set of frontend caching servers"""
        pass
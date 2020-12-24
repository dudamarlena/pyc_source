# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/gcp/facade/basefacade.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1765 bytes
import httplib2shim
httplib2shim.patch()
from googleapiclient import discovery

class GCPBaseFacade:

    def __init__(self, client_name: str, client_version: str):
        self._client_name = client_name
        self._client_version = client_version
        self._client = None

    def _build_client(self) -> discovery.Resource:
        return self._build_arbitrary_client(self._client_name, self._client_version)

    def _build_arbitrary_client(self, client_name, client_version, force_new=False):
        """
        :param client_name: name of the service
        :param client_version:  version of the client to create
        :param force_new: whether to create a new client - useful to create arbitrary clients from facades
        :return:
        """
        if force_new:
            return discovery.build(client_name, client_version, cache_discovery=False, cache=(MemoryCache()))
        if not self._client:
            self._client = discovery.build(client_name, client_version, cache_discovery=False, cache=(MemoryCache()))
        return self._client

    def _get_client(self) -> discovery.Resource:
        return self._build_client()


class MemoryCache:
    __doc__ = '\n    Workaround https://github.com/googleapis/google-api-python-client/issues/325#issuecomment-274349841\n    '
    _cache = {}

    def get(self, url):
        return MemoryCache._cache.get(url)

    def set(self, url, content):
        MemoryCache._cache[url] = content
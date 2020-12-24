# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/opensearchsdk/client.py
# Compiled at: 2015-11-22 10:59:09
__doc__ = '\nopensearch python sdk client.\n'
from opensearchsdk.apiclient import api_base
from opensearchsdk.v2 import app
from opensearchsdk.v2 import data
from opensearchsdk.v2 import search
from opensearchsdk.v2 import suggest
from opensearchsdk.v2 import index
from opensearchsdk.v2 import quota
from opensearchsdk.v2 import log
APP_URL = '/index'
DATA_URL = APP_URL + '/doc'
SEARCH_URL = '/search'
INDEX_URL = '/index'
SUGGEST_URL = '/suggest'
QUOTA_URL = ''
LOG_URL = APP_URL + '/error'

class Client(object):
    """opensearch python sdk client."""

    def __init__(self, base_url, key, key_id):
        self.base_url = base_url
        self.key = key
        self.key_id = key_id
        self.http_client = api_base.HTTPClient(base_url)
        self.app = app.AppManager(self, APP_URL)
        self.data = data.DataManager(self, DATA_URL)
        self.search = search.SearchManager(self, SEARCH_URL)
        self.suggest = suggest.SuggestManager(self, SUGGEST_URL)
        self.index = index.IndexManager(self, INDEX_URL)
        self.quota = quota.QuotaManager(self, QUOTA_URL)
        self.log = log.LogManager(self, LOG_URL)
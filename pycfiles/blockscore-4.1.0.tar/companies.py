# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johnbackus/Dropbox/coding/blockscore/blockscore-python/blockscore/api/companies.py
# Compiled at: 2015-03-04 21:31:22
COMPANIES_PATH = '/companies'

class Companies:

    def __init__(self, client):
        self.client = client

    def create(self, options={}):
        return self.client.post(COMPANIES_PATH, options)

    def retrieve(self, id, options={}):
        body = options['query'] if 'query' in options else {}
        return self.client.get('%s/%s' % (COMPANIES_PATH, str(id)), body)

    def all(self, count=None, offset=None, options={}):
        body = options['body'] if 'body' in options else {}
        if count:
            body['count'] = count
        if offset:
            body['offset'] = offset
        return self.client.get(COMPANIES_PATH, body)
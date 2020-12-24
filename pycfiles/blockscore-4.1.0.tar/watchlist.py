# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johnbackus/Dropbox/coding/blockscore/blockscore-python/blockscore/api/watchlist.py
# Compiled at: 2014-07-29 19:08:58
WATCHLIST_CANDIDATE_URI = '/watchlist_candidates'
WATCHLIST_SEARCH_URI = '/watchlists'

class Watchlist:

    def __init__(self, client):
        self.client = client

    @staticmethod
    def _create_body(date_of_birth=None, identification=None, name=None, address=None, note=None):
        body = {'date_of_birth': date_of_birth, 
           'note': note}
        if identification:
            body['ssn'] = identification.get('ssn')
            body['passport'] = identification.get('passport')
        if name:
            body['first_name'] = name.get('first')
            body['middle_name'] = name.get('middle')
            body['last_name'] = name.get('last')
        if address:
            body['address_street1'] = address.get('street1')
            body['address_street2'] = address.get('street2')
            body['address_city'] = address.get('city')
            body['address_state'] = address.get('state')
            body['address_postal_code'] = address.get('postal_code')
            body['address_country_code'] = address.get('country_code')
        return body

    def create(self, **kwargs):
        body = self._create_body(**kwargs)
        return self.client.post(WATCHLIST_CANDIDATE_URI, body)

    def edit(self, watchlist_candidate_id, **kwargs):
        body = self._create_body(**kwargs)
        return self.client.patch('%s/%s' % (WATCHLIST_CANDIDATE_URI,
         watchlist_candidate_id), body)

    def retrieve(self, watchlist_candidate_id):
        return self.client.get('%s/%s' % (WATCHLIST_CANDIDATE_URI,
         watchlist_candidate_id))

    def delete(self, watchlist_candidate_id):
        return self.client.delete('%s/%s' % (WATCHLIST_CANDIDATE_URI,
         watchlist_candidate_id))

    def list(self, count=None, offset=None):
        body = {'count': count, 
           'offset': offset}
        return self.client.get(WATCHLIST_CANDIDATE_URI, body)

    def search(self, watchlist_candidate_id, match_type=None):
        body = {'watchlist_candidate_id': watchlist_candidate_id, 
           'match_type': match_type}
        return self.client.post(WATCHLIST_SEARCH_URI, body)
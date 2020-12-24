# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/musicbot/graphql.py
# Compiled at: 2020-04-15 22:39:47
# Size of source mod 2**32: 972 bytes
import logging, requests
from musicbot.exceptions import FailedRequest
logger = logging.getLogger(__name__)

class GraphQL:

    def __init__(self, graphql, headers=None):
        self.graphql = graphql
        self.headers = headers

    def _post(self, query, failure=None):
        logger.debug(query)
        response = requests.post((self.graphql), json={'query': query}, headers=(self.headers))
        logger.debug(response)
        json_response = response.json()
        logger.debug(json_response)
        if response.status_code != 200:
            failure = failure if failure is not None else FailedRequest(f"Query failed: {json_response}")
            raise failure
        if 'errors' in json_response:
            if json_response['errors']:
                errors = [e['message'] for e in json_response['errors']]
                failure = failure if failure is not None else FailedRequest(f"Query failed: {errors}")
                raise failure
        return json_response
# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/api/client/json_client.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3667 bytes
__doc__ = 'JSON API Client'
from future.moves.urllib.parse import urljoin
import requests
from airflow.api.client import api_client

class Client(api_client.Client):
    """Client"""

    def _request(self, url, method='GET', json=None):
        params = {'url':url, 
         'auth':self._auth}
        if json is not None:
            params['json'] = json
        resp = (getattr(requests, method.lower()))(**params)
        if not resp.ok:
            try:
                data = resp.json()
            except Exception:
                data = {}

            raise IOError(data.get('error', 'Server error'))
        return resp.json()

    def trigger_dag(self, dag_id, run_id=None, conf=None, execution_date=None):
        endpoint = '/api/experimental/dags/{}/dag_runs'.format(dag_id)
        url = urljoin(self._api_base_url, endpoint)
        data = self._request(url, method='POST', json={'run_id':run_id, 
         'conf':conf, 
         'execution_date':execution_date})
        return data['message']

    def delete_dag(self, dag_id):
        endpoint = '/api/experimental/dags/{}/delete_dag'.format(dag_id)
        url = urljoin(self._api_base_url, endpoint)
        data = self._request(url, method='DELETE')
        return data['message']

    def get_pool(self, name):
        endpoint = '/api/experimental/pools/{}'.format(name)
        url = urljoin(self._api_base_url, endpoint)
        pool = self._request(url)
        return (
         pool['pool'], pool['slots'], pool['description'])

    def get_pools(self):
        endpoint = '/api/experimental/pools'
        url = urljoin(self._api_base_url, endpoint)
        pools = self._request(url)
        return [(p['pool'], p['slots'], p['description']) for p in pools]

    def create_pool(self, name, slots, description):
        endpoint = '/api/experimental/pools'
        url = urljoin(self._api_base_url, endpoint)
        pool = self._request(url, method='POST', json={'name':name, 
         'slots':slots, 
         'description':description})
        return (
         pool['pool'], pool['slots'], pool['description'])

    def delete_pool(self, name):
        endpoint = '/api/experimental/pools/{}'.format(name)
        url = urljoin(self._api_base_url, endpoint)
        pool = self._request(url, method='DELETE')
        return (
         pool['pool'], pool['slots'], pool['description'])
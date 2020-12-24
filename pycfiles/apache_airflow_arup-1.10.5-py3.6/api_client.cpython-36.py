# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/api/client/api_client.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2105 bytes
"""Client for all the API clients."""

class Client(object):
    __doc__ = 'Base API client for all API clients.'

    def __init__(self, api_base_url, auth):
        self._api_base_url = api_base_url
        self._auth = auth

    def trigger_dag(self, dag_id, run_id=None, conf=None, execution_date=None):
        """Create a dag run for the specified dag.

        :param dag_id:
        :param run_id:
        :param conf:
        :param execution_date:
        :return:
        """
        raise NotImplementedError()

    def delete_dag(self, dag_id):
        """Delete all DB records related to the specified dag.

        :param dag_id:
        """
        raise NotImplementedError()

    def get_pool(self, name):
        """Get pool.

        :param name: pool name
        """
        raise NotImplementedError()

    def get_pools(self):
        """Get all pools."""
        raise NotImplementedError()

    def create_pool(self, name, slots, description):
        """Create a pool.

        :param name: pool name
        :param slots: pool slots amount
        :param description: pool description
        """
        raise NotImplementedError()

    def delete_pool(self, name):
        """Delete pool.

        :param name: pool name
        """
        raise NotImplementedError()
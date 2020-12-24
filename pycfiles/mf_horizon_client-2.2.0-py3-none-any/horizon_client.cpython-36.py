# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stanley/IdeaProjects/horizon-python-client/src/mf_horizon_client/client/horizon_client.py
# Compiled at: 2020-05-09 10:25:59
# Size of source mod 2**32: 2395 bytes
import requests
from mf_horizon_client.client.datasets.data_interface import DataInterface
from mf_horizon_client.client.pipelines.pipeline_interface import PipelineInterface
from mf_horizon_client.client.session import HorizonSession
from mf_horizon_client.client.warnings import Warnings
from mf_horizon_client.endpoints import Endpoints
DEFAULT_MAX_RETRIES = 3
DEFAULT_CONCURRENT_TASKS = 1
ENDPOINTS = Endpoints()

class HorizonClient(HorizonSession):
    __doc__ = 'Sets up a connection to Horizon.\n\n    Args:\n        server_url (str): URL of your Horizon server\n        api_key (str): Your personal API key\n        max_retries (int, default 3): How many times to retry a request if a connection error occurs.\n        max_concurrent_pipelines (str, default 1): The maximum number of pipelines that may be run at any one time.\n            This must be set up from the deployment configuration.\n    '

    def __init__(self, server_url, api_key, max_retries=DEFAULT_MAX_RETRIES, max_concurrent_pipelines=DEFAULT_CONCURRENT_TASKS):
        if server_url[(-1)] != '/':
            server_url += '/'
        super().__init__(server_url, api_key, max_retries)
        if not max_concurrent_pipelines:
            print(Warnings.NO_MAX_FIRE_AND_FORGET_WORKERS_SPECIFIED)
        self._max_concurrent_tasks = max_concurrent_pipelines
        self.validate_connection()

    def validate_connection(self):
        """
        Checks that the connection is still open and valid
        """
        try:
            self.get(ENDPOINTS.ALL_DATASETS)
        except requests.exceptions.ConnectionError:
            raise ConnectionError('Failed to connect to Horizon API - likely network error or incorrect URL. Have you included `https://` in the URL?')
        except requests.exceptions.RetryError:
            raise ConnectionError('Failed to connect to Horizon API - likely incorrect API key.')

    def horizon_compute_status(self) -> dict:
        """
        Checks to see how many pipeline runners are not being used
        :return: WorkerStatusSchema
        """
        return self.get(ENDPOINTS.STATUS)

    def data_interface(self) -> DataInterface:
        return DataInterface(self)

    def pipeline_interface(self) -> PipelineInterface:
        return PipelineInterface(self)
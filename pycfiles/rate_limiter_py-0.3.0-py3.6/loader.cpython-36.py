# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/limiter/loader.py
# Compiled at: 2019-12-30 12:57:05
# Size of source mod 2**32: 5299 bytes
import json
from boto3.dynamodb.conditions import Key
from limiter.utils import validate_table_env_fallback
from limiter.clients import dynamodb
from limiter.managers import ACCOUNT_ID, RESOURCE_NAME, LIMIT, WINDOW_SEC
SERVICE_NAME = 'serviceName'
CONFIG_VERSION = 'configVersion'

class LimitLoader:
    __doc__ = '\n    Performs initial limit loading and updates for a specified service.\n\n    Instances of this class will only perform a single successful limit load. Subsequent\n    calls to load limits will exit without side effects.\n\n    Args:\n        service (str): Name of the service limits are being loaded for.\n        limit_table (str): Name of the DynamoDB table containing limits.\n                           Can be set via environment variable `LIMIT_TABLE`\n                           or synthesized using the `LIMITER_TABLES_BASE_NAME` environment variable.\n        limit_service_index (str): Name of the DynamoDB limit table service index.\n                                   Can be set via environment variable `LIMIT_SERVICE_INDEX`\n                                   or synthesized using the `LIMITER_TABLES_BASE_NAME` environment variable.\n    '

    def __init__(self, service, limit_table=None, limit_service_index=None):
        self.service = service
        self.limit_table_name = validate_table_env_fallback(limit_table, 'LIMIT_TABLE', 'limits')
        self.service_index_name = validate_table_env_fallback(limit_service_index, 'LIMIT_SERVICE_INDEX', 'limits-service-index')
        self.limit_table = dynamodb().Table(self.limit_table_name)
        self.is_loaded = False

    def load_limits(self, file_path, force=False):
        """
        Update the limits table entries for the given service with those contained in the specified file.

        First, the latest limits are read from the specified JSON file. Next, the limits table is queried for
        limits for the specified service. Any queried limits which are not in the latset limits will be deleted.
        Any queried limits which do not match the latest limits are updated. Any new limits are published.

        Args:
            service (str): Name of the service limits are being loaded for.
            force (bool): Update the limits even if a successful update has already occurred. Defaults to False.
        """
        if self.is_loaded:
            if not force:
                return
        with open(file_path, 'r') as (limits_file):
            limits_json = json.load(limits_file)
        latest_limits = limits_json['limits']
        if not latest_limits:
            self.is_loaded = True
            return
        current_limits_response = self._get_current_limits()
        indexed_put_requests = {}
        for limit in latest_limits:
            key, item = self._build_put_item(limit)
            indexed_put_requests[key] = item

        with self.limit_table.batch_writer() as (batch):
            for curr_limit in current_limits_response['Items']:
                account_id = curr_limit[ACCOUNT_ID]
                resource_name = curr_limit[RESOURCE_NAME]
                key = account_id + resource_name
                if key not in indexed_put_requests:
                    batch.delete_item(Key={ACCOUNT_ID: account_id, 
                     RESOURCE_NAME: resource_name})
                else:
                    put_request = indexed_put_requests[key]
                    if curr_limit[LIMIT] == put_request[LIMIT] and curr_limit[WINDOW_SEC] == put_request[WINDOW_SEC]:
                        del indexed_put_requests[key]

            for item in indexed_put_requests.values():
                batch.put_item(item)

        self.is_loaded = True

    def _get_current_limits(self):
        """
        Fetch the current service limits.

        Returns:
            (dict): Query response containing the current service limits.
        """
        return self.limit_table.query(IndexName=(self.service_index_name),
          KeyConditionExpression=(Key(SERVICE_NAME).eq(self.service)))

    def _build_put_item(self, limit):
        """
        Build the limit table item and account/resource key.

        Args:
            limit (dict): Limit to create a table item from. Expected to be pulled from the limits JSON file.

        Returns:
            (tuple): Two element tuple. First element is accound_id + resource_name str. Second is the table item.
        """
        account_id = limit[ACCOUNT_ID]
        resource_name = limit[RESOURCE_NAME]
        item = {ACCOUNT_ID: account_id, 
         RESOURCE_NAME: resource_name, 
         LIMIT: limit[LIMIT], 
         WINDOW_SEC: limit.get(WINDOW_SEC, 0), 
         SERVICE_NAME: self.service}
        key = account_id + resource_name
        return (key, item)
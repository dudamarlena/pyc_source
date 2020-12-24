# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taco/s3_config_manager/runtime_config_manager/runtime_config_manager.py
# Compiled at: 2019-09-05 09:49:59
from taco.s3_config_manager.base_config_manager import BaseConfigManager
import taco.s3_config_manager.exceptions as base_exceptions
from . import consts as runtime_config_consts

class RuntimeConfigManager(BaseConfigManager):

    def __init__(self, s3_wrapper, bucket_name, config_file_path=runtime_config_consts.RUNTIME_CONFIG_FILE_NAME, logger=None):
        super().__init__(s3_wrapper=s3_wrapper, bucket_name=bucket_name, config_file_path=config_file_path, logger=logger)

    def _get_config(self, resource_type, resource_name):
        category = self._get_value(resource_type)
        if isinstance(category, dict):
            value = category.get(resource_name)
            if value is not None:
                return value
        self._logger.log_and_raise(base_exceptions.MissingConfig, resource_name)
        return

    def get_sqs_queue(self, resource_name):
        return self._get_config(runtime_config_consts.ConfigKey.sqs.value, resource_name)

    def get_bucket(self, resource_name):
        return self._get_config(runtime_config_consts.ConfigKey.s3.value, resource_name)

    def get_generic_data(self, resource_name):
        return self._get_config(runtime_config_consts.ConfigKey.generic_data.value, resource_name)
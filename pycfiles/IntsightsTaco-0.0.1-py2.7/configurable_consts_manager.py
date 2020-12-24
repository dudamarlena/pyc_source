# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taco/s3_config_manager/configurable_consts_manager/configurable_consts_manager.py
# Compiled at: 2019-09-05 09:49:59
from taco.s3_config_manager.base_config_manager import BaseConfigManager

class ConfigurableConstsManager(BaseConfigManager):

    def __init__(self, s3_wrapper, consts_file_path, bucket_name, logger=None):
        super().__init__(s3_wrapper=s3_wrapper, bucket_name=bucket_name, config_file_path=consts_file_path, logger=logger)

    def get_const(self, const_name):
        return self._get_value(const_name)
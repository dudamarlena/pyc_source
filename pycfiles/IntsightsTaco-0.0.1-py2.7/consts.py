# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taco/s3_config_manager/runtime_config_manager/consts.py
# Compiled at: 2019-09-05 09:49:59
from enum import Enum
RUNTIME_CONFIG_FILE_NAME = 'runtime_configs.json'
NEO4J_RESOURCE_NAME = 'conclusion_db'
URLS_SEPARATOR = ','

class ConfigKey(Enum):
    sqs = 'SQS'
    s3 = 'S3'
    generic_data = 'GenericData'
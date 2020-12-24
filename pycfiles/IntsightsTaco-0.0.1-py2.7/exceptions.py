# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taco/s3_config_manager/exceptions.py
# Compiled at: 2019-09-05 09:49:59
import taco.common.exceptions

class RuntimeConfigManagerException(taco.common.exceptions.DataDictException):
    pass


class MissingConfig(RuntimeConfigManagerException):

    def __init__(self, key_name):
        data_dict = {'key_name': key_name}
        super().__init__('Failed to locate key', data_dict=data_dict)


class CorruptedConfigFile(RuntimeConfigManagerException):

    def __init__(self, bucket_name, config_file, exc=None):
        data_dict = {'config_file': config_file, 'bucket_name': bucket_name}
        super().__init__('Missing or invalid config file in S3', data_dict=data_dict, exc=exc)
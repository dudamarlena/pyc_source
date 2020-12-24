# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/wavescli/config.py
# Compiled at: 2020-01-30 19:05:11
# Size of source mod 2**32: 878 bytes
import os
from awsvault import Vault

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    AWS_SECRETS = os.getenv('AWS_SECRETS')
    vault = Vault([s.strip() for s in AWS_SECRETS.split(',')] if AWS_SECRETS else [])
    AWS_ENDPOINT_URL = vault.get('AWS_ENDPOINT_URL')
    BROKER_URL = vault.get('BROKER_URL')
    RESULT_BACKEND_URL = vault.get('RESULT_BACKEND_URL')
    WAVES_URL = vault.get('WAVES_URL')
    WAVES_RESULTS_PATH = vault.get('WAVES_RESULTS_PATH', 'waves/results')
    WAVES_CLI_NAME = os.getenv('WAVES_CLI_NAME', 'waves')
    QUEUE_NAME = os.getenv('QUEUE_NAME', 'waves_latest')


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass


def get_config(env='prod'):
    if env in ('development', 'dev'):
        return DevelopmentConfig()
    return ProductionConfig()
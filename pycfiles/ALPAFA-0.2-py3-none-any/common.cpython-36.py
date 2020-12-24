# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alpaca_trade_api_fixed/common.py
# Compiled at: 2020-02-14 14:55:34
# Size of source mod 2**32: 851 bytes
import os

def get_base_url():
    return os.environ.get('APCA_API_BASE_URL', 'https://api.alpaca.markets').rstrip('/')


def get_data_url():
    return os.environ.get('APCA_API_DATA_URL', 'https://data.alpaca.markets').rstrip('/')


def get_credentials(key_id=None, secret_key=None):
    key_id = key_id or os.environ.get('APCA_API_KEY_ID')
    if key_id is None:
        raise ValueError('Key ID must be given to access Alpaca trade API')
    secret_key = secret_key or os.environ.get('APCA_API_SECRET_KEY')
    if secret_key is None:
        raise ValueError('Secret key must be given to access Alpaca trade API')
    return (
     key_id, secret_key)


def get_api_version(api_version):
    api_version = api_version or os.environ.get('APCA_API_VERSION')
    if api_version is None:
        api_version = 'v1'
    return api_version
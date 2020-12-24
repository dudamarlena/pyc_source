# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/lnpay_py/__init__.py
# Compiled at: 2020-02-09 17:46:59
# Size of source mod 2**32: 1159 bytes
from .utility_helpers import post_request
__version__ = '0.1.0'
__VERSION__ = 'py' + __version__
__ENDPOINT_URL__ = 'https://lnpay.co/v1/'
__DEFAULT_WAK__ = ''
__PUBLIC_API_KEY__ = ''

def initialize(public_api_key, default_wak=None, params=None):
    """
    LNPay module initialization function required for interacting with the LNPay API.

    Parameters
    ----------
    public_api_key (str): Account public key from https://lnpay.co/dashboard/developers
    default_wak (str, optional): Default Wallet Access Key to use for a specific wallet when creating a `LNPayWallet`.
    params (Object): Object representing additional parameters to set globally. Example: {'endpoint_url': 'https://lnpay.co/v1/'}
    """
    global __DEFAULT_WAK__
    global __ENDPOINT_URL__
    global __PUBLIC_API_KEY__
    global __VERSION__
    if params is None:
        params = {}
    print('initializing lnpay..')
    __VERSION__ = 'py' + __version__
    __PUBLIC_API_KEY__ = public_api_key
    __ENDPOINT_URL__ = params.get('endpoint_url', __ENDPOINT_URL__)
    __DEFAULT_WAK__ = default_wak


def create_wallet(params):
    return post_request('wallet', params)
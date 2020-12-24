# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/Documents/VentasMedicas/openpay_python/build/lib/openpay/__init__.py
# Compiled at: 2018-02-27 01:49:10
# Size of source mod 2**32: 1217 bytes
from future.builtins import str
api_key = None
merchant_id = None
production = False
api_version = None
verify_ssl_certs = True
from openpay.resource import Card, Charge, Customer, Plan, Transfer, Fee, BankAccount, Payout, Subscription
from openpay.error import OpenpayError, APIError, APIConnectionError, AuthenticationError, CardError, InvalidRequestError
import sys as _sys
_dogetattr = object.__getattribute__
_ALLOWED_ATTRIBUTES = ('api_key', 'api_base', 'api_version', 'verify_ssl_certs', 'TEST_MODE')
_original_module = _sys.modules[__name__]

def get_api_base():
    if not production:
        api_base = str('https://sandbox-api.openpay.mx')
    else:
        api_base = str('https://api.openpay.mx')
    return api_base
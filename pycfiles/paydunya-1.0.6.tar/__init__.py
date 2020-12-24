# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/freedev/Code/OpenSource/paydunya-python/paydunya/__init__.py
# Compiled at: 2017-08-18 23:12:30
"""PAYDUNYA

PAYDUNYA Python client library.
Modules implemented: DirectPay, Invoice, and OPR
"""
__version__ = '1.0.6'
__author__ = 'PAYDUNYA <paydunya@paydunya.com>'
import sys, requests
try:
    import simplejson as json
except ImportError:
    import json

debug = False
api_keys = {}
API_VERSION = 'v1'
SERVER = 'app.paydunya.com'
SANDBOX_ENDPOINT = 'https://%s/sandbox-api/%s/' % (SERVER, API_VERSION)
LIVE_ENDPOINT = 'https://%s/api/%s/' % (SERVER, API_VERSION)
PAYDUNYA_USER_AGENT = 'paydunya-python/v%s' % __version__
__MODULE__ = sys.modules[__name__]

class PaydunyaError(Exception):
    """Base Exception class"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Store(object):
    """PAYDUNYA Store

    Creates a store object for PAYDUNYA transactions
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.tagline = kwargs.get('tagline', None)
        self.postal_address = kwargs.get('postal_address', None)
        self.phone_number = kwargs.get('phone_number', None)
        self.website_url = kwargs.get('website_url', None)
        self.logo_url = kwargs.get('logo_url', None)
        return

    @property
    def info(self):
        """Returns the store information

        What this does is simply return the store object's attributes
        """
        return self.__dict__


class Payment(object):
    """Base class for other PAYDUNYA classes"""

    def __init__(self):
        """Base class for all the other payment libraries"""
        self._headers = {'User-Agent': PAYDUNYA_USER_AGENT, 
           'Content-Type': 'application/json'}
        self._response = None
        self._data = None
        self.store = Store(name=None)
        return

    def _process(self, resource=None, data={}):
        """Processes the current transaction

        Sends an HTTP request to the PAYDUNYA API server
        """
        _data = data or self._data
        rsc_url = self.get_rsc_endpoint(resource)
        if _data:
            req = requests.post(rsc_url, data=json.dumps(_data), headers=self.headers)
        else:
            req = requests.get(rsc_url, params=_data, headers=self.headers)
        if req.status_code == 200:
            self._response = json.loads(req.text)
            if int(self._response['response_code']) == 0:
                return (True, self._response)
            return (False, self._response['response_text'])
        else:
            return (500, 'Request Failed')

    @property
    def headers(self):
        """Returns the client's Request headers"""
        return dict(self._config, **self._headers)

    def add_header(self, header):
        """Add a custom HTTP header to the client's request headers"""
        if type(header) is dict:
            self._headers.update(header)
        else:
            raise ValueError("Dictionary expected, got '%s' instead" % type(header))

    def get_rsc_endpoint(self, rsc):
        """Returns the HTTP API URL for current payment transaction"""
        if self.debug:
            return SANDBOX_ENDPOINT + rsc
        return LIVE_ENDPOINT + rsc

    @property
    def debug(self):
        """Returns the current transaction mode"""
        return __MODULE__.debug

    @property
    def _config(self):
        _m = __MODULE__
        return {'PAYDUNYA-MASTER-KEY': _m.api_keys.get('PAYDUNYA-MASTER-KEY'), 
           'PAYDUNYA-PRIVATE-KEY': _m.api_keys.get('PAYDUNYA-PRIVATE-KEY'), 
           'PAYDUNYA-TOKEN': _m.api_keys.get('PAYDUNYA-TOKEN')}


from .invoice import Invoice, InvoiceItem
from .direct_payments import DirectPay
from .opr import OPR
__all__ = [
 Store.__name__,
 Payment.__name__,
 Invoice.__name__,
 InvoiceItem.__name__,
 DirectPay.__name__,
 OPR.__name__]
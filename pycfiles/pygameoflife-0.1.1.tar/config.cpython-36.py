# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/daniel/Documentos/projetos/pypayments/pygamento/config.py
# Compiled at: 2020-02-28 18:34:14
# Size of source mod 2**32: 2483 bytes
from .request_payment import *
from .request_refund import *
from .cancel_payment import *
from .information_payment import *

class Config:

    def __init__(self, **kwargs):
        self.key = kwargs.get('key')
        self.modo = 0 if not kwargs.get('mode') else kwargs.get('mode')
        self.gateway = kwargs.get('gateway')
        self.url = {'direct':'https://api.ebanx.com.br/ws/direct', 
         'capture':'https://api.ebanx.com.br/ws/capture', 
         'cancel':'https://api.ebanx.com.br/ws/cancel', 
         'refund':'https://api.ebanx.com.br/ws/refund', 
         'refundOrCancel':'https://api.ebanx.com.br/ws/refundOrCancel', 
         'setCVV':'https://api.ebanx.com.br/ws/token/setCVV', 
         'token':'https://api.ebanx.com.br/ws/token', 
         'query':'https://api.ebanx.com.br/ws/query', 
         'print':'https://api.ebanx.com.br/print'}
        if self.modo == 1:
            self.url = {'direct':'https://staging.ebanx.com.br/ws/direct', 
             'capture':'https://staging.ebanx.com.br/ws/capture', 
             'cancel':'https://staging.ebanx.com.br/ws/cancel', 
             'refund':'https://staging.ebanx.com.br/ws/refund', 
             'refundOrCancel':'https://staging.ebanx.com.br/ws/refundOrCancel', 
             'setCVV':'https://staging.ebanx.com.br/ws/token/setCVV', 
             'token':'https://staging.ebanx.com.br/ws/token', 
             'query':'https://staging.ebanx.com.br/ws/query', 
             'print':'https://staging.ebanx.com.br/print'}

    def send(self, **kwargs):
        new = new_payment(key=self.key, url=self.url, gateway=self.gateway, **kwargs)
        return new

    def cancel(self, **kwargs):
        new = cancel_payment(key=self.key, url=self.url, gateway=self.gateway, **kwargs)
        return new

    def refund(self, **kwargs):
        new = new_refund(key=self.key, url=self.url, **kwargs)
        return new

    def refund_or_cancel(self, **kwargs):
        new = new_refund_or_cancel(key=self.key, url=self.url, **kwargs)
        return new

    def new_cancel_refund(self, **kwargs):
        new = new_cancel_refund(key=self.key, url=self.url, **kwargs)
        return new

    def info(self, **kwargs):
        new = info_payment(key=self.key, url=self.url, gateway=self.gateway, **kwargs)
        return new
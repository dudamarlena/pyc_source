# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/daniel/Documentos/projetos/pypayments/pypayment/request_refund.py
# Compiled at: 2020-02-27 19:32:13
# Size of source mod 2**32: 1142 bytes
import requests, json

def new_refund(**kwargs):
    item = {'integration_key':kwargs.get('key'), 
     'merchant_refund_code':kwargs.get('refund_code'), 
     'operation':'request', 
     'amount':kwargs.get('amount'), 
     'hash':kwargs.get('hash'), 
     'description':kwargs.get('description')}
    send = requests.post((kwargs.get('url')['refund']), data=item)
    r = send.json()
    return r


def new_refund_or_cancel(**kwargs):
    item = {'integration_key':kwargs.get('key'), 
     'merchant_refund_code':kwargs.get('refund_code'), 
     'operation':'request', 
     'hash':kwargs.get('hash'), 
     'description':kwargs.get('description')}
    send = requests.post((kwargs.get('url')['refundOrCancel']), data=item)
    r = send.json()
    return r


def new_cancel_refund(**kwargs):
    item = {'integration_key':kwargs.get('key'), 
     'merchant_refund_code':kwargs.get('refund_code'), 
     'operation':'cancel'}
    send = requests.post((kwargs.get('url')['refund']), data=item)
    r = send.json()
    return r
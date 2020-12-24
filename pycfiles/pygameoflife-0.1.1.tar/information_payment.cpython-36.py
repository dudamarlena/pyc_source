# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/daniel/Documentos/projetos/pypayments/pygamento/information_payment.py
# Compiled at: 2020-02-28 18:36:24
# Size of source mod 2**32: 377 bytes
import requests, json

def info_payment(**kwargs):
    if kwargs.get('gateway') == 'PicPay':
        headers = {'content-type':'application/json',  'x-picpay-token':kwargs.get('key')}
        get = requests.get(('https://appws.picpay.com/ecommerce/public/payments/{}/status'.format(kwargs.get('payment_code'))), headers=headers)
        r = get.json()
        return r
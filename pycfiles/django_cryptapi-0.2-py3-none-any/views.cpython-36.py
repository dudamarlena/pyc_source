# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dwjor/Google Drive/Code/Python/django-cryptapi/cryptapi/views.py
# Compiled at: 2020-05-04 23:03:03
# Size of source mod 2**32: 1560 bytes
import json
from django.http import HttpResponse
from cryptapi.forms import CallbackForm, BaseCallbackForm
from cryptapi.dispatchers import CallbackDispatcher

def callback(_r):
    pending = _r.GET.get('pending', False)
    if not pending:
        form = CallbackForm(data=(_r.GET))
    else:
        form = BaseCallbackForm(data=(_r.GET))
    if form.is_valid():
        coin = form.cleaned_data.get('coin')
        request = {'id':form.cleaned_data.get('request_id'), 
         'nonce':form.cleaned_data.get('nonce'), 
         'address_in':form.cleaned_data.get('address_in'), 
         'address_out':form.cleaned_data.get('address_out')}
        payment = {'txid_in':form.cleaned_data.get('txid_in'), 
         'value_paid':form.cleaned_data.get('value'), 
         'value_paid_coin':form.cleaned_data.get('value_coin'), 
         'confirmations':form.cleaned_data.get('confirmations')}
        if not pending:
            payment['txid_out'] = form.cleaned_data.get('txid_out')
            payment['value_received'] = form.cleaned_data.get('value_forwarded')
            payment['value_received_coin'] = form.cleaned_data.get('value_forwarded_coin')
        raw_data = json.dumps(_r.GET)
        dispatcher = CallbackDispatcher(coin, request, payment, raw_data, pending=pending)
        if dispatcher.callback():
            return HttpResponse('*ok*')
    return HttpResponse('Error')
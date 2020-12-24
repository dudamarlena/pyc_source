# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dwjor/Google Drive/Code/Python/django-cryptapi/cryptapi/views.py
# Compiled at: 2019-10-10 18:59:56
# Size of source mod 2**32: 1399 bytes
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
         'confirmations':form.cleaned_data.get('confirmations')}
        if not pending:
            payment['txid_out'] = form.cleaned_data.get('txid_out')
            payment['value_received'] = form.cleaned_data.get('value_forwarded')
        raw_data = json.dumps(_r.GET)
        dispatcher = CallbackDispatcher(coin, request, payment, raw_data, pending=pending)
        if dispatcher.callback():
            return HttpResponse('*ok*')
    return HttpResponse('Error')
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/zarinpals/views.py
# Compiled at: 2019-01-31 06:07:32
from __future__ import unicode_literals
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from zeep import Client
from aparnik.packages.shops.payments.models import Payment
from aparnik.settings import aparnik_settings, Setting
from .models import Bank

def send_request(request, payment):
    client = Client(b'https://www.zarinpal.com/pg/services/WebGate/wsdl')
    order = payment.order_obj
    description = b'خرید %s' % order.items.first().product_obj.title
    call_back_url = request.build_absolute_uri(reverse(b'aparnik:shops:zarinpals:verify', args=[payment.uuid]))
    merchent_code = Setting.objects.get(key=b'ZARINPAL_MERCHENT_CODE').get_value()
    result = client.service.PaymentRequest(merchent_code, order.get_total_cost(), description, b'', b'', call_back_url)
    if result.Status == 100:
        bank = Bank.objects.create(authority_id=result.Authority, status=result.Status, payment=payment)
        return redirect(b'https://www.zarinpal.com/pg/StartPay/%s/ZarinGate' % str(result.Authority))
    raise Http404


def verify(request, uuid):
    client = Client(b'https://www.zarinpal.com/pg/services/WebGate/wsdl')
    payment = get_object_or_404(Payment, uuid=uuid)
    if payment.status != Payment.STATUS_WAITING:
        raise Http404
    merchent_code = Setting.objects.get(key=b'ZARINPAL_MERCHENT_CODE').get_value()
    result = client.service.PaymentVerification(merchent_code, request.GET[b'Authority'], payment.order_obj.get_total_cost())
    bank = get_object_or_404(Bank, authority_id=request.GET[b'Authority'])
    if bank.payment != payment:
        raise Http404
    bank.ref_id = result.RefID
    bank.status = result.Status
    bank.save()
    if result.Status == 100 or result.Status == 101:
        payment.success()
    else:
        payment.cancel()
    from aparnik.packages.shops.payments.views import payment as payment_view
    return payment_view(request, uuid=payment.uuid)
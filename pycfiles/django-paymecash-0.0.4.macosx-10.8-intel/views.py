# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/drmartiner/projects/django-paymecash/paymecash/views.py
# Compiled at: 2013-09-17 23:44:23
import logging
from django.http import HttpResponse
from django.views.generic import View
from annoying.functions import get_object_or_None
from django.views.decorators.csrf import csrf_exempt
from .signals import payment_completed
from .signals import payment_fail
from .models import Payment
logger = logging.getLogger('paymecash')

class Confirm(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(Confirm, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('order_id')
        payment = get_object_or_None(Payment, order_id=order_id)
        if not payment:
            logger.error('Payment with order_id "%s" was not found' % order_id)
            payment_fail.send(sender=Payment, data=request.POST.copy())
            return HttpResponse()
        message = request.POST.get('message')
        if message:
            payment.result = Payment.RESULT_ERROR
            logger.error('Recieved error message for order_id %s' % order_id)
            payment_fail.send(sender=Payment, data=request.POST.copy())
            return HttpResponse()
        transaction_id = request.POST.get('transaction')
        if transaction_id.isdigit():
            payment.transaction_id = request.POST.get('transaction')
        payment.result = Payment.RESULT_OK
        payment.save()
        payment_completed.send(sender=Payment, data=request.POST.copy())
        logger.info('Payment with order_id "%s" and transaction_id "%s" was confirmed' % (order_id, transaction_id))
        return HttpResponse()
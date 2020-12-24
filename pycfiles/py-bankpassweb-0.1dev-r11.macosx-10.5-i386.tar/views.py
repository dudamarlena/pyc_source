# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.5/site-packages/bankpassweb/satchmo_payment/views.py
# Compiled at: 2008-01-28 10:43:57
from datetime import datetime
import logging
from django.core import urlresolvers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from satchmo.configuration import config_get_group
from satchmo.contact.models import Order
from satchmo.payment.common.views import payship
from satchmo.payment.common.views.checkout import success as checkout_success
from satchmo.payment.common.utils import record_payment, create_pending_payment
from satchmo.shop.models import Cart
from satchmo.shop.utils.dynamic import lookup_template, lookup_url
from satchmo.shop.views.utils import bad_or_missing
import processor as processing_module
from bankpassweb.datatypes import BPWCryptoException
from bankpassweb.webresults import Success
log = logging.getLogger('bankpassweb.satchmo_payment.views')

def pay_ship_info(request):
    return payship.base_pay_ship_info(request, config_get_group('PAYMENT_BANKPASSWEB'), payship.simple_pay_ship_process_form, 'checkout/base_pay_ship.html')


def complete_decoration(inner, decorated):
    for attr in ('__doc__', '__name__', '__dict__'):
        try:
            setattr(inner, attr, getattr(decorated, attr))
        except AttributeError:
            pass


def select_processor_and_order(func):
    """
        This decorator prepares the processor instance, and makes sure
        that the order we are going to process is still existing and
        valid.
        """

    def inner_func(request):

        class Collection:
            pass

        checkout_data = Collection()
        payment_module = config_get_group('PAYMENT_BANKPASSWEB')
        checkout_data.payment_module = payment_module
        checkout_data.processor = processing_module.PaymentProcessor(payment_module)
        try:
            order = Order.objects.from_request(request)
        except Order.DoesNotExist:
            url = lookup_url(payment_module, 'satchmo_checkout-step1')
            return HttpResponseRedirect(url)

        tempCart = Cart.objects.from_request(request)
        if tempCart.numItems == 0:
            template = lookup_template(payment_module, 'checkout/empty_cart.html')
            return render_to_response(template, RequestContext(request))
        if not order.validate(request):
            context = RequestContext(request, {'message': _('Your order is no longer valid.')})
            return render_to_response('shop_404.html', context)
        checkout_data.order = order
        checkout_data.cart = tempCart
        return func(request, checkout_data)

    complete_decoration(inner_func, func)
    return inner_func


@select_processor_and_order
def confirm_info(request, checkout):
    template = lookup_template(checkout.payment_module, 'checkout/bankpassweb/confirm.html')
    checkout.processor.prepare_data(checkout.order)
    log.info('Creating a PENDING transaction for order %s' % checkout.order)
    create_pending_payment(checkout.order, checkout.payment_module, amount=checkout.order.balance)
    ctx = RequestContext(request, {'order': checkout.order, 'start_url': checkout.processor.start_url, 
       'PAYMENT_LIVE': checkout.processor.live, 
       'invoice': checkout.order.id})
    return render_to_response(template, ctx)


@select_processor_and_order
def success(request, checkout):
    """
        This view handles the notification coming back from the BankPass
        Web system.  We have both our own cookies, stored in the customer's
        browser, and BankPass Web's data.
        
        First, we have our Engine check that the data is authentic and not
        corrupted.  Then we make some sanity checks to be sure that the order
        data (amount, ID, currency...) match what we have. If it does not,
        we bail out.
        
        Then we check if the outcome is successful. If it is not, we warn
        the user. If it is, we record the transaction and use the default
        success view to notify the user.
        """
    order = checkout.order
    try:
        outcome = checkout.processor.parse_answer(request.META['QUERY_STRING'])
    except BPWCryptoException, e:
        log.error('Forged or incorrect message from BankPass: ignoring. (%s)' % request.META['QUERY_STRING'])
        return bad_or_missing(request, _('The message from BankPass Web appears to be forged. Cannot process payment.'))

    if order.notes:
        notes = order.notes + '\n'
    else:
        notes = ''
    notes += '%s\n' % datetime.now()
    notes += outcome.summary
    order.notes = notes
    order.save()
    key = unicode(checkout.payment_module.KEY.value)
    pending_payments = order.payments.filter(transaction_id__exact='PENDING', payment__exact=key)
    pending_amount = pending_payments[0].amount
    try:
        assert isinstance(outcome.outcome, Success), _('The transaction was not successful')
        assert outcome.order_id == checkout.processor.id_prefix(order), _('The order ID does not match what we sent')
        assert outcome.amount.as_decimal == pending_amount, _('The amount that was paid does not match what we ordered. (Asked for %s, got %s)') % (
         pending_amount, outcome.amount.as_decimal)
        assert outcome.auth_id, _('The authorization ID for this transaction is missing')
        assert outcome.trans_id, _('The transaction ID is missing')
    except AssertionError, a:
        return bad_or_missing(request, unicode(a))

    log.info('Recording successful CC transaction (#%s) for order %s' % (
     pending_payments[0].id, order.id))
    record_payment(order, checkout.payment_module, amount=outcome.amount.as_decimal, transaction_id=outcome.trans_id)
    checkout.cart.empty()
    return checkout_success(request)


def ipn(request):
    raise Exception, 'IPN Not yet implemented'
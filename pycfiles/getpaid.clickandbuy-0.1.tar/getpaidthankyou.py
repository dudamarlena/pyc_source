# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/olauzanne/workspace/paguro/getpaid.clickandbuy/getpaid/clickandbuy/browser/getpaidthankyou.py
# Compiled at: 2009-01-30 04:18:04
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from getpaid.core.interfaces import IOrderManager, IShoppingCartUtility
from suds.client import Client, SoapClient, log
from suds import WebFault
from getpaid.clickandbuy.interfaces import IClickAndBuyStandardOptions, IClickAndBuyStandardProcessor
import logging
logger = logging.getLogger('Plone')

def failed(self, binding, error):
    """
    Request failed, process reply based on reason
    @param binding: The binding to be used to process the reply.
    @type binding: L{suds.bindings.binding.Binding}
    @param error: The http error message
    @type error: L{transport.TransportError}
    """
    status, reason = error.httpcode, str(error)
    reply = error.fp.read()
    log.debug('http failed:\n%s', reply)
    if status == 500:
        if len(reply) > 0:
            (r, p) = binding.get_fault(reply)
            self.last_received(r)
            return (status, p)
        else:
            return (
             status, None)
    if self.options.faults:
        raise Exception((status, reason))
    else:
        return (
         status, None)
    return


SoapClient.failed = failed

class GetpaidClickAndBuyThankyouView(BrowserView):
    """Class for overriding getpaid-thank-you view for paypal purchases
    """
    __module__ = __name__

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def success(self):
        if hasattr(self, '_success'):
            return self._success
        order_manager = getUtility(IOrderManager)
        externalBDRID = self.request.get('externalBDRID')
        order = order_manager.get(externalBDRID)
        if order is None or order.finance_state != 'CHARGING':
            return False
        if self.request.get('result') == 'success':
            client = Client('http://wsdl.eu.clickandbuy.com/TMI/1.4/TransactionManagerbinding.wsdl')
            options = IClickAndBuyStandardOptions(self.context)
            try:
                client.service.isExternalBDRIDCommitted(sellerID=options.seller_id, tmPassword=options.tm_password, slaveMerchantID=0, externalBDRID=externalBDRID)
                is_commited = result.isCommited
                clickandbuy_id = result.BDRID
                reason = ''
            except WebFault, e:
                is_commited = False
                reason = str(e.fault)
                logger.error('getpaid.clickandbuy: The soap transaction %s failed:\n %s' % (externalBDRID, reason))
            else:
                self._success = bool(is_commited)
                if self._success:
                    order.finance_workflow.fireTransition('charge-charging')
                    cart_util = getUtility(IShoppingCartUtility)
                    cart_util.destroy(self.context)
        else:
            self._success = False
        if not self._success:
            order.finance_workflow.fireTransition('decline-charging')
        return self._success

    def failure(self):
        return not self.success()

    def getInvoice(self):
        if self.request.has_key('externalBDRID'):
            return self.request['externalBDRID']
        else:
            return
        return

    def getURL(self):
        portalurl = getToolByName(self.context, 'portal_url').getPortalObject().absolute_url()
        if self.getInvoice() is not None:
            return '%s/@@getpaid-order/%s' % (portalurl, self.getInvoice())
        else:
            return ''
        return
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/olauzanne/workspace/paguro/getpaid.clickandbuy/getpaid/clickandbuy/browser/transaction.py
# Compiled at: 2009-01-30 04:18:04
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from getpaid.core.interfaces import IOrderManager
from persistent.dict import PersistentDict

class Transaction(BrowserView):
    __module__ = __name__

    def transaction(self):
        """ click and buy transaction """
        request = self.request
        environ = request.environ
        order_manager = getUtility(IOrderManager)
        cb_linknr = environ.get('HTTP_X_CONTENTID', '')
        cb_price = environ.get('HTTP_X_PRICE', '')
        if cb_price.isdigit():
            cb_price = str(int(cb_price) / 1000)
        else:
            cb_price = 'nan'
        cb_uid = environ.get('HTTP_X_USERID', '')
        cb_transaction_id = environ.get('HTTP_X_TRANSACTION', '')
        cb_currency = environ.get('HTTP_X_CURRENCY', '')
        cb_ip = environ.get('REMOTE_ADDR', '')
        portal_url = getToolByName(self.context, 'portal_url').getPortalObject().absolute_url()
        thank_you_page = '%s/@@getpaid-thank-you' % portal_url
        result = True
        reason = ''
        ext_bdr_id = request.get('externalBDRID')
        if not ext_bdr_id:
            result = False
            reason += 'invalid_order_id&'
            order = None
            myprice = None
        else:
            order = order_manager.get(ext_bdr_id)
            myprice = str(int(order.getTotalPrice() * 100))
            myprice = '100'
        if cb_uid in ('', 'nan'):
            result = False
            reason += 'cb_uid&'
        if cb_ip[0:11] != '217.22.128.':
            result = False
            reason += 'cb_ip&'
        if cb_transaction_id == '0':
            result = False
            reason += 'cb_transaction_id&'
        if cb_price in ('', 'nan'):
            result = False
            reason += 'cb_price1&%s#' % cb_price
        if cb_price != myprice:
            result = False
            reason += 'cb_price2=%s#' % cb_price
        if result:
            if order.finance_state != 'REVIEWING':
                result = False
                reason += 'wrong_workflow_state&' % cb_price
            else:
                order.finance_workflow.fireTransition('authorize')
                order.clickandbuy_data = data = PersistentDict()
                data['cb_linknr'] = cb_linknr
                data['cb_price'] = cb_price
                data['cb_uid'] = cb_uid
                data['cb_transaction_id'] = cb_transaction_id
                data['cb_currency'] = cb_currency
                data['cb_ip'] = cb_ip
        response = request.response
        if result:
            response.redirect(thank_you_page + '?result=success&externalBDRID=%s' % ext_bdr_id)
        else:
            response.redirect(thank_you_page + '?result=error&reason=%s' % reason)
        return
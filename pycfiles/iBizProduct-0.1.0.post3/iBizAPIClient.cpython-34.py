# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\lrivera\Documents\Visual Studio 2013\Projects\iBizProduct-Python\iBizProduct-Python\src\iBizAPIClient.py
# Compiled at: 2016-04-11 18:22:15
# Size of source mod 2**32: 14154 bytes
from __future__ import unicode_literals
from datetime import *
import itertools
from future.utils import raise_with_traceback
from future.utils import viewitems
from builtins import dict, int, str, bool
from src.Contracts.iBizAPIClientInterface import *
from src.Contracts.ProductOrderSpec import *
from src.Contracts.ProductOrderInfoToReturn import *
from src.Contracts.CaseSpec import *
from src.Contracts.EventStatus import *
from src.Contracts.ProductAuthentication import *
from src.iBizBE import *

class iBizAPIClient(iBizAPIClientInterface):

    def __init__(self, externalKey, productId, backend):
        self._ExternalKey = externalKey
        self._ProductId = productId
        self._isDev = backend.IsDev
        if backend != None and not isinstance(backend, iBizBE):
            raise_with_traceback(ValueError('You must supply a valid backend instance'))
        else:
            self._backend = backend

    def ProductOrderAdd(self, productOrderSpec, productId=None):
        self.VerifyExternalKey()
        if productId == None:
            if self._ProductId == None:
                raise_with_traceback(ValueError('You must supply a valid product id.'))
        if not isinstance(productOrderSpec, ProductOrderSpec):
            raise_with_traceback(ValueError('You must supply a valid product order spec.'))
        params = dict(external_key=self._ExternalKey, product_id=productId or self._ProductId, productorder_spec=productOrderSpec.getSpec())
        return self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalAdd', params)

    def ProductOrderEdit(self, productOrderId, productOrderSpec):
        self.VerifyExternalKey()
        if not isinstance(productOrderSpec, ProductOrderSpec):
            raise_with_traceback(ValueError('You must supply a valid product order spec.'))
        params = dict(external_key=self._ExternalKey, product_id=productOrderId or self._ProductId, productorder_spec=productOrderSpec.getSpec())
        return self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalEdit', params)

    def ProductOrderView(self, productOrderId, infoToReturn=None):
        self.VerifyExternalKey()
        if infoToReturn != None:
            if not isinstance(infoToReturn, ProductOrderInfoToReturn):
                raise_with_traceback(ValueError('You must supply a valid infor to return value'))
        params = dict(external_key=self._ExternalKey, product_id=productOrderId)
        params = self._iBizAPIClient__FilterDict(params)
        if infoToReturn != None:
            params['info_to_return'] = infoToReturn.getSpec()
        return self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalView', params)

    def ProductOrderBillOrderAddOneTime(self, cycleBeginDate, cycleEndDate, oneTimeCost, productOrderId, detailAddon=None, descriptionAddon=None, dueNow=0):
        self.VerifyExternalKey()
        if not isinstance(cycleBeginDate, datetime) or not isinstance(cycleEndDate, datetime):
            raise_with_traceback(ValueError('You must supply a valid cycle begin and end date value'))
        params = dict(external_key=self._ExternalKey, productorder_id=productOrderId, cycle_begin_date=cycleBeginDate.timestamp(), cycle_end_date=cycleEndDate.timestamp(), one_time_cost=oneTimeCost, detail_addon=detailAddon, description_addon=descriptionAddon, due_now=dueNow)
        params = self._iBizAPIClient__FilterDict(params)
        return self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalBillOrderAddOneTime', params)

    def PurchaseOrderAdd(self, accountId, offerChain, purchaseOrderSpec, orderName=''):
        self.VerifyExternalKey()
        params = dict(external_key=self._ExternalKey, offer_chain=offerChain, purhcaseorder_spec=purchaseOrderSpec, order_name=orderName)
        return self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalAdd', params)

    def PurchaseOrderEdit(self, purchaseOrderId, offerChain, purchaseOrderSpec):
        self.VerifyExternalKey()
        params = dict(external_key=self._ExternalKey, offer_chain=offerChain, purchaseorder_spec=purchaseOrderSpec, purchaseorder_id=purchaseOrderId)
        return self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalEdit', params)

    def PurchaseOrderListOnAccount(self, accountId, limit={}):
        self.VerifyExternalKey()
        params = dict(external_key=self._ExternalKey, account_id=accountId)
        if limit.__len__() > 0:
            params['limit'] = limit
        return self._backend.call('CommerceManager/ProductOffer/PurchaseOrder', 'ExternalListOnAccount', params)

    def PurchaseOrderCycleDelimiters(self, purchaseOrderId):
        self.VerifyExternalKey()
        params = dict(external_key=self._ExternalKey, purchaseorder_id=purchaseOrderId)
        return self._backend.call('CommerceManager/ProductOffer/PurchaseOrder', 'ExternalGetCycleDelimiters', params)

    def PurchaseOrderPrice(self, purchaseOrderId, accountId):
        self.VerifyExternalKey()
        params = dict(external_key=self._ExternalKey, purchaseorder_id=purchaseOrderId, account_id=accountId)
        return self._backend.call('CommerceManager/ProductOffer/PurchaseOrder', 'ExternalPriceFromPurchase', params)

    def ProductOpenCaseWithOwner(self, productOrderId, caseSpec):
        self.VerifyExternalKey()
        if not isinstance(caseSpec, CaseSpec):
            raise_with_traceback(ValueError('You must supply a valid case spec object'))
        params = dict(external_key=self._ExternalKey, productorder_id=productOrderId, case_spec=caseSpec.getSpec())
        params = self._iBizAPIClient__FilterDict(params)
        result = self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalOpenCaseWithOwner', params)
        return result.get('new_id')

    def ProductUpdateCaseWithOwner(self, productOrderId, caseId, caseSpec):
        self.VerifyExternalKey()
        if not isinstance(caseSpec, CaseSpec):
            raise_with_traceback(ValueError('You must supply a valid case spec object'))
        params = dict(external_key=self._ExternalKey, productorder_id=productOrderId, case_spec=caseSpec.getSpec(), case_id=caseId)
        params = self._iBizAPIClient__FilterDict(params)
        result = self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalUpdateCaseWithOwner', params)
        return result.get('effected_rows')

    def ProductOfferPrice(self, productOfferId, accountHost, accountId=None):
        self.VerifyExternalKey()
        params = dict(external_key=self._ExternalKey, account_host=accountHost, productoffer_id=productOfferId, account_id=accountId)
        params = self._iBizAPIClient__FilterDict(params)
        return self._backend.call('CommerceManager/ProductOffer', 'ExternalProductPrice', params)

    def ProductOrderNextChargeDate(self, productOrderId):
        self.VerifyExternalKey()
        params = dict(external_key=self._ExternalKey, productorder_id=productOrderId)
        params = self._iBizAPIClient__FilterDict(params)
        result = self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalGetNextChargeDate', params)
        return result.get('next_charge_date')

    def ProductOrderNonCurrentAccounts(self, productOrderId):
        self.VerifyExternalKey()
        params = dict(external_key=self._ExternalKey, productorder_id=productOrderId)
        params = self._iBizAPIClient__FilterDict(params)
        result = self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalNonCurrentAccounts', params)
        return result.get('data')

    def ListPurchases(self, limit=None, amount=None, start=None, sort=None):
        self.VerifyExternalKey()
        params = dict(external_key=self._ExternalKey, limit=limit, many=amount, product_id=self._ProductId, sort_by=sort, start=start)
        params = self._iBizAPIClient__FilterDict(params)
        result = self._backend.call('CommerceManager/ProductManager', 'ExternalListPurchases', params)
        error = result.get('error')
        if error != None:
            raise_with_traceback(ValueError(error))
        return result.get('LIST')

    def ProductOrderOwnerLanguage(self, productOrderId):
        self.VerifyExternalKey()
        params = dict(external_key=self._ExternalKey, productorder_id=self._ProductId)
        params = self._iBizAPIClient__FilterDict(params)
        return self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalGetOwnerLanguage', params)

    def ProductOrderPricing(self, productOrderId):
        self.VerifyExternalKey()
        params = dict(external_key=self._ExternalKey, productorder_id=self._ProductId)
        params = self._iBizAPIClient__FilterDict(params)
        return self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalProductOrderPricing', params)

    def ProductOrderUpdateInventory(self, productOrderId, inventoryData):
        self.VerifyExternalKey()
        params = dict(external_key=self._ExternalKey, inventory_data=inventoryData, productorder_id=productOrderId)
        params = self._iBizAPIClient__FilterDict(params)
        return self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalUpdateInventory', params)

    def UpdateEvent(self, eventId, status, message):
        self.VerifyExternalKey()
        params = dict(external_key=self._ExternalKey, productorderevent_id=eventId, message=message, status=status)
        params = self._iBizAPIClient__FilterDict(params)
        result = self._backend.call('CommerceManager/ProductManager/ProductOrder/Event', 'ExternalUpdateEvent', params)
        return result.get('success')

    def AuthenticateUser(self, productOrderAuthentication):
        pass

    def IsValidBackendRequest(self, externalKey):
        self.VerifyExternalKey()
        if self._ExternalKey != externalKey:
            raise_with_traceback(ValueError("Your request was not authorized. If you continue to see this message you're doing it wrong..."))
        return true

    def VerifyExternalKey(self):
        if not self.ExternalKeyExists():
            raise_with_traceback(ValueError('Your Products External Key was not found or is not accessible. Please verify that the key is set in the AppSettings " +\n                "section of your config file. You can find the Product External Key in the Panel under the External Attributes section " +\n                "of the ProductEdit page.'))

    def ExternalKeyExists(self):
        return self._ExternalKey != None

    def __FilterDict(self, dictionary):
        for item in viewitems(dictionary.copy()):
            if item[1] == None:
                del dictionary[item[0]]
                continue

        return dictionary
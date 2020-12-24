# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/BastionMerchantService.py
# Compiled at: 2015-07-18 19:38:10
import AccessControl, transaction
from AccessControl.Permissions import access_contents_information, view_management_screens
from Acquisition import aq_base
from OFS.PropertyManager import PropertyManager
from OFS.ObjectManager import ObjectManager
from OFS.Image import Image
from Products.ZCatalog.ZCatalog import ZCatalog
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2
from DateTime import DateTime
from Permissions import securityPolicy, operate_bastionbanking
import ZReturnCode
from ZCreditCard import ZCreditCard
from ZCurrency import ZCurrency
from config import MERCHANTTOOL
from Products.CMFCore.permissions import View
from PortalContent import PortalContent
from BastionPayment import BastionPayment
from BastionPayee import PayeeSupport
from Exceptions import *
manage_addBastionMerchantServiceForm = PageTemplateFile('zpt/add_merchantservice', globals())

def manage_addBastionMerchantService(self, service, title='Bastion Merchant Service', id=MERCHANTTOOL, REQUEST=None):
    """ 
    """
    try:
        exec 'from Products.BastionBanking.Merchants.%s.Z%s import Z%s' % (service, service, service)
        self._setObject(id, BastionMerchantService(id, title, eval("Z%s('service')" % service)))
    except:
        raise

    if REQUEST:
        REQUEST.RESPONSE.redirect('%s/%s/service/manage_workspace' % (REQUEST['URL3'], id))
    return id


class BastionMerchantService(BTreeFolder2, ZCatalog, PropertyManager, PortalContent, PayeeSupport):
    """
    An encapsulation of a card merchant service provider.
    """
    meta_type = portal_type = 'BastionMerchantService'
    modes = ('live', 'test')
    retentions = ('none', 'mangled', 'full')
    description = ''
    store_name = ''
    store_identifier = ''
    __ac_permissions__ = BTreeFolder2.__ac_permissions__ + ZCatalog.__ac_permissions__ + ((access_contents_information, ('isLive', 'isTest')), (View, ('serviceIcon', 'serviceLogo', 'serviceUrl', 'widget', 'formMacro', 'manage_pay', 'manage_payTransaction',
 'manage_payment', 'merchantAccount')), (view_management_screens, ('manage_service', )), (operate_bastionbanking, ('getSearchTerm', 'saveSearch', 'paymentResults', 'manage_refund', 'manage_reconcile',
 'manage_accept', 'manage_reject'))) + PropertyManager.__ac_permissions__ + PortalContent.__ac_permissions__ + PayeeSupport.__ac_permissions__
    manage_options = (
     {'label': 'Payments', 'action': 'manage_main', 'help': ('BastionBanking', 'search.stx')},
     {'label': 'Payees', 'action': 'manage_payees', 'help': ('BastionBanking', 'search.stx')}, {'label': 'View', 'action': ''},
     {'label': 'Pay', 'action': 'manage_payment', 'help': ('BastionBanking', 'merchantview.stx')}, {'label': 'Service', 'action': 'manage_service'}) + ZCatalog.manage_options[1:]

    def manage_service(self, REQUEST):
        """ """
        REQUEST.RESPONSE.redirect('service/manage_workspace')

    manage_main = PageTemplateFile('zpt/merchant_search', globals())
    manage_payment = PageTemplateFile('zpt/merchant_view', globals())
    _properties = PropertyManager._properties + ({'id': 'description', 'type': 'text', 'mode': 'w'}, {'id': 'mode', 'type': 'selection', 'mode': 'w', 'select_variable': 'modes'}, {'id': 'number_retention', 'type': 'selection', 'mode': 'w', 'select_variable': 'retentions'}, {'id': 'store_name', 'type': 'string', 'mode': 'w'}, {'id': 'store_identifier', 'type': 'string', 'mode': 'w'})

    def __init__(self, id, title, imp):
        BTreeFolder2.__init__(self, id)
        ZCatalog.__init__(self, id)
        self.title = title
        self.service = imp
        self.mode = 'test'
        self.number_retention = 'full'
        for id in ('meta_type', 'status', 'number'):
            self.addIndex(id, 'FieldIndex')

        self.addIndex('submitted', 'DateIndex')
        self.addIndex('reference', 'TextIndexNG3')
        self.addColumn('meta_type')

    def supportedCurrencies(self):
        """
        return a tuple of the currency codes supported by the underlying transport
        """
        return self.service.supportedCurrencies()

    def displayContentsTab(self):
        """
        we're not Plone-based ...
        """
        return False

    def manage_pay(self, amount, reference='', return_url='', REQUEST={}, txn=None):
        """
        the parameters explicitly defined reflect those defined in the widgets - and
        indeed the minimum required for any merchant txn, additional parameters will
        be in the request.
        
        return a returncode object containing results of interaction ...

        the REQUEST *must* contain appropriate fields to instantiate a creditcard object
        for the service you've configured

        """
        service = self.service
        if not isinstance(amount, ZCurrency):
            amount = ZCurrency(amount)
        if amount == 0:
            raise InvalidAmount, 'zero amount!'
        if amount.currency() not in self.supportedCurrencies():
            raise UnsupportedCurrency, amount.currency()
        id = self.generateId()
        pmt = service._generateBastionPayment(id, amount, reference, REQUEST)
        pmt.gateway = service.meta_type
        if pmt.payee:
            if not pmt.payee.validNumber():
                raise CreditCardInvalid, pmt.payee.number
            if not pmt.payee.validExpiry(DateTime()):
                raise CreditCardExpired, pmt.payee.expiry
        self._setObject(id, pmt)
        transaction.get().commit()
        payment = self._getOb(id)
        if txn:
            payment.setTransactionRef(txn)
        try:
            rc, redirect_url = service._pay(payment, return_url or '%s/pay' % self.absolute_url(), REQUEST)
        except ProcessingFailure as e:
            payment._status('rejected')
            transaction.get().commit()
            raise

        zrc = payment._setReturnCode(rc)
        if payment.payee:
            self._mask_payee(payment.payee)
        if not redirect_url:
            if rc.severity == ZReturnCode.OK:
                payment._status('paid')
            elif rc.severity in (ZReturnCode.FAIL, ZReturnCode.ERROR, ZReturnCode.FATAL):
                payment._status('rejected')
        transaction.get().commit()
        url = redirect_url or return_url or REQUEST.get('HTTP_REFERER', '')
        if url:
            if url.endswith('manage_payment'):
                REQUEST.RESPONSE.redirect('%s/manage_workspace' % payment.getId())
            REQUEST.RESPONSE.redirect(url)
        payment.reindexObject()
        return payment

    def widget(self, *args, **kw):
        """
        return the html-generated widget from the service
        """
        if getattr(aq_base(self.service), 'widget', None):
            return self.service.widget(args, kw)
        else:
            return ''

    def formMacro(self):
        """
        return the macro name as defined in bastionmerchant_macros
        """
        return self.service.form_macro

    def merchantAccount(self, ledger):
        """
        return the merchant account for the ledger (represented by gateway tag)
        """
        gateway = self.service.getId()
        for tag in (gateway, 'bank_account'):
            accs = ledger.accountValues(tags=tag)
            if accs:
                return accs[0]

        return

    def merchantFee(self, amount):
        """
        return the fee the merchant will charge on the amount
        """
        if not isinstance(amount, ZCurrency):
            raise InvalidAmount, amount
        return self.service.transactionFee(amount)

    def manage_payTransaction(self, txn, reference='', return_url='', REQUEST={}):
        """
        BastionLedger-aware payment mechanism.

        Since some payment methods can return success/failure asynchronously,
        this leaves us in a bind about when to post transactions.

        This method allows us to pass this responsibility on to the service,
        which knows this.
        """
        amount = txn.debitTotal()
        return self.manage_pay(amount, reference, return_url, REQUEST or self.REQUEST, txn)

    def manage_refund(self, payment, REQUEST=None):
        """
        delegate to service to refund payment - this is called via workflow - don't set returncode, that happens afterwards
        """
        if self.service._reconcile(payment):
            rc = self.service._refund(payment)
            payment._setReturnCode(rc)
            transaction.get().commit()
            if not rc.severity == ZReturnCode.OK:
                raise ProcessingFailure, rc.message
            txn = payment.getTransactionRef()
            if txn:
                try:
                    txn.manage_reverse('Reversal: BMS ref %s' % payment.getId())
                except:
                    pass

            if REQUEST:
                REQUEST.set('manage_tabs_message', 'Refunded')
        else:
            if REQUEST:
                REQUEST.set('manage_tabs_message', 'Not reconciled, unable to refund')
            else:
                raise ValueError, 'Cannot refund until payment confirmation'
            if REQUEST:
                return self.manage_main(self, REQUEST)

    def manage_reconcile(self, payment, REQUEST=None):
        """
        delegate to service to reconcile payment
        """
        status = payment.status()
        if status in ('paid', 'pending', 'refunded', 'reconciled', 'rejected') and self.service._reconcile(payment):
            if status != 'reconciled':
                payment._status('reconciled')
        else:
            if status == 'cancelled':
                pass
            elif status != 'rejected':
                payment._status('rejected')
            payment.reindexObject()
            if REQUEST:
                return self.manage_main(self, REQUEST)

    def manage_accept(self, payment, REQUEST=None):
        """
        cool - if it's a BLTransaction, then post it ...
        """
        txn = payment.getTransactionRef()
        if txn:
            txn.manage_post()
        if REQUEST:
            return self.manage_main(self, REQUEST)

    def manage_reject(self, payment, REQUEST=None):
        """
        uncool - if it's a BLTransaction, then cancel it
        """
        txn = payment.getTransactionRef()
        if txn:
            try:
                txn.manage_cancel()
            except:
                pass

        if REQUEST:
            return self.manage_main(self, REQUEST)

    def paymentResults(self, REQUEST, sort_on='submitted', sort_order='descending'):
        """
        return a list of pure payment objects reflecting the sort criteria
        """
        query = dict(REQUEST.has_key('form') and REQUEST.form or REQUEST)
        if query.has_key('from_date') and query.has_key('to_date'):
            try:
                query['submitted'] = (
                 DateTime(query['from_date']),
                 DateTime(query['to_date']))
            except:
                pass

            del query['from_date']
            del query['to_date']
        return self.searchResults(REQUEST=query, meta_type='BastionPayment', sort_on=sort_on, sort_order=sort_order)

    def saveSearch(self, REQUEST=None):
        """
        save search parameters in session object
        """
        if not REQUEST:
            REQUEST = self.REQUEST
        REQUEST.SESSION['bastionbanking'] = REQUEST.form

    def getSearchTerm(self, field, default, REQUEST=None):
        """
        return search term results for field
        """
        if not REQUEST:
            REQUEST = self.REQUEST
        if not REQUEST.has_key('SESSION'):
            return default
        return REQUEST.SESSION.get('bastionbanking', {}).get(field, default)

    def isLive(self):
        return self.mode == 'live'

    def isTest(self):
        return self.mode == 'test'

    def serviceIcon(self):
        """
        """
        return self.service.icon

    def serviceLogo(self):
        """
        """
        return self.service.serviceLogo()

    def serviceUrl(self):
        """
        """
        return self.service.serviceUrl()

    def _getPortalTypeName(self):
        """
        needed for the portal type view mechanism ...
        """
        return self.meta_type

    def _mask_payee(self, payee):
        """
        returns a card number based upon card number retention policy
        """
        payee.cvv2 = ''
        if self.number_retention == 'none':
            payee.number = 'XXXXXXXXXXXXXXXX'
            payee.expiry = DateTime(0)
        if self.number_retention == 'mangled':
            payee.number = '%sXXXXXX%s' % (payee.number[0:7], payee.number[-4:])

    def manage_repair(self, REQUEST=None):
        """
        Upgrade any underlying datastructure modifications between releases
        """
        if not getattr(aq_base(self), 'number_retention', None):
            self.number_retention = 'full'
        for pmt in self.objectValues('BastionPayment'):
            if not getattr(aq_base(pmt), 'returncodes', None):
                pmt.returncodes = BTreeFolder2('returncodes')

        self.refreshCatalog(clear=1)
        try:
            self.addIndex('reference', 'TextIndexNG3')
            self.manage_reindexIndex(['reference'])
        except:
            pass

        if REQUEST:
            REQUEST.set('manage_tabs_message', 'repaired')
            return self.manage_main(self, REQUEST)
        else:
            return

    def manage_fixupIndexes(self, REQUEST=None):
        """
        resurrect screwed up indexes
        """
        for pmt in self.objectValues('BastionPayment'):
            map(lambda x: x.reindexObject(), map(lambda x: x[1], pmt.getReturnCodes()))
            pmt.reindexObject()

        if REQUEST:
            REQUEST.set('manage_tabs_message', 'Reindexed ...')
            return self.manage_main(self, REQUEST)


AccessControl.class_init.InitializeClass(BastionMerchantService)

def addBastionMerchantService(ob, event):
    securityPolicy(ob)
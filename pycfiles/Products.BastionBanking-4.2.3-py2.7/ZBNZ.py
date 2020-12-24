# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/Merchants/BNZ/ZBNZ.py
# Compiled at: 2015-07-18 19:38:10
import os, AccessControl
from DateTime import DateTime
from bnz import bnz
from Products.BastionBanking.interfaces.BastionMerchantInterface import IBastionMerchant
from Products.BastionBanking.ZReturnCode import ZReturnCode
from Products.BastionBanking.ZCreditCard import ZCreditCard
from Products.BastionBanking.BastionPayment import BastionPayment
from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate
from OFS.ObjectManager import ObjectManager
from OFS.PropertyManager import PropertyManager
from OFS.SimpleItem import SimpleItem
from zope.interface import implements
form = '\n<img src="" height="16" width="16" valign="bottom"\n     tal:attributes="src string:${request/BASEPATH1}/${container/icon}"/>&nbsp;&nbsp;\n<select name="cc_type">\n   <option tal:repeat="type python: (\'VISA\', \'Delta\', \'Mastercard\', \'JCB\')"\n           tal:content="type"/>\n</select>\n<span class="form-label">Number</span>&nbsp;\n<input type="text" size="16" name="cc_number">&nbsp;&nbsp;\n<span class="form-label">Expires</span>&nbsp;\n<select name="cc_year" tal:define="year python: DateTime().year()">\n    <option tal:repeat="yy python: range(0, 4)" tal:content="python: year + yy"/>\n</select>\n<strong>&nbsp;/&nbsp;</strong>\n<select name="cc_month">\n    <option tal:repeat="mm python: range(1, 13)" tal:content="python: \'%02d\' % mm"/>\n</select>\n'

class ZBNZ(bnz, ObjectManager, PropertyManager, SimpleItem):
    """
    Zope-wrapped Bank of New Zealand accessor
    """
    meta_type = 'ZBNZ'
    implements(IBastionMerchant)
    property_extensible_schema__ = 0
    _properties = ({'id': 'cert_file', 'type': 'string', 'mode': 'w'}, {'id': 'cert_password', 'type': 'string', 'mode': 'w'}, {'id': 'merchant_id', 'type': 'string', 'mode': 'w'}, {'id': 'user', 'type': 'string', 'mode': 'w'}, {'id': 'realm', 'type': 'string', 'mode': 'w'})
    manage_options = ObjectManager.manage_options + ({'label': 'Configuration', 'action': 'manage_propertiesForm'},) + SimpleItem.manage_options
    id = 'BNZ'
    title = 'Bank of New Zealand'

    def __init__(self, id):
        self.merchant_id = '12341234'
        self.cert_file = os.path.join(os.path.dirname(__file__), 'gateway.cer')
        self.cert_password = 'a5de3fsA'
        self.user = 'user'
        self.realm = 'realm'
        self._setObject('widget', ZopePageTemplate('widget', form))

    def _generateBastionPayment(self, id, amount, ref, REQUEST):
        payee = ZCreditCard(REQUEST['cc_number'], DateTime('%s/%s/01' % (REQUEST['cc_year'], REQUEST['cc_month'])), REQUEST.get('cc_type', ''), REQUEST.get('cc_name', ''))
        return BastionPayment(id, payee, amount, ref)

    def _pay(self, payment, REQUEST=None):
        """
        make payment, coerce return type 
        """
        return bnz._pay(self, payment.payee, payment.amount, self.aq_parent.mode == 'test')

    def _refund(self, payment, REQUEST=None):
        """
        make refund, coerce return type 
        """
        return bnz._refund(self, payment.payee, payment.amount, payment.reference, self.aq_parent.mode == 'test')


AccessControl.class_init.InitializeClass(ZBNZ)
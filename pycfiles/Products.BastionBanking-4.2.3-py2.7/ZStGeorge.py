# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/Merchants/StGeorge/ZStGeorge.py
# Compiled at: 2015-07-18 19:38:10
import AccessControl
from stgeorge import stgeorge
from Products.BastionBanking.interfaces.BastionMerchantInterface import IBastionMerchant
from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate
from OFS.ObjectManager import ObjectManager
from OFS.PropertyManager import PropertyManager
from OFS.SimpleItem import SimpleItem
from zope.interface import implements
form = '\n<img src="" height="35" width="80" valign="bottom"\n     tal:attributes="src string:${request/BASEPATH1}/${container/icon}"/>&nbsp;&nbsp;\n<select name="type">\n   <option tal:repeat="type python: (\'VISA\', \'Delta\', \'Mastercard\', \'JCB\')"\n           tal:content="type"/>\n</select>\n<span class="form-label">Number</span>&nbsp;\n<input type="text" size="16" name="card">&nbsp;&nbsp;\n<span class="form-label">Expires</span>&nbsp;\n<strong>&nbsp;/&nbsp;</strong>\n<select name="expiry:list:int" tal:define="year python: DateTime().year()">\n    <option tal:repeat="yy python: range(0, 4)" tal:content="python: year + yy"/>\n</select>\n<select name="expiry:list:int">\n    <option tal:repeat="mm python: range(1, 13)" tal:content="python: \'%02d\' % mm"/>\n</select>\n<input type="hidden" name="expiry:list:int" value="1"/>\n'

class ZStGeorge(stgeorge, ObjectManager, PropertyManager, SimpleItem):
    """
    Zope-wrapped St Georges Bank accessor
    """
    meta_type = 'ZStGeorge'
    implements(IBastionMerchant)
    property_extensible_schema__ = 0
    _properties = ({'id': 'cert_file', 'type': 'string', 'mode': 'w'}, {'id': 'merchant_id', 'type': 'string', 'mode': 'w'}, {'id': 'user', 'type': 'string', 'mode': 'w'}, {'id': 'password', 'type': 'string', 'mode': 'w'}, {'id': 'realm', 'type': 'string', 'mode': 'w'})
    manage_options = ObjectManager.manage_options + ({'label': 'Configuration', 'action': 'manage_propertiesForm'},) + SimpleItem.manage_options
    id = 'St Georges'
    title = 'St Georges Bank - Australia'

    def __init__(self, id):
        self.merchant_id = ''
        self.cert_file = ''
        self.user = 'user'
        self.password = 'password'
        self.realm = 'realm'
        self._setObject('widget', ZopePageTemplate('widget', form))

    def _generateBastionPayment(self, id, amount, ref, REQUEST):
        """
        this should agree with stuff in our form (excepting amount) ...
        """
        payee = ZCreditCard(REQUEST['card'], DateTime('%s/%s/01' % (REQUEST['expiry'][0], REQUEST['expiry'][1])), REQUEST['type'])
        return BastionPayment(id, payee, amount, ref)

    def _pay(self, payment, REQUEST=None):
        return stgeorge._pay(self, payment.payee.number, payment.amount)

    def _refund(self, payment, ref, REQUEST=None):
        return stgeorge._refund(self, payment.payee.number, amount, ref)

    def supportedCurrencies(self):
        return ('AUD', )


AccessControl.class_init.InitializeClass(ZStGeorge)
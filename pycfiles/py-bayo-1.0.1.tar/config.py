# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.5/site-packages/bankpassweb/satchmo_payment/config.py
# Compiled at: 2008-01-28 08:22:18
from satchmo.configuration import *
from django.utils.translation import ugettext_lazy as _
gettext = lambda s: s
_strings = (gettext('CreditCard'), gettext('Credit Card'))
PAYMENT_MODULES = config_get('PAYMENT', 'MODULES')
PAYMENT_MODULES.add_choice(('PAYMENT_BANKPASSWEB', 'BankPass Web'))
PAYMENT_GROUP = ConfigurationGroup('PAYMENT_BANKPASSWEB', _('BankPass Web Payment Settings'), requires=PAYMENT_MODULES, ordering=101)
config_register([
 StringValue(PAYMENT_GROUP, 'CONNECTION', description=_('Submit to URL'), help_text=_('This is the address to submit live transactions.'), default='http://sis-bankpass.ssb.it/bankpass/master/main?PAGE=MASTER'),
 StringValue(PAYMENT_GROUP, 'CONNECTION_TEST', description=_('Submit to Test URL'), help_text='A Quick note on the urls.<br/>\nIf you are posting to https://test.authorize.net/gateway/transact.dll,\nand you are not using an account whose API login ID starts with\n&quot;cpdev&quot; or &quot;cnpdev&quot;, you will get an Error 13 message. \nMake sure you are posting to https://certification.authorize.net/gateway/transact.dll\nfor test transactions if you do not have a cpdev or cnpdev.\n', default='http://sis-test-bankpass.ssb.it/bankpass/master/main?PAGE=MASTER'),
 BooleanValue(PAYMENT_GROUP, 'SSL', description=_('Use SSL for the checkout pages?'), default=False),
 BooleanValue(PAYMENT_GROUP, 'LIVE', description=_('Accept real payments'), help_text=_('False if you want to be in test mode'), default=False),
 ModuleValue(PAYMENT_GROUP, 'MODULE', description=_('Implementation module'), hidden=True, default='bankpassweb.satchmo_payment'),
 StringValue(PAYMENT_GROUP, 'KEY', description=_('Module key'), hidden=True, default='BANKPASSWEB'),
 StringValue(PAYMENT_GROUP, 'LABEL', description=_('English name for this group on the checkout screens'), default='Credit Cards', help_text=_('This will be passed to the translation utility')),
 StringValue(PAYMENT_GROUP, 'URL_BASE', description=_('The url base used for constructing urlpatterns which will use this module'), default='^credit/'),
 StringValue(PAYMENT_GROUP, 'CRN', description=_('Your live BankPass Web CRN (shop ID number)'), default=''),
 StringValue(PAYMENT_GROUP, 'TRANKEY', description=_('Your live BankPass Web key (avvio)'), default=''),
 StringValue(PAYMENT_GROUP, 'RESULTKEY', description=_('Your live BankPass Web result key (esito/API)'), default=''),
 StringValue(PAYMENT_GROUP, 'CRN_TEST', description=_('Your test BankPass Web CRN (shop ID number)'), default=''),
 StringValue(PAYMENT_GROUP, 'TRANKEY_TEST', description=_('Your test BankPass Web key'), default=''),
 StringValue(PAYMENT_GROUP, 'RESULTKEY_TEST', description=_('Your test BankPass Web result key (esito/API)'), default=''),
 StringValue(PAYMENT_GROUP, 'ORDER_PREFIX', description=_("The prefix for BankPass Web's order ID"), default='Satchmo'),
 StringValue(PAYMENT_GROUP, 'CURRENCY', description=_('The currency identifier for generated payments'), default='EUR'),
 IntegerValue(PAYMENT_GROUP, 'SHIFT_DIGITS', description=_('How many digits the decimal point must be shifted'), default=2),
 StringValue(PAYMENT_GROUP, 'SUCCESS_RETURN_ADDRESS', description=_('Return URL'), help_text=_('Where BankPass Web will return the customer after the purchase is complete.  This can be a named url and defaults to the standard checkout success.'), default='BANKPASSWEB_satchmo_checkout-success'),
 StringValue(PAYMENT_GROUP, 'FAILURE_RETURN_ADDRESS', description=_('Return URL'), help_text=_('Where BankPass Web will return the customer after the purchase has failed.  This can be a named url and defaults to the standard checkout success.'), default='BANKPASSWEB_satchmo_checkout-success'),
 StringValue(PAYMENT_GROUP, 'URL_BASE', description=_('The url base used for constructing urlpatterns which will use this module'), default='^bankpassweb/')])
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/ZCreditCard.py
# Compiled at: 2015-07-18 19:38:10
import AccessControl
from AccessControl.Permissions import view
from AccessControl import ClassSecurityInfo
from PortalContent import PortalContent
from creditcard import creditcard, CreditCardException, CreditCardInvalid, CreditCardExpired

class ZCreditCard(creditcard, PortalContent):
    """
    A persistent creditcard ...

    This is supposed to be a first-class Zope object ...
    """
    meta_type = portal_type = 'ZCreditCard'
    icon = 'misc_/BastionBanking/creditcard'
    __ac_permissions__ = PortalContent.__ac_permissions__ + (
     (
      view, ('number_str', 'masked')),)
    property_extensible_schema__ = 0
    _properties = ({'id': 'title', 'type': 'string', 'mode': 'w'}, {'id': 'number', 'type': 'string', 'mode': 'r'}, {'id': 'expiry', 'type': 'date', 'mode': 'r'}, {'id': 'type', 'type': 'string', 'mode': 'r'}, {'id': 'name', 'type': 'string', 'mode': 'r'}, {'id': 'cvv2', 'type': 'string', 'mode': 'r'})
    _security = ClassSecurityInfo()

    def __init__(self, number, expiry, type='', name='', cvv2=''):
        self.id = number
        self.title = name
        creditcard.__init__(self, number, expiry, type, name, cvv2)

    def _repair(self):
        for attr in ('name', 'cvv2'):
            if not getattr(aq_base(self), attr, none):
                setattr(self, attr, '')

    def number_str(self):
        """
        return the formatted cardnumber
        """
        return '%s-%s-%s-%s' % (self.number[0:4],
         self.number[4:8],
         self.number[8:12],
         self.number[12:])

    def masked(self):
        """
        returns a card number based upon card number retention policy
        """
        return '%sXXXXXX%s' % (self.number[0:7], self.number[-4:])


AccessControl.class_init.InitializeClass(ZCreditCard)
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/payment/content/bank_account.py
# Compiled at: 2008-09-03 11:15:14
from zope.component.factory import Factory
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from plone.app.content.item import Item
from easyshop.core.config import _
from easyshop.core.interfaces import IBankAccount

class BankAccount(Item):
    """Holds all relevant informations for direct debit payment method. This is 
    a bank account.
    """
    __module__ = __name__
    implements(IBankAccount)
    portal_type = 'BankAccount'
    account_number = FieldProperty(IBankAccount['account_number'])
    bank_identification_code = FieldProperty(IBankAccount['bank_identification_code'])
    bank_name = FieldProperty(IBankAccount['bank_name'])
    depositor = FieldProperty(IBankAccount['depositor'])

    def Title(self):
        """
        """
        return self.bank_name + ' - ' + self.account_number


bankAccountFactory = Factory(BankAccount, title=_('Create a new bank account'))
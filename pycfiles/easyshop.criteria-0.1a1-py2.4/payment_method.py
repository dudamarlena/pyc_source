# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/criteria/content/payment_method.py
# Compiled at: 2008-09-03 11:14:39
import transaction
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from easyshop.core.config import *
from easyshop.core.interfaces import IPaymentMethodCriteria
from easyshop.core.interfaces import IPaymentMethodManagement
from easyshop.core.interfaces import IShopManagement
schema = Schema((StringField(name='title', widget=StringWidget(visible={'edit': 'invisible', 'view': 'invisible'}, label='Title', label_msgid='schema_title_label', i18n_domain='EasyShop'), required=0), LinesField(name='paymentMethods', widget=MultiSelectionWidget(label='Payment Methods', label_msgid='schema_payment_methods_label', i18n_domain='EasyShop'), multiValued=1, vocabulary='_getPaymentMethodsAsDL')))

class PaymentMethodCriteria(BaseContent):
    """
    """
    __module__ = __name__
    implements(IPaymentMethodCriteria)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def Title(self):
        """
        """
        return 'Payment Method'

    def getValue(self):
        """
        """
        return (', ').join(self.getPaymentMethods())

    def _getPaymentMethodsAsDL(self):
        """Returns all payment methods as DisplayList.
        """
        dl = DisplayList()
        shop = IShopManagement(self).getShop()
        for method in IPaymentMethodManagement(shop).getPaymentMethods():
            dl.add(method.getId(), method.Title())

        return dl

    def _renameAfterCreation(self, check_auto_id=False):
        """Overwritten to set the default value for id.
        """
        transaction.commit()
        new_id = 'PaymentMethodCriteria'
        self.setId(new_id)


registerType(PaymentMethodCriteria, PROJECTNAME)
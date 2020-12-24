# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/Banks/ManualPayment/ManualPayment.py
# Compiled at: 2015-07-18 19:38:10
import AccessControl
from Products.BastionBanking.interfaces.BastionBankInterface import IBastionBank
from Products.BastionBanking.PortalContent import PortalContent
from OFS.ObjectManager import ObjectManager
from OFS.PropertyManager import PropertyManager
from OFS.SimpleItem import SimpleItem
from DateTime import DateTime
from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from returncode import returncode, OK
from zope.interface import implements

class Cheque(PortalContent):
    """ describe a manual transaction ... """
    meta_type = portal_content = 'Cheque'
    icon = 'Banks/ManualPayment/www/cheque.gif'
    property_extensible_schema__ = 0
    _properties = ({'id': 'id', 'type': 'string', 'mode': 'r'}, {'id': 'date', 'type': 'date', 'mode': 'r'}, {'id': 'payee', 'type': 'string', 'mode': 'r'}, {'id': 'amount', 'type': 'string', 'mode': 'r'}, {'id': 'reference', 'type': 'string', 'mode': 'r'})

    def __init__(self, id, payee, amount, reference):
        self.id = id
        self.date = DateTime()
        self.payee = payee
        self.amount = amount
        self.reference = reference


AccessControl.class_init.InitializeClass(Cheque)

class ManualPayment(ObjectManager, PropertyManager):
    """ """
    meta_type = 'ManualPayment'
    implements(IBastionBank)
    all_meta_types = []
    dontAllowCopyAndPaste = 1
    id = 'ManualPayment'
    title = 'Payment Schedule'
    manage_options = ({'label': 'Payments', 'action': 'manage_main'}, {'label': 'Properties', 'action': 'manage_propertiesForm'}) + SimpleItem.manage_options
    _properties = ()
    manage_main = PageTemplateFile('zpt/payments', globals())

    def __init__(self):
        pass

    def _pay(self, amount, account, reference, REQUEST=None):
        """ """
        id = str(DateTime().timeTime())
        id.replace('.', '')
        self._setObject(id, Cheque(id, account.payee, amount, reference))
        return returncode(id, amount, OK, 0, '', '')


AccessControl.class_init.InitializeClass(ManualPayment)